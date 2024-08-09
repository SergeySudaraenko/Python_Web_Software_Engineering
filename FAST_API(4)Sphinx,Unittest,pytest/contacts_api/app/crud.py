from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .models import Contact, User
from .schemas import ContactCreate, ContactUpdate

def contact_creation_limit_exceeded(db: Session, user_id: int) -> bool:
    """
    Перевіряє, чи перевищено ліміт створення контактів для користувача.

    :param db: Об'єкт сесії SQLAlchemy для роботи з базою даних.
    :param user_id: ID користувача.
    :return: True, якщо ліміт перевищено, інакше False.
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

    :param db: Об'єкт сесії SQLAlchemy для роботи з базою даних.
    :param contact: Схема для створення контакту.
    :param owner_id: ID власника контакту.
    :return: Створений контакт.
    """
    db_contact = Contact(**contact.dict(), owner_id=owner_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, skip: int = 0, limit: int = 10, owner_id: int = None):
    """
    Отримує список контактів з бази даних.

    :param db: Об'єкт сесії SQLAlchemy для роботи з базою даних.
    :param skip: Кількість пропущених записів.
    :param limit: Максимальна кількість записів для повернення.
    :param owner_id: ID власника контактів.
    :return: Список контактів.
    """
    query = db.query(Contact)
    if owner_id:
        query = query.filter(Contact.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int, owner_id: int):
    """
    Отримує контакт за його ID.

    :param db: Об'єкт сесії SQLAlchemy для роботи з базою даних.
    :param contact_id: ID контакту.
    :param owner_id: ID власника контактів.
    :return: Контакт, якщо знайдено, інакше None.
    """
    return db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()

def update_contact(db: Session, contact_id: int, contact: ContactUpdate, owner_id: int):
    """
    Оновлює контакт за його ID.

    :param db: Об'єкт сесії SQLAlchemy для роботи з базою даних.
    :param contact_id: ID контакту.
    :param contact: Схема для оновлення контакту.
    :param owner_id: ID власника контактів.
    :return: Оновлений контакт, якщо знайдено, інакше None.
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
    Видаляє контакт за його ID.

    :param db: Об'єкт сесії SQLAlchemy для роботи з базою даних.
    :param contact_id: ID контакту.
    :param owner_id: ID власника контактів.
    :return: Видалений контакт, якщо знайдено, інакше None.
    """
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == owner_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return db_contact
    return None

def get_upcoming_birthdays(db: Session, owner_id: int):
    """
    Отримує контакти з найближчими днями народження.

    :param db: Об'єкт сесії SQLAlchemy для роботи з базою даних.
    :param owner_id: ID власника контактів.
    :return: Список контактів з найближчими днями народження.
    """
    now = datetime.utcnow()
    next_month = (now + timedelta(days=30)).month
    return db.query(Contact).filter(
        Contact.owner_id == owner_id,
        Contact.birthday.isnot(None),
        (func.extract('month', Contact.birthday) == now.month) |
        (func.extract('month', Contact.birthday) == next_month)
    ).all()

def update_avatar(db: Session, avatar_url: str, user_id: int):
    """
    Оновлює URL аватара користувача.

    :param db: Об'єкт сесії SQLAlchemy для роботи з базою даних.
    :param avatar_url: Новий URL аватара.
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
