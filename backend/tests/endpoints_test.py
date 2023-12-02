from typing import Dict, List

import pytest
from httpx import AsyncClient

from backend.app.main import app


@pytest.mark.asyncio
async def test_list_cars():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/cars/")
        assert response.status_code == 200
        assert isinstance(response.json(), List)


@pytest.mark.asyncio
async def test_create_find_delete_car():
    # Sample car data
    test_car_data = {
        "brand": "test",
        "make": "500",
        "year": 1998,
        "price": 3000,
        "km": 2000,
        "cm3": 2000,
        "car_type": "SDN",
        "color": "BL",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # test the create_car POST request
        create_response = await ac.post("/cars/", json=test_car_data)
        assert create_response.status_code == 201
        create_response_data: Dict = create_response.json()
        created_car_id: str = create_response_data["_id"]
        for k, v in create_response_data.items():
            if k != "_id":
                assert v == test_car_data[k]
        # test the show_car GET request
        get_response = await ac.get(f"/cars/{created_car_id}")
        assert get_response.status_code == 200
        assert get_response.json()["_id"] == created_car_id
        # test the delete_car POST request
        delete_response = await ac.delete(f"/cars/{created_car_id}")
        assert delete_response.status_code == 204
