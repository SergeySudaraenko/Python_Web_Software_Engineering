from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

config = dotenv_values(".env") 

DATABASE_URL = config.get("DATABASE_URL", "")
print(DATABASE_URL, "Тут повинен бути ЮРЛ")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

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

