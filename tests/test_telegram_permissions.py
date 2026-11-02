import pytest
from aiogram.types import ChatPermissions

from harilebs_core.telegram_permissions import (
    PERMISSION_FIELDS,
    build_chat_permissions,
    build_full_permissions,
    build_restricted_permissions,
)


def test_build_chat_permissions():
    result = build_chat_permissions(
        can_send_messages=True,
        can_send_photos=True,
    )
    assert isinstance(result, ChatPermissions)
    assert result.can_send_messages is True
    assert result.can_send_photos is True


def test_build_empty_permissions():
    result = build_chat_permissions()
    assert isinstance(result, ChatPermissions)


@pytest.mark.parametrize("value", [1, 0, "true", None])
def test_invalid_permission_type(value):
    with pytest.raises(TypeError):
        build_chat_permissions(can_send_messages=value)


def test_unknown_permission():
    with pytest.raises(ValueError, match="Unknown permission"):
        build_chat_permissions(can_delete_messages=True)


def test_multiple_unknown_permissions():
    with pytest.raises(ValueError):
        build_chat_permissions(
            unknown_one=True,
            unknown_two=False,
        )


def test_restricted_permissions():
    result = build_restricted_permissions()
    assert all(getattr(result, name) is False for name in PERMISSION_FIELDS)


def test_full_permissions():
    result = build_full_permissions()
    assert all(getattr(result, name) is True for name in PERMISSION_FIELDS)


def test_permission_fields_are_unique():
    assert len(PERMISSION_FIELDS) == len(set(PERMISSION_FIELDS))


def test_single_permission():
    result = build_chat_permissions(can_invite_users=False)
    assert result.can_invite_users is False


def test_permission_fields_count():
    assert len(PERMISSION_FIELDS) == 14
