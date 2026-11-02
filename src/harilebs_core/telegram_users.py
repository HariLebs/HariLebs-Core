"""Utilities for handling Telegram user information."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TelegramUserInfo:
    user_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_bot: bool = False


def build_user_info(
    user_id: int,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    is_bot: bool = False,
) -> TelegramUserInfo:
    """Build validated Telegram user information."""
    if isinstance(user_id, bool) or not isinstance(user_id, int):
        raise TypeError("user_id must be an integer.")
    if user_id <= 0:
        raise ValueError("user_id must be positive.")

    for name, value in (
        ("username", username),
        ("first_name", first_name),
        ("last_name", last_name),
    ):
        if value is not None and not isinstance(value, str):
            raise TypeError(f"{name} must be a string or None.")
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{name} cannot be empty.")

    if not isinstance(is_bot, bool):
        raise TypeError("is_bot must be a boolean.")

    if username is not None:
        username = username.removeprefix("@")

    return TelegramUserInfo(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        is_bot=is_bot,
    )


def get_display_name(user: TelegramUserInfo) -> str:
    """Return the best available display name."""
    if not isinstance(user, TelegramUserInfo):
        raise TypeError("user must be TelegramUserInfo.")

    full_name = " ".join(
        part for part in (user.first_name, user.last_name) if part
    )

    return full_name or user.username or str(user.user_id)


def get_user_mention_target(user: TelegramUserInfo) -> str:
    """Return a Telegram user ID mention target."""
    if not isinstance(user, TelegramUserInfo):
        raise TypeError("user must be TelegramUserInfo.")

    return f"tg://user?id={user.user_id}"
