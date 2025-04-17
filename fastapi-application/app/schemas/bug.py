from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.schemas.user import UserResponse
from app.schemas.note import NoteResponse

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class BugCreated(BaseModel):
    title: str
    description: str
    priority: PriorityEnum

class BugUpdated(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None

class BugResponse(BaseModel):
    id: UUID
    title: str
    description: str
    priority: PriorityEnum
    projectId: UUID
    isResolved: bool
    closedAt: Optional[datetime] = None
    reopenedAt: Optional[datetime] = None
    createdAt: datetime
    updatedAt: datetime
    createdBy: UserResponse
    updatedBy: Optional[UserResponse] = None
    closedBy: Optional[UserResponse] = None
    reopenedBy: Optional[UserResponse] = None
    notes: List[NoteResponse] = []# Assuming notes are stored as a list of strings

    class Config:
        from_attributes = True  # Enables SQLAlchemy ORM serialization
