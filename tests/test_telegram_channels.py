import pytest

from harilebs_core.telegram_channels import (
    TelegramChannelInfo,
    build_channel_info,
    get_channel_display_name,
    get_channel_link,
    is_public_channel,
)


def test_build_public_channel():
    channel = build_channel_info(-100123, "News", "@news_channel")
    assert channel == TelegramChannelInfo(-100123, "News", "news_channel")


def test_build_private_channel():
    channel = build_channel_info(-100123, "Private News")
    assert channel.username is None


def test_title_is_trimmed():
    assert build_channel_info(-100123, " News ").title == "News"


@pytest.mark.parametrize("chat_id", [True, "123", 1.5, None])
def test_chat_id_type(chat_id):
    with pytest.raises(TypeError):
        build_channel_info(chat_id, "News")


@pytest.mark.parametrize("chat_id", [0, 123])
def test_chat_id_must_be_negative(chat_id):
    with pytest.raises(ValueError):
        build_channel_info(chat_id, "News")


@pytest.mark.parametrize("title", [None, 123])
def test_title_type(title):
    with pytest.raises(TypeError):
        build_channel_info(-100123, title)


@pytest.mark.parametrize("title", ["", "   "])
def test_empty_title(title):
    with pytest.raises(ValueError):
        build_channel_info(-100123, title)


def test_username_type():
    with pytest.raises(TypeError):
        build_channel_info(-100123, "News", 123)


@pytest.mark.parametrize("username", ["", "   "])
def test_empty_username(username):
    with pytest.raises(ValueError):
        build_channel_info(-100123, "News", username)


@pytest.mark.parametrize("username", ["abc", "a" * 33, "news-channel"])
def test_invalid_username(username):
    with pytest.raises(ValueError):
        build_channel_info(-100123, "News", username)


def test_public_channel_detection():
    assert is_public_channel(build_channel_info(-100123, "News", "news_channel"))


def test_private_channel_detection():
    assert not is_public_channel(build_channel_info(-100123, "News"))


def test_public_channel_link():
    channel = build_channel_info(-100123, "News", "news_channel")
    assert get_channel_link(channel) == "https://t.me/news_channel"


def test_private_channel_link():
    channel = build_channel_info(-100123, "News")
    assert get_channel_link(channel) is None


def test_display_name():
    channel = build_channel_info(-100123, "World News")
    assert get_channel_display_name(channel) == "World News"


def test_invalid_channel_argument():
    with pytest.raises(TypeError):
        is_public_channel("not a channel")


def test_invalid_link_argument():
    with pytest.raises(TypeError):
        get_channel_link("not a channel")


def test_invalid_display_argument():
    with pytest.raises(TypeError):
        get_channel_display_name("not a channel")
