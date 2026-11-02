"""Common Telegram utility helpers."""

from html import escape

from aiogram.utils.text_decorations import html_decoration


def escape_html(text: str) -> str:
    """Escape special HTML characters."""
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")
    return escape(text, quote=True)


def split_text(text: str, limit: int = 4096) -> list[str]:
    """Split text into chunks without exceeding the limit."""
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("Limit must be a positive integer.")

    if not text:
        return []

    return [text[i:i + limit] for i in range(0, len(text), limit)]


def format_html(text: str) -> str:
    """Format plain text safely for Telegram HTML messages."""
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")
    return html_decoration.quote(text)
