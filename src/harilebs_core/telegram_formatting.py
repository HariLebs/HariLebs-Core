"""Utilities for formatting Telegram message text."""

from html import escape


def bold(text: str) -> str:
    """Format text as HTML bold."""
    return f"<b>{_validate_text(text)}</b>"


def italic(text: str) -> str:
    """Format text as HTML italic."""
    return f"<i>{_validate_text(text)}</i>"


def underline(text: str) -> str:
    """Format text as HTML underline."""
    return f"<u>{_validate_text(text)}</u>"


def strikethrough(text: str) -> str:
    """Format text as HTML strikethrough."""
    return f"<s>{_validate_text(text)}</s>"


def code(text: str) -> str:
    """Format text as HTML inline code."""
    return f"<code>{_validate_text(text)}</code>"


def pre(text: str) -> str:
    """Format text as an HTML preformatted block."""
    return f"<pre>{_validate_text(text)}</pre>"


def link(text: str, url: str) -> str:
    """Create a safe HTML link."""
    safe_text = _validate_text(text)

    if not isinstance(url, str):
        raise TypeError("URL must be a string.")

    if not url.startswith(("https://", "http://", "tg://")):
        raise ValueError("Unsupported URL scheme.")

    if any(char in url for char in ('"', "'", "<", ">", "\n", "\r")):
        raise ValueError("Invalid URL.")

    return f'<a href="{escape(url, quote=True)}">{safe_text}</a>'


def _validate_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("Text must be a string.")

    return escape(text, quote=True)
