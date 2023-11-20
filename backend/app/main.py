import uvicorn
from decouple import config
from fastapi import Depends, FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from routers.cars import router as cars_router

DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)


async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]
    print(f"{app.mongodb = }")


async def shutdown_db_client():
    app.mongodb_client.close()


app = FastAPI()
app.add_event_handler("startup", startup_db_client)
app.add_event_handler("shutdown", shutdown_db_client)


# Dependency
def get_db_client():
    client = AsyncIOMotorClient(DB_URL)
    try:
        yield client
    finally:
        client.close()


@app.get("/some_endpoint")
async def some_endpoint(client: AsyncIOMotorClient = Depends(get_db_client)):
    db = client[DB_NAME]


app.include_router(cars_router, prefix="/cars", tags=["cars"])
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
