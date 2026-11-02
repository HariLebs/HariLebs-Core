import logging

import pytest

from harilebs_core.metrics import MetricsService
from harilebs_core.telegram_middleware import TelegramMiddleware


@pytest.mark.asyncio
async def test_middleware_success():
    metrics = MetricsService()
    logger = logging.getLogger("test.middleware")
    middleware = TelegramMiddleware(metrics, logger)

    async def handler(event, data):
        return "success"

    result = await middleware(handler, object(), {})
    assert result == "success"
    assert metrics.get("telegram_updates") == 1
    assert metrics.get("telegram_errors") == 0


@pytest.mark.asyncio
async def test_middleware_error():
    metrics = MetricsService()
    middleware = TelegramMiddleware(metrics)

    async def handler(event, data):
        raise RuntimeError("Handler failed")

    with pytest.raises(RuntimeError, match="Handler failed"):
        await middleware(handler, object(), {})

    assert metrics.get("telegram_updates") == 1
    assert metrics.get("telegram_errors") == 1


@pytest.mark.asyncio
async def test_middleware_without_metrics():
    middleware = TelegramMiddleware()

    async def handler(event, data):
        return "ok"

    assert await middleware(handler, object(), {}) == "ok"


@pytest.mark.asyncio
async def test_middleware_preserves_handler_result():
    middleware = TelegramMiddleware()

    async def handler(event, data):
        return {"result": 123}

    assert await middleware(handler, object(), {}) == {"result": 123}


def test_default_logger():
    middleware = TelegramMiddleware()
    assert isinstance(middleware.logger, logging.Logger)
