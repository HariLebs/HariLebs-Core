"""Utilities for validating Telegram file information."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TelegramFileInfo:
    file_id: str
    file_unique_id: str
    file_size: int | None = None
    file_name: str | None = None


def build_file_info(
    file_id: str,
    file_unique_id: str,
    file_size: int | None = None,
    file_name: str | None = None,
) -> TelegramFileInfo:
    """Build validated Telegram file information."""
    if not isinstance(file_id, str):
        raise TypeError("file_id must be a string.")
    if not file_id.strip():
        raise ValueError("file_id cannot be empty.")

    if not isinstance(file_unique_id, str):
        raise TypeError("file_unique_id must be a string.")
    if not file_unique_id.strip():
        raise ValueError("file_unique_id cannot be empty.")

    if file_size is not None:
        if isinstance(file_size, bool) or not isinstance(file_size, int):
            raise TypeError("file_size must be an integer or None.")
        if file_size < 0:
            raise ValueError("file_size cannot be negative.")

    if file_name is not None:
        if not isinstance(file_name, str):
            raise TypeError("file_name must be a string or None.")
        if not file_name.strip():
            raise ValueError("file_name cannot be empty.")

    return TelegramFileInfo(
        file_id=file_id,
        file_unique_id=file_unique_id,
        file_size=file_size,
        file_name=file_name,
    )


def is_file_within_limit(
    file_info: TelegramFileInfo,
    max_size: int,
) -> bool:
    """Check whether a known file size is within the supplied limit."""
    if not isinstance(file_info, TelegramFileInfo):
        raise TypeError("file_info must be TelegramFileInfo.")

    if isinstance(max_size, bool) or not isinstance(max_size, int):
        raise TypeError("max_size must be an integer.")

    if max_size < 0:
        raise ValueError("max_size cannot be negative.")

    if file_info.file_size is None:
        return False

    return file_info.file_size <= max_size
