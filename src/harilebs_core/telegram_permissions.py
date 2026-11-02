"""Utilities for configuring Telegram chat permissions."""

from aiogram.types import ChatPermissions


PERMISSION_FIELDS = (
    "can_send_messages",
    "can_send_audios",
    "can_send_documents",
    "can_send_photos",
    "can_send_videos",
    "can_send_video_notes",
    "can_send_voice_notes",
    "can_send_polls",
    "can_send_other_messages",
    "can_add_web_page_previews",
    "can_change_info",
    "can_invite_users",
    "can_pin_messages",
    "can_manage_topics",
)


def build_chat_permissions(**permissions: bool) -> ChatPermissions:
    """Build validated Telegram chat permissions."""
    unknown = set(permissions) - set(PERMISSION_FIELDS)

    if unknown:
        raise ValueError(
            f"Unknown permission fields: {', '.join(sorted(unknown))}"
        )

    for name, value in permissions.items():
        if not isinstance(value, bool):
            raise TypeError(f"{name} must be a boolean.")

    return ChatPermissions(**permissions)


def build_restricted_permissions() -> ChatPermissions:
    """Build permissions that disable all optional actions."""
    return ChatPermissions(**{
        name: False for name in PERMISSION_FIELDS
    })


def build_full_permissions() -> ChatPermissions:
    """Build permissions that enable all supported actions."""
    return ChatPermissions(**{
        name: True for name in PERMISSION_FIELDS
    })
