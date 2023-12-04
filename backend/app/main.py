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
                <h1>Welcome to the Car Selling Store</h1>
                <p>Here are the current cars we have: </p>
            </body>
        </html>
    """


app.include_router(cars_router, prefix="/cars", tags=["cars"])
