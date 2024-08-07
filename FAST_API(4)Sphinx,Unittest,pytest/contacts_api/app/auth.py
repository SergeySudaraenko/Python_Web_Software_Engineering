from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from .models import User
from .schemas import UserCreate, Token
from .utils import RESET_TOKEN_EXPIRE_MINUTES, send_verification_email, send_password_reset_email, create_access_token, create_refresh_token, verify_password, hash_password, verify_token
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    """
    Генерує і повертає сесію бази даних.

    Повертає:
        Generator: Генератор сесії бази даних.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def register_user(db: Session, user: UserCreate):
    """
    Реєструє нового користувача в базі даних.

    Аргументи:
        db (Session): Сесія бази даних.
        user (UserCreate): Дані користувача для реєстрації.

    Повертає:
        User: Зареєстрований користувач.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, is_verified=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    verification_token = create_access_token({"sub": user.email}, expires_delta=timedelta(hours=1))
    send_verification_email(user.email, verification_token)
    return db_user

def login_user(db: Session, username: str, password: str):
    """
    Увійти в систему з використанням електронної пошти та пароля.

    Аргументи:
        db (Session): Сесія бази даних.
        username (str): Електронна пошта користувача.
        password (str): Пароль користувача.

    Повертає:
        Token: Токени доступу та оновлення.
    """
    db_user = db.query(User).filter(User.email == username).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not db_user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    access_token = create_access_token({"sub": db_user.email})
    refresh_token = create_refresh_token({"sub": db_user.email})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

def verify_email(db: Session, token: str):
    """
    Перевіряє електронну пошту користувача за допомогою токена.

    Аргументи:
        db (Session): Сесія бази даних.
        token (str): Токен для підтвердження електронної пошти.

    Повертає:
        str: Повідомлення про успішну перевірку.
    """
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    token_data = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    user.is_verified = True
    db.commit()
    return "Email verified successfully"

def reset_password(db: Session, email: str):
    """
    Скидає пароль користувача за допомогою електронної пошти.

    Аргументи:
        db (Session): Сесія бази даних.
        email (str): Електронна пошта користувача для скидання пароля.

    Повертає:
        str: Повідомлення про успішне скидання пароля.
    """
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    reset_token = create_access_token({"sub": email}, expires_delta=timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES))
    send_password_reset_email(email, reset_token)
    return "Password reset email sent"

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Отримує поточного користувача з токена.

    Аргументи:
        token (str): Токен доступу.
        db (Session): Сесія бази даних.

    Повертає:
        User: Поточний користувач.

    Викидає:
        HTTPException: Якщо токен недійсний або користувач не знайдений.
    """
    credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")
    token_data = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user
