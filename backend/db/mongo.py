import os
from pymongo import AsyncMongoClient


class MongoManager:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self, db_name: str):
        uri = os.getenv("MONGODB_CONNECT_STRING")

        self.client = AsyncMongoClient(uri)
        self.db = self.client[db_name]

        await self.client.admin.command("ping")
        print("Connected to MongoDB")

    async def close(self):
        if self.client:
            await self.client.close()


mongo = MongoManager()


def get_db():
    return mongo.db
