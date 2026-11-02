import pytest

from harilebs_core.telegram_files import (
    TelegramFileInfo,
    build_file_info,
    is_file_within_limit,
)


def test_build_file_info():
    result = build_file_info("file123", "unique123", 1024, "photo.jpg")
    assert result == TelegramFileInfo("file123", "unique123", 1024, "photo.jpg")


def test_build_minimal_file_info():
    result = build_file_info("file123", "unique123")
    assert result.file_size is None
    assert result.file_name is None


@pytest.mark.parametrize("file_id", ["", "   "])
def test_empty_file_id(file_id):
    with pytest.raises(ValueError):
        build_file_info(file_id, "unique123")


def test_file_id_type():
    with pytest.raises(TypeError):
        build_file_info(123, "unique123")


@pytest.mark.parametrize("value", ["", "   "])
def test_empty_unique_id(value):
    with pytest.raises(ValueError):
        build_file_info("file123", value)


def test_unique_id_type():
    with pytest.raises(TypeError):
        build_file_info("file123", 123)


@pytest.mark.parametrize("size", [-1, -100])
def test_negative_file_size(size):
    with pytest.raises(ValueError):
        build_file_info("file123", "unique123", size)


@pytest.mark.parametrize("size", ["100", 1.5, True])
def test_invalid_file_size(size):
    with pytest.raises(TypeError):
        build_file_info("file123", "unique123", size)


@pytest.mark.parametrize("name", ["", "   "])
def test_empty_file_name(name):
    with pytest.raises(ValueError):
        build_file_info("file123", "unique123", file_name=name)


def test_invalid_file_name_type():
    with pytest.raises(TypeError):
        build_file_info("file123", "unique123", file_name=123)


def test_file_within_limit():
    info = build_file_info("file123", "unique123", 500)
    assert is_file_within_limit(info, 1000) is True


def test_file_equal_to_limit():
    info = build_file_info("file123", "unique123", 500)
    assert is_file_within_limit(info, 500) is True


def test_file_exceeds_limit():
    info = build_file_info("file123", "unique123", 501)
    assert is_file_within_limit(info, 500) is False


def test_unknown_file_size():
    info = build_file_info("file123", "unique123")
    assert is_file_within_limit(info, 500) is False


def test_invalid_file_info():
    with pytest.raises(TypeError):
        is_file_within_limit("file123", 500)


@pytest.mark.parametrize("limit", ["500", 1.5, True])
def test_invalid_limit_type(limit):
    info = build_file_info("file123", "unique123", 100)
    with pytest.raises(TypeError):
        is_file_within_limit(info, limit)


def test_negative_limit():
    info = build_file_info("file123", "unique123", 100)
    with pytest.raises(ValueError):
        is_file_within_limit(info, -1)
