from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import Produit
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")

async def connect_db():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["produits_db"]
    await init_beanie(database=db, document_models=[Produit])
