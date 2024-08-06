import unittest
from app import crud, models, schemas
from app.database import SessionLocal
from datetime import date

class TestCRUD(unittest.TestCase):

    def setUp(self):
        self.db = SessionLocal()
        self.user = models.User(email="test@example.com", hashed_password="hashed_password")
        self.db.add(self.user)
        self.db.commit()
        self.contact_data = schemas.ContactCreate(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="123456789",
            birthday=date(1990, 1, 1)
        )

    def test_create_contact(self):
        contact = crud.create_contact(self.db, self.contact_data, self.user.id)
        self.assertEqual(contact.first_name, self.contact_data.first_name)

    def test_get_contacts(self):
        crud.create_contact(self.db, self.contact_data, self.user.id)
        contacts = crud.get_contacts(self.db, owner_id=self.user.id)
        self.assertGreater(len(contacts), 0)

    def tearDown(self):
        self.db.close()

if __name__ == "__main__":
    unittest.main()
