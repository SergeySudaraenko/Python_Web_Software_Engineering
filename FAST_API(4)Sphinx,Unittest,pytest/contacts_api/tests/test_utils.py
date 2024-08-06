import unittest
from app.utils import hash_password, verify_password

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.password = "password123"
        self.hashed_password = hash_password(self.password)

    def test_hash_password(self):
        self.assertTrue(self.hashed_password)

    def test_verify_password(self):
        self.assertTrue(verify_password(self.password, self.hashed_password))

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
