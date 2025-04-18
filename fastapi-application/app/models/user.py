from sqlalchemy import Column, String, Boolean
from app.models import BaseModel
from sqlalchemy.orm import relationship

class User(BaseModel):
    __tablename__ = "user"

    username = Column(String, index=True, unique=True)
    password = Column(String, index=True, nullable=True)  # Nullable for Google users
    email = Column(String, unique=True, nullable=True)  # For Google users
    is_google_user = Column(Boolean, default=False)
    # Many-to-Many Relationship
    created_projects = relationship("Project", back_populates="createdBy")
    project_member = relationship("ProjectMember", back_populates="members")
