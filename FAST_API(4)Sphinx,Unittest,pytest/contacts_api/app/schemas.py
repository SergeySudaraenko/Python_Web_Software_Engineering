from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    """
    Base schema for user information.
    
    Attributes:
        email (EmailStr): The user's email address.
        avatar_url (Optional[str]): URL to the user's avatar.
    """
    email: EmailStr
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    
    Attributes:
        password (str): The user's password.
    """
    password: str

class User(UserBase):
    """
    Schema for a user object returned by the API.
    
    Attributes:
        id (int): The unique identifier of the user.
        is_verified (bool): Flag indicating if the user has verified their email.
    """
    id: int
    is_verified: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    """
    Schema for authentication tokens.
    
    Attributes:
        access_token (str): The access token.
        refresh_token (str): The refresh token.
        token_type (str): The type of the token.
    """
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema for token data.
    
    Attributes:
        email (str): The user's email address.
    """
    email: str

class ContactBase(BaseModel):
    """
    Base schema for contact information.
    
    Attributes:
        first_name (str): The contact's first name.
        last_name (str): The contact's last name.
        email (str): The contact's email address.
        phone (Optional[str]): The contact's phone number.
        birthday (Optional[date]): The contact's birthday.
    """
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    birthday: Optional[date] = None

class ContactCreate(ContactBase):
    """
    Schema for creating a new contact.
    """
    pass

class ContactUpdate(ContactBase):
    """
    Schema for updating an existing contact.
    """
    pass

class Contact(ContactBase):
    """
    Schema for a contact object returned by the API.
    
    Attributes:
        id (int): The unique identifier of the contact.
    """
    id: int

    class Config:
        from_attributes = True
