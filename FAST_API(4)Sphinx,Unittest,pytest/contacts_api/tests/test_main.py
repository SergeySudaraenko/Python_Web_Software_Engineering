import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Contacts API"}

def test_register_user():
    response = client.post("/register/", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 201
    assert "id" in response.json()


