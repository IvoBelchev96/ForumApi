from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr, validator


class User(BaseModel):
    id: int | None
    email: str
    username: str
    password: str
    is_admin: bool = False

    @classmethod
    def from_query_result(cls, id, email, username, password):
        return cls(
            id=id,
            email=email,
            username=username,
            password=password
        )


class Topic(BaseModel):
    topic_name: str
    category_id: int
    user_id: int
    best_reply_id: Optional[int] = None
    is_locked: Optional[bool] = False

    @validator('topic_name')
    def topic_name_must_not_be_empty(cls, value):
        if not value or not value.strip():
            raise ValueError('Topic name must not be empty')
        return value
