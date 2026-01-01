import os

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool

from app.db.base import Base
from app.api.v1.deps import get_db
from app.main import app

DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://app_test:app_test@localhost:5432/app_test"
)

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def engine():
    """
    Engine создаётся один раз на всю тестовую сессию.
    NullPool обязателен, иначе будут залипания соединений.
    """
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )

    async with engine.begin() as conn:
        # ВАЖНО: если используешь Alembic — лучше прогонять миграции
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture
@pytest.fixture
async def db_session(engine):
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with engine.connect() as conn:
        trans = await conn.begin()  # внешняя транзакция

        async with async_session(bind=conn) as session:
            await session.begin_nested()  # SAVEPOINT
            yield session

        await trans.rollback()  # откат ВСЕГО теста



@pytest.fixture
async def override_get_db(db_session: AsyncSession):
    async def _override():
        yield db_session

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()

