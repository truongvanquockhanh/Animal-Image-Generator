from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.auth import create_token, sign_up
from app.schemas.auth import LoginResponse, LogInRequest, SignupRequest, SignupResponse
from app.api.dependencies import get_db

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def add_user(user: LogInRequest, db: Session = Depends(get_db)):
    return create_token(db, user)

@router.post("/signup", response_model=SignupResponse)
def add_user(user: SignupRequest, db: Session = Depends(get_db)):
    return sign_up(db, user)
