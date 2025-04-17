from sqlalchemy.orm import Session
from app.models.user import User
from fastapi import HTTPException
from app.schemas.user import UserResponse
from uuid import UUID
from app.schemas.user import UserUpdateRequest
from app.core.security import hash_password

def get_all_users(db: Session, username: str = None, sort_by: str = "username", sort_order: str = "asc"):
    query = db.query(User)

    # 🔹 Filter by username if provided
    if username:
        query = query.filter(User.username.ilike(f"%{username}%"))

    # 🔹 Sort by the specified field (username or id)
    if sort_by == "username":
        if sort_order == "asc":
            query = query.order_by(User.username.asc())
        else:
            query = query.order_by(User.username.desc())
    elif sort_by == "id":
        if sort_order == "asc":
            query = query.order_by(User.id.asc())
        else:
            query = query.order_by(User.id.desc())

    users = query.all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users

def update_user(db: Session, user_id: UUID, user_data: UserUpdateRequest):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields
    if user_data.username:
        user.username = user_data.username
    if user_data.password:
        user.password = hash_password(user_data.password)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: UUID):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

def get_user_by_id(db: Session, user_id: UUID):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
