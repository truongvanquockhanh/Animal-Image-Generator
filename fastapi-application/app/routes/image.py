from fastapi import APIRouter, HTTPException
from typing import List
from ..schemas.image import ImageCreate, ImageResponse
from ..services.image_service import ImageService

router = APIRouter()
image_service = ImageService()

@router.post("/generate", response_model=ImageResponse)
async def generate_image(image: ImageCreate):
    """Generate a new image based on the provided prompt."""
    try:
        return image_service.generate_image(image.prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[ImageResponse])
async def get_images():
    """Get all generated images."""
    return image_service.get_images()

@router.delete("/{image_id}")
async def delete_image(image_id: str):
    """Delete an image by its ID."""
    try:
        image_service.delete_image(image_id)
        return {"message": "Image deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 