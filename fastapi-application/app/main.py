from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine, Base
from app.api.routes import image, auth, google_auth  # Import google_auth router
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting App...")
    Base.metadata.create_all(bind=engine)  # Create database tables
    yield
    print("Shutting Down App...")

app = FastAPI(
    title="Image Generation API",
    description="API for generating, retrieving, and managing images",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration - Development settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=False,  # Set to False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(image.router, prefix="/images", tags=["images"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(google_auth.router, prefix="/auth", tags=["auth"])  # Add Google auth routes

@app.get("/")
async def root():
    return {"message": "Welcome to the Image Generation API"}
