from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas.image import ImageResponse
from ..services.image_service import ImageService

router = APIRouter()
image_service = ImageService()

@router.post("/generate", response_model=ImageResponse)
async def generate_image(prompt: str):
    try:
        return await image_service.generate_image(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ImageResponse])
async def get_images():
    return image_service.get_images()

@router.delete("/{image_id}")
async def delete_image(image_id: str):
    try:
        image_service.delete_image(image_id)
        return {"message": "Image deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 