import logging

import pytest

from harilebs_core.metrics import MetricsService
from harilebs_core.telegram_error_handler import TelegramErrorHandler


@pytest.mark.asyncio
async def test_handler_success():
    middleware = TelegramErrorHandler()

    async def handler(event, data):
        return "success"

    assert await middleware(handler, object(), {}) == "success"


@pytest.mark.asyncio
async def test_handler_error():
    middleware = TelegramErrorHandler()

    async def handler(event, data):
        raise ValueError("failure")

    with pytest.raises(ValueError, match="failure"):
        await middleware(handler, object(), {})


@pytest.mark.asyncio
async def test_handler_error_metrics():
    metrics = MetricsService()
    middleware = TelegramErrorHandler(metrics=metrics)

    async def handler(event, data):
        raise RuntimeError("failure")

    with pytest.raises(RuntimeError):
        await middleware(handler, object(), {})

    assert metrics.get("telegram_errors") == 1


@pytest.mark.asyncio
async def test_handler_success_with_metrics():
    metrics = MetricsService()
    middleware = TelegramErrorHandler(metrics=metrics)

    async def handler(event, data):
        return True

    assert await middleware(handler, object(), {}) is True
    assert metrics.get("telegram_errors") == 0


def test_default_logger():
    middleware = TelegramErrorHandler()
    assert isinstance(middleware.logger, logging.Logger)
