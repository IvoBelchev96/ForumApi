import unittest
from datetime import datetime
from unittest.mock import patch
from services.reply_services import create, change_vote_status, ReplyOut


class TestReplyServices(unittest.TestCase):
    @patch('services.reply_services.read_query')
    @patch('services.reply_services.insert_query')
    def test_create(self, mock_insert_query, mock_read_query):
        content = "test content"
        topic_id = 1
        user_id = 1
        category_id = 1
        access_type = 'write access'
        generated_id = 1
        created_at = datetime.strptime("2024-05-09 00:00:00", "%Y-%m-%d %H:%M:%S")

        mock_read_query.side_effect = [[(access_type,)], [(created_at,)]]
        mock_insert_query.side_effect = [generated_id, None]

        result = create(content, topic_id, user_id, category_id)

        expected_result = ReplyOut(id=generated_id, content=content, topic_id=topic_id, created_at=created_at)
        self.assertEqual(result, expected_result)

    @patch('services.reply_services.read_query')
    @patch('services.reply_services.insert_query')
    def test_create_with_write_access(self, mock_insert_query, mock_read_query):
        content = "test content"
        topic_id = 1
        user_id = 1
        category_id = 1
        access_type = 'read and write access'
        generated_id = 1
        created_at = datetime.strptime("2024-05-09 00:00:00", "%Y-%m-%d %H:%M:%S")

        mock_read_query.side_effect = [[(access_type,)], [(created_at,)]]
        mock_insert_query.side_effect = [generated_id, None]

        result = create(content, topic_id, user_id, category_id)

        expected_result = ReplyOut(id=generated_id, content=content, topic_id=topic_id,
                                   created_at=created_at.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(result, expected_result)

    @patch('services.reply_services.read_query')
    @patch('services.reply_services.insert_query')
    def test_create_with_query_exception(self, mock_insert_query, mock_read_query):
        content = "test content"
        topic_id = 1
        user_id = 1
        category_id = 1

        mock_read_query.side_effect = Exception
        mock_insert_query.side_effect = Exception

        with self.assertRaises(Exception):
            create(content, topic_id, user_id, category_id)

    @patch('services.reply_services.read_query')
    @patch('services.reply_services.insert_query')
    def test_create_with_empty_query_result(self, mock_insert_query, mock_read_query):
        content = "test content"
        topic_id = 1
        user_id = 1
        category_id = 1

        mock_read_query.side_effect = [[], []]
        mock_insert_query.side_effect = [None, None]

        result = create(content, topic_id, user_id, category_id)

        self.assertIsNone(result)

    @patch('services.reply_services.read_query')
    @patch('services.reply_services.update_query')
    @patch('services.reply_services.insert_query')
    def test_change_vote_status_with_none_values(self, mock_insert_query, mock_update_query, mock_read_query):
        reply_id = None
        vote_status = 'upvote'
        current_user_id = 1

        result = change_vote_status(reply_id, vote_status, current_user_id)
        self.assertIsNone(result)

        reply_id = 1
        vote_status = None
        current_user_id = 1

        result = change_vote_status(reply_id, vote_status, current_user_id)
        self.assertIsNone(result)

        reply_id = 1
        vote_status = 'upvote'
        current_user_id = None

        result = change_vote_status(reply_id, vote_status, current_user_id)
        self.assertIsNone(result)

    @patch('services.reply_services.read_query')
    @patch('services.reply_services.update_query')
    @patch('services.reply_services.insert_query')
    def test_change_vote_status_with_invalid_vote_status(self, mock_insert_query, mock_update_query, mock_read_query):
        reply_id = 1
        vote_status = 'not a valid vote status'
        current_user_id = 1

        result = change_vote_status(reply_id, vote_status, current_user_id)
        self.assertIsNone(result)

    @patch('services.reply_services.read_query')
    @patch('services.reply_services.update_query')
    @patch('services.reply_services.insert_query')
    def test_change_vote_status_when_user_already_voted_same_status(self, mock_insert_query, mock_update_query,
                                                                    mock_read_query):
        reply_id = 1
        vote_status = 'upvote'
        current_user_id = 1

        mock_read_query.return_value = [{'status': 'upvote'}]

        result = change_vote_status(reply_id, vote_status, current_user_id)
        self.assertIsNone(result)

    @patch('services.reply_services.read_query')
    @patch('services.reply_services.update_query')
    def test_change_vote_status_when_user_already_voted_different_status(self, mock_update_query,
                                                                         mock_read_query):
        reply_id = 1
        vote_status = 'downvote'
        current_user_id = 1

        mock_read_query.return_value = [{'status': 'upvote'}]
        mock_update_query.return_value = True

        result = change_vote_status(reply_id, vote_status, current_user_id)
        self.assertTrue(result)

    @patch('services.reply_services.read_query')
    @patch('services.reply_services.insert_query')
    def test_change_vote_status_when_user_has_not_voted(self, mock_insert_query, mock_read_query):
        reply_id = 1
        vote_status = 'upvote'
        current_user_id = 1

        mock_read_query.return_value = None
        mock_insert_query.return_value = False

        result = change_vote_status(reply_id, vote_status, current_user_id)
        self.assertTrue(result)