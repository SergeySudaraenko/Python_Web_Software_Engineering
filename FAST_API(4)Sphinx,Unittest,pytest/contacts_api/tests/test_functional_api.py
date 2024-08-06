import pytest
from fastapi.testclient import TestClient
from contacts_api.app.main import app

client = TestClient(app)

@pytest.fixture
def token():
  
    return "<valid_access_token>"

def test_create_contact(token):
    response = client.post(
        "/contacts/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "birthday": "1990-01-01"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201



