from fastapi import APIRouter, status, Depends, HTTPException

from common import authorization
from data import schemas
from data.schemas import CreateCategory, ChangeCategoryVisibility, RevokeAccess, Access
from services import category_services

# from services.category_services import give_read_access, give_write_access

categories_router = APIRouter(prefix='/categories')


@categories_router.get('/', tags=["Categories"])
def view_all_categories():
    categories = category_services.view_all_categories()
    return categories


@categories_router.get('/{category_id}', tags=["Categories"])
def view_category(category_id: int, search: str = None, sort: str = None, pagination: int = 0,
                  current_user: int = Depends(authorization.get_current_user)):
    category_with_topics = category_services.view_topics_in_category(category_id, current_user, search, sort,
                                                                     pagination)

    if not category_with_topics:
        raise HTTPException(status_code=404, detail=category_with_topics)
    elif category_with_topics == 'banned user':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'User is banned from category with id: {category_id}')
    elif category_with_topics == 'invalid user':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id: {current_user} is not a member of this category!')
    elif category_with_topics == 'invalid page':
        raise HTTPException(status_code=404, detail='Invalid page!')
    elif category_with_topics == 'wrong search parameter':
        raise HTTPException(status_code=404, detail=f"Topic with name: '{search}' does not exist!")
    elif category_with_topics == 'wrong sort parameter':
        raise HTTPException(status_code=404, detail=f"Sort parameter: '{sort}' is wrong, try 'desc' or 'asc'")

    return category_with_topics


@categories_router.post('/create', status_code=status.HTTP_201_CREATED, tags=["Categories"])
def create_category(category: CreateCategory, current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")
    new_category = category_services.create(category.name, category.is_private, category.is_locked, current_user)

    if new_category is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="The topic could not be created.")
    elif new_category == 'not admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Creating a category requires ADMIN access!")

    return new_category.dict(exclude_none=True)


@categories_router.put('/{category_id}', tags=["Categories"])
def change_visibility(category_id: int, change_category: schemas.ChangeCategoryVisibility,
                      current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")

    category_visibility = category_services.change_visibility(category_id, change_category.is_private,
                                                              change_category.is_locked,
                                                              current_user)
    if not category_visibility:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Cannot change category visibility!')
    elif category_visibility == 'not admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only ADMIN users can change category visibility!')

    messages = []
    if category_visibility['visibility_changed']:
        messages.append('Visibility status changed.')
    if category_visibility['lock_status_changed']:
        messages.append('Lock status changed.')
    if not messages:
        messages.append('No changes were made.')

    return ' '.join(messages)


@categories_router.put('/revoke_access/{category_id}', tags=["Categories"])
def revoke_user_access(category_id: int, revoke_access: RevokeAccess,
                       current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")

    revoke_access_result = category_services.revoke_access(category_id, revoke_access.user_id,
                                                           revoke_access.access_type, current_user)
    if not revoke_access_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid operation!')
    elif revoke_access_result == 'invalid access type':
        available_access_types = 'read access, read and write access or banned'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Invalid access type, try: {available_access_types}!')
    elif revoke_access_result == 'not admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='ONLY ADMIN can change user category access!')
    return f'Access type: {revoke_access.access_type.upper()} with user id: {revoke_access.user_id}'


@categories_router.get('/privileged_users/{category_id}', tags=["Categories"])
def view_privileged_users(category_id: int, current_user: int = Depends(authorization.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID not found. User may not be authenticated.")

    privileged_user_result = category_services.view_privileged_users(category_id, current_user)

    if privileged_user_result == 'invalid user id':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {current_user} is not found')
    elif privileged_user_result == 'not admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'User with id: {current_user} is not admin of this category!')
    elif privileged_user_result == 'invalid category':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Category with id: {category_id} not found!')
    elif privileged_user_result == 'not private':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Category with id: {category_id} is NOT private!')

    return privileged_user_result

# @categories_router.put('/{category_id}/users/{user_id}/access')
# def change_user_access(category_id: int, user_id: int, access: Access, current_user: int = Depends(authorization.get_current_user)):
#     if access.access_type == 'read':
#         result = give_read_access(category_id, user_id, current_user)
#     elif access.access_type == 'write':
#         result = give_write_access(category_id, user_id, current_user)
#     else:
#         result = 'invalid access type'
#
#     if result == 'not admin':
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only ADMIN users can change user access!')
#     elif result == 'invalid access type' or result == 'invalid access':
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result)
#     return {'access_type': result}
