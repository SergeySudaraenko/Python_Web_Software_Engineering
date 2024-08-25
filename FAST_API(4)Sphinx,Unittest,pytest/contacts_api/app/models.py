from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.sql import func
from .database import Base
# try:
#     from .database import Base
# except Exception:
#     pass

class User(Base):
    """
    Модель даних користувача.

    :param id: ID користувача.
    :param email: Email користувача.
    :param hashed_password: Хешований пароль.
    :param is_verified: Статус перевірки email.
    :param avatar_url: URL аватара користувача.
    :param verification_token: Токен перевірки email.
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
    Модель даних контакту.

    :param id: ID контакту.
    :param first_name: Ім'я контакту.
    :param last_name: Прізвище контакту.
    :param email: Email контакту.
    :param phone: Телефон контакту.
    :param birthday: День народження контакту.
    :param owner_id: ID власника контакту.
    :param created_at: Дата створення контакту.
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

