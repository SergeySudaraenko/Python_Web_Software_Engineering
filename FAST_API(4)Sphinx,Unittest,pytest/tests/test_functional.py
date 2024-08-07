import pytest
from fastapi.testclient import TestClient
from contacts_api import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
from utils import hash_password
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Налаштування тестової бази даних
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Створення клієнта для тестування FastAPI
client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    # Створення всіх таблиць перед тестуванням
    Base.metadata.create_all(bind=engine)
    yield
    # Видалення всіх таблиць після тестування
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def create_user(setup_database):
    db = SessionLocal()
    user = User(
        email="test@example.com",
        hashed_password=hash_password("testpassword"),
        is_verified=True,
        id=1
    )
    db.add(user)
    db.commit()
    db.close()
    return user

def test_create_contact(create_user):
    # Логін для отримання токену доступу
    response = client.post("/login/", data={"username": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    # Створення нового контакту
    headers = {"Authorization": f"Bearer {access_token}"}
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "123-456-7890",
        "birthday": "1990-01-01"
    }
    response = client.post("/contacts/", json=contact_data, headers=headers)
    assert response.status_code == 201
    contact = response.json()
    assert contact["first_name"] == "John"
    assert contact["last_name"] == "Doe"
    assert contact["email"] == "john@example.com"
    assert contact["phone"] == "123-456-7890"

def test_read_contact(create_user):
    # Логін для отримання токену доступу
    response = client.post("/login/", data={"username": "test@example.com", "password": "testpassword"})
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    # Створення нового контакту
    headers = {"Authorization": f"Bearer {access_token}"}
    contact_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "phone": "098-765-4321",
        "birthday": "1992-02-02"
    }
    response = client.post("/contacts/", json=contact_data, headers=headers)
    assert response.status_code == 201
    contact_id = response.json()["id"]

    # Отримання контакту
    response = client.get(f"/contacts/{contact_id}", headers=headers)
    assert response.status_code == 200
    contact = response.json()
    assert contact["first_name"] == "Jane"
    assert contact["last_name"] == "Doe"
    assert contact["email"] == "jane@example.com"

def test_create_contact_without_auth():
    # Спроба створити контакт без авторизації
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "123-456-7890",
        "birthday": "1990-01-01"
    }
    response = client.post("/contacts/", json=contact_data)
    assert response.status_code == 401  # Unauthorized
