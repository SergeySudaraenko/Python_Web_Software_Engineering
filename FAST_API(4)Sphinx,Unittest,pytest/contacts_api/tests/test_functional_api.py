import pytest
from fastapi.testclient import TestClient
from contacts_api.app.main import app

client = TestClient(app)

@pytest.fixture
def auth_header():
    response = client.post("/login/", data={"username": "testuser@example.com", "password": "testpassword"})
    assert response.status_code == 200  
    data = response.json()
    assert "access_token" in data  
    return {"Authorization": f"Bearer {data['access_token']}"}

def test_create_contact(auth_header):
    response = client.post(
        "/contacts/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "birthday": "1990-01-01"
        },
        headers=auth_header
    )
    assert response.status_code == 201
    assert "id" in response.json()





