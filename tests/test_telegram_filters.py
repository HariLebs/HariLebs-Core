from types import SimpleNamespace

import pytest

from harilebs_core.telegram_filters import (
    AdminFilter,
    ChatTypeFilter,
    UserIdFilter,
)


@pytest.mark.asyncio
async def test_user_id_allowed():
    assert await UserIdFilter([10])(SimpleNamespace(
        from_user=SimpleNamespace(id=10)
    )) is True


@pytest.mark.asyncio
async def test_user_id_denied():
    assert await UserIdFilter([10])(SimpleNamespace(
        from_user=SimpleNamespace(id=20)
    )) is False


@pytest.mark.asyncio
async def test_user_id_missing_user():
    assert await UserIdFilter([10])(SimpleNamespace()) is False


@pytest.mark.parametrize("ids", [[], [0], [-1], [True], ["10"]])
def test_invalid_user_ids(ids):
    with pytest.raises(ValueError):
        UserIdFilter(ids)


@pytest.mark.asyncio
async def test_admin_filter():
    assert await AdminFilter([1])(SimpleNamespace(
        from_user=SimpleNamespace(id=1)
    )) is True


@pytest.mark.asyncio
async def test_admin_filter_denied():
    assert await AdminFilter([1])(SimpleNamespace(
        from_user=SimpleNamespace(id=2)
    )) is False


@pytest.mark.asyncio
async def test_chat_type_allowed():
    assert await ChatTypeFilter(["private"])(SimpleNamespace(
        chat=SimpleNamespace(type="private")
    )) is True


@pytest.mark.asyncio
async def test_chat_type_denied():
    assert await ChatTypeFilter(["private"])(SimpleNamespace(
        chat=SimpleNamespace(type="group")
    )) is False


@pytest.mark.asyncio
async def test_chat_type_missing():
    assert await ChatTypeFilter(["private"])(SimpleNamespace()) is False


@pytest.mark.parametrize("types", [[], ["invalid"], [1], [None]])
def test_invalid_chat_types(types):
    with pytest.raises(ValueError):
        ChatTypeFilter(types)


@pytest.mark.asyncio
async def test_all_supported_chat_types():
    for chat_type in ("private", "group", "supergroup", "channel"):
        assert await ChatTypeFilter([chat_type])(
            SimpleNamespace(chat=SimpleNamespace(type=chat_type))
        ) is True
