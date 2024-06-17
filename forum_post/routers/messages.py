from fastapi import APIRouter, status, Depends, HTTPException
from common import authorization
from data import schemas, models
from typing import List
from services import message_services

messages_router = APIRouter(prefix='/messages')


@messages_router.post('/create', status_code=status.HTTP_201_CREATED, tags=["Messages"])
def create_message(message: schemas.CreateMessage, current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")

    new_message = message_services.create_message(message.content, message.receiver_id, current_user)

    if new_message is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="The message could not be created.")

    return new_message


@messages_router.get('/conversations/{receiver_id}', tags=["Messages"])
def view_conversation(receiver_id: int, current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")
    conversation = message_services.get_conversation_with_user(receiver_id, current_user)
    if conversation == 'invalid receiver':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Receiver with id: {receiver_id} is NOT found!')
    return conversation


@messages_router.get('/conversations', tags=["Messages"])
def view_conversations(current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")
    conversations = message_services.get_conversations(current_user)
    return conversations
