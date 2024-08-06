import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import models,database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

def test_create_contact(test_setup):
    token = get_access_token(test_setup)
    response = test_setup.post("/contacts/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "birthday": "1990-01-01"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201

def test_get_contacts(test_setup):
    token = get_access_token(test_setup)
    test_setup.post("/contacts/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "birthday": "1990-01-01"
    }, headers={"Authorization": f"Bearer {token}"})
    response = test_setup.get("/contacts/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0

def get_access_token(test_setup):
    response = test_setup.post("/login/", data={"username": "test@example.com", "password": "testpassword"})
    return response.json()["access_token"]
