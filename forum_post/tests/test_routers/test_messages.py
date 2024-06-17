import unittest
from unittest.mock import patch

import common.authorization
import routers.messages
from fastapi.testclient import TestClient
from main import app
from routers.messages import Depends, create_message, authorization
from data.schemas import CreateMessage, Message
from common.authorization import get_current_user


def fake_function():
    return int(1)


def fake_none():
    return None


CURRENT_USER = 1
MESSAGE_ID = 1
MESSAGE_CONTENT = 'test'
MESSAGE_RECEIVER_ID = 1
MESSAGE_SENDER_ID = 2
FAKE_MESSAGE = Message(id=MESSAGE_ID, content=MESSAGE_CONTENT, receiver_id=MESSAGE_RECEIVER_ID,
                       sender_id=MESSAGE_SENDER_ID)
FAKE_ACCESS_TOKEN = 'access'


class TestMessageRouter(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_correctly(self):
        # fake authentication process
        app.dependency_overrides[common.authorization.get_current_user] = fake_function

        with (patch('services.message_services.create_message') as mocked_create_message):
            mocked_create_message.return_value = FAKE_MESSAGE

            response = self.client.post('/messages/create', json={
                "content": MESSAGE_CONTENT,
                "receiver_id": MESSAGE_RECEIVER_ID
            })

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.json(),
                             {'id': 1, 'created_at': None, 'content': 'test', 'receiver_id': 1, 'sender_id': 2})

    def test_create_failed_not_authenticated_user(self):
        # fake authentication process
        app.dependency_overrides[authorization.get_current_user] = fake_none

        with (patch('services.message_services.create_message') as mocked_create_message):
            mocked_create_message.return_value = FAKE_MESSAGE

            response = self.client.post('/messages/create', json={
                "content": MESSAGE_CONTENT,
                "receiver_id": MESSAGE_RECEIVER_ID
            })

            self.assertEqual(response.status_code, 403)

    def test_create_failed_when_message_is_none(self):
        # fake authentication process
        app.dependency_overrides[common.authorization.get_current_user] = fake_function

        with (patch('services.message_services.create_message') as mocked_create_message):
            mocked_create_message.return_value = None

            response = self.client.post('/messages/create', json={
                "content": MESSAGE_CONTENT,
                "receiver_id": MESSAGE_RECEIVER_ID
            })

            self.assertEqual(response.status_code, 500)