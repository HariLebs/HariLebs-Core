import os


class Config:
    """Central configuration for HariLabs Core."""

    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    API_ID = os.getenv("API_ID", "")
    API_HASH = os.getenv("API_HASH", "")

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
