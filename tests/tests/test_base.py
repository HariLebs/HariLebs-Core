import pytest

from harilebs_core.base import BaseService


class TestService(BaseService):
    """Test implementation of BaseService."""


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
