"""Configuration management for HariLebs Core."""

from functools import lru_cache

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    bot_token: SecretStr
    api_id: int | None = None
    api_hash: SecretStr | None = None
    debug: bool = False

    @model_validator(mode="after")
    def validate_api_credentials(self):
        """Ensure API credentials are provided together."""

        if (self.api_id is None) != (self.api_hash is None):
            raise ValueError(
                "API_ID and API_HASH must be provided together."
            )

        return self

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
