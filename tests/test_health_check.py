import pytest

from harilebs_core.base import BaseService
from harilebs_core.health_check import HealthCheckService


class DummyService(BaseService):
    async def _on_initialize(self):
        pass

    async def _on_shutdown(self):
        pass


@pytest.fixture
def health():
    return HealthCheckService()


@pytest.mark.asyncio
async def test_register_and_check(health):
    service = DummyService("database")
    health.register(service)
    result = await health.check("database")
    assert result.healthy is False
    await service.initialize()
    result = await health.check("database")
    assert result.healthy is True


@pytest.mark.asyncio
async def test_check_all(health):
    service = DummyService("database")
    health.register(service)
    results = await health.check_all()
    assert len(results) == 1
    assert results[0].name == "database"
    assert results[0].healthy is False


@pytest.mark.asyncio
async def test_is_healthy(health):
    service = DummyService("database")
    health.register(service)
    assert await health.is_healthy() is False
    await service.initialize()
    assert await health.is_healthy() is True


def test_register_invalid_service(health):
    with pytest.raises(TypeError):
        health.register("invalid")


def test_register_self(health):
    with pytest.raises(ValueError):
        health.register(health)


def test_unregister(health):
    health.register(DummyService("database"))
    health.unregister("database")
    assert health._services == {}


def test_unregister_missing(health):
    health.unregister("missing")
    assert health._services == {}


@pytest.mark.asyncio
async def test_check_unknown_service(health):
    with pytest.raises(ValueError):
        await health.check("missing")


@pytest.mark.asyncio
async def test_check_invalid_name(health):
    with pytest.raises(ValueError):
        await health.check(" ")


def test_unregister_invalid_name(health):
    with pytest.raises(ValueError):
        health.unregister(" ")


def test_invalid_service_name():
    with pytest.raises(ValueError):
        HealthCheckService(" ")


def test_register_replaces_same_name(health):
    first = DummyService("database")
    second = DummyService("database")
    health.register(first)
    health.register(second)
    assert health._services["database"] is second
