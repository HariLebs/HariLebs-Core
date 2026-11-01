import pytest
from sqlalchemy import text

from harilebs_core.database import DatabaseService


@pytest.fixture
def database():
    return DatabaseService(
        database_url="sqlite+aiosqlite:///:memory:"
    )


def test_database_initialization_state(database):
    assert database.name == "database"
    assert database.is_initialized is False


def test_database_rejects_empty_url():
    with pytest.raises(ValueError):
        DatabaseService(database_url="")


def test_engine_requires_initialization(database):
    with pytest.raises(RuntimeError):
        _ = database.engine


@pytest.mark.asyncio
async def test_database_initialize(database):
    await database.initialize()

    assert database.is_initialized is True
    assert database.engine is not None

    await database.shutdown()


@pytest.mark.asyncio
async def test_database_session(database):
    await database.initialize()

    async with database.session() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar_one() == 1

    await database.shutdown()


@pytest.mark.asyncio
async def test_database_session_requires_initialization(database):
    with pytest.raises(RuntimeError):
        async with database.session():
            pass


@pytest.mark.asyncio
async def test_database_shutdown(database):
    await database.initialize()
    await database.shutdown()

    assert database.is_initialized is False

    with pytest.raises(RuntimeError):
        _ = database.engine


@pytest.mark.asyncio
async def test_database_connection_failure_disposes_engine(
    database, monkeypatch
):
    class FakeConnection:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        async def execute(self, query):
            raise RuntimeError("Connection failed")

    class FakeEngine:
        disposed = False

        def connect(self):
            return FakeConnection()

        async def dispose(self):
            self.disposed = True

    engine = FakeEngine()

    monkeypatch.setattr(
        "harilebs_core.database.create_async_engine",
        lambda *args, **kwargs: engine,
    )

    with pytest.raises(RuntimeError, match="Connection failed"):
        await database.initialize()

    assert engine.disposed is True
