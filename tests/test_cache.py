from unittest.mock import AsyncMock, patch

import pytest

from harilebs_core.cache import CacheService
from harilebs_core.exceptions import IntegrationError, ServiceError


@pytest.fixture
def redis_client():
    return AsyncMock()


@pytest.fixture
def cache(redis_client):
    with patch(
        "harilebs_core.cache.Redis.from_url",
        return_value=redis_client,
    ):
        yield CacheService("redis://localhost:6379/0")


@pytest.mark.asyncio
async def test_initialize(cache, redis_client):
    await cache.initialize()

    assert cache.is_initialized
    assert cache.client is redis_client
    redis_client.ping.assert_awaited_once()


@pytest.mark.asyncio
async def test_initialize_connection_error(cache, redis_client):
    redis_client.ping.side_effect = RuntimeError("Connection failed")

    with pytest.raises(IntegrationError):
        await cache.initialize()

    redis_client.aclose.assert_awaited_once()


@pytest.mark.asyncio
async def test_client_before_initialize():
    cache = CacheService("redis://localhost:6379/0")

    with pytest.raises(RuntimeError):
        _ = cache.client


@pytest.mark.asyncio
async def test_shutdown(cache, redis_client):
    await cache.initialize()
    await cache.shutdown()

    assert not cache.is_initialized
    redis_client.aclose.assert_awaited_once()


@pytest.mark.asyncio
async def test_set(cache, redis_client):
    await cache.initialize()
    redis_client.set.return_value = True

    result = await cache.set("key", "value", ex=60)

    assert result is True
    redis_client.set.assert_awaited_once_with("key", "value", ex=60)


@pytest.mark.asyncio
async def test_set_error(cache, redis_client):
    await cache.initialize()
    redis_client.set.side_effect = RuntimeError("Redis error")

    with pytest.raises(ServiceError):
        await cache.set("key", "value")


@pytest.mark.asyncio
async def test_get(cache, redis_client):
    await cache.initialize()
    redis_client.get.return_value = "value"

    assert await cache.get("key") == "value"


@pytest.mark.asyncio
async def test_get_error(cache, redis_client):
    await cache.initialize()
    redis_client.get.side_effect = RuntimeError("Redis error")

    with pytest.raises(ServiceError):
        await cache.get("key")


@pytest.mark.asyncio
async def test_delete(cache, redis_client):
    await cache.initialize()
    redis_client.delete.return_value = 1

    assert await cache.delete("key") is True


@pytest.mark.asyncio
async def test_delete_error(cache, redis_client):
    await cache.initialize()
    redis_client.delete.side_effect = RuntimeError("Redis error")

    with pytest.raises(ServiceError):
        await cache.delete("key")


@pytest.mark.asyncio
async def test_exists(cache, redis_client):
    await cache.initialize()
    redis_client.exists.return_value = 1

    assert await cache.exists("key") is True


@pytest.mark.asyncio
async def test_exists_error(cache, redis_client):
    await cache.initialize()
    redis_client.exists.side_effect = RuntimeError("Redis error")

    with pytest.raises(ServiceError):
        await cache.exists("key")


@pytest.mark.asyncio
async def test_set_json(cache, redis_client):
    await cache.initialize()
    redis_client.set.return_value = True

    result = await cache.set_json("user", {"name": "Hari"})

    assert result is True
    redis_client.set.assert_awaited_once_with(
        "user",
        '{"name": "Hari"}',
        ex=None,
    )


@pytest.mark.asyncio
async def test_set_json_invalid_value(cache):
    await cache.initialize()

    with pytest.raises(ValueError):
        await cache.set_json("key", object())


@pytest.mark.asyncio
async def test_get_json(cache, redis_client):
    await cache.initialize()
    redis_client.get.return_value = '{"name": "Hari"}'

    assert await cache.get_json("user") == {"name": "Hari"}


@pytest.mark.asyncio
async def test_get_json_missing(cache, redis_client):
    await cache.initialize()
    redis_client.get.return_value = None

    assert await cache.get_json("missing") is None


@pytest.mark.asyncio
async def test_get_json_invalid_data(cache, redis_client):
    await cache.initialize()
    redis_client.get.return_value = "invalid-json"

    with pytest.raises(ServiceError):
        await cache.get_json("key")


def test_invalid_redis_url():
    with pytest.raises(ValueError):
        CacheService("  ")


def test_invalid_service_name():
    with pytest.raises(ValueError):
        CacheService("redis://localhost:6379/0", name="")
