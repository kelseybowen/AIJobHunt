import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.db.mongo import connect_to_mongo_test, close_mongo, get_db


@pytest_asyncio.fixture
async def client():
    await connect_to_mongo_test()

    transport = ASGITransport(
        app=app
    )

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

    await close_mongo()


@pytest_asyncio.fixture(autouse=True)
async def clean_users_collection(client):
    yield
    db = get_db()
    await db.users.delete_many({})
