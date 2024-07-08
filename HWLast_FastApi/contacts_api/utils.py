from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from . import models

def get_upcoming_birthdays(db: Session, days: int = 7):
    today = datetime.today()
    upcoming_date = today + timedelta(days=days)
    today_month_day = (today.month, today.day)
    upcoming_birthdays = []
    
    contacts = db.query(models.Contact).all()
    for contact in contacts:
        birthday_month_day = (contact.birthday.month, contact.birthday.day)
        if today_month_day <= birthday_month_day <= (upcoming_date.month, upcoming_date.day):
            upcoming_birthdays.append(contact)
    
    return upcoming_birthdays
