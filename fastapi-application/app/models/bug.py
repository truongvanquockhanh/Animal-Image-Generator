from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models import BaseModel
from sqlalchemy import Enum, Boolean, DateTime
import enum

class PriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Bug(BaseModel):
    __tablename__ = "bug"

    projectId = Column(UUID(as_uuid=True), ForeignKey("project.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(60), nullable=False)
    description = Column(String, nullable=True)
    priority = Column(Enum(PriorityEnum), nullable=False, default=PriorityEnum.medium)
    isResolved = Column(Boolean, nullable=False, default=False)
    closedById = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    closedAt = Column(DateTime, nullable=True)
    reopendById = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    reopendAt = Column(DateTime, nullable=True)
    createdById = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    updatedById = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)

    # Relationship
    project = relationship("Project", back_populates="bug")
    createdBy = relationship("User", foreign_keys=[createdById])
    updatedBy = relationship("User", foreign_keys=[updatedById])
