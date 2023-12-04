"""
Script to import the sample dataset in `cars_data.csv` into MongoDB
Source: https://github.com/PacktPublishing/Full-Stack-FastAPI-React-and-MongoDB/blob/main/chapter5/backend/importScript.py
"""


import csv
from pathlib import Path

from decouple import config
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from ..app.models.car_model import CarBase

DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)
COLLECTION_NAME = config("CARS_COLLECTION_NAME", cast=str)

# read csv
with open(Path.cwd() / "backend/data/cars_data.csv", encoding="utf-8") as f:
    csv_reader = csv.DictReader(f)
    name_records = list(csv_reader)

mongo_client = MongoClient(DB_URL)
db = mongo_client[DB_NAME]
cars_collection = db[COLLECTION_NAME]

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

mongo_client.close()
