from sqlalchemy import Column, Integer, String, UUID
from sqlalchemy.orm import relationship
from app.models.basemodel import BaseModel
from sqlalchemy import ForeignKey

class Project(BaseModel):
    __tablename__ = "project"

    name = Column(String, nullable=False)
    createdById = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)  # ForeignKey to User

    # Relationships
    createdBy = relationship("User", back_populates="created_projects")  # Link to User
    members = relationship("ProjectMember", back_populates="project", cascade="all, delete-orphan")  
    bug = relationship("Bug", back_populates="project", cascade="all, delete-orphan")
