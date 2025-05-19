from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

from .core.config import settings
from .api.endpoints import patients, blood_tests

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for tracking patient health data and blood tests",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# Include routers
app.include_router(
    patients.router,
    prefix=f"{settings.API_V1_PREFIX}/patients",
    tags=["patients"]
)

app.include_router(
    blood_tests.router,
    prefix=f"{settings.API_V1_PREFIX}/blood-tests",
    tags=["blood-tests"]
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to People Health Tracker API",
        "status": "operational"
    } 