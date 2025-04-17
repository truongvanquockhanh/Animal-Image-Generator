from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.schemas.user import UserResponse

class NoteResponse(BaseModel):
  id: UUID
  body: str
  bugId: UUID
  createdAt: datetime
  updatedAt: datetime
  author: UserResponse

  class Config:
    from_arttributes = True

class NoteRequest(BaseModel):
  body: str
