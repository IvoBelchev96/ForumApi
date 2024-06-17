import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

class TestMessageRouter(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('services.message_services.create_message')
    @patch('common.authorization.get_current_user', return_value=1)
    def test_create_message(self, mock_get_current_user, mock_create_message):
        mock_create_message.return_value = {"content": "Hello", "receiver_id": 2, "sender_id": 1}
        response = self.client.post("/messages/create", json={"content": "Hello", "receiver_id": 2})
        self.assertEqual(response.status_code, 201)

    @patch('services.message_services.get_conversation_with_user')
    @patch('common.authorization.get_current_user', return_value=1)
    def test_view_conversation(self, mock_get_current_user, mock_get_conversation_with_user):
        mock_get_conversation_with_user.return_value = [{"content": "Hello", "receiver_id": 2, "sender_id": 1}]
        response = self.client.get("/messages/conversations/2")
        self.assertEqual(response.status_code, 200)

    @patch('services.message_services.get_conversations')
    @patch('common.authorization.get_current_user', return_value=1)
    def test_view_conversations(self, mock_get_current_user, mock_get_conversations):
        mock_get_conversations.return_value = [
            {"content": "Hello", "receiver_id": 2, "sender_id": 1},
            {"content": "Hi", "receiver_id": 3, "sender_id": 1}
        ]
        response = self.client.get("/messages/conversations")
        self.assertEqual(response.status_code, 200)
