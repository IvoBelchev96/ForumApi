from data.database_queries import insert_query, update_query, read_query
from data.schemas import CreateCategory, CategoryOut, ViewCategory, ViewTopicsInCategory, ChangeCategoryVisibility, \
    ViewPrivilegedUser


def view_all_categories():
    category_data = read_query('select id,name,created_at from category')
    return (ViewCategory(id=id, name=name, created_at=created_at) for id, name, created_at in category_data)


def view_topics_in_category(category_id: int, current_user, search: str = None, sort: str = None, pagination: int = 0):
    if pagination > 0:
        page_size = 10
        pages_offset = (pagination - 1) * page_size
    else:
        page_size = 10
        pages_offset = 0
    category_data = read_query('select id,is_private from category where id=?',
                               sql_params=(category_id,))

    category_has_user_data = read_query(
        'select access_type from category_has_user where category_id = ? and user_id = ?',
        (category_id, current_user,))

    if not category_has_user_data:
        return 'invalid user'

    user_access = category_has_user_data[0][0]

    if user_access == 'banned':
        return 'banned user'

    # check if category_data with this id exists
    if not category_data:
        return f'Category with id: {category_id} does not exist!'

    topics = read_query('select id,topic_name,category_id,created_at from topic where category_id=? limit ? offset ?',
                        sql_params=(category_id, page_size, pages_offset,))

    is_private = category_data[0][1]

    # check if page exists
    if not topics:
        return f'invalid page'

    if search:
        topics = read_query(
            'select id,topic_name,category_id,created_at from topic where category_id=? and topic_name = ?',
            sql_params=(category_id, search,))  # if search parameter value is wrong -> return empty list
        if not topics:  # if list is empty -> return 'wrong search parameter'
            return 'wrong search parameter'

    if sort:
        if 'asc' in sort or 'desc' in sort:
            reverse = 'desc' in sort
            topics = sorted(topics, key=lambda t: t[3], reverse=reverse)
        else:  # if sort parameter value is wrong -> return 'wrong sort parameter'
            return 'wrong sort parameter'

    return (ViewTopicsInCategory(topic_id=id, topic_name=topic_name, category_id=category_id, created_at=created_at) for
            id, topic_name, category_id, created_at in topics)


def create(name: str, is_private: bool, is_locked: bool, current_user: int):
    admin_data = read_query('select is_admin from user where id=?', (current_user,))
    is_admin = admin_data[0][0]

    if not is_admin:
        return 'not admin'

    generated_id = insert_query(
        'INSERT INTO category(name, is_private, is_locked) VALUES(?, ?, ?)',
        (name, is_private, is_locked))

    # insert creator of category and category_id into junction table category_has_user
    insert_query('insert into category_has_user (category_id, user_id) values (?,?)',
                 (generated_id, current_user,))

    created_at_result = read_query('SELECT created_at FROM category WHERE id = ?', (generated_id,))
    created_at = created_at_result[0][0].strftime("%Y-%m-%d %H:%M:%S")

    return CategoryOut(id=generated_id, name=name, is_private=is_private, is_locked=is_locked, created_at=created_at)


def update_category(category_id: int, is_private: bool, is_locked: bool) -> bool:
    category_data = update_query(
        'UPDATE category SET is_private = ?, is_locked = ? WHERE id = ?',
        (is_private, is_locked, category_id))

    if category_data:
        return True
    else:
        return False


def change_visibility(category_id: int, is_private: bool, is_locked: bool, current_user: int):
    admin_data = read_query('select is_admin from user where id=?', (current_user,))
    is_admin = admin_data[0][0]
    if not is_admin:
        return 'not admin'
    old_category_data = read_query('SELECT is_private, is_locked FROM category WHERE id = ?', (category_id,))
    if not old_category_data:
        return None
    old_is_private, old_is_locked = old_category_data[0]
    category_visibility = update_category(category_id, is_private, is_locked)  # return True or False

    return {
        'visibility_changed': old_is_private != is_private,
        'lock_status_changed': old_is_locked != is_locked,
        'update_successful': category_visibility
    }


