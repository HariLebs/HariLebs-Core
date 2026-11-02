from unittest.mock import AsyncMock

import pytest

from harilebs_core.cache import CacheService
from harilebs_core.exceptions import ServiceError
from harilebs_core.rate_limiter import (
    RateLimitResult,
    RateLimiterService,
)


@pytest.fixture
def cache():
    return CacheService("redis://localhost:6379/0")


@pytest.fixture
def limiter(cache):
    return RateLimiterService(cache)


@pytest.mark.asyncio
async def test_initialize_requires_cache(limiter):
    with pytest.raises(ServiceError):
        await limiter.initialize()


@pytest.mark.asyncio
async def test_initialize_and_shutdown(limiter, cache):
    cache._initialized = True

    await limiter.initialize()
    assert limiter.is_initialized

    await limiter.shutdown()
    assert not limiter.is_initialized


@pytest.mark.asyncio
async def test_check_allowed(limiter, cache):
    cache._initialized = True
    cache._redis = AsyncMock()
    cache._redis.eval.return_value = [1, 60]

    await limiter.initialize()
    result = await limiter.check("user:1", 5, 60)

    assert result == RateLimitResult(
        allowed=True,
        limit=5,
        remaining=4,
        retry_after=60,
    )


@pytest.mark.asyncio
async def test_check_limit_reached(limiter, cache):
    cache._initialized = True
    cache._redis = AsyncMock()
    cache._redis.eval.return_value = [5, 30]

    await limiter.initialize()
    result = await limiter.check("user:1", 5, 60)

    assert result.allowed is True
    assert result.remaining == 0


@pytest.mark.asyncio
async def test_check_limit_exceeded(limiter, cache):
    cache._initialized = True
    cache._redis = AsyncMock()
    cache._redis.eval.return_value = [6, 25]

    await limiter.initialize()
    result = await limiter.check("user:1", 5, 60)

    assert result.allowed is False
    assert result.remaining == 0
    assert result.retry_after == 25


@pytest.mark.asyncio
async def test_check_zero_ttl(limiter, cache):
    cache._initialized = True
    cache._redis = AsyncMock()
    cache._redis.eval.return_value = [1, -1]

    await limiter.initialize()
    result = await limiter.check("user:1", 5, 60)

    assert result.retry_after == 0


@pytest.mark.asyncio
async def test_check_redis_error(limiter, cache):
    cache._initialized = True
    cache._redis = AsyncMock()
    cache._redis.eval.side_effect = RuntimeError("Redis error")

    await limiter.initialize()

    with pytest.raises(ServiceError):
        await limiter.check("user:1", 5, 60)


@pytest.mark.asyncio
async def test_invalid_key(limiter):
    with pytest.raises(ValueError):
        await limiter.check(" ", 5, 60)


@pytest.mark.asyncio
@pytest.mark.parametrize("limit", [0, -1, True, 1.5])
async def test_invalid_limit(limiter, limit):
    with pytest.raises(ValueError):
        await limiter.check("user:1", limit, 60)


@pytest.mark.asyncio
@pytest.mark.parametrize("window", [0, -1, True, 1.5])
async def test_invalid_window(limiter, window):
    with pytest.raises(ValueError):
        await limiter.check("user:1", 5, window)


def test_invalid_cache():
    with pytest.raises(TypeError):
        RateLimiterService(None)


def test_invalid_service_name():
    cache = CacheService("redis://localhost:6379/0")

    with pytest.raises(ValueError):
        RateLimiterService(cache, name="")
