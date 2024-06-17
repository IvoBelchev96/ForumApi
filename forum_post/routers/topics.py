from fastapi import APIRouter, status, Depends, HTTPException

from common import authorization
from data import schemas
from services import topic_services

topics_router = APIRouter(prefix='/topics')


@topics_router.get('/', tags=["Topics"])
def get_all_topics(search: str = None, sort: str = None, pagination: int = 1):
    topics_result = topic_services.get_all_topics(search, sort, pagination)

    if topics_result == 'invalid page':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid page!')
    if topics_result == 'wrong search parameter':
        raise HTTPException(status_code=404,
                            detail=f"Topic 'search' parameter is wrong, try with existing topic name!")
    elif topics_result == 'wrong sort parameter':
        raise HTTPException(status_code=404,
                            detail=f"Topic 'sort' parameter is wrong, try 'asc' or 'desc'")

    return topics_result


@topics_router.get('/{topic_id}', tags=["Topics"])
def get_topic_by_id(topic_id: int):
    topic_result = topic_services.get_topic_by_id(topic_id)

    if topic_result == 'wrong topic id':
        raise HTTPException(status_code=404, detail=f"Topic with id: {topic_id} does not exist!")

    return topic_result


@topics_router.post('/create', status_code=status.HTTP_201_CREATED, tags=["Topics"])
def create_topic(topic: schemas.TopicCreate, current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")
    new_topic = topic_services.create(topic.name, topic.category_id, current_user)

    if isinstance(new_topic, str):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=new_topic)

    if new_topic is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No existing category with id {topic.category_id}")

    return new_topic.dict(exclude_none=True)


@topics_router.put('/{topic_id}', tags=["Topics"])
def update_best_reply(topic_id: int, best_reply: schemas.BestReply,
                      owner_id: int = Depends(authorization.get_current_user)):
    if owner_id is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")

    best_reply = topic_services.update_best_reply(topic_id, best_reply.best_reply_id, owner_id)

    if not best_reply:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Setting best reply failed!')

    return f"Best reply was set successfully on topic with id: {topic_id}!"


@topics_router.put('/lock/{topic_id}', tags=["Topics"])
def lock_topic(topic_id: int, is_locked: schemas.LockTopic,
               current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")

    lock_topic_result = topic_services.lock_topic(topic_id, is_locked.is_locked, current_user)

    if lock_topic_result == 'not admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only admins can change lock status on topic!')
    elif lock_topic_result == 'not valid topic':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Topic with id: {topic_id} does not exist!')
    elif lock_topic_result == 'is locked is already set':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Lock status: {is_locked.is_locked} is already set!')

    return f'Successfully update lock status: {is_locked.is_locked} on topic with id: {topic_id}'
