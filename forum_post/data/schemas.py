from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str


class TopicCreate(BaseModel):
    name: str
    category_id: int



class Topic(BaseModel):
    topic_name: str
    category_id: int
    created_at: Optional[datetime] = None
    best_reply_id: Optional[int] = None


class CreateCategory(BaseModel):
    name: str
    is_private: Optional[bool] = None
    is_locked: Optional[bool] = None


class CategoryOut(CreateCategory):
    name: str
    id: int
    created_at: str


class ViewCategory(BaseModel):
    id: int
    name: str
    created_at: datetime


class ViewTopicsInCategory(BaseModel):
    topic_id: int
    topic_name: str
    category_id: int
    created_at: datetime


class ViewTopic(BaseModel):
    id: int
    topic_name: str
    category_id: int
    created_at: datetime


class ViewReply(BaseModel):
    id: int
    content: str
    created_at: datetime


class CreateReply(BaseModel):
    category_id: int
    content: str
    topic_id: int



class ReplyOut(BaseModel):
    content: str
    topic_id: int
    created_at: datetime


class UserReply(BaseModel):
    user_id: int
    reply_id: int


class UpdateReply(BaseModel):
    reply_id: int
    status: str


class CreateMessage(BaseModel):
    content: str
    receiver_id: int


class Message(BaseModel):
    id: int
    created_at: Optional[datetime] = None
    content: str
    receiver_id: int
    sender_id: int


class BestReply(BaseModel):
    best_reply_id: int


class ChangeCategoryVisibility(BaseModel):
    is_private: bool
    is_locked: bool


class ViewConversation(BaseModel):
    id: int
    created_at: datetime
    content: str
    receiver_id: int
    sender_id: int

    @classmethod
    def from_query_result(cls, id, created_at, content, receiver_id, sender_id):
        return cls(
            id=id,
            created_at=created_at,
            content=content,
            receiver_id=receiver_id,
            sender_id=sender_id
        )


class RevokeAccess(BaseModel):
    user_id: int
    access_type: str


class Access(BaseModel):
    access_type: str

class LockTopic(BaseModel):
    is_locked:bool

class ViewPrivilegedUser(BaseModel):
    username: str | None
    access_type: str | None
