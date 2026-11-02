"""Utilities for generating and parsing Telegram deep links."""

import re
from urllib.parse import parse_qs, urlparse


_USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{5,32}$")
_PARAMETER_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def build_start_link(bot_username: str, parameter: str) -> str:
    """Build a Telegram bot start deep link."""
    if not isinstance(bot_username, str):
        raise TypeError("Bot username must be a string.")

    if not isinstance(parameter, str):
        raise TypeError("Start parameter must be a string.")

    username = bot_username.removeprefix("@")

    if not _USERNAME_PATTERN.fullmatch(username):
        raise ValueError("Invalid Telegram bot username.")

    if not _PARAMETER_PATTERN.fullmatch(parameter):
        raise ValueError("Invalid Telegram start parameter.")

    return f"https://t.me/{username}?start={parameter}"


def parse_start_parameter(link: str) -> str | None:
    """Extract the start parameter from a Telegram deep link."""
    if not isinstance(link, str):
        raise TypeError("Link must be a string.")

    parsed = urlparse(link)

    if parsed.scheme != "https" or parsed.netloc.lower() != "t.me":
        raise ValueError("Invalid Telegram deep link.")

    if not _USERNAME_PATTERN.fullmatch(parsed.path.lstrip("/")):
        raise ValueError("Invalid Telegram bot username.")

    parameters = parse_qs(parsed.query, keep_blank_values=True)

    values = parameters.get("start")

    if not values:
        return None

    if len(values) != 1:
        raise ValueError("Multiple start parameters are not allowed.")

    parameter = values[0]

    if not _PARAMETER_PATTERN.fullmatch(parameter):
        raise ValueError("Invalid Telegram start parameter.")

    return parameter
