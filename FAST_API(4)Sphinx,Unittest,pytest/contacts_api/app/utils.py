from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

from contacts_api.app.schemas import TokenData

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
RESET_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Хешує пароль.

    :param password: Пароль, який потрібно хешувати.
    :return: Хешований пароль.
    """
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Перевіряє, чи збігається пароль з хешованим паролем.

    :param password: Пароль для перевірки.
    :param hashed_password: Хешований пароль.
    :return: True, якщо паролі збігаються, інакше False.
    """
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    """
    Створює токен доступу.

    :param data: Дані для кодування в токен.
    :param expires_delta: Час до закінчення терміну дії токена.
    :return: Токен доступу.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)) -> str:
    """
    Створює токен оновлення.

    :param data: Дані для кодування в токен.
    :param expires_delta: Час до закінчення терміну дії токена.
    :return: Токен оновлення.
    """
    return create_access_token(data, expires_delta)

def verify_token(token: str, credentials_exception):
    """
    Перевіряє токен і повертає дані токена.

    :param token: Токен для перевірки.
    :param credentials_exception: Виняток, який потрібно кинути, якщо токен недійсний.
    :return: Дані токена.
    :raises credentials_exception: Якщо токен недійсний або протермінований.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return TokenData(email=email)
    except JWTError:
        raise credentials_exception

def send_verification_email(email: str, token: str):
    """
    Відправляє email з токеном підтвердження.

    :param email: Email користувача.
    :param token: Токен підтвердження email.
    """
    pass

def send_password_reset_email(email: str, token: str):
    """
    Відправляє email з токеном для скидання пароля.

    :param email: Email користувача.
    :param token: Токен для скидання пароля.
    """
    pass
