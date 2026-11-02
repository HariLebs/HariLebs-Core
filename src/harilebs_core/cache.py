"""Redis cache management for Harilebs Core."""

import json
from typing import Any

from redis.asyncio import Redis

from .base import BaseService
from .exceptions import IntegrationError, ServiceError


class CacheService(BaseService):
    """Manage asynchronous Redis cache operations."""

    def __init__(
        self,
        redis_url: str,
        name: str = "cache",
    ) -> None:
        if not isinstance(redis_url, str) or not redis_url.strip():
            raise ValueError("Redis URL must be a non-empty string.")

        super().__init__(name)
        self.redis_url = redis_url.strip()
        self._redis: Redis | None = None

    @property
    def client(self) -> Redis:
        """Return the active Redis client."""
        if self._redis is None:
            raise RuntimeError("Cache is not initialized.")
        return self._redis

    async def _on_initialize(self) -> None:
        """Create and verify the Redis connection."""
        client = Redis.from_url(
            self.redis_url,
            decode_responses=True,
        )

        try:
            await client.ping()
        except Exception as exc:
            await client.aclose()
            raise IntegrationError(
                "Failed to connect to Redis."
            ) from exc

        self._redis = client

    async def _on_shutdown(self) -> None:
        """Close the Redis connection."""
        if self._redis is not None:
            await self._redis.aclose()
            self._redis = None

    async def set(
        self,
        key: str,
        value: str,
        ex: int | None = None,
    ) -> bool:
        """Store a string value in Redis."""
        try:
            result = await self.client.set(key, value, ex=ex)
            return bool(result)
        except Exception as exc:
            raise ServiceError("Failed to set cache value.") from exc

    async def get(self, key: str) -> str | None:
        """Retrieve a string value from Redis."""
        try:
            return await self.client.get(key)
        except Exception as exc:
            raise ServiceError("Failed to get cache value.") from exc

    async def delete(self, key: str) -> bool:
        """Delete a cache key."""
        try:
            return bool(await self.client.delete(key))
        except Exception as exc:
            raise ServiceError("Failed to delete cache value.") from exc

    async def exists(self, key: str) -> bool:
        """Check whether a cache key exists."""
        try:
            return bool(await self.client.exists(key))
        except Exception as exc:
            raise ServiceError("Failed to check cache key.") from exc

    async def set_json(
        self,
        key: str,
        value: Any,
        ex: int | None = None,
    ) -> bool:
        """Store a JSON-serializable value in Redis."""
        try:
            serialized = json.dumps(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("Value must be JSON serializable.") from exc

        return await self.set(key, serialized, ex=ex)

    async def get_json(self, key: str) -> Any | None:
        """Retrieve and deserialize a JSON value."""
        value = await self.get(key)

        if value is None:
            return None

        try:
            return json.loads(value)
        except (TypeError, ValueError) as exc:
            raise ServiceError("Failed to decode cached JSON.") from exc
