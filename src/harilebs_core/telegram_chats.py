"""Utilities for handling Telegram chat information."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TelegramChatInfo:
    chat_id: int
    chat_type: str
    title: str | None = None
    username: str | None = None


VALID_CHAT_TYPES = {"private", "group", "supergroup", "channel"}


def build_chat_info(
    chat_id: int,
    chat_type: str,
    title: str | None = None,
    username: str | None = None,
) -> TelegramChatInfo:
    """Build validated Telegram chat information."""
    if isinstance(chat_id, bool) or not isinstance(chat_id, int):
        raise TypeError("chat_id must be an integer.")
    if chat_id == 0:
        raise ValueError("chat_id cannot be zero.")

    if not isinstance(chat_type, str):
        raise TypeError("chat_type must be a string.")
    if chat_type not in VALID_CHAT_TYPES:
        raise ValueError("Unsupported Telegram chat type.")

    for name, value in (("title", title), ("username", username)):
        if value is not None and not isinstance(value, str):
            raise TypeError(f"{name} must be a string or None.")
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{name} cannot be empty.")

    if username is not None:
        username = username.removeprefix("@")

    return TelegramChatInfo(chat_id, chat_type, title, username)


def get_chat_display_name(chat: TelegramChatInfo) -> str:
    """Return the best available chat display name."""
    if not isinstance(chat, TelegramChatInfo):
        raise TypeError("chat must be TelegramChatInfo.")

    return chat.title or chat.username or str(chat.chat_id)
