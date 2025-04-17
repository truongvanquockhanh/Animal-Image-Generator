from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.image import ImageCreate, ImageResponse, LikeRequest
from app.services.image_service import ImageService
from app.api.dependencies import get_db

router = APIRouter()
image_service = ImageService()

@router.post("/generate", response_model=ImageResponse)
async def generate_image(image: ImageCreate, db: Session = Depends(get_db)):
    """
    Generate a new image based on the provided prompt.
    Does not save to database.
    """
    try:
        return await image_service.generate_image(db, image.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save", response_model=ImageResponse)
async def save_image(image: ImageResponse, db: Session = Depends(get_db)):
    """
    Save a generated image to the database.
    """
    try:
        return image_service.save_image(db, image)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ImageResponse])
async def get_images(db: Session = Depends(get_db)):
    """
    Get all generated images.
    """
    try:
        return image_service.get_images(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{image_id}")
async def delete_image(image_id: str, db: Session = Depends(get_db)):
    """
    Delete an image by its ID.
    """
    try:
        image_service.delete_image(db, image_id)
        return {"message": "Image deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/like")
async def like_image(like_request: LikeRequest, db: Session = Depends(get_db)):
    """
    Update likes for an image (like or unlike).
    """
    try:
        result = image_service.update_likes(db, like_request.image_id, like_request.action)
        return {"success": True, "likes": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 