from typing import Dict, List

from decouple import config
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from ..dependencies.database import get_db
from ..models.car_model import CarBase, CarDB

if config("DEV_MODE"):
    CAR_COLLECTION = config("CARS_COLLECTION_NAME", cast=str) + "_dev"
else:
    CAR_COLLECTION = config("CARS_COLLECTION_NAME", cast=str)

router = APIRouter()


@router.get("/", response_description="List all cars")
async def list_cars(db: AsyncIOMotorDatabase = Depends(get_db)) -> List:
    """List all cars"""
    cars_collection: AsyncIOMotorCollection = db[CAR_COLLECTION]
    documents = []
    async for document in cars_collection.find():
        documents.append(document)
    return documents


@router.post("/", response_description="Add new car")
async def create_car(
    car: CarBase = Body(...),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> JSONResponse:
    car_json: Dict = jsonable_encoder(car)
    new_car = await db[CAR_COLLECTION].insert_one(car_json)
    created_car = await db[CAR_COLLECTION].find_one({"_id": new_car.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_car)


@router.get("/{id}", response_description="Get a car")
async def show_car(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> CarDB:
    car = await db[CAR_COLLECTION].find_one({"_id": id})
    if car is not None:
        return CarDB(**car)
    raise HTTPException(status_code=404, detail=f"Car with  {id} not found")
