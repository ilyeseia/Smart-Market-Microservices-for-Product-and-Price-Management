from fastapi import APIRouter, HTTPException
from app.models import Produit
from app.schemas import ProduitModel
from typing import List
from beanie import PydanticObjectId

router = APIRouter()

@router.post("/produits", response_model=ProduitModel)
async def create_produit(produit: ProduitModel):
    new_produit = await Produit.create(**produit.dict())
    return new_produit

@router.get("/produits", response_model=List[ProduitModel])
async def get_produits():
    produits = await Produit.find_all().to_list()
    return produits

@router.get("/produits/{id}", response_model=ProduitModel)
async def get_produit(id: PydanticObjectId):
    produit = await Produit.get(id)
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return produit
