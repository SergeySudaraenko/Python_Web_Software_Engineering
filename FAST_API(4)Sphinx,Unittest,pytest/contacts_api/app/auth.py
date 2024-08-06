from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from contacts_api.app.database import SessionLocal
from .models import User
from .schemas import UserCreate, Token, TokenData
from .utils import send_verification_email, send_password_reset_email, create_access_token, create_refresh_token, verify_password, hash_password, verify_token
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    """
    Dependency that provides a database session.
    
    Yields:
        Session: The database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def register_user(db: Session, user: UserCreate):
    """
    Registers a new user by hashing their password and creating a verification token.
    
    Args:
        db (Session): The database session.
        user (UserCreate): The user data for registration.
        
    Returns:
        User: The created user.
        
    Raises:
        HTTPException: If the email is already registered.
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

def login_user(db: Session, email: str, password: str):
    """
    Logs in a user by verifying credentials and generating access and refresh tokens.
    
    Args:
        db (Session): The database session.
        email (str): The user's email.
        password (str): The user's password.
        
    Returns:
        dict: A dictionary containing access and refresh tokens.
        
    Raises:
        HTTPException: If credentials are invalid or email is not verified.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=401, detail="Email not verified")
    access_token = create_access_token({"sub": email})
    refresh_token = create_refresh_token({"sub": email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

def verify_email(db: Session, token: str):
    """
    Verifies a user's email using the provided token.
    
    Args:
        db (Session): The database session.
        token (str): The verification token.
        
    Returns:
        User: The verified user.
        
    Raises:
        HTTPException: If the token is invalid or expired.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user.is_verified = True
    db.commit()
    db.refresh(user)
    return user

def reset_password(db: Session, email: str):
    """
    Sends a password reset email to the user.
    
    Args:
        db (Session): The database session.
        email (str): The user's email.
        
    Returns:
        dict: A message indicating that the password reset email has been sent.
        
    Raises:
        HTTPException: If the email is not registered.
    """
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Email not registered")
    reset_token = create_reset_token({"sub": email})
    send_password_reset_email(email, reset_token)
    return {"message": "Password reset email sent"}

def create_reset_token(data: dict) -> str:
    """
    Creates a password reset token.
    
    Args:
        data (dict): The data to include in the token.
        
    Returns:
        str: The created token.
    """
    return create_access_token(data, expires_delta=timedelta(hours=1))

def send_verification_email(email: str, token: str):
    """
    Placeholder function for sending a verification email.
    
    Args:
        email (str): The user's email.
        token (str): The verification token.
    """
    pass

def send_password_reset_email(email: str, token: str):
    """
    Placeholder function for sending a password reset email.
    
    Args:
        email (str): The user's email.
        token (str): The password reset token.
    """
    pass

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Retrieves the current user based on the provided token.
    
    Args:
        db (Session): The database session.
        token (str): The access token.
        
    Returns:
        User: The current user.
        
    Raises:
        HTTPException: If the token is invalid or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

def update_avatar(db: Session, avatar_url: str, user_id: int):
    """
    Updates the user's avatar URL.
    
    Args:
        db (Session): The database session.
        avatar_url (str): The new avatar URL.
        user_id (int): The user's ID.
        
    Returns:
        User: The user with the updated avatar URL.
        
    Raises:
        HTTPException: If the user is not found.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.avatar_url = avatar_url
    db.commit()
    db.refresh(user)
    return user







