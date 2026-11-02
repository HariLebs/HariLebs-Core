"""Harilebs Core.

Reusable core framework for Harilebs Telegram bots.
"""

from .base import BaseService
from .bot_manager import BotManager
from .cache import CacheService
from .rate_limiter import RateLimitResult, RateLimiterService
from .scheduler import SchedulerService

from .health_check import HealthCheckResult, HealthCheckService

from .metrics import MetricsService

from .telegram_middleware import TelegramMiddleware

from .telegram_filters import AdminFilter, ChatTypeFilter, UserIdFilter

from .telegram_keyboards import build_inline_keyboard, build_reply_keyboard

from .telegram_helpers import escape_html, format_html, split_text

from .telegram_error_handler import TelegramErrorHandler

from .telegram_commands import build_bot_commands

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
    "CacheService",
    "SchedulerService",
    "RateLimitResult",
    "RateLimiterService",
    "HealthCheckResult",
    "HealthCheckService",
    "MetricsService",
    "TelegramMiddleware",
    "build_bot_commands",
    "TelegramErrorHandler",
    "split_text",
    "format_html",
    "escape_html",
    "build_reply_keyboard",
    "build_inline_keyboard",
    "UserIdFilter",
    "ChatTypeFilter",
    "AdminFilter",
    "HariLebsError",
    "ConfigurationError",
    "InitializationError",
    "ServiceError",
    "IntegrationError",
    "generate_token",
    "hash_secret",
    "verify_secret",
]
