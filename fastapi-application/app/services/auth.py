from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import LogInRequest, SignupRequest, SignupResponse
from app.core.security import hash_password
from app.core.security import verify_password
from app.core.security import create_access_token
from fastapi import HTTPException
import uuid

def check_username_exists(db: Session, username: str) -> bool:
    """Check if a username already exists in the database."""
    db_user = db.query(User).filter(User.username == username).first()
    return db_user is not None

def check_user(db: Session, user: LogInRequest):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    return db_user

def create_token(db: Session, user: LogInRequest):
    db_user = check_user(db, user)
    if db_user:
        to_token = {
            "username": db_user.username,
            "password": db_user.password,
        }
        return {
            "id": db_user.id,
            "username": db_user.username,
            "token": create_access_token(to_token)
        }
    return

def sign_up(db: Session, user: SignupRequest):
    # Check if username exists before attempting to create
    if check_username_exists(db, user.username):
        raise HTTPException(status_code=409, detail="Username is already taken")
        
    password = hash_password(user.password)
    db_user = User(username=user.username, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    to_token = {
        "username": db_user.username,
        "password": db_user.password,
    }
    token = create_access_token(to_token)
    return SignupResponse(id=db_user.id, username=db_user.username, token=token)

def get_or_create_google_user(db: Session, email: str, username: str) -> User:
    """Get existing Google user or create a new one."""
    # First try to find user by email
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        return db_user

    # If not found by email, check username and generate a unique one if needed
    base_username = username
    counter = 1
    while check_username_exists(db, username):
        username = f"{base_username}{counter}"
        counter += 1

    # Create new user
    db_user = User(
        username=username,
        email=email,
        is_google_user=True,
        password=None  # Google users don't need a password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def handle_google_user(db: Session, email: str, username: str):
    """Handle Google user authentication and return token."""
    db_user = get_or_create_google_user(db, email, username)
    
    to_token = {
        "username": db_user.username,
        "is_google_user": True
    }
    
    token = create_access_token(to_token)
    return {
        "access_token": token,
        "token_type": "bearer"
    }
