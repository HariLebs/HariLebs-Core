"""Tests for SchedulerService."""

from datetime import datetime, timedelta
from unittest.mock import MagicMock, PropertyMock, patch

import pytest
from apscheduler.schedulers.base import BaseScheduler

from harilebs_core.exceptions import ServiceError
from harilebs_core.scheduler import SchedulerService


def test_scheduler_initialization():
    service = SchedulerService()
    assert service.is_running is False


def test_add_date_job():
    service = SchedulerService()
    job = MagicMock()

    with patch.object(service._scheduler, "add_job", return_value=job) as mock:
        result = service.add_date_job(
            lambda: None, datetime.now() + timedelta(hours=1), "date_job"
        )

    assert result is job
    mock.assert_called_once()


def test_add_interval_job():
    service = SchedulerService()
    job = MagicMock()

    with patch.object(service._scheduler, "add_job", return_value=job) as mock:
        result = service.add_interval_job(lambda: None, 10, "interval_job")

    assert result is job
    mock.assert_called_once()


def test_add_interval_job_invalid_seconds():
    service = SchedulerService()

    with pytest.raises(ValueError):
        service.add_interval_job(lambda: None, 0, "invalid_job")


def test_add_cron_job():
    service = SchedulerService()
    job = MagicMock()

    with patch.object(service._scheduler, "add_job", return_value=job) as mock:
        result = service.add_cron_job(lambda: None, "cron_job", hour=9, minute=30)

    assert result is job
    mock.assert_called_once()


def test_add_job_error():
    service = SchedulerService()

    with patch.object(service._scheduler, "add_job", side_effect=Exception("error")):
        with pytest.raises(ServiceError):
            service.add_interval_job(lambda: None, 10, "error_job")


def test_remove_job():
    service = SchedulerService()

    with patch.object(service._scheduler, "remove_job") as mock:
        service.remove_job("job1")

    mock.assert_called_once_with("job1")


def test_remove_job_error():
    service = SchedulerService()

    with patch.object(service._scheduler, "remove_job", side_effect=Exception("error")):
        with pytest.raises(ServiceError):
            service.remove_job("missing")


def test_get_jobs():
    service = SchedulerService()
    jobs = [MagicMock()]

    with patch.object(service._scheduler, "get_jobs", return_value=jobs):
        assert service.get_jobs() == jobs


def test_get_job():
    service = SchedulerService()
    job = MagicMock()

    with patch.object(service._scheduler, "get_job", return_value=job):
        assert service.get_job("job1") is job


def test_get_missing_job():
    service = SchedulerService()

    with patch.object(service._scheduler, "get_job", return_value=None):
        assert service.get_job("missing") is None


@pytest.mark.asyncio
async def test_scheduler_initialize_and_shutdown():
    service = SchedulerService()

    with patch.object(
        BaseScheduler,
        "running",
        new_callable=PropertyMock,
        side_effect=[False, True],
    ), patch.object(service._scheduler, "start") as start, patch.object(
        service._scheduler, "shutdown"
    ) as shutdown:
        await service.initialize()
        start.assert_called_once()

        await service.shutdown()
        shutdown.assert_called_once_with(wait=False)
@pytest.mark.asyncio
async def test_scheduler_initialize_error():
    service = SchedulerService()

    with patch.object(service._scheduler, "start", side_effect=Exception("error")):
        with pytest.raises(ServiceError):
            await service.initialize()


@pytest.mark.asyncio
async def test_scheduler_shutdown_error():
    service = SchedulerService()

    with patch.object(
        BaseScheduler, "running",
        new_callable=PropertyMock, return_value=False
    ), patch.object(service._scheduler, "start"):
        await service.initialize()

    with patch.object(
        BaseScheduler, "running",
        new_callable=PropertyMock, return_value=True
    ), patch.object(
        service._scheduler, "shutdown",
        side_effect=Exception("error")
    ):
        with pytest.raises(ServiceError):
            await service.shutdown()
