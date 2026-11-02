"""Reusable Telegram keyboard builders."""

from collections.abc import Iterable

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def _validate_rows(rows):
    if not isinstance(rows, (list, tuple)) or not rows:
        raise ValueError("Keyboard rows cannot be empty.")

    for row in rows:
        if not isinstance(row, (list, tuple)) or not row:
            raise ValueError("Keyboard rows cannot be empty.")

        for button in row:
            if not isinstance(button, (list, tuple)) or len(button) != 2:
                raise ValueError("Each button must contain text and data.")

            if any(
                not isinstance(value, str) or not value.strip()
                for value in button
            ):
                raise ValueError("Button values must be non-empty strings.")


def build_inline_keyboard(
    rows: Iterable[Iterable[tuple[str, str]]],
) -> InlineKeyboardMarkup:
    """Build an inline keyboard from text and callback-data pairs."""
    _validate_rows(rows)

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text, callback_data=data)
                for text, data in row
            ]
            for row in rows
        ]
    )


def build_reply_keyboard(
    rows: Iterable[Iterable[tuple[str, str]]],
    resize_keyboard: bool = True,
    one_time_keyboard: bool = False,
) -> ReplyKeyboardMarkup:
    """Build a reply keyboard from text pairs."""
    _validate_rows(rows)

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=text) for text, _ in row]
            for row in rows
        ],
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
    )
