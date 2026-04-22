import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(
        settings.database_url_async,
        pool_pre_ping=True,
    )
    yield engine
    await engine.dispose()


@pytest.fixture
async def async_session(async_engine):
    SessionLocal = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
    )

    async with SessionLocal() as session:
        yield session
