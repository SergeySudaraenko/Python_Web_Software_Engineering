from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    """
    Модель користувача для бази даних.

    Атрибути:
        id (int): Ідентифікатор користувача.
        email (str): Електронна пошта користувача.
        hashed_password (str): Хешований пароль користувача.
        is_verified (bool): Статус підтвердження електронної пошти.
        avatar_url (str, optional): URL аватара користувача.
        verification_token (str, optional): Токен підтвердження електронної пошти.
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
    Модель контакту для бази даних.

    Атрибути:
        id (int): Ідентифікатор контакту.
        first_name (str): Ім'я контакту.
        last_name (str): Прізвище контакту.
        email (str): Електронна пошта контакту.
        phone (str, optional): Телефонний номер контакту.
        birthday (date, optional): Дата народження контакту.
        owner_id (int): Ідентифікатор власника контакту.
        created_at (date): Дата створення контакту.
    """
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    birthday = Column(Date, index=True)
    owner_id = Column(Integer, index=True)
    created_at = Column(Date, default=func.now())
