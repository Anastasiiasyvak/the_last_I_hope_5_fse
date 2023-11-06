from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_user():
    data = {"username": "testuser", "email": "test@example.com"}
    response = client.post("/users/", json=data)
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"


def test_get_user():
    response = client.get("/users/testuser")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"
