from unittest import TestCase

from unittest.mock import patch

from fastapi import HTTPException
from fastapi.testclient import TestClient
from pydantic import ValidationError

from data.schemas import ReplyOut, UpdateReply
from main import app
from routers.replies import update_vote_on_reply

REPLY_CONTENT = 'This is a reply'
USER_ID = 1
ACCESS_TOKEN = 'access_token'


class TestRepliesRouter(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('routers.replies.authorization.get_current_user', return_value=USER_ID)
    @patch('routers.replies.reply_services.create',
           return_value=ReplyOut(id=1, content=REPLY_CONTENT, topic_id=1, created_at="2022-01-01 00:00:00"))
    def test_create_reply_success(self, mock_create_reply, mock_get_current_user):
        response = self.client.post('/create', json={'content': REPLY_CONTENT, 'topic_id': 1, 'category_id': 1},
                                    headers={'Authorization': f'Bearer {ACCESS_TOKEN}'})
        self.assertEqual(response.status_code, 201)

    @patch('routers.replies.authorization.get_current_user', return_value=None)
    def test_create_reply_no_current_user(self, mock_get_current_user):
        response = self.client.post('/', json={'content': REPLY_CONTENT},
                                    headers={'Authorization': f'Bearer {ACCESS_TOKEN}'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['detail'], "Not Found")

    @patch('routers.replies.authorization.get_current_user', return_value=USER_ID)
    @patch('routers.replies.reply_services.create', return_value=None)
    def test_create_reply_failed(self, mock_create_reply, mock_get_current_user):
        response = self.client.post('/', json={'content': REPLY_CONTENT},
                                    headers={'Authorization': f'Bearer {ACCESS_TOKEN}'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['detail'], "Not Found")

    @patch('routers.replies.authorization.get_current_user', return_value=USER_ID)
    def test_create_reply_no_body(self, mock_get_current_user):
        response = self.client.post('/', headers={'Authorization': f'Bearer {ACCESS_TOKEN}'})
        self.assertEqual(response.status_code, 404)

    @patch('routers.replies.authorization.get_current_user', return_value=None)
    def test_update_vote_on_reply_no_user(self, mock_get_current_user):
        update_reply = UpdateReply(reply_id=1, status='upvote')
        with self.assertRaises(HTTPException) as context:
            update_vote_on_reply(update_reply)
        self.assertEqual(context.exception.status_code, 400)

    @patch('routers.replies.authorization.get_current_user', return_value=1)
    @patch('routers.replies.reply_services.change_vote_status', return_value=None)
    def test_update_vote_on_reply_no_update(self, mock_change_vote_status, mock_get_current_user):
        update_reply = UpdateReply(reply_id=1, status='upvote')
        with self.assertRaises(HTTPException) as context:
            update_vote_on_reply(update_reply)
        self.assertEqual(context.exception.status_code, 400)

    # Test successful vote update
    @patch('routers.replies.authorization.get_current_user', return_value=1)
    @patch('routers.replies.reply_services.change_vote_status', return_value=True)
    def test_update_vote_on_reply_success(self, mock_change_vote_status, mock_get_current_user):
        update_reply = UpdateReply(reply_id=1, status='upvote')
        response = update_vote_on_reply(update_reply)
        self.assertEqual(response, "You upvoted reply with id: 1")

    @patch('routers.replies.authorization.get_current_user', return_value=1)
    def test_update_vote_on_reply_no_reply_id(self, mock_get_current_user):
        with self.assertRaises(ValidationError):
            update_reply = UpdateReply(reply_id=None, status='upvote')

    @patch('routers.replies.authorization.get_current_user', return_value=1)
    def test_update_vote_on_reply_no_status(self, mock_get_current_user):
        with self.assertRaises(ValidationError):
            update_reply = UpdateReply(reply_id=1, status=None)

    @patch('routers.replies.authorization.get_current_user', return_value=1)
    def test_update_vote_on_reply_invalid_status(self, mock_get_current_user):
        update_reply = UpdateReply(reply_id=1, status='invalid')
        with self.assertRaises(HTTPException) as context:
            update_vote_on_reply(update_reply)
        self.assertEqual(context.exception.status_code, 400)
