from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .models import Contact

def get_upcoming_birthdays(db: Session, days: int = 30):
    today = datetime.today().date()
    upcoming_date = today + timedelta(days=days)
    return db.query(Contact).filter(Contact.birthday >= today, Contact.birthday <= upcoming_date).all()

