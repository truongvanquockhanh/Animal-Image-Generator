from pydantic import BaseModel
from uuid import UUID

class UserResponse(BaseModel):
    id: UUID
    username: str

    class Config:
        from_attributes = True

class UserUpdateRequest(BaseModel):
    username: str = None
    password: str = None
