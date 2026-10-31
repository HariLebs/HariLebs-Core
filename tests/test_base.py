import pytest

from harilebs_core.base import BaseService


class TestService(BaseService):
    __test__ = False

    """Test implementation of BaseService."""

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.initialize_count = 0
        self.shutdown_count = 0

    async def _on_initialize(self) -> None:
        self.initialize_count += 1

    async def _on_shutdown(self) -> None:
        self.shutdown_count += 1
def test_service_initialization():
    service = TestService("test_service")

    assert service.name == "test_service"
    assert service.is_initialized is False


def test_service_name_is_trimmed():
    service = TestService("  test_service  ")

    assert service.name == "test_service"


@pytest.mark.parametrize("name", ["", "   ", None, 123])
def test_service_rejects_invalid_name(name):
    with pytest.raises(ValueError):
        TestService(name)


def test_service_initialization_state_is_read_only():
    service = TestService("test_service")

    with pytest.raises(AttributeError):
        service.is_initialized = True


@pytest.mark.asyncio
async def test_service_initialize():
    service = TestService("test_service")

    await service.initialize()

    assert service.is_initialized is True
    assert service.initialize_count == 1


@pytest.mark.asyncio
async def test_service_shutdown():
    service = TestService("test_service")

    await service.initialize()
    await service.shutdown()

    assert service.is_initialized is False
    assert service.shutdown_count == 1


@pytest.mark.asyncio
async def test_service_initialize_only_once():
    service = TestService("test_service")

    await service.initialize()
    await service.initialize()

    assert service.initialize_count == 1


@pytest.mark.asyncio
async def test_service_shutdown_only_once():
    service = TestService("test_service")

    await service.initialize()
    await service.shutdown()
    await service.shutdown()

    assert service.shutdown_count == 1
