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

    assert database.is_initialized is False


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
