from app.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, func

class BaseModel(Base):
  __abstract__ = True

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
   # created_at will be automatically set when a record is created
  createdAt = Column(DateTime, default=func.now())

  # updated_at will be updated every time the record is modified
  updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
