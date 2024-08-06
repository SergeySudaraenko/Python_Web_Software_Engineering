from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    """
    Represents a user in the system.
    
    Attributes:
        id (int): The unique identifier of the user.
        email (str): The user's email address.
        hashed_password (str): The hashed password of the user.
        is_verified (bool): Flag indicating if the user has verified their email.
        avatar_url (Optional[str]): URL to the user's avatar.
        verification_token (Optional[str]): Token used for email verification.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)
    avatar_url = Column(String, nullable=True)
    verification_token = Column(String, nullable=True)

class Contact(Base):
    """
    Represents a contact associated with a user.
    
    Attributes:
        id (int): The unique identifier of the contact.
        first_name (str): The contact's first name.
        last_name (str): The contact's last name.
        email (str): The contact's email address.
        phone (Optional[str]): The contact's phone number.
        birthday (Optional[Date]): The contact's birthday.
        owner_id (int): The ID of the user who owns this contact.
        created_at (Date): The date and time when the contact was created.
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True, nullable=True)
    birthday = Column(Date, index=True, nullable=True)
    owner_id = Column(Integer, index=True)
    created_at = Column(Date, default=func.now())
