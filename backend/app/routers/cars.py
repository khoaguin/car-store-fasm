from typing import Dict, List, Optional

from decouple import config
from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from ..dependencies.database import get_db
from ..models.car_model import CarBase, CarDB, CarUpdate

if config("DEV_MODE"):
    CAR_COLLECTION = config("CARS_COLLECTION_NAME", cast=str) + "_dev"
else:
    CAR_COLLECTION = config("CARS_COLLECTION_NAME", cast=str)

router = APIRouter()


@router.get("/all_cars", response_description="List all cars")
async def list_all_cars(
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> List[CarDB]:
    """List all cars"""
    cars_collection: AsyncIOMotorCollection = db[CAR_COLLECTION]
    documents = []
    async for document in cars_collection.find():
        documents.append(document)
    return documents


@router.get("/", response_description="List cars according to conditions")
async def list_cars(
    db: AsyncIOMotorDatabase = Depends(get_db),
    min_price: int = 0,
    max_price: int = 1_000_000,
    brand: Optional[str] = None,
    page: int = 1,
) -> List[CarDB]:
    """List all cars"""
    results_per_page = 25
    skip = (page - 1) * results_per_page
    query = {"price": {"$lt": max_price, "$gt": min_price}}
    if brand:
        query["brand"] = brand
    full_query = (
        db[CAR_COLLECTION]
        .find(query)
        .sort("_id", -1)
        .skip(skip)
        .limit(results_per_page)
    )
    results = [CarDB(**raw_car) async for raw_car in full_query]
    return results


@router.post("/create_car", response_description="Add new car")
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


@router.delete("/{id}", response_description="Delete car")
async def delete_car(id: str, db: AsyncIOMotorDatabase = Depends(get_db)) -> Response:
    delete_result = await db[CAR_COLLECTION].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Car with {id} not found")


@router.patch("/{id}", response_description="Update car")
async def update_car(
    id: str,
    db: AsyncIOMotorDatabase = Depends(get_db),
    car_update: CarUpdate = Body(...),
) -> CarDB:
    await db[CAR_COLLECTION].update_one(
        {"_id": id}, {"$set": car_update.dict(exclude_unset=True)}
    )
    updated_car = await db[CAR_COLLECTION].find_one({"_id": id})
    if updated_car is not None:
        return CarDB(**updated_car)
    raise HTTPException(status_code=404, detail=f"Car with {id} not found")
