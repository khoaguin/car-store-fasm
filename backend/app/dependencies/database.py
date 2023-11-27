from typing import AsyncGenerator

from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)


# Dependency
def get_db_client() -> AsyncGenerator[AsyncIOMotorClient, None]:
    client = AsyncIOMotorClient(DB_URL)
    try:
        yield client
    finally:
        client.close()


# Dependency
def get_db() -> AsyncGenerator[AsyncIOMotorClient, None]:
    client = AsyncIOMotorClient(DB_URL)
    db: AsyncIOMotorDatabase = client[DB_NAME]
    try:
        yield db
    finally:
        client.close()


if __name__ == "__main__":
    print(DB_NAME, DB_URL)
