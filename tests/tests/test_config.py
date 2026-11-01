import pytest
from pydantic import SecretStr, ValidationError

from harilebs_core import config
from harilebs_core.config import Settings


def test_settings_load_successfully():
    settings = Settings(
        _env_file=None,
        bot_token="test-token",
    )

    assert isinstance(settings.bot_token, SecretStr)
    assert settings.bot_token.get_secret_value() == "test-token"
    assert settings.debug is False


def test_settings_require_bot_token():
    with pytest.raises(ValidationError):
        Settings(_env_file=None)


def test_api_credentials_must_be_provided_together():
    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            bot_token="test-token",
            api_id=12345,
        )


def test_settings_accept_complete_api_credentials():
    settings = Settings(
        _env_file=None,
        bot_token="test-token",
        api_id=12345,
        api_hash="test-api-hash",
    )

    assert settings.api_id == 12345
    assert settings.api_hash.get_secret_value() == "test-api-hash"


def test_get_settings_returns_cached_instance(monkeypatch):
    config.get_settings.cache_clear()
    monkeypatch.setattr(config, "Settings", lambda: object())

    try:
        first = config.get_settings()
        second = config.get_settings()

        assert first is second
    finally:
        config.get_settings.cache_clear()
