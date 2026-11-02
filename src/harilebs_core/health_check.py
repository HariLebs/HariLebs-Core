"""Health checks for HariLebs Core services."""

from dataclasses import dataclass

from .base import BaseService


@dataclass(frozen=True)
class HealthCheckResult:
    """Result of a service health check."""

    name: str
    healthy: bool


class HealthCheckService(BaseService):
    """Monitor the initialization status of registered services."""

    def __init__(self, name: str = "health_check") -> None:
        super().__init__(name)
        self._services: dict[str, BaseService] = {}

    def register(self, service: BaseService) -> None:
        """Register a service for health monitoring."""
        if not isinstance(service, BaseService):
            raise TypeError("service must be a BaseService instance.")

        if service is self:
            raise ValueError("A health check service cannot register itself.")

        self._services[service.name] = service

    def unregister(self, name: str) -> None:
        """Remove a registered service."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Service name must be a non-empty string.")

        self._services.pop(name.strip(), None)

    async def check(self, name: str) -> HealthCheckResult:
        """Check one registered service."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Service name must be a non-empty string.")

        service_name = name.strip()
        service = self._services.get(service_name)

        if service is None:
            raise ValueError(f"Service '{service_name}' is not registered.")

        return HealthCheckResult(
            name=service_name,
            healthy=service.is_initialized,
        )

    async def check_all(self) -> list[HealthCheckResult]:
        """Check all registered services."""
        return [
            HealthCheckResult(name=name, healthy=service.is_initialized)
            for name, service in self._services.items()
        ]

    async def is_healthy(self) -> bool:
        """Return whether all registered services are healthy."""
        return all(
            service.is_initialized
            for service in self._services.values()
        )
