from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse, UserUpdateRequest
from app.services.user import update_user, delete_user, get_user_by_id, get_all_users
from uuid import UUID
from app.api.dependencies import get_db, get_current_user
from fastapi import Query

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
def get_user(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
    username: str = Query(None, description="Filter by username"),
    sort_by: str = Query("username", regex="^(username|id)$", description="Sort by username or id"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order (asc or desc)")
):
    users = get_all_users(db, username=username, sort_by=sort_by, sort_order=sort_order)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id_endpoint(
    user_id: UUID, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(get_current_user)
):
    return get_user_by_id(db, user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(
    user_id: UUID,
    user_data: UserUpdateRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return update_user(db, user_id, user_data)

@router.delete("/{user_id}")
def delete_user_route(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return delete_user(db, user_id)
