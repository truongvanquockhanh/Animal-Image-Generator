# Secret key for signing JWT
import os
import jwt  # PyJWT
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Generate JWT token"""
    to_encode = data.copy()
    print(to_encode)
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    print("after: ", to_encode)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

user = {
    'username': "Khanh",
    'password': "Khanh12212112"
}
def decode_access_token(token: str) -> dict:
    """Decode JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
    
token = create_access_token(user)
print(token)
decode = decode_access_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IktoYW5oIiwicGFzc3dvcmQiOiJLaGFuaDEyMjEyMTEyIiwiZXhwIjoxNzQzNTYxNzM5fQ.qK2nlertmaEvTA_JYNIuIr8iC4IHajnaNR-dtO75Ikc')
print(decode)