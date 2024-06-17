from datetime import datetime

from mariadb import IntegrityError

from data.database_queries import insert_query, read_query, update_query
from data.schemas import UserReply, ReplyOut


def create(content: str, topic_id: int, user_id: int, category_id):
    topic_data = read_query('select id from topic where id = ?', (topic_id,))
    category_data = read_query('select id from category where id=?', (category_id,))
    if not topic_data and not category_data:
        return 'invalid topic and category'
    elif not topic_data:
        return 'invalid topic'
    elif not category_data:
        return 'invalid category'

    check_user_access = read_query('SELECT access_type from category_has_user WHERE user_id = ? AND category_id = ?',
                                   (user_id, category_id))
    if not check_user_access:
        return None

    user_access = check_user_access[0][0]

    if user_access == 'read access':
        return f"user with id {user_id} has read only access"

    if user_access == "banned":
        return f"user with id {user_id} is banned."

    generated_id = insert_query(
        'INSERT INTO reply(content, topic_id) VALUES (?, ?)',
        (content, topic_id))

    insert_query(
        'INSERT INTO votes(user_id, reply_id) VALUES (?, ?)', (user_id, generated_id))

    created_at_result = read_query('SELECT created_at FROM reply WHERE id = ?', (generated_id,))
    created_at = created_at_result[0][0].strftime("%Y-%m-%d %H:%M:%S")

    return ReplyOut(id=generated_id, content=content, topic_id=topic_id, created_at=created_at)


def change_vote_status(reply_id, vote_status, current_user_id):
    if reply_id is None or vote_status is None or current_user_id is None:
        return None

    if vote_status not in ['upvote', 'downvote']:
        return None
    try:
        # Check if the user has already voted on this reply
        existing_vote_data = read_query('SELECT status FROM votes WHERE reply_id = ? AND user_id = ?',
                                        (reply_id, current_user_id))
        existing_vote = existing_vote_data[0][0]
        if existing_vote:
            # If an existing vote is found, update it
            if existing_vote != vote_status:
                vote_data = update_query('UPDATE votes SET status = ? WHERE reply_id = ? AND user_id = ?',
                                         (vote_status, reply_id, current_user_id))
                if vote_data:
                    return True
                else:
                    return False
            else:
                return None
        else:
            vote_data = update_query('update votes set status = ? where reply_id = ? and user_id = ?',
                                     (vote_status, reply_id, current_user_id))
            if vote_data:
                return True
            else:
                return False
    except Exception as e:
        return False
