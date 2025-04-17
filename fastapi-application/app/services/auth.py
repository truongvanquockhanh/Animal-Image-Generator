from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import LogInRequest, SignupRequest, SignupResponse
from app.core.security import hash_password
from app.core.security import verify_password
from app.core.security import create_access_token
from fastapi import HTTPException

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
