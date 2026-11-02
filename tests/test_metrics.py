import pytest

from harilebs_core.metrics import MetricsService


def test_increment():
    metrics = MetricsService()
    assert metrics.increment("requests") == 1
    assert metrics.increment("requests", 3) == 4


def test_get():
    metrics = MetricsService()
    metrics.increment("requests", 5)
    assert metrics.get("requests") == 5


def test_get_missing():
    metrics = MetricsService()
    assert metrics.get("missing") == 0


def test_get_all():
    metrics = MetricsService()
    metrics.increment("requests")
    metrics.increment("errors", 2)
    assert metrics.get_all() == {"requests": 1, "errors": 2}


def test_reset_one():
    metrics = MetricsService()
    metrics.increment("requests")
    metrics.increment("errors")
    metrics.reset("requests")
    assert metrics.get_all() == {"errors": 1}


def test_reset_all():
    metrics = MetricsService()
    metrics.increment("requests")
    metrics.reset()
    assert metrics.get_all() == {}


def test_reset_missing():
    metrics = MetricsService()
    metrics.reset("missing")
    assert metrics.get_all() == {}


@pytest.mark.parametrize("key", ["", " "])
def test_invalid_key(key):
    metrics = MetricsService()
    with pytest.raises(ValueError):
        metrics.increment(key)
    with pytest.raises(ValueError):
        metrics.get(key)
    with pytest.raises(ValueError):
        metrics.reset(key)


@pytest.mark.parametrize("value", [0, -1, True, 1.5, "2"])
def test_invalid_increment_value(value):
    metrics = MetricsService()
    with pytest.raises(ValueError):
        metrics.increment("requests", value)


def test_invalid_name():
    with pytest.raises(ValueError):
        MetricsService(" ")


def test_increment_returns_updated_value():
    metrics = MetricsService()
    assert metrics.increment("requests", 2) == 2
    assert metrics.increment("requests") == 3
