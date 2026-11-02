"""Utilities for Telegram callback data."""

from typing import Any


MAX_CALLBACK_DATA_BYTES = 64


def _validate_separator(separator: str) -> None:
    if not isinstance(separator, str):
        raise TypeError("Separator must be a string.")
    if len(separator) != 1:
        raise ValueError("Separator must be exactly one character.")


def validate_callback_data(data: str) -> bool:
    """Validate callback data against Telegram's 64-byte limit."""
    if not isinstance(data, str):
        raise TypeError("Callback data must be a string.")
    if not data:
        raise ValueError("Callback data cannot be empty.")
    if len(data.encode("utf-8")) > MAX_CALLBACK_DATA_BYTES:
        raise ValueError("Callback data cannot exceed 64 bytes.")
    return True


def build_callback_data(*parts: Any, separator: str = ":") -> str:
    """Build callback data from individual parts."""
    _validate_separator(separator)

    if not parts:
        raise ValueError("At least one callback data part is required.")

    values = []

    for part in parts:
        if isinstance(part, bool) or not isinstance(part, (str, int)):
            raise TypeError("Callback data parts must be strings or integers.")

        value = str(part)

        if not value:
            raise ValueError("Callback data parts cannot be empty.")
        if separator in value:
            raise ValueError("Callback data parts cannot contain the separator.")

        values.append(value)

    result = separator.join(values)
    validate_callback_data(result)
    return result


def parse_callback_data(
    data: str,
    separator: str = ":",
) -> tuple[str, ...]:
    """Split callback data into its original parts."""
    _validate_separator(separator)
    validate_callback_data(data)
    return tuple(data.split(separator))
