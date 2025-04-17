from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from app.schemas.user import UserResponse

class ProjectCreated(BaseModel):
    name: str

class ProjectCreateReponse(BaseModel):
    id: UUID
    name: str

class ProjectMemberResponse(BaseModel):
    id: UUID
    joinedAt: datetime
    member: UserResponse

class UpdateProject(BaseModel):

    name: Optional[str] = None
    members: Optional[List[UUID]] = None

class UpdateProjectResponse(BaseModel):

    id: UUID
    createdAt: datetime
    updatedAt: datetime
    name: str
    createdById: UUID

    class config:
        from_attributes = True

class ProjectResponse(BaseModel):
    id: UUID
    name: str
    createdAt: datetime
    updatedAt: datetime
    createdBy: UserResponse
    members: List[ProjectMemberResponse]
    bugs: List[dict] = []

    class Config:
        from_attributes = True
