from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.auth import create_token, sign_up, check_username_exists
from app.schemas.auth import LoginResponse, LogInRequest, SignupRequest, SignupResponse
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def add_user(user: LogInRequest, db: Session = Depends(get_db)):
    return create_token(db, user)

@router.post("/signup", response_model=SignupResponse)
def add_user(user: SignupRequest, db: Session = Depends(get_db)):
    return sign_up(db, user)

@router.get("/check-username")
def check_username(username: str, db: Session = Depends(get_db)):
    """Check if a username is available."""
    exists = check_username_exists(db, username)
    if exists:
        raise HTTPException(status_code=409, detail="Username is already taken")
    return {"available": True}
