"""Metrics collection for HariLebs Core."""

from collections import defaultdict
from typing import DefaultDict

from .base import BaseService


class MetricsService(BaseService):
    """Collect counters and measurements for bot services."""

    def __init__(self, name: str = "metrics") -> None:
        super().__init__(name)
        self._counters: DefaultDict[str, int] = defaultdict(int)

    def increment(self, key: str, value: int = 1) -> int:
        """Increment a metric counter."""
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Metric key must be a non-empty string.")
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            raise ValueError("Value must be a positive integer.")

        self._counters[key.strip()] += value
        return self._counters[key.strip()]

    def get(self, key: str) -> int:
        """Get the value of a metric counter."""
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Metric key must be a non-empty string.")
        return self._counters[key.strip()]

    def get_all(self) -> dict[str, int]:
        """Return all collected metrics."""
        return dict(self._counters)

    def reset(self, key: str | None = None) -> None:
        """Reset one metric or all metrics."""
        if key is None:
            self._counters.clear()
            return

        if not isinstance(key, str) or not key.strip():
            raise ValueError("Metric key must be a non-empty string.")
        self._counters.pop(key.strip(), None)
