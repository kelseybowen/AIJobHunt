import os
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.db.mongo import mongo, get_db


@pytest_asyncio.fixture
async def client():
    await mongo.connect(os.getenv("TEST_DB"))

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac

    await mongo.close()


@pytest_asyncio.fixture(autouse=True)
async def clean_users_collection(client):
    yield
    db = get_db()
    await db.users.delete_many({})
