"""Utilities for handling Telegram contact information."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TelegramContactInfo:
    phone_number: str
    first_name: str
    last_name: str | None = None
    user_id: int | None = None


def build_contact_info(
    phone_number: str,
    first_name: str,
    last_name: str | None = None,
    user_id: int | None = None,
) -> TelegramContactInfo:
    """Build validated Telegram contact information."""
    if not isinstance(phone_number, str):
        raise TypeError("phone_number must be a string.")

    phone_number = phone_number.strip()

    if not phone_number:
        raise ValueError("phone_number cannot be empty.")

    normalized_phone = phone_number.removeprefix("+")

    if not normalized_phone.isdigit():
        raise ValueError("phone_number must contain digits and an optional leading +.")

    if not 5 <= len(normalized_phone) <= 15:
        raise ValueError("phone_number must contain between 5 and 15 digits.")

    if not isinstance(first_name, str):
        raise TypeError("first_name must be a string.")

    first_name = first_name.strip()

    if not first_name:
        raise ValueError("first_name cannot be empty.")

    if last_name is not None:
        if not isinstance(last_name, str):
            raise TypeError("last_name must be a string or None.")
        last_name = last_name.strip()
        if not last_name:
            raise ValueError("last_name cannot be empty.")

    if user_id is not None:
        if isinstance(user_id, bool) or not isinstance(user_id, int):
            raise TypeError("user_id must be an integer or None.")
        if user_id <= 0:
            raise ValueError("user_id must be positive.")

    return TelegramContactInfo(
        phone_number=phone_number,
        first_name=first_name,
        last_name=last_name,
        user_id=user_id,
    )


def get_contact_display_name(contact: TelegramContactInfo) -> str:
    """Return the contact's display name."""
    if not isinstance(contact, TelegramContactInfo):
        raise TypeError("contact must be TelegramContactInfo.")

    if contact.last_name:
        return f"{contact.first_name} {contact.last_name}"

    return contact.first_name


def format_phone_number(contact: TelegramContactInfo) -> str:
    """Return the contact's normalized phone number."""
    if not isinstance(contact, TelegramContactInfo):
        raise TypeError("contact must be TelegramContactInfo.")

    digits = contact.phone_number.removeprefix("+")
    return f"+{digits}"


def has_telegram_user_id(contact: TelegramContactInfo) -> bool:
    """Check whether the contact has a Telegram user ID."""
    if not isinstance(contact, TelegramContactInfo):
        raise TypeError("contact must be TelegramContactInfo.")

    return contact.user_id is not None
