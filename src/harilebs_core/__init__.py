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

from .telegram_callback_data import (
    MAX_CALLBACK_DATA_BYTES,
    build_callback_data,
    parse_callback_data,
    validate_callback_data,
)

from .telegram_deep_links import (
    build_start_link,
    parse_start_parameter,
)

from .telegram_mentions import build_user_mention

from .telegram_formatting import (
    bold,
    code,
    italic,
    link,
    pre,
    strikethrough,
    underline,
)

from .telegram_messages import (
    TELEGRAM_MESSAGE_LIMIT,
    count_message_chunks,
    prepare_message,
    validate_message_text,
)

from .telegram_permissions import (
    PERMISSION_FIELDS,
    build_chat_permissions,
    build_full_permissions,
    build_restricted_permissions,
)

from .telegram_files import (
    TelegramFileInfo,
    build_file_info,
    is_file_within_limit,
)

from .telegram_users import (
    TelegramUserInfo,
    build_user_info,
    get_display_name,
    get_user_mention_target,
)

from .telegram_chats import (
    TelegramChatInfo,
    build_chat_info,
    get_chat_display_name,
)

from .telegram_media import (
    get_file_extension,
    get_media_type,
    get_media_type_from_mime,
)

from .telegram_groups import (
    TelegramGroupInfo,
    build_group_info,
    get_group_display_name,
    is_group_admin,
)

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
    "is_group_admin",
    "get_group_display_name",
    "build_group_info",
    "TelegramGroupInfo",
    "get_media_type_from_mime",
    "get_media_type",
    "get_file_extension",
    "get_chat_display_name",
    "build_chat_info",
    "TelegramChatInfo",
    "get_user_mention_target",
    "get_display_name",
    "build_user_info",
    "TelegramUserInfo",
    "is_file_within_limit",
    "build_file_info",
    "TelegramFileInfo",
    "build_restricted_permissions",
    "build_full_permissions",
    "build_chat_permissions",
    "PERMISSION_FIELDS",
    "validate_message_text",
    "prepare_message",
    "count_message_chunks",
    "TELEGRAM_MESSAGE_LIMIT",
    "underline",
    "strikethrough",
    "pre",
    "link",
    "italic",
    "code",
    "bold",
    "build_user_mention",
    "parse_start_parameter",
    "build_start_link",
    "validate_callback_data",
    "parse_callback_data",
    "build_callback_data",
    "MAX_CALLBACK_DATA_BYTES",
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
