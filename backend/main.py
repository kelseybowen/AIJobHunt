from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from backend.db.mongo import connect_to_mongo, close_mongo
from backend.routers import users

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo()


app = FastAPI(lifespan=lifespan)

app.include_router(users.router, prefix="/users", tags=["Users"])
