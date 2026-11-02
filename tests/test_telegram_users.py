import pytest

from harilebs_core.telegram_users import (
    TelegramUserInfo,
    build_user_info,
    get_display_name,
    get_user_mention_target,
)


def test_build_user_info():
    user = build_user_info(123, "@hari", "Hari", "Beniwal")
    assert user == TelegramUserInfo(123, "hari", "Hari", "Beniwal")


def test_build_minimal_user():
    user = build_user_info(123)
    assert user.user_id == 123
    assert user.username is None


def test_username_normalization():
    assert build_user_info(123, "@hari").username == "hari"


@pytest.mark.parametrize("user_id", [0, -1])
def test_invalid_user_id(user_id):
    with pytest.raises(ValueError):
        build_user_info(user_id)


@pytest.mark.parametrize("user_id", [True, "123", 1.5, None])
def test_user_id_type(user_id):
    with pytest.raises(TypeError):
        build_user_info(user_id)


@pytest.mark.parametrize("field", ["username", "first_name", "last_name"])
def test_invalid_name_type(field):
    with pytest.raises(TypeError):
        build_user_info(123, **{field: 123})


@pytest.mark.parametrize("field", ["username", "first_name", "last_name"])
def test_empty_name(field):
    with pytest.raises(ValueError):
        build_user_info(123, **{field: "   "})


@pytest.mark.parametrize("value", [1, "true", None])
def test_invalid_is_bot(value):
    with pytest.raises(TypeError):
        build_user_info(123, is_bot=value)


def test_bot_user():
    assert build_user_info(123, is_bot=True).is_bot is True


def test_display_full_name():
    user = build_user_info(123, first_name="Hari", last_name="Beniwal")
    assert get_display_name(user) == "Hari Beniwal"


def test_display_first_name():
    user = build_user_info(123, first_name="Hari")
    assert get_display_name(user) == "Hari"


def test_display_username_fallback():
    user = build_user_info(123, username="hari")
    assert get_display_name(user) == "hari"


def test_display_id_fallback():
    assert get_display_name(build_user_info(123)) == "123"


def test_display_invalid_user():
    with pytest.raises(TypeError):
        get_display_name("Hari")


def test_mention_target():
    assert get_user_mention_target(build_user_info(123)) == "tg://user?id=123"


def test_mention_target_invalid_user():
    with pytest.raises(TypeError):
        get_user_mention_target(123)
