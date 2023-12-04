from pprint import pprint

from decouple import config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from .routers.cars import router as cars_router

DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)

# define origins that are allowed to access the serve
origins = [
    "http://localhost:5000",  # default port for the Svelte frontend
]

app = FastAPI()

# configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  #  Allows cookies or authorization headers to be sent along with requests
    allow_methods=["*"],  # Allows all HTTP methods (like GET, POST, etc.).
    allow_headers=["*"],  # Allows all headers in the HTTP requests.
)


async def startup_db_client() -> None:
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]


async def shutdown_db_client() -> None:
    app.mongodb_client.close()


app.add_event_handler("startup", startup_db_client)
app.add_event_handler("shutdown", shutdown_db_client)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Home page"""
    print("this is our home page")
    cars_collection: AsyncIOMotorCollection = request.app.mongodb["cars_dev"]
    documents = []
    async for document in cars_collection.find():
        documents.append(document)
    return """
        <!DOCTYPE html>
        <html>
            <head>
                <title>Home Page</title>
            </head>
            <body>
                <h1>Welcome to the Home Page</h1>
                <p>This is a simple HTML response from FastAPI.</p>
            </body>
        </html>
    """


@app.post("/upload_data", response_description="Upload all data")
async def upload_data(request: Request):
    import csv
    from pathlib import Path

    from fastapi.encoders import jsonable_encoder

    from .models.car_model import CarBase

    cars_collection: AsyncIOMotorCollection = request.app.mongodb["cars"]

    with open(Path.cwd() / "backend/data/cars_data.csv", encoding="utf-8") as f:
        csv_reader = csv.DictReader(f)
        name_records = list(csv_reader)

    for rec in name_records:
        try:
            rec["price"] = int(rec["price"])
            rec["year"] = int(rec["year"])
            rec["cm3"] = int(float(rec["cm3"]))

            if rec["price"] > 1000:
                car = jsonable_encoder(CarBase(**rec))
                print("Inserting:", car)
                cars_collection.insert_one(car)
        except ValueError as e:
            print(e)


app.include_router(cars_router, prefix="/cars", tags=["cars"])
