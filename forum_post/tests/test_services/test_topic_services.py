import unittest
from unittest.mock import patch
from services.topic_services import get_all_topics, get_topic_by_id, category_exists, create, update_best_reply, \
    lock_topic


class TestTopicServices(unittest.TestCase):
    @patch('services.topic_services.read_query')
    def test_get_all_topics(self, mock_read_query):
        mock_read_query.return_value = []
        result = get_all_topics()
        self.assertEqual(result, 'invalid page')

    @patch('services.topic_services.read_query')
    def test_get_topic_by_id(self, mock_read_query):
        mock_read_query.return_value = []
        result = get_topic_by_id(1)
        self.assertEqual(result, 'wrong topic id')

    @patch('services.topic_services.read_query')
    def test_category_exists(self, mock_read_query):
        mock_read_query.return_value = None
        result = category_exists(1)
        self.assertEqual(result, False)

    @patch('services.topic_services.read_query')
    @patch('services.topic_services.insert_query')
    def test_create(self, mock_insert_query, mock_read_query):
        mock_read_query.return_value = []
        result = create('topic', 1, 1)
        self.assertEqual(result, "No existing category with id 1")

    @patch('services.topic_services.update_query')
    def test_update_best_reply(self, mock_update_query):
        mock_update_query.return_value = None
        result = update_best_reply(1, 1, 1)
        self.assertEqual(result, None)

    @patch('services.topic_services.read_query')
    @patch('services.topic_services.update_query')
    def test_lock_topic(self, mock_update_query, mock_read_query):
        mock_read_query.return_value = []
        result = lock_topic(1, True, 1)
        self.assertEqual(result, 'not admin')

    @patch('services.topic_services.update_query')
    def test_update_best_reply_unsuccessful(self, mock_update_query):
        mock_update_query.return_value = None

        result = update_best_reply(1, 1, 1)

        self.assertIsNone(result)
        mock_update_query.assert_called_once_with('update topic set best_reply_id=? where id = ? and user_id = ?',
                                                  (1, 1, 1))

    @patch('services.topic_services.update_query')
    def test_update_best_reply_successful(self, mock_update_query):
        mock_update_query.return_value = 'Some result'

        result = update_best_reply(2, 2, 2)

        self.assertEqual(result, 'Some result')
        mock_update_query.assert_called_once_with('update topic set best_reply_id=? where id = ? and user_id = ?',
                                                  (2, 2, 2))

    @patch('services.topic_services.read_query')
    def test_lock_topic_not_admin(self, mock_read_query):
        mock_read_query.return_value = None

        result = lock_topic(1, True, 1)

        self.assertEqual(result, 'not admin')
        mock_read_query.assert_called_once_with('select is_admin from user where id = ?', (1,))

    @patch('services.topic_services.read_query')
    def test_lock_topic_not_valid_topic(self, mock_read_query):
        mock_read_query.side_effect = [[(True,)], None]

        result = lock_topic(1, True, 1)

        self.assertEqual(result, 'not valid topic')
        mock_read_query.assert_any_call('select is_locked from topic where id = ?', (1,))

    @patch('services.topic_services.read_query')
    def test_lock_topic_already_locked(self, mock_read_query):
        mock_read_query.side_effect = [[(True,)], [(True,)]]

        result = lock_topic(1, True, 1)

        self.assertEqual(result, 'is locked is already set')

    @patch('services.topic_services.read_query')
    @patch('services.topic_services.update_query')
    def test_lock_topic_update_unsuccessful(self, mock_update_query, mock_read_query):
        mock_read_query.side_effect = [[(True,)], [(False,)]]
        mock_update_query.return_value = None

        result = lock_topic(1, True, 1)

        self.assertEqual(result, 'not valid topic')

    @patch('services.topic_services.read_query')
    @patch('services.topic_services.update_query')
    def test_lock_topic_update_successful(self, mock_update_query, mock_read_query):
        mock_read_query.side_effect = [[(True,)], [(False,)]]
        mock_update_query.return_value = 'Some result'

        result = lock_topic(1, True, 1)

        self.assertEqual(result, 'Some result')