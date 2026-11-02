import pytest
from aiogram.types import BotCommand

from harilebs_core.telegram_commands import build_bot_commands


def test_build_commands_from_dict():
    result = build_bot_commands({
        "start": "Start the bot",
        "help": "Get help",
    })

    assert result == [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Get help"),
    ]


def test_build_commands_from_list():
    result = build_bot_commands([
        ("start", "Start the bot"),
        ("settings", "Open settings"),
    ])

    assert len(result) == 2
    assert result[0].command == "start"


def test_build_commands_from_tuple():
    result = build_bot_commands((("help", "Get help"),))
    assert result[0].description == "Get help"


def test_empty_commands():
    assert build_bot_commands({}) == []
    assert build_bot_commands([]) == []


@pytest.mark.parametrize("value", ["start", 123, None, set()])
def test_invalid_container(value):
    with pytest.raises(TypeError):
        build_bot_commands(value)


@pytest.mark.parametrize("item", [
    ("start",),
    ("start", "description", "extra"),
    "start",
    123,
])
def test_invalid_command_item(item):
    with pytest.raises(ValueError):
        build_bot_commands([item])


@pytest.mark.parametrize("command", [
    "",
    "Start",
    "two words",
    "bad-command",
    "bad.command",
    "हिंदी",
    "a" * 33,
])
def test_invalid_command_name(command):
    with pytest.raises(ValueError):
        build_bot_commands([(command, "Description")])


@pytest.mark.parametrize("description", ["", "   ", "d" * 257])
def test_invalid_description(description):
    with pytest.raises(ValueError):
        build_bot_commands([("start", description)])


@pytest.mark.parametrize("item", [
    (123, "Description"),
    ("start", 123),
])
def test_invalid_field_types(item):
    with pytest.raises(TypeError):
        build_bot_commands([item])


def test_maximum_command_length():
    result = build_bot_commands([("a" * 32, "Valid description")])
    assert len(result[0].command) == 32


def test_maximum_description_length():
    result = build_bot_commands([("start", "d" * 256)])
    assert len(result[0].description) == 256
