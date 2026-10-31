"""Logging utilities for HariLebs Core."""

import logging


DEFAULT_LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


def configure_logging(
    level: int = logging.INFO,
    log_format: str = DEFAULT_LOG_FORMAT,
) -> None:
    """Configure logging for HariLebs Core."""

    logger = logging.getLogger("harilebs_core")

    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Get a named logger for a bot or core component."""

    if not isinstance(name, str) or not name.strip():
        raise ValueError("Logger name must be a non-empty string.")

    return logging.getLogger(f"harilebs_core.{name}")
