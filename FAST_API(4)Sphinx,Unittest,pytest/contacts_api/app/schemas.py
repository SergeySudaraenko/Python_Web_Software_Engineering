from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    """
    Основна схема даних користувача.

    :param email: Email користувача.
    :param avatar_url: URL аватара користувача.
    """
    email: EmailStr
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    """
    Схема для створення нового користувача.

    :param password: Пароль користувача.
    """
    password: str

class User(UserBase):
    """
    Схема даних користувача, що включає додаткову інформацію.

    :param id: ID користувача.
    :param is_verified: Статус перевірки email.
    """
    id: int
    is_verified: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    """
    Схема токенів для авторизації.

    :param access_token: Токен доступу.
    :param refresh_token: Токен оновлення.
    :param token_type: Тип токена.
    """
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Схема даних токена.

    :param email: Email користувача.
    """
    email: str

class ContactBase(BaseModel):
    """
    Основна схема даних контакту.

    :param first_name: Ім'я контакту.
    :param last_name: Прізвище контакту.
    :param email: Email контакту.
    :param phone: Телефон контакту.
    :param birthday: День народження контакту.
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
    """
    pass

class Contact(ContactBase):
    """
    Схема даних контакту, що включає ID.

    :param id: ID контакту.
    """
    id: int

    class Config:
        from_attributes = True



