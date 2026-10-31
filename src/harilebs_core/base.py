"""Base classes for HariLebs Core."""

from abc import ABC


class BaseService(ABC):
    """Base class for shared core services."""

    def__init__(self, name: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Service name must be a non-empty string.")

        self.name = name.strip()
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check whether the service is initialized."""

        return self._initialized

    async def initialize(self) -> None:
        """Initialize the service."""

        if self._initialized:
            return

        await self._on_initialize()
        self._initialized = True

    async def shutdown(self) -> None:
        """Shut down the service."""

        if not self._initialized:
            return

        await self._on_shutdown()
        self._initialized = False

    async def _on_initialize(self) -> None:
        """Override this method to add initialization logic."""

    async def _on_shutdown(self) -> None:
        """Override this method to add shutdown logic."""
