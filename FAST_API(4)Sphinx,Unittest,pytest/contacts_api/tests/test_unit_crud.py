import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contacts_api.app.crud import  (
    contact_creation_limit_exceeded,
    create_contact,
    get_contacts,
    get_contact,
    update_contact,
    delete_contact,
    get_upcoming_birthdays,
    update_avatar
)
from contacts_api.app.models import Base,Contact,User
from contacts_api.app.schemas import ContactCreate, ContactUpdate
from contacts_api.app.schemas import get_db
from sqlalchemy.ext.declarative import declarative_base

# Налаштування для тестової бази даних
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

class TestCRUD(unittest.TestCase):

    def setUp(self):
        self.db = SessionLocal()
        self.user_id = 1
        self.contact_data = ContactCreate(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            birthday=datetime(1990, 1, 1).date()
        )
        self.contact_update = ContactUpdate(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com",
            phone="0987654321",
            birthday=datetime(1991, 2, 2).date()
        )

    def tearDown(self):
        self.db.query(Contact).delete()
        self.db.query(User).delete()
        self.db.commit()
        self.db.close()

    def test_contact_creation_limit_exceeded(self):
        create_contact(self.db, self.contact_data, self.user_id)
        self.assertTrue(contact_creation_limit_exceeded(self.db, self.user_id))
        self.assertFalse(contact_creation_limit_exceeded(self.db, self.user_id + 1))

    def test_create_contact(self):
        contact = create_contact(self.db, self.contact_data, self.user_id)
        self.assertIsNotNone(contact.id)
        self.assertEqual(contact.first_name, "John")

    def test_get_contacts(self):
        create_contact(self.db, self.contact_data, self.user_id)
        contacts = get_contacts(self.db, owner_id=self.user_id)
        self.assertGreater(len(contacts), 0)

    def test_get_contact(self):
        contact = create_contact(self.db, self.contact_data, self.user_id)
        retrieved_contact = get_contact(self.db, contact.id, self.user_id)
        self.assertEqual(retrieved_contact.email, "john.doe@example.com")

    def test_update_contact(self):
        contact = create_contact(self.db, self.contact_data, self.user_id)
        updated_contact = update_contact(self.db, contact.id, self.contact_update, self.user_id)
        self.assertEqual(updated_contact.first_name, "Jane")

    def test_delete_contact(self):
        contact = create_contact(self.db, self.contact_data, self.user_id)
        deleted_contact = delete_contact(self.db, contact.id, self.user_id)
        self.assertIsNotNone(deleted_contact)
        self.assertIsNone(get_contact(self.db, contact.id, self.user_id))

    def test_get_upcoming_birthdays(self):
        create_contact(self.db, self.contact_data, self.user_id)
        upcoming_birthdays = get_upcoming_birthdays(self.db, self.user_id)
        self.assertGreater(len(upcoming_birthdays), 0)

    def test_update_avatar(self):
        user = User(email="user@example.com", hashed_password="hashedpassword")
        self.db.add(user)
        self.db.commit()
        updated_user = update_avatar(self.db, "http://example.com/avatar.png", user.id)
        self.assertEqual(updated_user.avatar_url, "http://example.com/avatar.png")

if __name__ == "__main__":
    unittest.main()
