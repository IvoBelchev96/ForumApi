import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from data.models import User
from main import app


ID = 1
EMAIL = 'test@test.bg'
USERNAME = 'test'
PASSWORD = 'test'
ACCESS_TOKEN = 'access_token'


class TestUserRouter(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_user_correctly(self):
        with (patch('routers.users.get_password_hash') as mock_password_hash,
              patch('services.user_services.create') as mock_create_user):
            mock_password_hash.return_value = PASSWORD
            mock_create_user.return_value = User(id=ID, email=EMAIL, username=USERNAME, password=PASSWORD)

            response = self.client.post("/users/register", json={
                "email": EMAIL,
                "username": USERNAME,
                "password": PASSWORD
            })

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json(), {"id": ID, "username": USERNAME, "email": EMAIL})

    def test_create_user_failed(self):
        with (patch('routers.users.get_password_hash') as mock_password_hash,
              patch('services.user_services.create') as mock_create_user):
            mock_password_hash.return_value = PASSWORD
            mock_create_user.return_value = None

            response = self.client.post("/users/register", json={
                "email": EMAIL,
                "username": USERNAME,
                "password": PASSWORD
            })

            self.assertEqual(response.status_code, 400)
            self.assertEqual(b"Username or email is already taken.", response.content)

    def test_login_user_correctly(self):
        with (patch('services.user_services.try_login') as mocked_try_login,
              patch('routers.users.create_access_token') as mocked_access_token,
              patch('routers.users.verify_password') as mocked_verify_password):
            mocked_try_login.return_value = User(id=ID, email=EMAIL, username=USERNAME, password=PASSWORD)
            mocked_access_token.return_value = ACCESS_TOKEN
            mocked_verify_password.return_value = True

            response = self.client.post('/users/login', json={
                "email": EMAIL,
                "password": PASSWORD
            })

            result_from_login = {"access_token": ACCESS_TOKEN, "token_type": "bearer"}

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), result_from_login)

    def test_login_user_failed_user_not_found(self):
        with (patch('services.user_services.try_login') as mocked_try_login,
              patch('routers.users.create_access_token') as mocked_access_token,
              patch('routers.users.verify_password') as mocked_verify_password):
            mocked_try_login.return_value = None
            mocked_access_token.return_value = ACCESS_TOKEN
            mocked_verify_password.return_value = True

            response = self.client.post('/users/login', json={
                "email": EMAIL,
                "password": PASSWORD
            })

            result_from_login = "Invalid Credentials"

            self.assertEqual(response.status_code, 403)
            self.assertEqual(result_from_login, response.json()['detail'])

    def test_login_user_failed_password_not_verified(self):
        with (patch('services.user_services.try_login') as mocked_try_login,
              patch('routers.users.create_access_token') as mocked_access_token,
              patch('routers.users.verify_password') as mocked_verify_password):
            mocked_try_login.return_value = User(id=ID, email=EMAIL, username=USERNAME, password=PASSWORD)
            mocked_access_token.return_value = ACCESS_TOKEN
            mocked_verify_password.return_value = False

            response = self.client.post('/users/login', json={
                "email": EMAIL,
                "password": PASSWORD
            })

            result_from_login = "Invalid Credentials"

            self.assertEqual(response.status_code, 403)
            self.assertEqual(result_from_login, response.json()['detail'])


if __name__ == '__main__':
    unittest.main()
