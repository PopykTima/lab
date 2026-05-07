"""
Test configuration with database setup/teardown.
Uses separate test database for isolation.
"""
import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from app.core.database import Base
from app.core.config import settings


# Test database URL - uses separate database (from docker-compose)
# Uses db_test service on port 5433
TEST_DATABASE_URL = "postgresql+asyncpg://admin:rootpassword@db_test:5432/app_test"

# Alternative: derive from main database URL
# TEST_DATABASE_URL = settings.DATABASE_URL.replace(
#     "/app", "/app_test"
# ) if "/app" in settings.DATABASE_URL else settings.DATABASE_URL + "_test"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """
    Create test database engine.
    Creates tables once per session.
    """
    # Try to use test database URL, fallback to local
    db_url = TEST_DATABASE_URL
    
    engine = create_async_engine(
        db_url,
        echo=False,
        poolclass=NullPool,
    )
    
    # Create all tables once per session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Drop all tables after session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_db_session(test_engine):
    """
    Create test database session with transaction rollback.
    """
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        # Rollback any changes after test
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def test_client(test_db_session):
    """
    Create test client with overridden database dependency.
    """
    from httpx import AsyncClient, ASGITransport
    from app.main import app
    from app.core.database import get_db
    
    async def override_get_db():
        yield test_db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()
