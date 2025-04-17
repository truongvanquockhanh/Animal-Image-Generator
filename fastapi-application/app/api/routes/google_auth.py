from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.services.auth import create_token
from app.schemas.auth import LoginResponse
import os
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

@router.post("/google", response_model=LoginResponse)
async def google_auth(token: str, db: Session = Depends(get_db)):
    try:
        # Verify the Google token
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), GOOGLE_CLIENT_ID)

        # Get user info from the token
        user_email = idinfo['email']
        user_name = idinfo.get('name', user_email.split('@')[0])

        # Create or get user and generate JWT token
        user_data = {
            "username": user_name,
            "email": user_email,
            "is_google_user": True
        }
        
        # Use the existing create_token service but modify it to handle Google users
        return create_token(db, user_data)

    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Google token"
        ) 