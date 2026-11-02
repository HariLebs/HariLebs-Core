"""Reusable Telegram filters for HariLebs Core."""

from collections.abc import Iterable
from typing import Any

from aiogram.filters import BaseFilter


class UserIdFilter(BaseFilter):
    """Allow only users whose IDs are registered."""

    def __init__(self, user_ids: Iterable[int]) -> None:
        ids = list(user_ids)
        if not ids or any(
            isinstance(item, bool) or not isinstance(item, int) or item < 1
            for item in ids
        ):
            raise ValueError("User IDs must be positive integers.")

        self.user_ids = frozenset(ids)

    async def __call__(self, event: Any) -> bool:
        user = getattr(event, "from_user", None)
        user_id = getattr(user, "id", None)
        return user_id in self.user_ids


class AdminFilter(UserIdFilter):
    """Allow only registered administrators."""

    pass


class ChatTypeFilter(BaseFilter):
    """Allow only selected Telegram chat types."""

    VALID_TYPES = frozenset({"private", "group", "supergroup", "channel"})

    def __init__(self, chat_types: Iterable[str]) -> None:
        types = list(chat_types)
        if not types or any(
            not isinstance(item, str) or item not in self.VALID_TYPES
            for item in types
        ):
            raise ValueError("Invalid or empty chat types.")

        self.chat_types = frozenset(types)

    async def __call__(self, event: Any) -> bool:
        chat = getattr(event, "chat", None)
        chat_type = getattr(chat, "type", None)
        return chat_type in self.chat_types
