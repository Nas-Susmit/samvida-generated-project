import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the backend"}

def test_login_user():
    response = client.post("/api/login")
    assert response.status_code == 200

def test_register_user():
    response = client.post("/api/register")
    assert response.status_code == 200

def test_get_users():
    response = client.get("/api/users")
    assert response.status_code == 200

def test_get_food_intake():
    response = client.get("/api/food_intake")
    assert response.status_code == 200

def test_get_physical_activity():
    response = client.get("/api/physical_activity")
    assert response.status_code == 200
