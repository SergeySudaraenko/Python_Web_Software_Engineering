from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .models import Contact, User
from .schemas import ContactCreate, ContactUpdate

def contact_creation_limit_exceeded(db: Session, user_id: int) -> bool:
    last_contact = db.query(Contact).filter(Contact.owner_id == user_id).order_by(Contact.created_at.desc()).first()
    if last_contact:
        now = datetime.utcnow()
        if (now - last_contact.created_at).total_seconds() < 60:  
            return True
    return False

def create_contact(db: Session, contact: ContactCreate, owner_id: int):
    db_contact = Contact(**contact.dict(), owner_id=owner_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, skip: int = 0, limit: int = 10, owner_id: int = None):
    query = db.query(Contact)
    if owner_id:
        query = query.filter(Contact.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int, owner_id: int):
    return db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()

def update_contact(db: Session, contact_id: int, contact: ContactUpdate, owner_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int, owner_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def get_upcoming_birthdays(db: Session, days: int = 30, owner_id: int = None):
    today = datetime.today().date()
    upcoming_date = today + timedelta(days=days)
    query = db.query(Contact).filter(Contact.birthday >= today, Contact.birthday <= upcoming_date)
    if owner_id:
        query = query.filter(Contact.owner_id == owner_id)
    return query.all()







