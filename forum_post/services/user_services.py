from mariadb import IntegrityError

import security.password_hashing
from data.database_queries import insert_query, read_query
from data.models import User


def create(email: str, username: str, password: str) -> User | None:

    try:
        generated_id = insert_query(
            'insert into user(email, username, password) values(?, ?, ?)',
            (email, username, password))

        return User(id=generated_id, email=email, username=username, password='')

    except IntegrityError:
        return None


def find_by_email(email: str) -> User | None:
    data = read_query(
        'SELECT id, email, username, password FROM user WHERE email = ?',
        (email,))

    return next((User.from_query_result(*row) for row in data), None)


def try_login(email: str, password: str) -> User | None:
    user = find_by_email(email)
    hashed_pass = security.password_hashing.get_password_hash(password)
    return user if user and user.password == hashed_pass else None