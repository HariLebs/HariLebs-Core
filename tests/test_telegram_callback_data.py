import pytest

from harilebs_core.telegram_callback_data import (
    MAX_CALLBACK_DATA_BYTES,
    build_callback_data,
    parse_callback_data,
    validate_callback_data,
)


def test_build_callback_data():
    assert build_callback_data("user", 123) == "user:123"


def test_build_with_custom_separator():
    assert build_callback_data("menu", "open", separator="|") == "menu|open"


def test_build_single_part():
    assert build_callback_data("start") == "start"


def test_build_without_parts():
    with pytest.raises(ValueError):
        build_callback_data()


@pytest.mark.parametrize("part", ["", "hello:world"])
def test_invalid_string_parts(part):
    with pytest.raises(ValueError):
        build_callback_data(part)


@pytest.mark.parametrize("part", [True, False, 1.5, None, []])
def test_invalid_part_types(part):
    with pytest.raises(TypeError):
        build_callback_data(part)


def test_invalid_separator_type():
    with pytest.raises(TypeError):
        build_callback_data("test", separator=1)


@pytest.mark.parametrize("separator", ["", "::", "abc"])
def test_invalid_separator_length(separator):
    with pytest.raises(ValueError):
        build_callback_data("test", separator=separator)


def test_callback_data_over_limit():
    with pytest.raises(ValueError):
        build_callback_data("a" * 65)


def test_callback_data_exact_limit():
    data = "a" * MAX_CALLBACK_DATA_BYTES
    assert validate_callback_data(data) is True


def test_utf8_byte_limit():
    with pytest.raises(ValueError):
        validate_callback_data("अ" * 22)


def test_validate_invalid_type():
    with pytest.raises(TypeError):
        validate_callback_data(123)


def test_validate_empty_data():
    with pytest.raises(ValueError):
        validate_callback_data("")


def test_parse_callback_data():
    assert parse_callback_data("user:123") == ("user", "123")


def test_parse_custom_separator():
    assert parse_callback_data("menu|open", "|") == ("menu", "open")


def test_parse_single_part():
    assert parse_callback_data("start") == ("start",)


def test_parse_invalid_data():
    with pytest.raises(ValueError):
        parse_callback_data("")


def test_parse_invalid_separator():
    with pytest.raises(ValueError):
        parse_callback_data("test", "::")


def test_parse_invalid_separator_type():
    with pytest.raises(TypeError):
        parse_callback_data("test", 1)
