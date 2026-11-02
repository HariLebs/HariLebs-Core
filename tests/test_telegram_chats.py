import pytest

from harilebs_core.telegram_chats import (
    TelegramChatInfo,
    build_chat_info,
    get_chat_display_name,
)


def test_build_chat_info():
    assert build_chat_info(-100123, "supergroup", "Test") == (
        TelegramChatInfo(-100123, "supergroup", "Test")
    )


@pytest.mark.parametrize("chat_type", ["private", "group", "supergroup", "channel"])
def test_valid_chat_types(chat_type):
    assert build_chat_info(123, chat_type).chat_type == chat_type


def test_username_normalization():
    assert build_chat_info(123, "private", username="@hari").username == "hari"


def test_optional_fields():
    chat = build_chat_info(123, "private")
    assert chat.title is None
    assert chat.username is None


@pytest.mark.parametrize("chat_id", [True, "123", 1.5, None])
def test_chat_id_type(chat_id):
    with pytest.raises(TypeError):
        build_chat_info(chat_id, "private")


def test_zero_chat_id():
    with pytest.raises(ValueError):
        build_chat_info(0, "private")


def test_invalid_chat_type_value():
    with pytest.raises(ValueError):
        build_chat_info(123, "unknown")


def test_chat_type_must_be_string():
    with pytest.raises(TypeError):
        build_chat_info(123, 123)


@pytest.mark.parametrize("field", ["title", "username"])
def test_invalid_optional_field_type(field):
    with pytest.raises(TypeError):
        build_chat_info(123, "private", **{field: 123})


@pytest.mark.parametrize("field", ["title", "username"])
def test_empty_optional_field(field):
    with pytest.raises(ValueError):
        build_chat_info(123, "private", **{field: "   "})


def test_display_title():
    assert get_chat_display_name(
        build_chat_info(123, "group", title="My Group")
    ) == "My Group"


def test_display_username_fallback():
    assert get_chat_display_name(
        build_chat_info(123, "channel", username="news")
    ) == "news"


def test_display_id_fallback():
    assert get_chat_display_name(
        build_chat_info(123, "private")
    ) == "123"


def test_display_title_preferred():
    chat = build_chat_info(123, "group", title="Group", username="groupname")
    assert get_chat_display_name(chat) == "Group"


def test_display_invalid_chat():
    with pytest.raises(TypeError):
        get_chat_display_name("not a chat")
