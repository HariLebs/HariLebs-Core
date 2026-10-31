"""Base classes for HariLebs Core."""

from abc import ABC


class BaseService(ABC):
    """Base class for shared core services."""

    def init(self, name: str) -> None:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Service name must be a non-empty string.")

        self.name = name.strip()
        self._initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check whether the service is initialized."""

        return self._initialized
