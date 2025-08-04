from fastapi import APIRouter, HTTPException
from app.schemas import PrixModel
from app.models import Prix
from typing import List
from app.utils import check_produit_exists

router = APIRouter()

@router.post("/prix", response_model=PrixModel)
async def add_prix(prix: PrixModel):
    exists = await check_produit_exists(prix.produit_id)
    if not exists:
        raise HTTPException(status_code=404, detail="Produit inexistant")

    new_entry = await Prix.create(**prix.dict())
    return new_entry

@router.get("/prix", response_model=List[PrixModel])
async def get_all_prix():
    return await Prix.find_all().to_list()
