import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import User
from app.utils import hash_password
from contacts_api.main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.query(User).delete()
        db.commit()
        db.close()

@pytest.fixture
def create_test_user(db):
    password = "testpassword"
    hashed_password = hash_password(password)
    user = User(email="testuser@example.com", hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def test_register_user(db):
    response = client.post("/register/", json={
        "email": "newuser@example.com",
        "password": "newpassword"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "newuser@example.com"

# def test_login_user(create_test_user):
#     response = client.post("/login/", data={
#         "username": "testuser@example.com",
#         "password": "testpassword"
#     })
#     assert response.status_code == 200
#     assert "access_token" in response.json()
#     assert "refresh_token" in response.json()

# def test_create_contact(create_test_user):
#     token_response = client.post("/login/", data={
#         "username": "testuser@example.com",
#         "password": "testpassword"
#     })
#     token = token_response.json()["access_token"]

#     response = client.post("/contacts/", json={
#         "first_name": "Alice",
#         "last_name": "Smith",
#         "email": "alice.smith@example.com",
#         "phone": "5551234",
#         "birthday": "1990-01-01"
#     }, headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 201
#     assert response.json()["email"] == "alice.smith@example.com"

# def test_update_contact(create_test_user):
#     token_response = client.post("/login/", data={
#         "username": "testuser@example.com",
#         "password": "testpassword"
#     })
#     token = token_response.json()["access_token"]

#     contact_response = client.post("/contacts/", json={
#         "first_name": "Bob",
#         "last_name": "Brown",
#         "email": "bob.brown@example.com",
#         "phone": "5555678",
#         "birthday": "1985-05-05"
#     }, headers={"Authorization": f"Bearer {token}"})
#     contact_id = contact_response.json()["id"]

#     response = client.put(f"/contacts/{contact_id}", json={
#         "first_name": "Robert",
#         "last_name": "Brown",
#         "email": "robert.brown@example.com",
#         "phone": "5558765",
#         "birthday": "1985-05-05"
#     }, headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
#     assert response.json()["email"] == "robert.brown@example.com"

# def test_delete_contact(create_test_user):
#     token_response = client.post("/login/", data={
#         "username": "testuser@example.com",
#         "password": "testpassword"
#     })
#     token = token_response.json()["access_token"]

#     contact_response = client.post("/contacts/", json={
#         "first_name": "Charlie",
#         "last_name": "Johnson",
#         "email": "charlie.johnson@example.com",
#         "phone": "5559876",
#         "birthday": "1992-12-12"
#     }, headers={"Authorization": f"Bearer {token}"})
#     contact_id = contact_response.json()["id"]

#     response = client.delete(f"/contacts/{contact_id}", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
#     assert response.json()["email"] == "charlie.johnson@example.com"

# def test_get_upcoming_birthdays(create_test_user):
#     token_response = client.post("/login/", data={
#         "username": "testuser@example.com",
#         "password": "testpassword"
#     })
#     token = token_response.json()["access_token"]

#     contact_response = client.post("/contacts/", json={
#         "first_name": "David",
#         "last_name": "Williams",
#         "email": "david.williams@example.com",
#         "phone": "5551234",
#         "birthday": "2024-08-20"
#     }, headers={"Authorization": f"Bearer {token}"})

#     response = client.get("/contacts/upcoming_birthdays/", headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
#     assert any(contact["email"] == "david.williams@example.com" for contact in response.json())
