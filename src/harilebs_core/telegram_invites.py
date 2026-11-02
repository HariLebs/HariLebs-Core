"""Utilities for handling Telegram invite links."""

from urllib.parse import urlparse


def build_invite_link(invite_hash: str) -> str:
    """Build a Telegram invite link from an invite hash."""
    if not isinstance(invite_hash, str):
        raise TypeError("invite_hash must be a string.")

    invite_hash = invite_hash.strip().removeprefix("+")

    if not invite_hash:
        raise ValueError("invite_hash cannot be empty.")

    if not invite_hash.replace("_", "").replace("-", "").isalnum():
        raise ValueError("invite_hash contains invalid characters.")

    return f"https://t.me/+{invite_hash}"


def is_valid_invite_link(link: str) -> bool:
    """Check whether a link uses a supported Telegram invite format."""
    if not isinstance(link, str):
        raise TypeError("link must be a string.")

    try:
        parsed = urlparse(link.strip())
    except ValueError:
        return False

    if parsed.scheme not in {"http", "https"}:
        return False

    if parsed.netloc.lower() not in {"t.me", "www.t.me"}:
        return False

    path = parsed.path.strip("/")

    if path.startswith("+"):
        code = path[1:]
    elif path.startswith("joinchat/"):
        code = path.removeprefix("joinchat/")
    else:
        return False

    return bool(code) and code.replace("_", "").replace("-", "").isalnum()


def extract_invite_hash(link: str) -> str:
    """Extract the invite hash from a supported Telegram invite link."""
    if not isinstance(link, str):
        raise TypeError("link must be a string.")

    if not is_valid_invite_link(link):
        raise ValueError("Invalid Telegram invite link.")

    path = urlparse(link.strip()).path.strip("/")

    if path.startswith("+"):
        return path[1:]

    return path.removeprefix("joinchat/")
