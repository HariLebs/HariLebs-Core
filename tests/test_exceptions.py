import pytest

from harilebs_core.exceptions import (
    ConfigurationError,
    HariLebsError,
    InitializationError,
    IntegrationError,
    ServiceError,
)


def test_base_exception():
    assert issubclass(HariLebsError, Exception)


@pytest.mark.parametrize(
    "exception_class",
    [
        ConfigurationError,
        InitializationError,
        ServiceError,
        IntegrationError,
    ],
)
def test_custom_exceptions_inherit_from_base(exception_class):
    assert issubclass(exception_class, HariLebsError)


def test_exception_message():
    error = ConfigurationError("Invalid configuration")

    assert str(error) == "Invalid configuration"
