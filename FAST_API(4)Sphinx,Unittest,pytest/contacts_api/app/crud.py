from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .models import Contact
from .schemas import ContactCreate, ContactUpdate

def contact_creation_limit_exceeded(db: Session, user_id: int) -> bool:
    """
    Checks if the user has exceeded the contact creation limit.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.

    Returns:
        bool: True if the user has exceeded the limit, False otherwise.
    """
    last_contact = db.query(Contact).filter(Contact.owner_id == user_id).order_by(Contact.created_at.desc()).first()
    if last_contact:
        now = datetime.utcnow()
        if (now - last_contact.created_at).total_seconds() < 60:  
            return True
    return False

def create_contact(db: Session, contact: ContactCreate, owner_id: int):
    """
    Creates a new contact for the specified owner.

    Args:
        db (Session): The database session.
        contact (ContactCreate): The contact data.
        owner_id (int): The ID of the contact owner.

    Returns:
        Contact: The created contact.
    """
    db_contact = Contact(**contact.dict(), owner_id=owner_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, skip: int = 0, limit: int = 10, owner_id: int = None):
    """
    Retrieves a list of contacts for the specified owner.

    Args:
        db (Session): The database session.
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to return.
        owner_id (int, optional): The ID of the contact owner.

    Returns:
        List[Contact]: The list of contacts.
    """
    query = db.query(Contact)
    if owner_id:
        query = query.filter(Contact.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int, owner_id: int):
    """
    Retrieves a specific contact for the specified owner.

    Args:
        db (Session): The database session.
        contact_id (int): The ID of the contact.
        owner_id (int): The ID of the contact owner.

    Returns:
        Contact: The contact if found, None otherwise.
    """
    return db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()

def update_contact(db: Session, contact_id: int, contact: ContactUpdate, owner_id: int):
    """
    Updates a specific contact for the specified owner.

    Args:
        db (Session): The database session.
        contact_id (int): The ID of the contact.
        contact (ContactUpdate): The new contact data.
        owner_id (int): The ID of the contact owner.

    Returns:
        Contact: The updated contact if successful, None otherwise.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    return None

def delete_contact(db: Session, contact_id: int, owner_id: int):
    """
    Deletes a specific contact for the specified owner.

    Args:
        db (Session): The database session.
        contact_id (int): The ID of the contact.
        owner_id (int): The ID of the contact owner.

    Returns:
        Contact: The deleted contact if successful, None otherwise.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return db_contact
    return None

def get_upcoming_birthdays(db: Session, owner_id: int):
    """
    Retrieves contacts with upcoming birthdays for the specified owner.

    Args:
        db (Session): The database session.
        owner_id (int): The ID of the contact owner.

    Returns:
        List[Contact]: The list of contacts with upcoming birthdays.
    """
    today = datetime.utcnow().date()
    upcoming_date = today + timedelta(days=30)
    return db.query(Contact).filter(
        Contact.birthday >= today,
        Contact.birthday <= upcoming_date,
        Contact.owner_id == owner_id
    ).all()
