import unittest
from app.auth import register_user, login_user
from app.database import SessionLocal
from app.schemas import UserCreate

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.db = SessionLocal()
        self.user = UserCreate(email="test@example.com", password="password123")

    def test_register_user(self):
        user = register_user(self.db, self.user)
        self.assertEqual(user.email, self.user.email)

    def test_login_user(self):
        register_user(self.db, self.user)
        tokens = login_user(self.db, self.user.email, self.user.password)
        self.assertIn('access_token', tokens)

    def tearDown(self):
        self.db.close()

if __name__ == "__main__":
    unittest.main()
