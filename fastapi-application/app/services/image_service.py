import os
import random
import httpx
from typing import List, Dict, Optional, Literal
from sqlalchemy.orm import Session
from app.schemas.image import ImageResponse
from app.models.image import Image
from dotenv import load_dotenv
from datetime import datetime
import uuid
import replicate
from replicate.client import Client

load_dotenv()

# List of available animals for random selection
AVAILABLE_ANIMALS = [
    "dog", "cat", "lion", "tiger", "elephant", "penguin", "panda", 
    "koala", "giraffe", "dolphin", "fox", "wolf", "rabbit", "cow", 
    "horse", "sheep", "goat", "pig", "chicken", "duck", "turkey", 
    "peacock", "parrot", "pigeon", "sparrow", "rooster", "hen", "cock", "fish", 
    "shark", "whale", "dolphin", "octopus", "crab", "lobster", "snail", "butterfly", 
    "bee", "ant", "spider", "snake", "lizard", "turtle", "tortoise", "bird", 
    "owl", "eagle", "hawk", "falcon" 
]

class ImageService:
    def __init__(self):
        self.pexels_api_key = os.getenv("PEXELS_API_KEY")
        self.replicate_api_token = os.getenv("REPLICATE_API_TOKEN")
        if self.replicate_api_token:
            self.client = Client(api_token=self.replicate_api_token)

    def get_random_animal(self) -> str:
        """Return a random animal from the available list."""
        return random.choice(AVAILABLE_ANIMALS)
        
    def is_animal_prompt(self, prompt: str) -> bool:
        """
        Check if the prompt contains any known animal names.
        Handles case-insensitive matching and spaces.
        """
        # Clean the prompt: convert to lowercase and remove extra spaces
        cleaned_prompt = ' '.join(prompt.lower().split())
        
        # Check each animal name
        for animal in AVAILABLE_ANIMALS:
            # Clean the animal name too for consistency
            cleaned_animal = ' '.join(animal.lower().split())
            # Check if the animal name is a complete word in the prompt
            if any(
                word == cleaned_animal 
                for word in cleaned_prompt.split()
            ):
                return True
        return False

    async def generate_image(self, db: Session, prompt: str) -> ImageResponse:
        """
        Generate an image based on the prompt using Pexels API.
        Does not save to database immediately.
        """
        try:
            if not self.pexels_api_key:
                raise ValueError("Pexels API key not found")

            print(f"Prompt: {prompt}")
            print(f"Is animal prompt: {self.is_animal_prompt(prompt)}")

            # Check if prompt contains an animal name
            if not self.is_animal_prompt(prompt):
                # If no animal found, get a random one
                random_animal = self.get_random_animal()
                # Return both the image and the suggested animal
                search_prompt = f"{random_animal} animal"
                is_random = True
                original_input = prompt  # Store the original user input
            else:
                search_prompt = f"{prompt} animal"
                is_random = False
                original_input = None

            print(f"Search prompt: {search_prompt}")
            # Search for animal photos
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.pexels.com/v1/search?query={search_prompt}&per_page=15&size=medium",
                    headers={
                        'Authorization': self.pexels_api_key
                    }
                )

                if not response.status_code == 200:
                    raise ValueError('Failed to fetch image from Pexels')

                data = response.json()
                
                if not data.get("photos"):
                    raise ValueError('No images found')

                # Get a random photo from the results
                random_index = random.randint(0, len(data["photos"]) - 1)
                image_url = data["photos"][random_index]["src"]["medium"]

                # Create new image record but don't save to database yet
                image = Image(
                    id=str(uuid.uuid4()),
                    prompt=random_animal if is_random else prompt,
                    url=image_url,
                    likes=0,
                    is_suggested=is_random,
                    original_input=original_input if is_random else None
                )

                # Return image response without saving to database
                return ImageResponse(
                    id=image.id,
                    prompt=image.prompt,
                    url=image.url,
                    created_at=datetime.utcnow(),
                    likes=image.likes,
                    is_suggested=is_random,
                    suggested_animal=random_animal if is_random else None,
                    original_input=original_input if is_random else None
                )

        except Exception as e:
            print(f"Error generating image: {str(e)}")
            raise

    def save_image(self, db: Session, image_data: ImageResponse) -> ImageResponse:
        """
        Save the generated image to database.
        """
        try:
            # Create new image record
            image = Image(
                id=image_data.id,
                prompt=image_data.prompt,
                url=image_data.url,
                likes=image_data.likes,
                is_suggested=image_data.is_suggested,
                original_input=image_data.original_input
            )

            # Save to database
            db.add(image)
            db.commit()
            db.refresh(image)

            return image_data

        except Exception as e:
            db.rollback()
            print(f"Error saving image: {str(e)}")
            raise

    def get_images(self, db: Session) -> List[ImageResponse]:
        """
        Get all generated images from database.
        """
        try:
            images = db.query(Image).order_by(Image.created_at.desc()).all()
            return [
                ImageResponse(
                    id=image.id,
                    prompt=image.prompt,
                    url=image.url,
                    created_at=image.created_at,
                    likes=image.likes,
                    is_suggested=False,  # Default value since column doesn't exist yet
                    suggested_animal=None  # Default value since this is a new feature
                ) for image in images
            ]
        except Exception as e:
            print(f"Error fetching images: {str(e)}")
            raise

    def delete_image(self, db: Session, image_id: str) -> bool:
        """
        Delete an image by ID from database.
        """
        try:
            image = db.query(Image).filter(Image.id == image_id).first()
            if not image:
                return False
            
            db.delete(image)
            db.commit()
            return True
        except Exception as e:
            print(f"Error deleting image: {str(e)}")
            db.rollback()
            raise

    def update_likes(self, db: Session, image_id: str, action: Literal['like', 'unlike']) -> int:
        """
        Update likes count for an image.
        """
        try:
            image = db.query(Image).filter(Image.id == image_id).first()
            if not image:
                raise ValueError(f"Image with id {image_id} not found")
            
            if action == 'like':
                image.likes += 1
            else:
                image.likes = max(0, image.likes - 1)
            
            db.commit()
            db.refresh(image)
            return image.likes
        except Exception as e:
            print(f"Error updating likes: {str(e)}")
            db.rollback()
            raise

    def generate_image_replicate(self, prompt: str) -> ImageResponse:
        """Generate a new image using Replicate's API."""
        try:
            # Call Replicate API to generate image
            output = replicate.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={"prompt": prompt}
            )
            
            # Create image response
            image_id = str(uuid.uuid4())
            image = ImageResponse(
                id=image_id,
                url=output[0],  # Replicate returns a list of URLs
                prompt=prompt,
                created_at=datetime.utcnow()
            )
            
            # Store image
            self.images.append(image)
            return image
            
        except Exception as e:
            raise Exception(f"Failed to generate image: {str(e)}") 