import unittest
from app.utils import hash_password, verify_password

class TestUtils(unittest.TestCase):

    def setUp(self):
        """Підготовка до тестів: хешування пароля."""
        self.password = "password123"
        self.hashed_password = hash_password(self.password)

    def test_hash_password(self):
        """Перевірка, що хешування пароля повертає значення."""
        self.assertTrue(self.hashed_password)
        self.assertNotEqual(self.password, self.hashed_password, "Password should be hashed")

    def test_verify_password(self):
        """Перевірка, що перевірка пароля працює правильно для правильного пароля."""
        self.assertTrue(verify_password(self.password, self.hashed_password))

    def test_verify_password_incorrect(self):
        """Перевірка, що перевірка пароля повертає False для неправильного пароля."""
        self.assertFalse(verify_password("wrongpassword", self.hashed_password))

    def tearDown(self):
        """Очищення після тестів (якщо потрібно)."""
        pass

if __name__ == "__main__":
    unittest.main()
