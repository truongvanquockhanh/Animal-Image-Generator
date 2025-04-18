from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import GoogleAuthRequest, GoogleLoginResponse
from app.services.auth import handle_google_user
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth import jwt
import os
from app.api.dependencies import get_db

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

@router.post("/google", response_model=GoogleLoginResponse)
async def google_auth(request: GoogleAuthRequest, db: Session = Depends(get_db)):
    try:
        if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
            raise HTTPException(
                status_code=500,
                detail="Google OAuth configuration is missing"
            )

        # Verify the Google token with both CLIENT_ID and CLIENT_SECRET
        idinfo = id_token.verify_oauth2_token(
            request.token, 
            requests.Request(), 
            GOOGLE_CLIENT_ID,
            clock_skew_in_seconds=10  # Allow 10 seconds of clock skew
        )

        # Additional verification of the token
        if idinfo['aud'] != GOOGLE_CLIENT_ID:
            raise HTTPException(
                status_code=401,
                detail="Invalid token audience"
            )

        # Get user info from the verified token
        email = idinfo['email']
        # Use given_name or email prefix as base username
        username = idinfo.get('given_name', email.split('@')[0])

        # Handle the Google user authentication
        return handle_google_user(db, email, username)

    except ValueError as e:
        # Invalid token
        raise HTTPException(status_code=401, detail="Invalid Google token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 