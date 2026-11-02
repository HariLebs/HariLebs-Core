import pytest

from harilebs_core.telegram_invites import (
    build_invite_link,
    extract_invite_hash,
    is_valid_invite_link,
)


def test_build_invite_link():
    assert build_invite_link("Abc123") == "https://t.me/+Abc123"


def test_build_invite_link_with_plus():
    assert build_invite_link("+Abc123") == "https://t.me/+Abc123"


def test_build_invite_link_trims_spaces():
    assert build_invite_link(" Abc123 ") == "https://t.me/+Abc123"


@pytest.mark.parametrize("value", [123, None, True])
def test_build_invite_link_type(value):
    with pytest.raises(TypeError):
        build_invite_link(value)


@pytest.mark.parametrize("value", ["", "   "])
def test_build_invite_link_empty(value):
    with pytest.raises(ValueError):
        build_invite_link(value)


def test_build_invite_link_invalid_characters():
    with pytest.raises(ValueError):
        build_invite_link("abc/123")


@pytest.mark.parametrize(
    "link",
    [
        "https://t.me/+Abc123",
        "https://t.me/joinchat/Abc123",
        "http://t.me/+Abc_123",
        "https://www.t.me/+Abc-123",
    ],
)
def test_valid_invite_links(link):
    assert is_valid_invite_link(link) is True


@pytest.mark.parametrize(
    "link",
    [
        "https://example.com/+Abc123",
        "https://t.me/channelname",
        "https://t.me/",
        "ftp://t.me/+Abc123",
        "not-a-link",
        "https://t.me/+",
        "https://t.me/joinchat/",
        "https://t.me/+abc/extra",
    ],
)
def test_invalid_invite_links(link):
    assert is_valid_invite_link(link) is False


def test_invite_link_type():
    with pytest.raises(TypeError):
        is_valid_invite_link(123)


def test_extract_plus_link():
    assert extract_invite_hash("https://t.me/+Abc123") == "Abc123"


def test_extract_joinchat_link():
    assert extract_invite_hash("https://t.me/joinchat/Abc123") == "Abc123"


def test_extract_invalid_link():
    with pytest.raises(ValueError):
        extract_invite_hash("https://t.me/channelname")


def test_extract_link_type():
    with pytest.raises(TypeError):
        extract_invite_hash(123)
