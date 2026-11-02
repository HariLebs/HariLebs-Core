"""Telegram middleware for HariLebs Core."""

import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware

from .metrics import MetricsService


class TelegramMiddleware(BaseMiddleware):
    """Log Telegram updates and track request metrics."""

    def __init__(
        self,
        metrics: MetricsService | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.metrics = metrics
        self.logger = logger or logging.getLogger(
            "harilebs_core.telegram_middleware"
        )

    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        """Process and monitor a Telegram update."""
        event_name = type(event).__name__

        if self.metrics is not None:
            self.metrics.increment("telegram_updates")

        self.logger.info("Processing Telegram update: %s", event_name)

        try:
            result = await handler(event, data)
        except Exception:
            if self.metrics is not None:
                self.metrics.increment("telegram_errors")
            self.logger.exception(
                "Telegram update failed: %s", event_name
            )
            raise

        self.logger.info("Telegram update processed: %s", event_name)
        return result
