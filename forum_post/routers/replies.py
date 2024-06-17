from fastapi import APIRouter, Depends, HTTPException, status

from common import authorization
from data.schemas import UpdateReply, CreateReply
from services import reply_services

replies_router = APIRouter(prefix='/replies')


@replies_router.put('/', tags=["Replies"])
def update_vote_on_reply(update_reply: UpdateReply, current_user_id: int = Depends(authorization.get_current_user)

                         ):
    if not current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")

    reply = reply_services.change_vote_status(update_reply.reply_id, update_reply.status, current_user_id)

    if not reply:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reply vote cannot be updated!")

    return f"You {update_reply.status}d reply with id: {update_reply.reply_id}"


@replies_router.post('/create', status_code=status.HTTP_201_CREATED, tags=["Replies"])
def create_reply(reply: CreateReply, current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")
    new_reply = reply_services.create(reply.content, reply.topic_id, current_user, reply.category_id)

    if new_reply is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The reply could not be created.")
    if new_reply == 'invalid topic and category':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Topic with id:{reply.topic_id} and category with id: {reply.category_id} does '
                                   f'NOT exist!')
    elif new_reply == 'invalid topic':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Topic with id: {reply.topic_id} does NOT exist!')
    elif new_reply == 'invalid category':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Category with id: {reply.category_id} does NOT exist!')
    if isinstance(new_reply, str):
        return new_reply

    return new_reply.dict(exclude_none=True)
