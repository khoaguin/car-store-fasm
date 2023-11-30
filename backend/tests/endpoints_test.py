from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from backend.app.dependencies.database import get_db
from backend.app.main import app

# Initialize the TestClient
# client = TestClient(app)


@pytest.mark.asyncio
async def test_list_cars():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/cars/")
        assert response.status_code == 200
        # assert response.json() == {"item_id": 5}
        print(response.json())
        import pdb

        pdb.set_trace()
        assert False


@pytest.mark.asyncio
async def test_create_car():
    # Sample car data
    test_car_data = {
        "brand": "Fiat",
        "make": "500",
        "year": 1998,
        "price": 3000,
        "km": 2000,
        "cm3": 2000,
        "car_type": "SDN",
        "color": "BL",
    }

    # # Send a POST request to the endpoint
    # response = client.post("/cars/", json=test_car_data)

    # # Assert that the status code is 201
    # assert response.status_code == 201

    # # Assert that the response data matches the test data
    # response_data = response.json()
    # for k, v in response_data.items():
    #     assert v == test_car_data[k]
