from pydantic import BaseModel, Field
from uuid import UUID

class LogInRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    id: UUID
    username: str
    token: str
    

class SignupRequest(BaseModel):
    username: str
    password: str

class SignupResponse(BaseModel):
    id: UUID
    username: str
    token: str
