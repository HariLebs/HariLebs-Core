"""Utilities for identifying Telegram media types."""

from pathlib import PurePath


MEDIA_TYPES = {
    "image": {".jpg", ".jpeg", ".png", ".webp", ".gif"},
    "video": {".mp4", ".mov", ".mkv", ".webm"},
    "audio": {".mp3", ".wav", ".ogg", ".m4a", ".flac"},
    "document": {".pdf", ".txt", ".doc", ".docx", ".zip"},
}


def get_media_type(file_name: str) -> str:
    """Identify media type using a file extension."""
    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string.")
    if not file_name.strip():
        raise ValueError("file_name cannot be empty.")

    extension = PurePath(file_name.strip()).suffix.lower()

    for media_type, extensions in MEDIA_TYPES.items():
        if extension in extensions:
            return media_type

    return "unknown"


def get_file_extension(file_name: str) -> str:
    """Return a normalized file extension."""
    if not isinstance(file_name, str):
        raise TypeError("file_name must be a string.")
    if not file_name.strip():
        raise ValueError("file_name cannot be empty.")

    return PurePath(file_name.strip()).suffix.lower()


def get_media_type_from_mime(mime_type: str) -> str:
    """Identify media type using a MIME type."""
    if not isinstance(mime_type, str):
        raise TypeError("mime_type must be a string.")
    if not mime_type.strip():
        raise ValueError("mime_type cannot be empty.")

    mime_type = mime_type.strip().lower()

    if "/" not in mime_type:
        return "unknown"

    category = mime_type.split("/", 1)[0]

    if category in {"image", "video", "audio"}:
        return category

    return "document" if category == "application" else "unknown"
