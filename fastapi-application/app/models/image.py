from sqlalchemy import Column, String, DateTime, Integer, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(String, primary_key=True)
    prompt = Column(String, nullable=False)
    url = Column(String, nullable=False)
    likes = Column(Integer, nullable=False, default=0, server_default='0')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_suggested = Column(Boolean, nullable=True)
    original_input = Column(String, nullable=True)

    class Config:
        orm_mode = True 