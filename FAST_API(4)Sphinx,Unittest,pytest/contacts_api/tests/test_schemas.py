import pytest
from pydantic import ValidationError
from datetime import date
from schemas import (
    UserBase,
    UserCreate,
    User,
    Token,
    TokenData,
    ContactBase,
    ContactCreate,
    ContactUpdate,
    Contact
)

def test_user_base():
    
    user_base = UserBase(email="test@example.com", avatar_url="http://example.com/avatar.jpg")
    assert user_base.email == "test@example.com"
    assert user_base.avatar_url == "http://example.com/avatar.jpg"

    
    user_base = UserBase(email="test@example.com")
    assert user_base.avatar_url is None

def test_user_create():
   
    user_create = UserCreate(email="test@example.com", password="securepassword")
    assert user_create.email == "test@example.com"
    assert user_create.password == "securepassword"

    
    with pytest.raises(ValidationError):
        UserCreate(email="not-an-email", password="securepassword")

def test_user():
   
    user = User(id=1, email="test@example.com", is_verified=True, avatar_url="http://example.com/avatar.jpg")
    assert user.id == 1
    assert user.email == "test@example.com"
    assert user.is_verified is True
    assert user.avatar_url == "http://example.com/avatar.jpg"

def test_token():
    
    token = Token(access_token="access-token", refresh_token="refresh-token", token_type="bearer")
    assert token.access_token == "access-token"
    assert token.refresh_token == "refresh-token"
    assert token.token_type == "bearer"

def test_token_data():
    
    token_data = TokenData(email="test@example.com")
    assert token_data.email == "test@example.com"

def test_contact_base():
    
    contact_base = ContactBase(first_name="John", last_name="Doe", email="john.doe@example.com", phone="1234567890", birthday=date(1990, 1, 1))
    assert contact_base.first_name == "John"
    assert contact_base.last_name == "Doe"
    assert contact_base.email == "john.doe@example.com"
    assert contact_base.phone == "1234567890"
    assert contact_base.birthday == date(1990, 1, 1)

    
    contact_base = ContactBase(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert contact_base.phone is None
    assert contact_base.birthday is None

def test_contact_create():
    
    contact_create = ContactCreate(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert contact_create.first_name == "John"
    assert contact_create.last_name == "Doe"
    assert contact_create.email == "john.doe@example.com"

def test_contact_update():
    
    contact_update = ContactUpdate(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert contact_update.first_name == "John"
    assert contact_update.last_name == "Doe"
    assert contact_update.email == "john.doe@example.com"

def test_contact():
    
    contact = Contact(id=1, first_name="John", last_name="Doe", email="john.doe@example.com")
    assert contact.id == 1
    assert contact.first_name == "John"
    assert contact.last_name == "Doe"
    assert contact.email == "john.doe@example.com"
