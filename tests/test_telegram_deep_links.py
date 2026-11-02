import pytest

from harilebs_core.telegram_deep_links import (
    build_start_link,
    parse_start_parameter,
)


def test_build_start_link():
    assert build_start_link("MyTestBot", "welcome") == (
        "https://t.me/MyTestBot?start=welcome"
    )


def test_build_start_link_with_at():
    assert build_start_link("@MyTestBot", "welcome") == (
        "https://t.me/MyTestBot?start=welcome"
    )


def test_build_start_link_with_special_parameter_chars():
    assert build_start_link("MyTestBot", "user_123-abc") == (
        "https://t.me/MyTestBot?start=user_123-abc"
    )


@pytest.mark.parametrize("username", [
    "",
    "abcd",
    "a" * 33,
    "invalid-name",
    "invalid name",
    "bot.name",
])
def test_invalid_username(username):
    with pytest.raises(ValueError):
        build_start_link(username, "welcome")


@pytest.mark.parametrize("username", [123, None])
def test_username_type_error(username):
    with pytest.raises(TypeError):
        build_start_link(username, "welcome")


@pytest.mark.parametrize("parameter", [
    "",
    "contains spaces",
    "invalid.value",
    "invalid/value",
    "a" * 65,
])
def test_invalid_parameter(parameter):
    with pytest.raises(ValueError):
        build_start_link("MyTestBot", parameter)


@pytest.mark.parametrize("parameter", [123, None])
def test_parameter_type_error(parameter):
    with pytest.raises(TypeError):
        build_start_link("MyTestBot", parameter)


def test_parse_start_parameter():
    assert parse_start_parameter(
        "https://t.me/MyTestBot?start=welcome"
    ) == "welcome"


def test_parse_start_parameter_with_hyphen():
    assert parse_start_parameter(
        "https://t.me/MyTestBot?start=user_123-abc"
    ) == "user_123-abc"


def test_parse_missing_parameter():
    assert parse_start_parameter(
        "https://t.me/MyTestBot"
    ) is None


def test_parse_empty_parameter():
    with pytest.raises(ValueError):
        parse_start_parameter("https://t.me/MyTestBot?start=")


def test_parse_duplicate_parameters():
    with pytest.raises(ValueError):
        parse_start_parameter(
            "https://t.me/MyTestBot?start=one&start=two"
        )


@pytest.mark.parametrize("link", [
    "http://t.me/MyTestBot?start=welcome",
    "https://example.com/MyTestBot?start=welcome",
    "https://t.me.evil.com/MyTestBot?start=welcome",
    "not-a-url",
])
def test_invalid_link(link):
    with pytest.raises(ValueError):
        parse_start_parameter(link)


def test_parse_invalid_username():
    with pytest.raises(ValueError):
        parse_start_parameter("https://t.me/abcd?start=welcome")


def test_parse_invalid_parameter():
    with pytest.raises(ValueError):
        parse_start_parameter(
            "https://t.me/MyTestBot?start=bad.value"
        )


def test_parse_link_type_error():
    with pytest.raises(TypeError):
        parse_start_parameter(123)
