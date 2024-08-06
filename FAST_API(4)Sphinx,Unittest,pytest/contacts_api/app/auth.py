from datetime import timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from . import models, schemas, utils, crud
from .database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def register_user(db: Session, user: schemas.UserCreate):
    """
    Реєстрація нового користувача в системі.

    :param db: Сесія бази даних.
    :param user: Дані користувача для реєстрації.
    :raises HTTPException: Якщо email вже зареєстрований.
    :return: Створений користувач.
    """
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = utils.hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, email: str, password: str):
    """
    Авторизація користувача та отримання токенів.

    :param db: Сесія бази даних.
    :param email: Email користувача.
    :param password: Пароль користувача.
    :raises HTTPException: Якщо облікові дані недійсні.
    :return: Словник з токенами та типом токена.
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None or not utils.verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = utils.create_access_token(data={"sub": email})
    refresh_token = utils.create_refresh_token(data={"sub": email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

def verify_email(db: Session, token: str):
    """
    Підтвердження email користувача за допомогою токена.

    :param db: Сесія бази даних.
    :param token: Токен для підтвердження.
    :raises HTTPException: Якщо токен недійсний.
    :return: Повідомлення про підтвердження email.
    """
    user = db.query(models.User).filter(models.User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    user.is_verified = True
    user.verification_token = None
    db.commit()
    return {"message": "Email verified"}

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Отримання поточного користувача з бази даних на основі токена.

    :param db: Сесія бази даних.
    :param token: JWT токен користувача.
    :raises HTTPException: Якщо не вдалося перевірити облікові дані.
    :return: Користувач з бази даних.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = utils.verify_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

def reset_password(db: Session, email: str):
    """
    Запит на скидання пароля для користувача.

    :param db: Сесія бази даних.
    :param email: Email користувача, для якого потрібно скинути пароль.
    :raises HTTPException: Якщо користувача не знайдено.
    :return: Повідомлення про те, що лист для скидання пароля відправлено.
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    reset_token = utils.create_access_token(data={"sub": email}, expires_delta=timedelta(minutes=utils.RESET_TOKEN_EXPIRE_MINUTES))
    utils.send_password_reset_email(email, reset_token)
    return {"message": "Password reset email sent"}