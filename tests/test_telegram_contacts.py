import pytest

from harilebs_core.telegram_contacts import (
    TelegramContactInfo,
    build_contact_info,
    format_phone_number,
    get_contact_display_name,
    has_telegram_user_id,
)


def test_build_contact():
    contact = build_contact_info("+919876543210", "Hari", "Beniwal", 123)
    assert contact == TelegramContactInfo(
        "+919876543210", "Hari", "Beniwal", 123
    )


def test_build_minimal_contact():
    contact = build_contact_info("9876543210", "Hari")
    assert contact.last_name is None
    assert contact.user_id is None


def test_phone_without_plus():
    contact = build_contact_info("9876543210", "Hari")
    assert contact.phone_number == "9876543210"


def test_phone_with_spaces_around():
    contact = build_contact_info(" +919876543210 ", "Hari")
    assert contact.phone_number == "+919876543210"


@pytest.mark.parametrize("phone", [12345, None, True])
def test_phone_type(phone):
    with pytest.raises(TypeError):
        build_contact_info(phone, "Hari")


@pytest.mark.parametrize("phone", ["", "   "])
def test_empty_phone(phone):
    with pytest.raises(ValueError):
        build_contact_info(phone, "Hari")


@pytest.mark.parametrize("phone", ["abc12345", "++919876543210", "+91-9876543210"])
def test_invalid_phone_characters(phone):
    with pytest.raises(ValueError):
        build_contact_info(phone, "Hari")


@pytest.mark.parametrize("phone", ["1234", "1" * 16])
def test_invalid_phone_length(phone):
    with pytest.raises(ValueError):
        build_contact_info(phone, "Hari")


@pytest.mark.parametrize("name", [123, None])
def test_first_name_type(name):
    with pytest.raises(TypeError):
        build_contact_info("9876543210", name)


@pytest.mark.parametrize("name", ["", "   "])
def test_empty_first_name(name):
    with pytest.raises(ValueError):
        build_contact_info("9876543210", name)


def test_last_name_type():
    with pytest.raises(TypeError):
        build_contact_info("9876543210", "Hari", 123)


def test_empty_last_name():
    with pytest.raises(ValueError):
        build_contact_info("9876543210", "Hari", "  ")


def test_user_id_type():
    with pytest.raises(TypeError):
        build_contact_info("9876543210", "Hari", user_id=True)


@pytest.mark.parametrize("user_id", [0, -1])
def test_invalid_user_id(user_id):
    with pytest.raises(ValueError):
        build_contact_info("9876543210", "Hari", user_id=user_id)


def test_display_full_name():
    contact = build_contact_info("9876543210", "Hari", "Beniwal")
    assert get_contact_display_name(contact) == "Hari Beniwal"


def test_display_first_name_only():
    contact = build_contact_info("9876543210", "Hari")
    assert get_contact_display_name(contact) == "Hari"


def test_format_phone_number():
    contact = build_contact_info("9876543210", "Hari")
    assert format_phone_number(contact) == "+9876543210"


def test_has_user_id():
    contact = build_contact_info("9876543210", "Hari", user_id=123)
    assert has_telegram_user_id(contact) is True


def test_has_no_user_id():
    contact = build_contact_info("9876543210", "Hari")
    assert has_telegram_user_id(contact) is False


def test_invalid_display_contact():
    with pytest.raises(TypeError):
        get_contact_display_name("Hari")


def test_invalid_phone_format_contact():
    with pytest.raises(TypeError):
        format_phone_number("9876543210")


def test_invalid_user_id_contact():
    with pytest.raises(TypeError):
        has_telegram_user_id("contact")
