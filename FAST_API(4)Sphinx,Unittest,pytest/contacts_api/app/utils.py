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
    Хешує пароль користувача.

    Аргументи:
        password (str): Пароль користувача.

    Повертає:
        str: Хешований пароль.
    """
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Перевіряє правильність пароля.

    Аргументи:
        password (str): Пароль користувача.
        hashed_password (str): Хешований пароль.

    Повертає:
        bool: True, якщо пароль правильний, інакше False.
    """
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    """
    Створює токен доступу.

    Аргументи:
        data (dict): Дані для кодування у токен.
        expires_delta (timedelta): Час дії токена.

    Повертає:
        str: Токен доступу.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)) -> str:
    """
    Створює токен для оновлення.

    Аргументи:
        data (dict): Дані для кодування у токен.
        expires_delta (timedelta): Час дії токена.

    Повертає:
        str: Токен для оновлення.
    """
    return create_access_token(data, expires_delta)

def verify_token(token: str, credentials_exception):
    """
    Перевіряє токен і декодує дані.

    Аргументи:
        token (str): Токен для перевірки.
        credentials_exception (HTTPException): Виняток, що викидається при помилці.

    Повертає:
        TokenData: Декодовані дані з токена.

    Викидає:
        credentials_exception: Якщо токен недійсний.
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
    Надсилає електронний лист для підтвердження електронної пошти.

    Аргументи:
        email (str): Електронна пошта користувача.
        token (str): Токен для підтвердження.
    """
    # Реалізуйте функцію надсилання електронної пошти
    pass

def send_password_reset_email(email: str, token: str):
    """
    Надсилає електронний лист для скидання пароля.

    Аргументи:
        email (str): Електронна пошта користувача.
        token (str): Токен для скидання пароля.
    """
    # Реалізуйте функцію надсилання електронної пошти
    pass
