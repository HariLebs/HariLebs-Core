"""Redis-backed rate limiting for Harilebs Core."""

from dataclasses import dataclass

from .base import BaseService
from .cache import CacheService
from .exceptions import ServiceError


@dataclass(frozen=True)
class RateLimitResult:
    """Result of a rate limit check."""

    allowed: bool
    limit: int
    remaining: int
    retry_after: int


class RateLimiterService(BaseService):
    """Apply atomic fixed-window rate limits using Redis."""

    _SCRIPT = """
    local count = redis.call('INCR', KEYS[1])
    if count == 1 then
        redis.call('EXPIRE', KEYS[1], ARGV[1])
    end
    local ttl = redis.call('TTL', KEYS[1])
    return {count, ttl}
    """

    def __init__(
        self,
        cache: CacheService,
        name: str = "rate_limiter",
    ) -> None:
        if not isinstance(cache, CacheService):
            raise TypeError("cache must be a CacheService instance.")

        super().__init__(name)
        self.cache = cache

    async def _on_initialize(self) -> None:
        """Verify that the shared cache is initialized."""
        if not self.cache.is_initialized:
            raise ServiceError("CacheService must be initialized first.")

    async def _on_shutdown(self) -> None:
        """No separate resources need to be released."""

    async def check(
        self,
        key: str,
        limit: int,
        window_seconds: int,
    ) -> RateLimitResult:
        """Check and consume one request from a fixed time window."""
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Rate limit key must be a non-empty string.")

        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError("Limit must be a positive integer.")

        if (
            isinstance(window_seconds, bool)
            or not isinstance(window_seconds, int)
            or window_seconds < 1
        ):
            raise ValueError("Window must be a positive integer.")

        try:
            count, ttl = await self.cache.client.eval(
                self._SCRIPT,
                1,
                f"harilebs:rate_limit:{key}",
                window_seconds,
            )
        except Exception as exc:
            raise ServiceError("Rate limit check failed.") from exc

        count = int(count)
        ttl = max(int(ttl), 0)

        return RateLimitResult(
            allowed=count <= limit,
            limit=limit,
            remaining=max(limit - count, 0),
            retry_after=ttl,
        )
