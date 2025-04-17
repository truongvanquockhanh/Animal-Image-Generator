from sqlalchemy import Column, Integer, String, UUID
from sqlalchemy.orm import relationship
from app.models.basemodel import BaseModel
from sqlalchemy import ForeignKey

class Note(BaseModel):
    __tablename__ = "note"

    body = Column(String, nullable=False)
    authorId = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)  # ForeignKey to User
    bugId = Column(UUID(as_uuid=True), ForeignKey("bug.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    author = relationship("User", foreign_keys=[authorId])
