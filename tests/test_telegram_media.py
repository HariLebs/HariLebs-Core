import pytest

from harilebs_core.telegram_media import (
    get_file_extension,
    get_media_type,
    get_media_type_from_mime,
)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("photo.jpg", "image"),
        ("photo.PNG", "image"),
        ("animation.gif", "image"),
        ("video.mp4", "video"),
        ("movie.mkv", "video"),
        ("song.mp3", "audio"),
        ("sound.wav", "audio"),
        ("file.pdf", "document"),
        ("archive.zip", "document"),
        ("file.unknown", "unknown"),
        ("file", "unknown"),
    ],
)
def test_get_media_type(name, expected):
    assert get_media_type(name) == expected


def test_get_media_type_invalid_type():
    with pytest.raises(TypeError):
        get_media_type(123)


def test_get_media_type_empty():
    with pytest.raises(ValueError):
        get_media_type(" ")


@pytest.mark.parametrize(
    ("name", "expected"),
    [("photo.JPG", ".jpg"), ("file.PDF", ".pdf"), ("README", "")],
)
def test_get_file_extension(name, expected):
    assert get_file_extension(name) == expected


def test_get_file_extension_invalid_type():
    with pytest.raises(TypeError):
        get_file_extension(None)


def test_get_file_extension_empty():
    with pytest.raises(ValueError):
        get_file_extension("")


@pytest.mark.parametrize(
    ("mime", "expected"),
    [
        ("image/jpeg", "image"),
        ("video/mp4", "video"),
        ("audio/mpeg", "audio"),
        ("application/pdf", "document"),
        ("text/plain", "unknown"),
        ("invalid", "unknown"),
    ],
)
def test_get_media_type_from_mime(mime, expected):
    assert get_media_type_from_mime(mime) == expected


def test_mime_case_and_spaces():
    assert get_media_type_from_mime(" IMAGE/PNG ") == "image"


def test_mime_invalid_type():
    with pytest.raises(TypeError):
        get_media_type_from_mime(123)


def test_mime_empty():
    with pytest.raises(ValueError):
        get_media_type_from_mime(" ")
