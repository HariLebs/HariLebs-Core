import logging

import pytest

from harilebs_core.logger import (
    configure_logging,
    get_logger,
)


def test_get_logger():
    logger = get_logger("test_bot")

    assert isinstance(logger, logging.Logger)
    assert logger.name == "harilebs_core.test_bot"


def test_get_logger_returns_same_instance():
    first_logger = get_logger("test_bot")
    second_logger = get_logger("test_bot")

    assert first_logger is second_logger


def test_get_logger_rejects_empty_name():
    with pytest.raises(ValueError):
        get_logger("")


def test_get_logger_rejects_invalid_name():
    with pytest.raises(ValueError):
        get_logger("   ")


def test_configure_logging():
    logger = logging.getLogger("harilebs_core")

    original_level = logger.level
    original_propagate = logger.propagate
    original_handlers = logger.handlers[:]

    try:
        configure_logging(level=logging.DEBUG)

        assert logger.level == logging.DEBUG
        assert logger.propagate is False
        assert len(logger.handlers) >= 1

    finally:
        for handler in logger.handlers[:]:
            if handler not in original_handlers:
                logger.removeHandler(handler)
                handler.close()

        logger.setLevel(original_level)
        logger.propagate = original_propagate
