"""Scheduler service for HariLebs Core."""

from datetime import datetime
from typing import Any, Callable

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .base import BaseService
from .exceptions import ServiceError


class SchedulerService(BaseService):
    """Manage scheduled and recurring tasks."""

    def __init__(self, timezone: str = "UTC") -> None:
        super().__init__("SchedulerService")
        self._scheduler = AsyncIOScheduler(timezone=timezone)

    @property
    def is_running(self) -> bool:
        """Check whether the scheduler is running."""
        return self._scheduler.running

    async def _on_initialize(self) -> None:
        """Start the scheduler."""
        try:
            if not self._scheduler.running:
                self._scheduler.start()
        except Exception as exc:
            raise ServiceError("Failed to start scheduler.") from exc

    async def _on_shutdown(self) -> None:
        """Stop the scheduler."""
        try:
            if self._scheduler.running:
                self._scheduler.shutdown(wait=False)
        except Exception as exc:
            raise ServiceError("Failed to stop scheduler.") from exc

    def add_date_job(
        self,
        func: Callable[..., Any],
        run_date: datetime,
        job_id: str,
        **kwargs: Any,
    ) -> Job:
        """Add a one-time scheduled job."""
        return self._add_job(
            func,
            "date",
            job_id=job_id,
            run_date=run_date,
            **kwargs,
        )

    def add_interval_job(
        self,
        func: Callable[..., Any],
        seconds: int,
        job_id: str,
        **kwargs: Any,
    ) -> Job:
        """Add a recurring interval job."""
        if seconds <= 0:
            raise ValueError("Interval seconds must be greater than zero.")

        return self._add_job(
            func,
            "interval",
            job_id=job_id,
            seconds=seconds,
            **kwargs,
        )

    def add_cron_job(
        self,
        func: Callable[..., Any],
        job_id: str,
        **kwargs: Any,
    ) -> Job:
        """Add a cron-based recurring job."""
        return self._add_job(
            func,
            "cron",
            job_id=job_id,
            **kwargs,
        )

    def _add_job(
        self,
        func: Callable[..., Any],
        trigger: str,
        **kwargs: Any,
    ) -> Job:
        """Add a job to the scheduler."""
        try:
            return self._scheduler.add_job(
                func,
                trigger,
                **kwargs,
            )
        except Exception as exc:
            raise ServiceError("Failed to add scheduled job.") from exc

    def remove_job(self, job_id: str) -> None:
        """Remove a scheduled job."""
        try:
            self._scheduler.remove_job(job_id)
        except Exception as exc:
            raise ServiceError(
                f"Failed to remove job: {job_id}"
            ) from exc

    def get_jobs(self) -> list[Job]:
        """Return all scheduled jobs."""
        return self._scheduler.get_jobs()

    def get_job(self, job_id: str) -> Job | None:
        """Return a job by its ID."""
        return self._scheduler.get_job(job_id)
