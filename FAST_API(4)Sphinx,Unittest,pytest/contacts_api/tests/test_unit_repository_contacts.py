import unittest
from unittest.mock import MagicMock
from contacts_api.app.crud import create_contact
from contacts_api.app.models import Contact

class TestCRUD(unittest.TestCase):
    def test_create_contact(self):
        db = MagicMock()
        contact_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "birthday": "1990-01-01"
        }
        result = create_contact(db, contact_data)
        self.assertEqual(result.first_name, "John")
        self.assertEqual(result.email, "john.doe@example.com")

if __name__ == '__main__':
    unittest.main()
