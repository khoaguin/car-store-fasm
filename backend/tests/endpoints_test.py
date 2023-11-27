from app.main import app
from fastapi.testclient import TestClient

# Initialize the TestClient
client = TestClient(app)


def test_create_car():
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

    # Send a POST request to the endpoint
    response = client.post("/cars/", json=test_car_data)

    # Assert that the status code is 201
    assert response.status_code == 201

    # Assert that the response data matches the test data
    response_data = response.json()
    for k, v in response_data.items():
        assert v == test_car_data[k]
