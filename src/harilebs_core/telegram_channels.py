"""Utilities for handling Telegram channel information."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TelegramChannelInfo:
    chat_id: int
    title: str
    username: str | None = None


def build_channel_info(
    chat_id: int,
    title: str,
    username: str | None = None,
) -> TelegramChannelInfo:
    """Build validated Telegram channel information."""
    if isinstance(chat_id, bool) or not isinstance(chat_id, int):
        raise TypeError("chat_id must be an integer.")
    if chat_id >= 0:
        raise ValueError("Channel chat_id must be negative.")

    if not isinstance(title, str):
        raise TypeError("title must be a string.")
    if not title.strip():
        raise ValueError("title cannot be empty.")

    if username is not None:
        if not isinstance(username, str):
            raise TypeError("username must be a string or None.")
        username = username.removeprefix("@")
        if not username.strip():
            raise ValueError("username cannot be empty.")
        if not username.replace("_", "").isalnum():
            raise ValueError("username can contain only letters, numbers, and underscores.")
        if len(username) < 5 or len(username) > 32:
            raise ValueError("username must be between 5 and 32 characters.")

    return TelegramChannelInfo(
        chat_id=chat_id,
        title=title.strip(),
        username=username,
    )


def is_public_channel(channel: TelegramChannelInfo) -> bool:
    """Return whether the channel has a public username."""
    if not isinstance(channel, TelegramChannelInfo):
        raise TypeError("channel must be TelegramChannelInfo.")
    return channel.username is not None


def get_channel_link(channel: TelegramChannelInfo) -> str | None:
    """Return the public channel link, or None for private channels."""
    if not isinstance(channel, TelegramChannelInfo):
        raise TypeError("channel must be TelegramChannelInfo.")
    if channel.username is None:
        return None
    return f"https://t.me/{channel.username}"


def get_channel_display_name(channel: TelegramChannelInfo) -> str:
    """Return the channel's display name."""
    if not isinstance(channel, TelegramChannelInfo):
        raise TypeError("channel must be TelegramChannelInfo.")
    return channel.title
