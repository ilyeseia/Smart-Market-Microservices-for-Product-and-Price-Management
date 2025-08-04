from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import Prix
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27018")

async def connect_db():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["prix_db"]
    await init_beanie(database=db, document_models=[Prix])
