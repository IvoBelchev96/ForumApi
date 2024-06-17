import unittest
from unittest.mock import patch
from services.user_services import create, find_by_email, try_login,  User, IntegrityError


ID = 1
EMAIL = 'test@test.bg'
USERNAME = 'test'
PASSWORD = 'test'


class TestUserServices(unittest.TestCase):
    @patch('services.user_services.insert_query')
    def test_create_user_correctly(self, mock_insert_query):
        mock_id = 1
        mock_insert_query = mock_id

        result = create(EMAIL, USERNAME, PASSWORD)

        self.assertIsInstance(result, User)
        self.assertEqual(result.id, mock_id)
        self.assertEqual(result.username, USERNAME)
        self.assertEqual(result.password, '')

    @patch('services.user_services.insert_query')
    def test_create_user_failed(self, mock_insert_query):
        mock_insert_query.side_effect = IntegrityError

        result = create(EMAIL, USERNAME, PASSWORD)

        self.assertIsNone(result)

    @patch('services.user_services.read_query')
    def test_find_by_email_correctly(self, mock_read_query):
        mock_read_query.return_value = [(ID, EMAIL, USERNAME, PASSWORD)]

        result = find_by_email(EMAIL)

        self.assertIsInstance(result, User)
        self.assertEqual(result.id, ID)
        self.assertEqual(result.email, EMAIL)
        self.assertEqual(result.username, USERNAME)
        self.assertEqual(result.password, PASSWORD)

    @patch('services.user_services.read_query')
    def test_find_by_email_failed(self, mock_read_query):
        mock_read_query.side_effect = None

        result = find_by_email(EMAIL)

        self.assertIsNone(result)

    def test_try_login_correctly(self):
        with (patch('services.user_services.find_by_email') as mock_find_by_email,
              patch('security.password_hashing.get_password_hash') as mock_password_hash):
            mock_find_by_email.return_value = User(id=ID, email=EMAIL, username=USERNAME, password=PASSWORD)

            mock_password_hash.return_value = PASSWORD

            result = try_login(EMAIL, PASSWORD)

            self.assertIsInstance(result, User)
            self.assertEqual(result.id, ID)
            self.assertEqual(result.email, EMAIL)
            self.assertEqual(result.username, USERNAME)
            self.assertEqual(result.password, PASSWORD)

    @patch('services.user_services.find_by_email')
    @patch('security.password_hashing.get_password_hash')
    def test_try_login_failed_when_hashed_password_is_None(self, mock_hashed_password, mock_find_by_email):
        mock_find_by_email.return_value = User(id=ID, email=EMAIL, username=USERNAME, password=PASSWORD)
        mock_hashed_password.return_value = None

        result = try_login(EMAIL, PASSWORD)

        self.assertIsNone(result)

    @patch('services.user_services.find_by_email')
    @patch('security.password_hashing.get_password_hash')
    def test_try_login_failed_when_find_by_email_is_None(self, mock_hashed_password, mock_find_by_email):
        mock_find_by_email.return_value = None
        mock_hashed_password.return_value = PASSWORD

        result = try_login(EMAIL, PASSWORD)

        self.assertIsNone(result)

    @patch('services.user_services.find_by_email')
    @patch('security.password_hashing.get_password_hash')
    def test_try_login_failed_when_both_are_None(self, mock_hashed_password, mock_find_by_email):
        mock_find_by_email.return_value = None
        mock_hashed_password.return_value = None

        result = try_login(EMAIL, PASSWORD)

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