def revoke_access(category_id: int, user_id: int, access_type: str, current_user: int):
    is_admin_data = read_query('select is_admin from user where id= ?', (current_user,))
    is_admin = is_admin_data[0][0]
    if not is_admin:
        return 'not admin'

    access_type_params = ['read access', 'read and write access', 'banned']

    if access_type not in access_type_params:
        return 'invalid access type'

    # Add the user to the category
    add_member_result = add_category_member(category_id, user_id, access_type)
    if add_member_result != 'User added to category successfully':
        return add_member_result

    change_user_access_type_data = update_query(
        'update category_has_user set access_type = ? where category_id = ? and user_id = ?',
        (access_type, category_id, user_id))

    if not change_user_access_type_data:
        return 'invalid access'

    access_type_data = read_query('select access_type from category_has_user where category_id = ? and user_id = ?',
                                  (category_id, user_id,))
    access_type = access_type_data[0][0]

    return access_type


# def give_read_access(category_id: int, user_id: int, current_user: int):
#     admin_data = read_query('select is_admin from user where id=?', (current_user,))
#     is_admin = admin_data[0][0]
#     if not is_admin:
#         return "not admin"
#
#     access_type = 'read access'
#     add_member_result = add_category_member((category_id, user_id, access_type))
#     if add_member_result != 'User added to category successfully':
#         return add_member_result
#
#     return revoke_access(category_id, user_id, access_type)
#
#
# def give_write_access(category_id: int, user_id: int, current_user: int):
#     admin_data = read_query('select is_admin from user where id=?', (current_user,))
#     is_admin = admin_data[0][0]
#     if not is_admin:
#         return "not admin"
#
#     access_type = 'write access'
#     add_member_result = add_category_member((category_id, user_id, access_type))
#     if add_member_result != 'User added to category successfully':
#         return add_member_result
#
#     return revoke_access(category_id, user_id, access_type)


def add_category_member(category_id: int, user_id: int, access_type: str):
    # check if the user is already a member of the category
    existing_member_data = read_query('select * from category_has_user where category_id=? and user_id=?',
                                      (category_id, user_id,))
    if existing_member_data:
        # if the user is already a member, update their access type
        update_query('update category_has_user set access_type=? where category_id=? and user_id=?',
                     (access_type, category_id, user_id))
        return 'User access type updated successfully'

    # if the user is not a member, add them to the category
    add_member_data = update_query('insert into category_has_user (category_id, user_id, access_type) values (?, ?, ?)',
                                   (category_id, user_id, access_type))
    if not add_member_data:
        return 'Failed to add user to category'

    return 'User added to category successfully'


def view_privileged_users(category_id: int, current_user: int):
    # check if user is admin
    is_admin_data = read_query('select is_admin from user where id = ?', (current_user,))
    if not is_admin_data:
        return 'invalid user id'

    is_admin = is_admin_data[0][0]

    if not is_admin:
        return 'not admin'

    # check if category is private
    is_private_data = read_query('select is_private from category where id = ?', (category_id,))
    if not is_private_data:
        return 'invalid category'

    is_private = is_private_data[0][0]

    if not is_private:
        return 'not private'

    category_has_user_data = read_query('select user_id, access_type from category_has_user where category_id = ?',
                                        (category_id,))

    # get users_ids and their access_type from current category
    users_ids = [u[0] for u in category_has_user_data]
    access_types = [a[1] for a in category_has_user_data]
    users_usernames = []

    # create list of usernames from users_ids
    for user_id in users_ids:
        users_usernames_data = read_query('select username from user where id = ?', (user_id,))
        users_usernames.append(users_usernames_data[0][0])

    return (ViewPrivilegedUser(username=username, access_type=access_type) for username, access_type in
            zip(users_usernames, access_types))
