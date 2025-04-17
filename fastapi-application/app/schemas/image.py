from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Literal

class ImageBase(BaseModel):
    prompt: str

class ImageCreate(ImageBase):
    pass

class ImageResponse(BaseModel):
    id: str
    prompt: str
    url: str
    likes: int = 0
    created_at: datetime
    is_suggested: bool = False
    suggested_animal: Optional[str] = None
    original_input: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True

class LikeRequest(BaseModel):
    image_id: str
    action: Literal['like', 'unlike'] 