from http.client import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already registered")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if user and user.verify_password(password):
        return user
    return None

def create_contact(db: Session, contact: schemas.ContactCreate, owner_id: int):
    db_contact = models.Contact(**contact.dict(), owner_id=owner_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, skip: int = 0, limit: int = 10, owner_id: int = None):
    query = db.query(models.Contact)
    if owner_id:
        query = query.filter(models.Contact.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int, owner_id: int):
    return db.query(models.Contact).filter(
        models.Contact.id == contact_id,
        models.Contact.owner_id == owner_id
    ).first()

def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate, owner_id: int):
    db_contact = db.query(models.Contact).filter(
        models.Contact.id == contact_id,
        models.Contact.owner_id == owner_id
    ).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int, owner_id: int):
    db_contact = db.query(models.Contact).filter(
        models.Contact.id == contact_id,
        models.Contact.owner_id == owner_id
    ).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact





