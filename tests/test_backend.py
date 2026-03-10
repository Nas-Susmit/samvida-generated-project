import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to the API'}

def test_get_users():
    response = client.get('/users')
    assert response.status_code == 200

def test_get_foods():
    response = client.get('/foods')
    assert response.status_code == 200
