from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models import BaseModel
from sqlalchemy import func

class ProjectMember(BaseModel):
    __tablename__ = "project_member"

    project_id = Column(UUID(as_uuid=True), ForeignKey("project.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    joined_at = Column(DateTime, default=func.now())
    # Relationships
    project = relationship("Project", back_populates="members")
    members = relationship("User", back_populates="project_member")
