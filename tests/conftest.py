from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import pytest
import asyncio

from httpx import AsyncClient

from app.db.models.employee import Employee
from app.main import app
from app.db.session import get_db
from app.db.base import Base


test_engine = create_async_engine("postgresql+psycopg://postgres_test:postgres_test@db_test:5433/test_task_shift_test")

test_session = async_sessionmaker(bind=test_engine, expire_on_commit=False)

CLEAN_TABLES = [
    "employee",
]


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    async def setup_db():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def teardown_db():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    asyncio.run(setup_db())
    yield
    asyncio.run(teardown_db())


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_session() as session:
        await session.begin_nested()
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000/") as async_client:
        yield async_client


@pytest.fixture()
def create_employee_in_db(db_session: AsyncSession):
    async def wrapper(employee_data: dict) -> Employee:
       employee = Employee(**employee_data)
       db_session.add(employee)
       await db_session.flush()
       await db_session.refresh(employee)
       return employee

    return wrapper
