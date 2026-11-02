"""Utilities for handling Telegram group information."""

from dataclasses import dataclass


GROUP_TYPES = {"group", "supergroup"}


@dataclass(frozen=True, slots=True)
class TelegramGroupInfo:
    chat_id: int
    title: str
    group_type: str


def build_group_info(
    chat_id: int,
    title: str,
    group_type: str = "supergroup",
) -> TelegramGroupInfo:
    """Build validated Telegram group information."""
    if isinstance(chat_id, bool) or not isinstance(chat_id, int):
        raise TypeError("chat_id must be an integer.")
    if chat_id >= 0:
        raise ValueError("Group chat_id must be negative.")

    if not isinstance(title, str):
        raise TypeError("title must be a string.")
    if not title.strip():
        raise ValueError("title cannot be empty.")

    if not isinstance(group_type, str):
        raise TypeError("group_type must be a string.")
    if group_type not in GROUP_TYPES:
        raise ValueError("group_type must be group or supergroup.")

    return TelegramGroupInfo(chat_id, title.strip(), group_type)


def is_group_admin(user_id: int, admin_ids: set[int] | list[int] | tuple[int, ...]) -> bool:
    """Check whether a user ID belongs to the admin collection."""
    if isinstance(user_id, bool) or not isinstance(user_id, int):
        raise TypeError("user_id must be an integer.")

    if not isinstance(admin_ids, (set, list, tuple)):
        raise TypeError("admin_ids must be a set, list, or tuple.")

    if any(isinstance(item, bool) or not isinstance(item, int) for item in admin_ids):
        raise TypeError("All admin IDs must be integers.")

    return user_id in admin_ids


def get_group_display_name(group: TelegramGroupInfo) -> str:
    """Return the group's display name."""
    if not isinstance(group, TelegramGroupInfo):
        raise TypeError("group must be TelegramGroupInfo.")

    return group.title
