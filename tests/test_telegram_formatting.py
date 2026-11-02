import pytest

from harilebs_core.telegram_formatting import (
    bold,
    code,
    italic,
    link,
    pre,
    strikethrough,
    underline,
)


@pytest.mark.parametrize(
    ("formatter", "expected"),
    [
        (bold, "<b>Hello</b>"),
        (italic, "<i>Hello</i>"),
        (underline, "<u>Hello</u>"),
        (strikethrough, "<s>Hello</s>"),
        (code, "<code>Hello</code>"),
        (pre, "<pre>Hello</pre>"),
    ],
)
def test_formatters(formatter, expected):
    assert formatter("Hello") == expected


@pytest.mark.parametrize(
    "formatter",
    [bold, italic, underline, strikethrough, code, pre],
)
def test_formatters_escape_html(formatter):
    assert "&lt;script&gt;" in formatter("<script>")


@pytest.mark.parametrize(
    "formatter",
    [bold, italic, underline, strikethrough, code, pre],
)
@pytest.mark.parametrize("value", [123, None, True])
def test_formatters_reject_invalid_text(formatter, value):
    with pytest.raises(TypeError):
        formatter(value)


def test_empty_text():
    assert bold("") == "<b></b>"


def test_link():
    assert link("Open", "https://example.com") == (
        '<a href="https://example.com">Open</a>'
    )


def test_link_escapes_text():
    assert link("<Open>", "https://example.com") == (
        '<a href="https://example.com">'
        '&lt;Open&gt;</a>'
    )


def test_link_escapes_url():
    assert link("Open", "https://example.com/?a=1&b=2") == (
        '<a href="https://example.com/?a=1&amp;b=2">Open</a>'
    )


@pytest.mark.parametrize("url", [
    "javascript:alert(1)",
    "file:///test",
    "ftp://example.com",
    "",
])
def test_invalid_url_scheme(url):
    with pytest.raises(ValueError):
        link("Open", url)


@pytest.mark.parametrize("url", [
    'https://example.com/"test"',
    "https://example.com/<test>",
    "https://example.com/\ntest",
    "https://example.com/\rtest",
])
def test_invalid_url_characters(url):
    with pytest.raises(ValueError):
        link("Open", url)


@pytest.mark.parametrize("url", [123, None])
def test_invalid_url_type(url):
    with pytest.raises(TypeError):
        link("Open", url)


@pytest.mark.parametrize("text", [123, None])
def test_invalid_link_text(text):
    with pytest.raises(TypeError):
        link(text, "https://example.com")


def test_telegram_url():
    assert link("Profile", "tg://user?id=123") == (
        '<a href="tg://user?id=123">Profile</a>'
    )
