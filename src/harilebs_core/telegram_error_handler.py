"""Centralized Telegram error handling."""

import logging
from typing import Any

from aiogram import BaseMiddleware


class TelegramErrorHandler(BaseMiddleware):
    """Log Telegram handler errors and optionally track them."""

    def __init__(
        self,
        logger: logging.Logger | None = None,
        metrics: Any = None,
    ) -> None:
        self.logger = logger or logging.getLogger(
            "harilebs_core.telegram_errors"
        )
        self.metrics = metrics

    async def __call__(self, handler, event, data):
        """Execute handler and process unexpected errors."""
        try:
            return await handler(event, data)
        except Exception:
            self.logger.exception("Unhandled Telegram update error")
            if self.metrics is not None:
                self.metrics.increment("telegram_errors")
            raise
