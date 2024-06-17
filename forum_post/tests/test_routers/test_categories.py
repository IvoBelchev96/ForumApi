import unittest
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient
from main import app

class TestCategoryRouter(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('services.category_services.view_all_categories')
    def test_view_all_categories(self, mock_view_all_categories):
        # Test for viewing all categories. It should return a 200 status code.
        mock_view_all_categories.return_value = []
        response = self.client.get("/categories/")
        self.assertEqual(response.status_code, 200)

    @patch('services.category_services.create')
    def test_create_category_invalid_user(self, mock_create):
        # Test for creating a category with an invalid user. It should return a 403 status code.
        mock_create.return_value = None
        response = self.client.post("/categories/create",
                                    json={'name': 'Test Category', 'is_private': False, 'is_locked': False})
        self.assertEqual(response.status_code, 403)

    @patch('services.category_services.change_visibility')
    def test_change_visibility(self, mock_change_visibility):
        # Test for changing the visibility of a category by a non-admin user. It should return a 403 status code.
        mock_change_visibility.return_value = 'not admin'
        response = self.client.put("/categories/1", json={'is_private': True, 'is_locked': False})
        self.assertEqual(response.status_code, 403)

    @patch('services.category_services.revoke_access')
    def test_revoke_user_access_invalid_access_type(self, mock_revoke_access):
        # Test for revoking access with an invalid access type. It should return a 403 status code.
        mock_revoke_access.return_value = 'invalid access type'
        response = self.client.put("/categories/revoke_access/1",
                                   json={'user_id': 1, 'access_type': 'invalid_access_type'})
        self.assertEqual(response.status_code, 403)

    @patch('services.category_services.view_privileged_users')
    def test_view_privileged_users_not_private(self, mock_view_privileged_users):
        # Test for viewing privileged users of a non-private category. It should return a 403 status code.
        mock_view_privileged_users.return_value = 'not private'
        response = self.client.get("/categories/privileged_users/1")
        self.assertEqual(response.status_code, 403)

    @patch('services.category_services.create')
    def test_create_category_existing_name(self, mock_create):
        # Test for creating a category with an existing name. It should return a 403 status code.
        mock_create.return_value = None
        response = self.client.post("/categories/create",
                                    json={'name': 'Existing Category', 'is_private': False, 'is_locked': False})
        self.assertEqual(response.status_code, 403)

    @patch('services.category_services.change_visibility')
    def test_change_visibility_non_existent_category(self, mock_change_visibility):
        # Test for changing the visibility of a non-existent category. It should return a 403 status code.
        mock_change_visibility.return_value = 'category does not exist'
        response = self.client.put("/categories/9999", json={'is_private': True, 'is_locked': False})
        self.assertEqual(response.status_code, 403)

    @patch('services.category_services.revoke_access')
    def test_revoke_user_access_no_access(self, mock_revoke_access):
        # Test for revoking access from a user who does not have access. It should return a 403 status code.
        mock_revoke_access.return_value = 'user does not have access'
        response = self.client.put("/categories/revoke_access/1",
                                   json={'user_id': 1, 'access_type': 'read'})
        self.assertEqual(response.status_code, 403)

    @patch('services.category_services.view_privileged_users')
    def test_view_privileged_users_non_private(self, mock_view_privileged_users):
        # Test for viewing privileged users of a non-private category. It should return a 403 status code.
        mock_view_privileged_users.return_value = 'category is not private'
        response = self.client.get("/categories/privileged_users/1")
        self.assertEqual(response.status_code, 403)

    @patch('services.category_services.view_all_categories')
    def test_view_all_categories_no_categories(self, mock_view_all_categories):
        # Test for viewing all categories when there are no categories. It should return a 200 status code and an empty list.
        mock_view_all_categories.return_value = []
        response = self.client.get("/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])