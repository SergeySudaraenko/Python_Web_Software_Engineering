import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contacts_api.app import crud, models, schemas

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class TestCreateContact(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        models.Base.metadata.create_all(bind=engine)

    @classmethod
    def tearDownClass(cls):
        models.Base.metadata.drop_all(bind=engine)

    def setUp(self):
        self.db = SessionLocal()
        self.user = models.User(email="testuser@example.com", hashed_password="hashedpassword")
        self.db.add(self.user)
        self.db.commit()
        self.db.refresh(self.user)

    def tearDown(self):
        self.db.close()

    def test_create_contact(self):
        contact_data = schemas.ContactCreate(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            birthday="1990-01-01"
        )
        contact = crud.create_contact(self.db, contact_data, owner_id=self.user.id)
        
        self.assertIsInstance(contact, models.Contact)
        self.assertEqual(contact.first_name, "John")
        self.assertEqual(contact.last_name, "Doe")
        self.assertEqual(contact.email, "john.doe@example.com")
        self.assertEqual(contact.phone, "1234567890")
        self.assertEqual(contact.birthday, "1990-01-01")
        
if __name__ == "__main__":
    unittest.main()
