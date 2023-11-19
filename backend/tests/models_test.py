from typing import Dict

from app.models.car_model import CarDB
from bson import ObjectId
from fastapi.encoders import jsonable_encoder


def test_car_model() -> None:
    car1 = {
        "_id": ObjectId("64cca8a68efc81fc425aa864"),
        "brand": "Fiat",
        "make": "500",
        "km": 4000,
        "cm3": 2000,
        "price": 3000,
        "year": 1998,
    }
    car2 = {
        "_id": "64cca8a68efc81fc425aa864",
        "brand": "Fiat",
        "make": "500",
        "km": 4000,
        "cm3": 2000,
        "price": 3000,
        "year": 1998,
    }
    # Test if `ObjectId` can be used as string
    car1_db = CarDB(**car1)
    car2_db = CarDB(**car2)
    assert car1_db == car2_db
    # Serialization
    assert (
        repr(car1_db) == "CarDB(id=ObjectId('64cca8a68efc81fc425aa864'), brand='Fiat', "
        "make='500', year=1998, price=3000, km=4000, cm3=2000)"
    )
    assert car1_db.model_dump() == {
        "id": ObjectId("64cca8a68efc81fc425aa864"),
        "brand": "Fiat",
        "make": "500",
        "year": 1998,
        "price": 3000,
        "km": 4000,
        "cm3": 2000,
    }
    json_encoded_str = (
        '{"id":"64cca8a68efc81fc425aa864",'
        '"brand":"Fiat",'
        '"make":"500",'
        '"year":1998,'
        '"price":3000,'
        '"km":4000,'
        '"cm3":2000}'
    )
    assert car1_db.model_dump_json() == json_encoded_str
    assert jsonable_encoder(car1_db, by_alias=True) == car2