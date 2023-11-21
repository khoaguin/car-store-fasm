from typing import Dict

from decouple import config
from fastapi import APIRouter, Body, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.car_model import CarBase

CAR_COLLECTION = config("CARS_COLLECTION_NAME", cast=str)
router = APIRouter()


@router.get("/", response_description="List all cars")
async def list_cars() -> Dict:
    return {"data": "All cars will go here."}


@router.post("/", response_description="Add new car")
async def create_car(request: Request, car: CarBase = Body(...)):
    car_json: Dict = jsonable_encoder(car)
    import pdb

    pdb.set_trace()
    # new_car = await request.app.mongodb[CAR_COLLECTION].insert_one(car)
    # created_car = await request.app.mongodb["cars1"].find_one(
    #     {"_id": new_car.inserted_id}
    # )
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_car)
