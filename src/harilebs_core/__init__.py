"""
HariLebs Core
=============

Reusable core framework for HariLebs Telegram bots.
"""

version = "0.1.0"

from .exceptions import (
    ConfigurationError,
    HariLebsError,
    InitializationError,
    IntegrationError,
    ServiceError,
)

all = [
    "version",
    "HariLebsError",
    "ConfigurationError",
    "InitializationError",
    "ServiceError",
    "IntegrationError",
]
