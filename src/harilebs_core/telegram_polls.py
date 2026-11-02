"""Utilities for validating Telegram poll configuration."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TelegramPollInfo:
    question: str
    options: tuple[str, ...]
    is_anonymous: bool = True
    allows_multiple_answers: bool = False
    poll_type: str = "regular"
    correct_option_id: int | None = None


def build_poll_info(
    question: str,
    options: list[str] | tuple[str, ...],
    is_anonymous: bool = True,
    allows_multiple_answers: bool = False,
    poll_type: str = "regular",
    correct_option_id: int | None = None,
) -> TelegramPollInfo:
    """Build validated Telegram poll information."""
    if not isinstance(question, str):
        raise TypeError("question must be a string.")
    if not question.strip():
        raise ValueError("question cannot be empty.")
    if len(question) > 300:
        raise ValueError("question cannot exceed 300 characters.")

    if not isinstance(options, (list, tuple)):
        raise TypeError("options must be a list or tuple.")
    if not 2 <= len(options) <= 10:
        raise ValueError("poll must contain between 2 and 10 options.")

    for option in options:
        if not isinstance(option, str):
            raise TypeError("each option must be a string.")
        if not option.strip():
            raise ValueError("options cannot be empty.")
        if len(option) > 100:
            raise ValueError("each option cannot exceed 100 characters.")

    if not isinstance(is_anonymous, bool):
        raise TypeError("is_anonymous must be a boolean.")
    if not isinstance(allows_multiple_answers, bool):
        raise TypeError("allows_multiple_answers must be a boolean.")

    if poll_type not in {"regular", "quiz"}:
        raise ValueError("poll_type must be regular or quiz.")

    if correct_option_id is not None:
        if isinstance(correct_option_id, bool) or not isinstance(correct_option_id, int):
            raise TypeError("correct_option_id must be an integer or None.")
        if poll_type != "quiz":
            raise ValueError("correct_option_id is only valid for quiz polls.")
        if not 0 <= correct_option_id < len(options):
            raise ValueError("correct_option_id is outside the options range.")

    if poll_type == "quiz" and allows_multiple_answers:
        raise ValueError("quiz polls cannot allow multiple answers.")

    return TelegramPollInfo(
        question=question.strip(),
        options=tuple(option.strip() for option in options),
        is_anonymous=is_anonymous,
        allows_multiple_answers=allows_multiple_answers,
        poll_type=poll_type,
        correct_option_id=correct_option_id,
    )
