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
    Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed password.

    Args:
        password (str): The password to verify.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    return pwd_context.verify(password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    """
    Creates an access token with the given data and expiration time.

    Args:
        data (dict): The data to include in the token.
        expires_delta (timedelta): The expiration time of the token.

    Returns:
        str: The created token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "sub": data.get("sub")})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=7)) -> str:
    """
    Creates a refresh token with the given data and expiration time.

    Args:
        data (dict): The data to include in the token.
        expires_delta (timedelta): The expiration time of the token.

    Returns:
        str: The created token.
    """
    return create_access_token(data, expires_delta)

def verify_token(token: str, credentials_exception) -> TokenData:
    """
    Verifies a token and extracts the data.

    Args:
        token (str): The token to verify.
        credentials_exception: Exception to raise if the token is invalid.

    Returns:
        TokenData: The token data if the token is valid.

    Raises:
        credentials_exception: If the token is invalid.
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
