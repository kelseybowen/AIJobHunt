import os
from pymongo import AsyncMongoClient


client = None
_db = None


async def connect_to_mongo():
    global client, _db

    uri = os.getenv("MONGODB_CONNECT_STRING")
    db_name = os.getenv("PROD_DB")

    client = AsyncMongoClient(uri)
    _db = client[db_name]

    await client.admin.command("ping")
    print("Connected to MongoDB")


async def connect_to_mongo_test():
    global client, _db

    uri = os.getenv("MONGODB_CONNECT_STRING")
    db_name = os.getenv("TEST_DB")

    client = AsyncMongoClient(uri)
    _db = client[db_name]

    await client.admin.command("ping")
    print("Connected to MongoDB")


async def close_mongo():
    global client
    if client:
        await client.close()


def get_db():
    return _db
