"""Manager for running multiple Telegram bots."""

import asyncio
from typing import Any

from harilebs_core.base import BaseService
from harilebs_core.exceptions import ServiceError


class BotManager(BaseService):
    """Manage multiple Telegram bots with independent polling tasks."""

    def __init__(self) -> None:
        super().__init__(name="bot_manager")
        self._bots: dict[str, tuple[Any, Any]] = {}
        self._tasks: dict[str, asyncio.Task[None]] = {}
        self._errors: dict[str, str] = {}
        self._lock = asyncio.Lock()

    def register_bot(
        self,
        bot_id: str,
        bot: Any,
        dispatcher: Any,
    ) -> None:
        """Register a bot and its dispatcher."""
        if not isinstance(bot_id, str) or not bot_id.strip():
            raise ValueError("Bot ID must be a non-empty string.")

        bot_id = bot_id.strip()

        if bot_id in self._bots:
            raise ServiceError(f"Bot '{bot_id}' is already registered.")

        if bot is None or dispatcher is None:
            raise ValueError("Bot and dispatcher are required.")

        if not callable(getattr(dispatcher, "start_polling", None)):
            raise ValueError("Dispatcher must provide start_polling().")

        self._bots[bot_id] = (bot, dispatcher)

    def unregister_bot(self, bot_id: str) -> None:
        """Remove a registered bot that is not currently running."""
        if bot_id not in self._bots:
            raise ServiceError(f"Bot '{bot_id}' is not registered.")

        task = self._tasks.get(bot_id)
        if task is not None and not task.done():
            raise ServiceError("Stop the bot before unregistering it.")

        self._bots.pop(bot_id)
        self._tasks.pop(bot_id, None)
        self._errors.pop(bot_id, None)

    def get_status(self, bot_id: str) -> str:
        """Return the current status of a registered bot."""
        if bot_id not in self._bots:
            raise ServiceError(f"Bot '{bot_id}' is not registered.")

        task = self._tasks.get(bot_id)

        if task is None:
            return "stopped"

        if task.cancelled():
            return "stopped"

        if task.done():
            return "error" if bot_id in self._errors else "stopped"

        return "running"

    def get_all_statuses(self) -> dict[str, str]:
        """Return the status of every registered bot."""
        return {
            bot_id: self.get_status(bot_id)
            for bot_id in self._bots
        }

    async def start_bot(self, bot_id: str) -> None:
        """Start polling for one registered bot."""
        async with self._lock:
            if not self.is_initialized:
                raise ServiceError("BotManager is not initialized.")

            if bot_id not in self._bots:
                raise ServiceError(f"Bot '{bot_id}' is not registered.")

            current = self._tasks.get(bot_id)

            if current is not None and not current.done():
                raise ServiceError(f"Bot '{bot_id}' is already running.")

            bot, dispatcher = self._bots[bot_id]
            self._errors.pop(bot_id, None)

            coroutine = dispatcher.start_polling(
                bot,
                handle_signals=False,
                close_bot_session=False,
            )

            task = asyncio.create_task(
                coroutine,
                name=f"bot-polling-{bot_id}",
            )
            self._tasks[bot_id] = task

            def record_error(
                completed_task: asyncio.Task[None],
            ) -> None:
                if completed_task.cancelled():
                    return

                error = completed_task.exception()
                if error is not None:
                    self._errors[bot_id] = str(error)

            task.add_done_callback(record_error)

    async def stop_bot(self, bot_id: str) -> None:
        """Stop polling for one registered bot."""
        async with self._lock:
            if bot_id not in self._bots:
                raise ServiceError(f"Bot '{bot_id}' is not registered.")

            task = self._tasks.get(bot_id)

            if task is None or task.done():
                return

            task.cancel()

        await asyncio.gather(task, return_exceptions=True)

    async def start_all(self) -> None:
        """Start all registered bots independently."""
        if not self.is_initialized:
            raise ServiceError("BotManager is not initialized.")

        for bot_id in self._bots:
            if self.get_status(bot_id) != "running":
                await self.start_bot(bot_id)

    async def stop_all(self) -> None:
        """Stop all running bots."""
        bot_ids = list(self._tasks)

        await asyncio.gather(
            *(self.stop_bot(bot_id) for bot_id in bot_ids),
            return_exceptions=True,
        )

    async def _on_initialize(self) -> None:
        """Prepare the manager for use."""
        self._errors.clear()

    async def _on_shutdown(self) -> None:
        """Stop every bot during manager shutdown."""
        await self.stop_all()
