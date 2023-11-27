from typing import Dict

from decouple import config
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from ..main import get_db_client
from ..models.car_model import CarBase, CarDB

if config("DEV_MODE"):
    CAR_COLLECTION = config("CARS_COLLECTION_NAME", cast=str) + "_dev"
else:
    CAR_COLLECTION = config("CARS_COLLECTION_NAME", cast=str)

router = APIRouter()


@router.get("/", response_description="List all cars")
async def list_cars() -> Dict:
    return {"data": "All cars will go here."}


@router.post("/", response_description="Add new car")
async def create_car(request: Request, car: CarBase = Body(...)) -> JSONResponse:
    car_json: Dict = jsonable_encoder(car)
    new_car = await request.app.mongodb[CAR_COLLECTION].insert_one(car_json)
    created_car = await request.app.mongodb[CAR_COLLECTION].find_one(
        {"_id": new_car.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_car)


@router.get("/{id}", response_description="Get a car")
async def show_car(id: str, request: Request) -> CarDB:
    car = await request.app.mongodb[CAR_COLLECTION].find_one({"_id": id})
    if car is not None:
        return CarDB(**car)
    raise HTTPException(status_code=404, detail=f"Car with  {id} not found")
