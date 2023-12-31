# AI-powered Car Selling Store

![](./assets/banner.png)

An AI-powered Car Selling Store App Written in FastAPI, Svelte and MongoDB.

## Database

Setting your free Mongo Atlas account at https://cloud.mongodb.com/. Then, create an instance, a database, and a collection. After that, create a `.env` file at the root folder of the project and fill in the connection string (should be kept private), the database and collection name like below

```bash
DB_URL=""
DB_NAME=""
CARS_COLLECTION_NAME=""
```

In the `backend/data/data_script.py`, we have the code needed to upload the data in `backend/data/cars_data.csv` to MongoDB Atlas according to the data model defined in `backend/app/models/car_model.py`. Run it with

```bash
python -m backend.data.data_script
```

> Note: If you get the `pymongo.errors.ServerSelectionTimeoutError: SSL handshake failed`, it is probably because you try to connect to the database from an IP address which is not on the list of allowed IPs for accessing your MongoDB database. To fix this, you'll need to add your current IP address to the IP whitelist in your MongoDB Atlas account. Or you can allow access from anywhere in the `Network Access` tab of MongoDB Atlas

## Backend

The backend is written in FastAPI and requires Python 3.11

```bash
conda create -n carstore python=3.11
conda activate carstore
pip install -r backend/requirements.txt
```

To run the backend server, run the following in the terminal

```bash
bash backend.sh
```

Assuming the backend server is run at `http://localhost:8000/`, we can test it with the installed `HTTPie` Python package like below

```bash
http "http://localhost:8000/"
```

The backend is deployed on AWS Elastic Beanstalk at the URL `http://car-store-fasm-dev.ap-southeast-1.elasticbeanstalk.com/`

## Frontend

The frontend is built using Svelte 5.0 and SvelteKit 2.0
To run the frontend do

```bash
bash frontend.sh
```

## Tests

To run the backend tests, do `pytest backend/tests`

## References

- [Full Stack FastAPI, React, and MongoDB, published by Packt](https://github.com/PacktPublishing/Full-Stack-FastAPI-React-and-MongoDB/tree/main)
