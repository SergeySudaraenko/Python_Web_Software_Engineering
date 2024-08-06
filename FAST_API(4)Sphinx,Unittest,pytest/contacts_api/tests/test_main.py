import pytest
from fastapi.testclient import TestClient
from app.main import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import database
import models

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = models.Base

def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[database.get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module")
def test_setup():
    setup_database()
    yield client

def test_register_user(test_setup):
    response = test_setup.post("/register/", json={"email": "test@example.com", "password": "testpassword"})
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_login_user(test_setup):
    test_setup.post("/register/", json={"email": "test@example.com", "password": "testpassword"})
    response = test_setup.post("/login/", data={"username": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
