import pytest

from harilebs_core.telegram_helpers import (
    escape_html,
    format_html,
    split_text,
)


def test_escape_html():
    assert escape_html("<hello> & 'world'") == (
        "&lt;hello&gt; &amp; &#x27;world&#x27;"
    )


def test_escape_html_invalid():
    with pytest.raises(TypeError):
        escape_html(123)


def test_split_text():
    assert split_text("abcdefgh", 3) == ["abc", "def", "gh"]


def test_split_text_empty():
    assert split_text("") == []


def test_split_text_short():
    assert split_text("hello", 10) == ["hello"]


def test_split_text_invalid_type():
    with pytest.raises(TypeError):
        split_text(123)


@pytest.mark.parametrize("limit", [0, -1, True, 1.5, "5"])
def test_split_text_invalid_limit(limit):
    with pytest.raises(ValueError):
        split_text("hello", limit)


def test_format_html():
    assert format_html("<hello> & world") == "&lt;hello&gt; &amp; world"


def test_format_html_invalid():
    with pytest.raises(TypeError):
        format_html(None)
