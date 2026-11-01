import asyncio

import pytest

from harilebs_core.bot_manager import BotManager
from harilebs_core.exceptions import ServiceError


class FakeBot:
    pass


class FakeDispatcher:
    async def start_polling(self, bot, **kwargs):
        await asyncio.Event().wait()


class FailingDispatcher:
    async def start_polling(self, bot, **kwargs):
        raise RuntimeError("Polling failed")


def test_manager_initialization():
    manager = BotManager()

    assert manager.name == "bot_manager"
    assert manager.is_initialized is False


def test_register_bot():
    manager = BotManager()

    manager.register_bot("bot1", FakeBot(), FakeDispatcher())

    assert manager.get_status("bot1") == "stopped"


@pytest.mark.parametrize("bot_id", ["", "   ", None])
def test_register_invalid_bot_id(bot_id):
    manager = BotManager()

    with pytest.raises(ValueError):
        manager.register_bot(bot_id, FakeBot(), FakeDispatcher())


def test_register_bot_requires_bot_and_dispatcher():
    manager = BotManager()

    with pytest.raises(ValueError):
        manager.register_bot("bot1", None, FakeDispatcher())

    with pytest.raises(ValueError):
        manager.register_bot("bot2", FakeBot(), None)


def test_register_bot_requires_valid_dispatcher():
    manager = BotManager()

    with pytest.raises(ValueError):
        manager.register_bot("bot1", FakeBot(), object())


def test_register_duplicate_bot():
    manager = BotManager()
    manager.register_bot("bot1", FakeBot(), FakeDispatcher())

    with pytest.raises(ServiceError):
        manager.register_bot("bot1", FakeBot(), FakeDispatcher())


def test_unregister_unknown_bot():
    manager = BotManager()

    with pytest.raises(ServiceError):
        manager.unregister_bot("unknown")


def test_unregister_bot():
    manager = BotManager()
    manager.register_bot("bot1", FakeBot(), FakeDispatcher())

    manager.unregister_bot("bot1")

    assert manager.get_all_statuses() == {}


@pytest.mark.asyncio
async def test_unregister_running_bot():
    manager = BotManager()
    manager.register_bot("bot1", FakeBot(), FakeDispatcher())
    await manager.initialize()
    await manager.start_bot("bot1")

    with pytest.raises(ServiceError):
        manager.unregister_bot("bot1")

    await manager.shutdown()


def test_get_status_unknown_bot():
    manager = BotManager()

    with pytest.raises(ServiceError):
        manager.get_status("unknown")


@pytest.mark.asyncio
async def test_start_requires_initialization():
    manager = BotManager()
    manager.register_bot("bot1", FakeBot(), FakeDispatcher())

    with pytest.raises(ServiceError):
        await manager.start_bot("bot1")


@pytest.mark.asyncio
async def test_start_unknown_bot():
    manager = BotManager()
    await manager.initialize()

    with pytest.raises(ServiceError):
        await manager.start_bot("unknown")

    await manager.shutdown()


@pytest.mark.asyncio
async def test_start_and_stop_bot():
    manager = BotManager()
    manager.register_bot("bot1", FakeBot(), FakeDispatcher())

    await manager.initialize()
    await manager.start_bot("bot1")

    assert manager.get_status("bot1") == "running"

    with pytest.raises(ServiceError):
        await manager.start_bot("bot1")

    await manager.stop_bot("bot1")

    assert manager.get_status("bot1") == "stopped"

    await manager.shutdown()


@pytest.mark.asyncio
async def test_stop_unknown_bot():
    manager = BotManager()

    with pytest.raises(ServiceError):
        await manager.stop_bot("unknown")


@pytest.mark.asyncio
async def test_start_all_and_stop_all():
    manager = BotManager()
    manager.register_bot("bot1", FakeBot(), FakeDispatcher())
    manager.register_bot("bot2", FakeBot(), FakeDispatcher())

    await manager.initialize()
    await manager.start_all()

    assert manager.get_all_statuses() == {
        "bot1": "running",
        "bot2": "running",
    }

    await manager.stop_all()

    assert manager.get_all_statuses() == {
        "bot1": "stopped",
        "bot2": "stopped",
    }

    await manager.shutdown()


@pytest.mark.asyncio
async def test_start_all_requires_initialization():
    manager = BotManager()

    with pytest.raises(ServiceError):
        await manager.start_all()


@pytest.mark.asyncio
async def test_polling_failure_sets_error_status():
    manager = BotManager()
    manager.register_bot("bot1", FakeBot(), FailingDispatcher())

    await manager.initialize()
    await manager.start_bot("bot1")

    await asyncio.sleep(0)
    await asyncio.sleep(0)

    assert manager.get_status("bot1") == "error"

    await manager.shutdown()


@pytest.mark.asyncio
async def test_shutdown_stops_running_bots():
    manager = BotManager()
    manager.register_bot("bot1", FakeBot(), FakeDispatcher())

    await manager.initialize()
    await manager.start_bot("bot1")
    await manager.shutdown()

    assert manager.is_initialized is False
    assert manager.get_status("bot1") == "stopped"


@pytest.mark.asyncio
async def test_stop_all_without_running_bots():
    manager = BotManager()
    manager.register_bot("bot1", FakeBot(), FakeDispatcher())

    await manager.initialize()
    await manager.stop_all()

    assert manager.get_status("bot1") == "stopped"

    await manager.shutdown()
