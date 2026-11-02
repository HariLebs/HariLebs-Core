"""Utilities for validating and preparing Telegram messages."""

from harilebs_core.telegram_helpers import split_text


TELEGRAM_MESSAGE_LIMIT = 4096


def validate_message_text(text: str) -> bool:
    """Validate Telegram message text."""
    if not isinstance(text, str):
        raise TypeError("Message text must be a string.")

    if not text:
        raise ValueError("Message text cannot be empty.")

    if len(text) > TELEGRAM_MESSAGE_LIMIT:
        raise ValueError("Message text exceeds Telegram's 4096 character limit.")

    return True


def prepare_message(text: str) -> list[str]:
    """Validate text and return one or more Telegram-sized chunks."""
    if not isinstance(text, str):
        raise TypeError("Message text must be a string.")

    if not text:
        raise ValueError("Message text cannot be empty.")

    return split_text(text, TELEGRAM_MESSAGE_LIMIT)


def count_message_chunks(text: str) -> int:
    """Return the number of chunks required for a Telegram message."""
    return len(prepare_message(text))
