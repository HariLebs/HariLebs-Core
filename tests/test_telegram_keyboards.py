import pytest

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

from harilebs_core.telegram_keyboards import (
    build_inline_keyboard,
    build_reply_keyboard,
)


def test_inline_keyboard():
    keyboard = build_inline_keyboard([[("Open", "open")]])
    assert isinstance(keyboard, InlineKeyboardMarkup)
    assert keyboard.inline_keyboard[0][0].text == "Open"
    assert keyboard.inline_keyboard[0][0].callback_data == "open"


def test_inline_multiple_rows():
    keyboard = build_inline_keyboard([
        [("One", "one"), ("Two", "two")],
        [("Three", "three")],
    ])
    assert len(keyboard.inline_keyboard) == 2
    assert len(keyboard.inline_keyboard[0]) == 2


def test_reply_keyboard():
    keyboard = build_reply_keyboard([[("Start", "ignored")]])
    assert isinstance(keyboard, ReplyKeyboardMarkup)
    assert keyboard.keyboard[0][0].text == "Start"
    assert keyboard.resize_keyboard is True
    assert keyboard.one_time_keyboard is False


def test_reply_keyboard_options():
    keyboard = build_reply_keyboard(
        [[("Start", "ignored")]],
        resize_keyboard=False,
        one_time_keyboard=True,
    )
    assert keyboard.resize_keyboard is False
    assert keyboard.one_time_keyboard is True


@pytest.mark.parametrize("rows", [[], None, "invalid", [[]], [()]])
def test_invalid_rows(rows):
    with pytest.raises(ValueError):
        build_inline_keyboard(rows)


@pytest.mark.parametrize(
    "button",
    ["invalid", ("Only one",), ("", "data"), ("text", ""), (1, "data")],
)
def test_invalid_buttons(button):
    with pytest.raises(ValueError):
        build_inline_keyboard([[button]])


def test_reply_keyboard_invalid_rows():
    with pytest.raises(ValueError):
        build_reply_keyboard([])


def test_reply_keyboard_invalid_button():
    with pytest.raises(ValueError):
        build_reply_keyboard([[("Text", "")]])
