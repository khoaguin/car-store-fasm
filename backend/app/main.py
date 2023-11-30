from pprint import pprint

from decouple import config
from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

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


@app.get("/")
async def home(request: Request):
    """Home page"""
    cars_collection: AsyncIOMotorCollection = request.app.mongodb["cars_dev"]
    documents = []
    async for document in cars_collection.find():
        documents.append(document)
    pprint(documents)


app.include_router(cars_router, prefix="/cars", tags=["cars"])
