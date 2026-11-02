import pytest

from harilebs_core.telegram_mentions import build_user_mention


def test_build_user_mention():
    assert build_user_mention(12345, "Hari") == (
        '<a href="tg://user?id=12345">Hari</a>'
    )


def test_escape_html_characters():
    result = build_user_mention(123, '<Hari & "Friends">')
    assert result == (
        '<a href="tg://user?id=123">'
        '&lt;Hari &amp; &quot;Friends&quot;&gt;</a>'
    )


def test_escape_apostrophe():
    result = build_user_mention(123, "Hari's Bot")
    assert "&#x27;" in result


@pytest.mark.parametrize("user_id", [0, -1, -123])
def test_invalid_user_id(user_id):
    with pytest.raises(ValueError):
        build_user_mention(user_id, "Hari")


@pytest.mark.parametrize("user_id", ["123", None, 1.5, True, False])
def test_user_id_type_error(user_id):
    with pytest.raises(TypeError):
        build_user_mention(user_id, "Hari")


@pytest.mark.parametrize("name", ["", "   "])
def test_empty_name(name):
    with pytest.raises(ValueError):
        build_user_mention(123, name)


@pytest.mark.parametrize("name", [123, None, True])
def test_name_type_error(name):
    with pytest.raises(TypeError):
        build_user_mention(123, name)


def test_unicode_name():
    assert build_user_mention(123, "हरि") == (
        '<a href="tg://user?id=123">हरि</a>'
    )


def test_name_whitespace_is_preserved():
    assert build_user_mention(123, " Hari ") == (
        '<a href="tg://user?id=123"> Hari </a>'
    )
