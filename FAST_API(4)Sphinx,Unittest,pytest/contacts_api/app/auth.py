
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from datetime import timedelta

from database import SessionLocal
from models import User
from schemas import UserCreate
from utils import (
    send_verification_email, 
    send_password_reset_email, 
    create_access_token, 
    create_refresh_token, 
    verify_password, 
    hash_password, 
    verify_token
)
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    """
    Створює і повертає об'єкт сесії бази даних SQLAlchemy.

    :yield: Об'єкт сесії SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def register_user(db: Session, user: UserCreate):
    """
    Реєструє нового користувача в базі даних.

    :param db: Об'єкт сесії SQLAlchemy для роботи з базою даних.
    :param user: Схема для створення користувача, яка містить email і пароль.
    :return: Створений користувач.
    :raises HTTPException: Якщо email вже зареєстровано.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=409, detail="Email вже зареєстровано")
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, is_verified=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    verification_token = create_access_token({"sub": user.email}, expires_delta=timedelta(hours=1))
    send_verification_email(user.email, verification_token)
    return db_user

def login_user(db: Session, email: str, password: str):
    """
    Логін користувача за email і паролем.

    :param db: Об'єкт сесії SQLAlchemy для роботи з базою даних.
    :param email: Email користувача.
    :param password: Пароль користувача.
    :return: Словник з токеном доступу і токеном оновлення.
    :raises HTTPException: Якщо дані для входу неправильні або email не підтверджений.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неправильні дані для входу")
    if not user.is_verified:
        raise HTTPException(status_code=401, detail="Email не підтверджений")
    access_token = create_access_token({"sub": email})
    refresh_token = create_refresh_token({"sub": email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

def verify_email(db: Session, token: str):
    """
    Підтверджує email користувача за допомогою токена.

    :param db: Об'єкт сесії SQLAlchemy для роботи з базою даних.
    :param token: Токен підтвердження email.
    :return: Оновлений користувач.
    :raises HTTPException: Якщо токен недійсний або протермінований.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не вдалося перевірити облікові дані",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise HTTPException(status_code=400, detail="Недійсний або протермінований токен")
    user.is_verified = True
    db.commit()
    db.refresh(user)
    return user

def reset_password(db: Session, email: str):
    """
    Ініціює процес скидання пароля, відправляючи email з токеном скидання.

    :param db: Об'єкт сесії SQLAlchemy для роботи з базою даних.
    :param email: Email користувача, для якого потрібно скинути пароль.
    :return: Повідомлення про те, що email для скидання пароля відправлено.
    :raises HTTPException: Якщо email не зареєстровано.
    """
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Email не зареєстровано")
    reset_token = create_reset_token({"sub": email})
    send_password_reset_email(email, reset_token)
    return {"message": "Email для скидання пароля відправлено"}

def create_reset_token(data: dict) -> str:
    """
    Створює токен для скидання пароля.

    :param data: Дані, які потрібно закодувати в токен.
    :return: Токен для скидання пароля.
    """
    return create_access_token(data, expires_delta=timedelta(hours=1))

def send_password_reset_email(email: str, token: str):
    """
    Відправляє email для скидання пароля.

    :param email: Email користувача.
    :param token: Токен для скидання пароля.
    """
    pass

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Отримує поточного користувача на основі токена.

    :param db: Об'єкт сесії SQLAlchemy для роботи з базою даних.
    :param token: Токен доступу.
    :return: Поточний користувач.
    :raises HTTPException: Якщо токен недійсний або користувач не знайдений.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не вдалося перевірити облікові дані",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

def update_avatar(db: Session, avatar_url: str, user_id: int):
    """
    Оновлює URL аватара користувача.

    :param db: Об'єкт сесії SQLAlchemy для роботи з базою даних.
    :param avatar_url: URL новий аватара.
    :param user_id: ID користувача, для якого потрібно оновити аватар.
    :return: Оновлений користувач.
    :raises HTTPException: Якщо користувач не знайдений.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    user.avatar_url = avatar_url
    db.commit()
    db.refresh(user)
    return user






