"""HariLebs Core.

Reusable core framework for Harilebs Telegram bots.
"""

from .base import BaseService
from .bot_manager import BotManager
from .exceptions import (
    ConfigurationError,
    HariLebsError,
    InitializationError,
    IntegrationError,
    ServiceError,
)
from .security import (
    generate_token,
    hash_secret,
    verify_secret,
)

__version__ = "0.1.0"
version = __version__

__all__ = [
    "__version__",
    "version",
    "BaseService",
    "BotManager",
    "HariLebsError",
    "ConfigurationError",
    "InitializationError",
    "ServiceError",
    "IntegrationError",
    "generate_token",
    "hash_secret",
    "verify_secret",
]
