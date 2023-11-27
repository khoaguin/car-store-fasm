from pprint import pprint
from typing import AsyncGenerator

import uvicorn
from decouple import config
from fastapi import Depends, FastAPI
from motor.motor_asyncio import (AsyncIOMotorClient, AsyncIOMotorCollection,
                                 AsyncIOMotorDatabase)

from .dependencies.database import get_db, get_db_client
from .routers.cars import router as cars_router

DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)


async def startup_db_client() -> None:
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]


async def shutdown_db_client() -> None:
    app.mongodb_client.close()


app = FastAPI()
app.add_event_handler("startup", startup_db_client)
app.add_event_handler("shutdown", shutdown_db_client)


# Dependency
def get_db_client() -> AsyncGenerator[AsyncIOMotorClient, None]:
    client = AsyncIOMotorClient(DB_URL)
    try:
        yield client
    finally:
        client.close()


@app.get("/")
async def home(db: AsyncIOMotorClient = Depends(get_db)):
    cars_collection: AsyncIOMotorCollection = db["cars_dev"]
    documents = []
    print(cars_collection)
    async for document in cars_collection.find():
        documents.append(document)
    pprint(documents)


@app.get("/")
def home() -> str:
    return "hello to my car store"


# app.include_router(cars_router, prefix="/cars", tags=["cars"])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
