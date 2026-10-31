"""Database management for HariLebs Core."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .base import BaseService


class DatabaseService(BaseService):
    """Manage asynchronous database connections and sessions."""

    def __init__(
        self,
        database_url: str,
        echo: bool = False,
        name: str = "database",
    ) -> None:
        if not isinstance(database_url, str) or not database_url.strip():
            raise ValueError("Database URL must be a non-empty string.")

        super().__init__(name)

        self.database_url = database_url.strip()
        self.echo = echo

        self._engine: AsyncEngine | None = None
        self._session_factory: (
            async_sessionmaker[AsyncSession] | None
        ) = None

    @property
    def engine(self) -> AsyncEngine:
        """Return the active database engine."""

        if self._engine is None:
            raise RuntimeError("Database is not initialized.")

        return self._engine

    async def _on_initialize(self) -> None:
        """Create and verify the database connection."""

        engine = create_async_engine(
            self.database_url,
            echo=self.echo,
            pool_pre_ping=True,
        )

        try:
            async with engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
        except Exception:
            await engine.dispose()
            raise

        self._engine = engine

        self._session_factory = async_sessionmaker(
            engine,
            expire_on_commit=False,
        )

    async def _on_shutdown(self) -> None:
        """Dispose the database engine."""

        if self._engine is not None:
            await self._engine.dispose()

        self._engine = None
        self._session_factory = None

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Provide an asynchronous database session."""

        session_factory = self._session_factory

        if session_factory is None:
            raise RuntimeError("Database is not initialized.")

        async with session_factory() as session:
            yield session
