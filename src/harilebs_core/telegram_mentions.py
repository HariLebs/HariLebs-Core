"""Utilities for creating Telegram user mentions."""

from html import escape


def build_user_mention(user_id: int, name: str) -> str:
    """Build a clickable HTML mention using a Telegram user ID."""
    if isinstance(user_id, bool) or not isinstance(user_id, int):
        raise TypeError("User ID must be an integer.")

    if user_id <= 0:
        raise ValueError("User ID must be positive.")

    if not isinstance(name, str):
        raise TypeError("Name must be a string.")

    if not name.strip():
        raise ValueError("Name cannot be empty.")

    safe_name = escape(name, quote=True)

    return f'<a href="tg://user?id={user_id}">{safe_name}</a>'
