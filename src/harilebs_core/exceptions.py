"""Custom exceptions for HariLebs Core."""


class HariLebsError(Exception):
    """Base exception for all HariLebs Core errors."""


class ConfigurationError(HariLebsError):
    """Raised when configuration is invalid."""


class InitializationError(HariLebsError):
    """Raised when core initialization fails."""


class ServiceError(HariLebsError):
    """Raised when a core service fails."""


class IntegrationError(HariLebsError):
    """Raised when an external integration fails."""
