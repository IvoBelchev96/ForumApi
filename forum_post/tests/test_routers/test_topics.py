import unittest
from unittest.mock import patch, Mock
from fastapi import HTTPException
from starlette import status

from data.schemas import LockTopic, TopicCreate
from routers.topics import get_all_topics, get_topic_by_id, lock_topic, create_topic


class TestTopicsRouter(unittest.TestCase):

    @patch('routers.topics.topic_services.get_all_topics')
    def test_get_all_topics_invalid_page(self, mock_get_all_topics):
        mock_get_all_topics.return_value = 'invalid page'

        with self.assertRaises(HTTPException) as context:
            get_all_topics()

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, 'Invalid page!')

    @patch('routers.topics.topic_services.get_all_topics')
    def test_get_all_topics_wrong_search_parameter(self, mock_get_all_topics):
        mock_get_all_topics.return_value = 'wrong search parameter'

        with self.assertRaises(HTTPException) as context:
            get_all_topics()

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Topic 'search' parameter is wrong, try with existing topic name!")

    @patch('routers.topics.topic_services.get_all_topics')
    def test_get_all_topics_wrong_sort_parameter(self, mock_get_all_topics):

        mock_get_all_topics.return_value = 'wrong sort parameter'

        with self.assertRaises(HTTPException) as context:
            get_all_topics()

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Topic 'sort' parameter is wrong, try 'asc' or 'desc'")

    @patch('routers.topics.topic_services.get_all_topics')
    def test_get_all_topics_successful(self, mock_get_all_topics):
        mock_get_all_topics.return_value = 'Some result'

        result = get_all_topics()

        self.assertEqual(result, 'Some result')

    @patch('routers.topics.topic_services.get_topic_by_id')
    def test_get_topic_by_id_wrong_id(self, mock_get_topic_by_id):
        mock_get_topic_by_id.return_value = 'wrong topic id'

        with self.assertRaises(HTTPException) as context:
            get_topic_by_id(1)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Topic with id: wrong topic id does not exist!")

    @patch('routers.topics.topic_services.get_topic_by_id')
    def test_get_topic_by_id_successful(self, mock_get_topic_by_id):
        mock_get_topic_by_id.return_value = 'Some result'

        result = get_topic_by_id(1)

        self.assertEqual(result, 'Some result')

    @patch('routers.topics.authorization.get_current_user')
    def test_lock_topic_not_authenticated(self, mock_get_current_user):
        mock_get_current_user.return_value = None

        with self.assertRaises(HTTPException) as context:
            lock_topic(1, LockTopic(is_locked=True))

        self.assertEqual(context.exception.status_code, 403)
        self.assertEqual(context.exception.detail, "Only admins can change lock status on topic!")

    @patch('routers.topics.authorization.get_current_user')
    @patch('routers.topics.topic_services.lock_topic')
    def test_lock_topic_not_admin(self, mock_lock_topic, mock_get_current_user):
        mock_get_current_user.return_value = 1
        mock_lock_topic.return_value = 'not admin'

        with self.assertRaises(HTTPException) as context:
            lock_topic(1, LockTopic(is_locked=True))

        self.assertEqual(context.exception.status_code, 403)
        self.assertEqual(context.exception.detail, "Only admins can change lock status on topic!")

    @patch('routers.topics.authorization.get_current_user')
    @patch('routers.topics.topic_services.lock_topic')
    def test_lock_topic_not_valid_topic(self, mock_lock_topic, mock_get_current_user):
        mock_get_current_user.return_value = 1
        mock_lock_topic.return_value = 'not valid topic'

        with self.assertRaises(HTTPException) as context:
            lock_topic(1, LockTopic(is_locked=True))

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Topic with id: 1 does not exist!")

    @patch('routers.topics.authorization.get_current_user')
    @patch('routers.topics.topic_services.lock_topic')
    def test_lock_topic_already_locked(self, mock_lock_topic, mock_get_current_user):
        mock_get_current_user.return_value = 1
        mock_lock_topic.return_value = 'is locked is already set'

        with self.assertRaises(HTTPException) as context:
            lock_topic(1, LockTopic(is_locked=True))

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Lock status: True is already set!")

    @patch('routers.topics.authorization.get_current_user')
    @patch('routers.topics.topic_services.lock_topic')
    def test_lock_topic_successful(self, mock_lock_topic, mock_get_current_user):
        mock_get_current_user.return_value = 1
        mock_lock_topic.return_value = 'Some result'

        result = lock_topic(1, LockTopic(is_locked=True))

        self.assertEqual(result, "Successfully update lock status: True on topic with id: 1")

    @patch('routers.topics.authorization.get_current_user')
    def test_create_topic_not_authenticated(self, mock_get_current_user):
        mock_get_current_user.return_value = None
        topic = TopicCreate(name='name', category_id=1)

        with self.assertRaises(HTTPException) as context:
            create_topic(topic, current_user=None)
        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(context.exception.detail, "User ID not found. User may not be authenticated.")

    @patch('routers.topics.authorization.get_current_user')
    @patch('routers.topics.topic_services.create')
    def test_create_topic_error(self, mock_create, mock_get_current_user):
        mock_get_current_user.return_value = 1
        mock_create.return_value = 'error'
        topic = TopicCreate(name='name', category_id=1)

        with self.assertRaises(HTTPException) as context:
            create_topic(topic)
        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(context.exception.detail, 'error')

    @patch('routers.topics.authorization.get_current_user')
    @patch('routers.topics.topic_services.create')
    def test_create_topic_invalid_category_id(self, mock_create, mock_get_current_user):
        mock_get_current_user.return_value = 1
        mock_create.return_value = None
        topic = TopicCreate(name='name', category_id=1)

        with self.assertRaises(HTTPException) as context:
            create_topic(topic)
        self.assertEqual(context.exception.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(context.exception.detail, f"No existing category with id {topic.category_id}")

    @patch('routers.topics.authorization.get_current_user')
    @patch('routers.topics.topic_services.create')
    def test_create_topic_successful(self, mock_create, mock_get_current_user):
        mock_get_current_user.return_value = 1
        mock_create.return_value = Mock(dict=Mock(return_value={'id': 'id', 'name': 'name', 'category_id': 'category_id'}))
        topic = TopicCreate(name='name', category_id=1)

        result = create_topic(topic)

        self.assertEqual(result, {'id': 'id', 'name': 'name', 'category_id': 'category_id'})