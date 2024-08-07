from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from schemas import ContactCreate, ContactUpdate
from .models import Contact, User


def contact_creation_limit_exceeded(db: Session, user_id: int) -> bool:
    """
    Перевіряє, чи перевищив користувач ліміт на створення контактів.

    Аргументи:
        db (Session): Сесія бази даних.
        user_id (int): Ідентифікатор користувача.

    Повертає:
        bool: True, якщо ліміт перевищено, інакше False.
    """
    last_contact = db.query(Contact).filter(Contact.owner_id == user_id).order_by(Contact.created_at.desc()).first()
    if last_contact:
        now = datetime.utcnow()
        if (now - last_contact.created_at).total_seconds() < 60:
            return True
    return False

def create_contact(db: Session, contact: ContactCreate, owner_id: int):
    """
    Створює новий контакт у базі даних.

    Аргументи:
        db (Session): Сесія бази даних.
        contact (ContactCreate): Дані контакту.
        owner_id (int): Ідентифікатор власника контакту.

    Повертає:
        Contact: Створений контакт.
    """
    db_contact = Contact(**contact.dict(), owner_id=owner_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, skip: int = 0, limit: int = 10, owner_id: int = None):
    """
    Отримує список контактів з бази даних.

    Аргументи:
        db (Session): Сесія бази даних.
        skip (int): Кількість записів для пропуску.
        limit (int): Кількість записів для повернення.
        owner_id (int, optional): Ідентифікатор власника контакту.

    Повертає:
        list: Список контактів.
    """
    query = db.query(Contact)
    if owner_id:
        query = query.filter(Contact.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int, owner_id: int):
    """
    Отримує конкретний контакт з бази даних.

    Аргументи:
        db (Session): Сесія бази даних.
        contact_id (int): Ідентифікатор контакту.
        owner_id (int): Ідентифікатор власника контакту.

    Повертає:
        Contact: Контакт, якщо знайдено, або None.
    """
    return db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()

def update_contact(db: Session, contact_id: int, contact: ContactUpdate, owner_id: int):
    """
    Оновлює конкретний контакт у базі даних.

    Аргументи:
        db (Session): Сесія бази даних.
        contact_id (int): Ідентифікатор контакту.
        contact (ContactUpdate): Оновлені дані контакту.
        owner_id (int): Ідентифікатор власника контакту.

    Повертає:
        Contact: Оновлений контакт, якщо знайдено, або None.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int, owner_id: int):
    """
    Видаляє конкретний контакт з бази даних.

    Аргументи:
        db (Session): Сесія бази даних.
        contact_id (int): Ідентифікатор контакту.
        owner_id (int): Ідентифікатор власника контакту.

    Повертає:
        Contact: Видалений контакт, якщо знайдено, або None.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def get_upcoming_birthdays(db: Session, days: int = 30, owner_id: int = None):
    """
    Отримує контакти з наближеними днями народження протягом вказаної кількості днів.

    Аргументи:
        db (Session): Сесія бази даних.
        days (int): Кількість днів для перегляду.
        owner_id (int, optional): Ідентифікатор власника контакту.

    Повертає:
        list: Список контактів з наближеними днями народження.
    """
    today = datetime.today().date()
    upcoming_date = today + timedelta(days=days)
    query = db.query(Contact).filter(Contact.birthday >= today, Contact.birthday <= upcoming_date)
    if owner_id:
        query = query.filter(Contact.owner_id == owner_id)
    return query.all()
