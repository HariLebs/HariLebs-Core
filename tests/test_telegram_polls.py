import pytest

from harilebs_core.telegram_polls import (
    TelegramPollInfo,
    build_poll_info,
)


def test_build_regular_poll():
    poll = build_poll_info("Favorite color?", ["Red", "Blue"])
    assert poll == TelegramPollInfo(
        "Favorite color?", ("Red", "Blue")
    )


def test_build_quiz_poll():
    poll = build_poll_info(
        "Capital of France?",
        ["Paris", "London"],
        poll_type="quiz",
        correct_option_id=0,
    )
    assert poll.poll_type == "quiz"
    assert poll.correct_option_id == 0


def test_options_are_normalized():
    poll = build_poll_info(" Question ", [" Red ", " Blue "])
    assert poll.question == "Question"
    assert poll.options == ("Red", "Blue")


def test_multiple_answers():
    poll = build_poll_info(
        "Choose colors", ["Red", "Blue"], allows_multiple_answers=True
    )
    assert poll.allows_multiple_answers is True


def test_non_anonymous_poll():
    poll = build_poll_info("Question", ["A", "B"], is_anonymous=False)
    assert poll.is_anonymous is False


@pytest.mark.parametrize("question", ["", "   "])
def test_empty_question(question):
    with pytest.raises(ValueError):
        build_poll_info(question, ["A", "B"])


@pytest.mark.parametrize("question", [123, None])
def test_question_type(question):
    with pytest.raises(TypeError):
        build_poll_info(question, ["A", "B"])


def test_question_too_long():
    with pytest.raises(ValueError):
        build_poll_info("Q" * 301, ["A", "B"])


@pytest.mark.parametrize("options", [None, "A,B", 123])
def test_options_type(options):
    with pytest.raises(TypeError):
        build_poll_info("Question", options)


@pytest.mark.parametrize("options", [[], ["A"], ["A"] * 11])
def test_invalid_option_count(options):
    with pytest.raises(ValueError):
        build_poll_info("Question", options)


def test_option_item_type():
    with pytest.raises(TypeError):
        build_poll_info("Question", ["A", 123])


def test_empty_option():
    with pytest.raises(ValueError):
        build_poll_info("Question", ["A", "  "])


def test_option_too_long():
    with pytest.raises(ValueError):
        build_poll_info("Question", ["A", "B" * 101])


def test_anonymous_type():
    with pytest.raises(TypeError):
        build_poll_info("Question", ["A", "B"], is_anonymous=1)


def test_multiple_answers_type():
    with pytest.raises(TypeError):
        build_poll_info("Question", ["A", "B"], allows_multiple_answers=1)


def test_invalid_poll_type():
    with pytest.raises(ValueError):
        build_poll_info("Question", ["A", "B"], poll_type="unknown")


def test_quiz_multiple_answers_rejected():
    with pytest.raises(ValueError):
        build_poll_info(
            "Question", ["A", "B"],
            poll_type="quiz",
            allows_multiple_answers=True,
        )


def test_correct_option_requires_quiz():
    with pytest.raises(ValueError):
        build_poll_info("Question", ["A", "B"], correct_option_id=0)


def test_correct_option_type():
    with pytest.raises(TypeError):
        build_poll_info(
            "Question", ["A", "B"],
            poll_type="quiz",
            correct_option_id=True,
        )


def test_correct_option_out_of_range():
    with pytest.raises(ValueError):
        build_poll_info(
            "Question", ["A", "B"],
            poll_type="quiz",
            correct_option_id=2,
        )


def test_quiz_without_correct_option():
    poll = build_poll_info("Question", ["A", "B"], poll_type="quiz")
    assert poll.correct_option_id is None
