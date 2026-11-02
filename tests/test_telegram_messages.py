import pytest

from harilebs_core.telegram_messages import (
    TELEGRAM_MESSAGE_LIMIT,
    count_message_chunks,
    prepare_message,
    validate_message_text,
)


def test_validate_message_text():
    assert validate_message_text("Hello") is True


def test_validate_maximum_length():
    assert validate_message_text("a" * TELEGRAM_MESSAGE_LIMIT) is True


def test_validate_empty_text():
    with pytest.raises(ValueError):
        validate_message_text("")


@pytest.mark.parametrize("value", [123, None, True])
def test_validate_invalid_type(value):
    with pytest.raises(TypeError):
        validate_message_text(value)


def test_validate_text_over_limit():
    with pytest.raises(ValueError):
        validate_message_text("a" * (TELEGRAM_MESSAGE_LIMIT + 1))


def test_prepare_short_message():
    assert prepare_message("Hello") == ["Hello"]


def test_prepare_empty_message():
    with pytest.raises(ValueError):
        prepare_message("")


def test_prepare_exact_limit():
    text = "a" * TELEGRAM_MESSAGE_LIMIT
    assert prepare_message(text) == [text]


def test_prepare_long_message():
    text = "a" * (TELEGRAM_MESSAGE_LIMIT + 1)
    chunks = prepare_message(text)

    assert len(chunks) == 2
    assert "".join(chunks) == text
    assert all(len(chunk) <= TELEGRAM_MESSAGE_LIMIT for chunk in chunks)


def test_prepare_invalid_type():
    with pytest.raises(TypeError):
        prepare_message(123)


def test_count_one_chunk():
    assert count_message_chunks("Hello") == 1


def test_count_multiple_chunks():
    text = "a" * (TELEGRAM_MESSAGE_LIMIT * 2 + 1)
    assert count_message_chunks(text) == 3


def test_count_empty_message():
    with pytest.raises(ValueError):
        count_message_chunks("")


def test_count_invalid_type():
    with pytest.raises(TypeError):
        count_message_chunks(None)
