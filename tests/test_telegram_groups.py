import pytest

from harilebs_core.telegram_groups import (
    TelegramGroupInfo,
    build_group_info,
    get_group_display_name,
    is_group_admin,
)


def test_build_group_info():
    assert build_group_info(-100123, "Test Group") == TelegramGroupInfo(
        -100123, "Test Group", "supergroup"
    )


def test_build_basic_group():
    assert build_group_info(-123, "Group", "group").group_type == "group"


def test_title_is_trimmed():
    assert build_group_info(-123, "  Group  ").title == "Group"


@pytest.mark.parametrize("chat_id", [True, "123", 1.5, None])
def test_chat_id_type(chat_id):
    with pytest.raises(TypeError):
        build_group_info(chat_id, "Group")


@pytest.mark.parametrize("chat_id", [0, 123, -0])
def test_chat_id_must_be_negative(chat_id):
    with pytest.raises(ValueError):
        build_group_info(chat_id, "Group")


@pytest.mark.parametrize("title", [None, 123])
def test_title_type(title):
    with pytest.raises(TypeError):
        build_group_info(-123, title)


@pytest.mark.parametrize("title", ["", "   "])
def test_empty_title(title):
    with pytest.raises(ValueError):
        build_group_info(-123, title)


def test_group_type_type():
    with pytest.raises(TypeError):
        build_group_info(-123, "Group", 123)


def test_invalid_group_type():
    with pytest.raises(ValueError):
        build_group_info(-123, "Group", "channel")


def test_admin_found():
    assert is_group_admin(10, [10, 20]) is True


def test_admin_not_found():
    assert is_group_admin(30, [10, 20]) is False


def test_admin_with_set():
    assert is_group_admin(10, {10, 20}) is True


def test_admin_with_tuple():
    assert is_group_admin(10, (10, 20)) is True


def test_admin_user_id_type():
    with pytest.raises(TypeError):
        is_group_admin(True, [1])


def test_admin_collection_type():
    with pytest.raises(TypeError):
        is_group_admin(10, "10")


def test_admin_ids_type():
    with pytest.raises(TypeError):
        is_group_admin(10, [10, "20"])


def test_display_name():
    group = build_group_info(-123, "My Group")
    assert get_group_display_name(group) == "My Group"


def test_display_invalid_group():
    with pytest.raises(TypeError):
        get_group_display_name("Group")
