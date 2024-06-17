from mariadb import IntegrityError

from data.database_queries import insert_query, read_query, update_query
from data.models import Topic
from data.schemas import TopicCreate, ViewTopic, ViewReply


def get_all_topics(search: str = None, sort: str = None, pagination: int = 1):
    page_size = 10
    pages_offset = (pagination - 1) * page_size

    topics_data = read_query('select id,topic_name,category_id,created_at from topic limit ? offset ?',
                             (page_size, pages_offset,))

    if not topics_data:
        return 'invalid page'

    if search:
        topics_data = read_query('select id,topic_name,category_id,created_at from topic where topic_name = ?',
                                 sql_params=(search,))
        if not topics_data:
            return 'wrong search parameter'

    if sort:
        if 'asc' in sort or 'desc' in sort:
            reverse = 'desc' in sort
            topics_data = sorted(topics_data, key=lambda t: t[3], reverse=reverse)
        else:  # if sort parameter value is wrong -> return 'wrong sort parameter'
            return 'wrong sort parameter'

    return (ViewTopic(id=id, topic_name=topic_name, category_id=category_id, created_at=created_at) for
            id, topic_name, category_id, created_at in topics_data)


def get_topic_by_id(id: int):
    topic_data = read_query('select id,topic_name,category_id,created_at,user_id from topic where id=?',
                            sql_params=(id,))

    if not topic_data:
        return 'wrong topic id'

    topic_user_creator_data = read_query('select username from user where id=?', sql_params=(topic_data[0][4],))
    topic_user_creator = str(topic_user_creator_data[0][0])

    reply_data = read_query('select id, content, created_at from reply where topic_id = ?', sql_params=(id,))
    replies = (ViewReply(id=id, content=content, created_at=created_at) for id, content, created_at in reply_data)

    if not reply_data:  # check if the current topic has replies, if not, return 'no replies' as result in JSON response
        replies = 'no replies'

    topics = {
        "id": topic_data[0][0],
        "topic_name": topic_data[0][1],
        "category_id": topic_data[0][2],
        "created_at": topic_data[0][3],
        "creator": topic_user_creator,
        "creator_id": topic_data[0][4],
        "replies": replies
    }

    return topics


def category_exists(category_id: int) -> bool:
    result = read_query('SELECT id FROM category WHERE id = ?', (category_id,))
    return result is not None


def create(topic_name: str, category_id: int, user_id: int) -> Topic | None:
    check_category = read_query('SELECT is_locked from category WHERE id = ?', (category_id,))
    if not check_category:
        return f"No existing category with id {category_id}"
    category_status = check_category[0][0]

    if category_status:
        return f"New topic cannot be created. The category is locked"

    generated_id = insert_query(
        'INSERT INTO topic(topic_name, category_id, user_id) VALUES (?, ?, ?)',
        (topic_name, category_id, user_id))
    return Topic(id=generated_id, topic_name=topic_name, category_id=category_id, user_id=user_id,
                 best_reply_id=None)


def update_best_reply(topic_id: int, reply_id: int, owner_id: int):
    reply_data = update_query('update topic set best_reply_id=? where id = ? and user_id = ?',
                              (reply_id, topic_id, owner_id))

    return reply_data


def lock_topic(topic_id: int, is_locked: bool, current_user: int):
    admin_data = read_query('select is_admin from user where id = ?', (current_user,))
    is_admin = admin_data[0][0]

    # check if current user is admin
    if is_admin == 0:
        return 'not admin'

    # check if is_locked attribute exists
    is_locked_topic_data = read_query('select is_locked from topic where id = ?', (topic_id,))

    if not is_locked_topic_data:
        return 'not valid topic'

    is_locked_topic = is_locked_topic_data[0][0]

    # check if current topic lock status is already set. For example: if is_locked is true on current topic,
    # and we try to set it again to true, it will return "is locked is already set"

    if is_locked_topic == is_locked:
        return 'is locked is already set'

    lock_topic_data = update_query('update topic set is_locked = ? where id = ?', (is_locked, topic_id,))

    if not lock_topic_data:
        return 'not valid topic'

    return lock_topic_data
