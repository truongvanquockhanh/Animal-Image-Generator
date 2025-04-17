from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime
from app.api.dependencies import get_db
from app.models import Image
from app.schemas.image import ImageCreate, ImageResponse
from app.services.image_service import ImageService

router = APIRouter()
image_service = ImageService()

@router.post("/generate", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def generate_image(image_data: ImageCreate, db: Session = Depends(get_db)):
    """Generate a new image based on the provided prompt."""
    try:
        return await image_service.generate_image(db, image_data.prompt)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def save_image(image_data: ImageResponse, db: Session = Depends(get_db)):
    try:
        return image_service.save_image(db, image_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("", response_model=List[ImageResponse])
async def get_images(db: Session = Depends(get_db)):
    try:
        return image_service.get_images(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{image_id}/like", status_code=status.HTTP_200_OK)
async def like_image(image_id: str, db: Session = Depends(get_db)):
    try:
        likes = image_service.update_likes(db, image_id, 'like')
        return {"success": True, "likes": likes}
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{image_id}", status_code=status.HTTP_200_OK)
async def delete_image(image_id: str, db: Session = Depends(get_db)):
    try:
        success = image_service.delete_image(db, image_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
        return {"success": True}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 