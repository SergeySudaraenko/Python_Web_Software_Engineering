from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    """
    Основна схема для користувача.

    Атрибути:
        email (EmailStr): Електронна пошта користувача.
        avatar_url (str, optional): URL аватара користувача.
    """
    email: EmailStr
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    """
    Схема для створення нового користувача.

    Атрибути:
        password (str): Пароль користувача.
    """
    password: str

class User(UserBase):
    """
    Схема для користувача з додатковими полями.

    Атрибути:
        id (int): Ідентифікатор користувача.
        is_verified (bool): Статус підтвердження електронної пошти.
    """
    id: int
    is_verified: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    """
    Схема для токенів доступу та оновлення.

    Атрибути:
        access_token (str): Токен доступу.
        refresh_token (str): Токен для оновлення.
        token_type (str): Тип токена (наприклад, "bearer").
    """
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Схема для даних токена.

    Атрибути:
        email (str): Електронна пошта користувача.
    """
    email: str

class ContactBase(BaseModel):
    """
    Основна схема для контакту.

    Атрибути:
        first_name (str): Ім'я контакту.
        last_name (str): Прізвище контакту.
        email (str): Електронна пошта контакту.
        phone (str, optional): Телефонний номер контакту.
        birthday (date, optional): Дата народження контакту.
    """
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    birthday: Optional[date] = None

class ContactCreate(ContactBase):
    """
    Схема для створення нового контакту.
    """
    pass

class ContactUpdate(ContactBase):
    """
    Схема для оновлення контакту.

    Атрибути:
        first_name (str, optional): Нове ім'я контакту.
        last_name (str, optional): Нове прізвище контакту.
        email (str, optional): Нова електронна пошта контакту.
        phone (str, optional): Новий телефонний номер контакту.
        birthday (date, optional): Нова дата народження контакту.
    """
    pass
