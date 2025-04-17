from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime
from app.api.dependencies import get_db
from app.models import Image
from app.schemas.image import ImageCreate, ImageResponse

router = APIRouter()

@router.post("/generate", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def generate_image(image_data: ImageCreate, db: Session = Depends(get_db)):
    try:
        image_id = str(uuid.uuid4())
        image_url = f"https://picsum.photos/seed/{image_id}/400/400"
        
        db_image = Image(
            id=image_id,
            prompt=image_data.prompt,
            url=image_url,
            likes=0
        )
        
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        
        return db_image
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("", response_model=List[ImageResponse])
async def get_images(db: Session = Depends(get_db)):
    try:
        return db.query(Image).order_by(Image.created_at.desc()).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/{image_id}/like", status_code=status.HTTP_200_OK)
async def like_image(image_id: str, db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
        
        image.likes += 1
        db.commit()
        db.refresh(image)
        return {"success": True, "likes": image.likes}
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete("/{image_id}", status_code=status.HTTP_200_OK)
async def delete_image(image_id: str, db: Session = Depends(get_db)):
    try:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found"
            )
        
        db.delete(image)
        db.commit()
        return {"success": True}
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        ) 