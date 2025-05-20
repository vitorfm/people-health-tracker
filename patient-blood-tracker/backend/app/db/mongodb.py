from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends
from ..core.config import settings

async def get_database() -> AsyncIOMotorClient:
    """Get MongoDB database instance"""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    try:
        yield client[settings.MONGODB_DB_NAME]
    finally:
        client.close() 