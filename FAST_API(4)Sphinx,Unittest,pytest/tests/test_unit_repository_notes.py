import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contacts_api.app.models import Base,User
from crud import create_contact, contact_creation_limit_exceeded
from contacts_api.app.schemas import ContactBase,ContactCreate,ContactUpdate
import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TestCRUD(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
    
    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=engine)

    def setUp(self):
        self.db = SessionLocal()
        self.user_id = 1  # Створюємо користувача для тестів
        self.db.add(User(email="test@example.com", hashed_password="hashed_password", is_verified=True, id=self.user_id))
        self.db.commit()

    def tearDown(self):
        self.db.close()

    def test_contact_creation_limit_exceeded(self):
        contact_data = ContactCreate(first_name="John", last_name="Doe", email="john@example.com")
        create_contact(self.db, contact_data, owner_id=self.user_id)
        self.assertTrue(contact_creation_limit_exceeded(self.db, self.user_id))
