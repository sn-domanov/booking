from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.api.deps.database import get_uow
from app.core.config import get_settings
from app.db.base import Base
from app.db.uow import UnitOfWork
from app.main import create_app

# ─────────────────────────────────────────
# App
# ─────────────────────────────────────────


settings = get_settings()
app = create_app()


# ─────────────────────────────────────────
# Database
# ─────────────────────────────────────────


@pytest.fixture(scope="session")
async def engine() -> AsyncGenerator[AsyncEngine]:
    if settings.app_env != "testing":
        raise RuntimeError("Tests must be run in test environment")

    engine = create_async_engine(
        settings.db.url,
        # Disable connection pooling: released DB connections are closed
        # instead of being retained for reuse by the engine.
        poolclass=NullPool,
        echo=settings.db_echo,
    )

    yield engine

    await engine.dispose()


@pytest.fixture(scope="session")
async def setup_db(engine: AsyncEngine) -> AsyncGenerator[None]:
    """
    Create all database tables once per test session
    and drop them when the session finishes.
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session(engine: AsyncEngine, setup_db: None) -> AsyncGenerator[AsyncSession]:
    # Connection - test isolation boundary
    conn = await engine.connect()

    # Explicit transaction handle
    outer_tx = await conn.begin()

    # Session is bound to the connection - not to the engine
    session_factory = async_sessionmaker(
        bind=conn,
        expire_on_commit=False,
        # Fake commit - create a savepoint instead of commit
        join_transaction_mode="create_savepoint",
    )

    # Yield session
    async with session_factory() as session:
        try:
            yield session
        finally:
            await outer_tx.rollback()  # roll back via transaction handle
            await conn.close()  # then close connection


@pytest.fixture
def uow(session: AsyncSession) -> UnitOfWork:
    return UnitOfWork(session)


# ─────────────────────────────────────────
# FastAPI client
# ─────────────────────────────────────────


@pytest.fixture
async def client(
    uow: UnitOfWork,
) -> AsyncGenerator[AsyncClient]:
    """
    HTTP client configured with:
    - test UnitOfWork dependency
    """

    async def get_test_uow() -> AsyncGenerator[UnitOfWork]:
        yield uow

    app.dependency_overrides[get_uow] = get_test_uow

    try:
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as ac:
            yield ac
    finally:
        app.dependency_overrides.clear()
