"""Utilities for building Telegram bot commands."""

from collections.abc import Mapping, Sequence

from aiogram.types import BotCommand


def build_bot_commands(
    commands: Mapping[str, str] | Sequence[tuple[str, str]],
) -> list[BotCommand]:
    """Build validated Telegram BotCommand objects."""
    if not isinstance(commands, (Mapping, list, tuple)):
        raise TypeError("Commands must be a mapping, list, or tuple.")

    items = list(commands.items()) if isinstance(commands, Mapping) else list(commands)

    result = []

    for item in items:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise ValueError("Each command must contain a name and description.")

        command, description = item

        if not isinstance(command, str) or not isinstance(description, str):
            raise TypeError("Command names and descriptions must be strings.")

        if (
            not command
            or len(command) > 32
            or not command.isascii()
            or not command.islower()
            or not all(char.isalnum() or char == "_" for char in command)
        ):
            raise ValueError("Invalid Telegram command name.")

        if not description.strip() or len(description) > 256:
            raise ValueError("Invalid Telegram command description.")

        result.append(
            BotCommand(command=command, description=description)
        )

    return result
