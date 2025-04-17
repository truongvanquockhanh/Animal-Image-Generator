from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Literal
from ..services.image_service import ImageService
from ..database import get_db
from ..schemas.image import ImageResponse

router = APIRouter()
image_service = ImageService()

class LikeRequest(BaseModel):
    image_id: str
    action: Literal['like', 'unlike']

@router.get("/", response_model=List[ImageResponse])
async def get_images(db: Session = Depends(get_db)):
    try:
        return image_service.get_images(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/like")
async def like_image(request: LikeRequest, db: Session = Depends(get_db)):
    try:
        updated_likes = image_service.update_likes(db, request.image_id, request.action)
        return {"success": True, "likes": updated_likes}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{image_id}")
async def delete_image(image_id: str, db: Session = Depends(get_db)):
    try:
        success = image_service.delete_image(db, image_id)
        if not success:
            raise HTTPException(status_code=404, detail="Image not found")
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 