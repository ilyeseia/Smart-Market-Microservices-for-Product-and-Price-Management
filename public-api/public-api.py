# services/public-api
from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
import asyncio

app = FastAPI(title="Public API", version="1.0.0")

@app.get("/api/v1/prices/current")
async def get_current_prices(
    category: Optional[str] = Query(None, description="Catégorie de produit"),
    limit: int = Query(50, ge=1, le=100, description="Nombre maximum de résultats")
):
    """Récupération des prix actuels"""
    try:
        prices = await get_latest_prices(category, limit)
        return {
            "status": "success",
            "data": prices,
            "total": len(prices)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/products/{product_id}/history")
async def get_price_history(
    product_id: str,
    days: int = Query(30, ge=1, le=365, description="Nombre de jours")
):
    """Historique des prix d'un produit"""
    try:
        history = await get_product_price_history(product_id, days)
        return {
            "status": "success",
            "product_id": product_id,
            "data": history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/predictions/{product_id}")
async def get_price_predictions(
    product_id: str,
    days: int = Query(7, ge=1, le=30, description="Nombre de jours à prédire")
):
    """Prédictions des prix"""
    try:
        predictions = await get_price_predictions(product_id, days)
        return {
            "status": "success",
            "product_id": product_id,
            "predictions": predictions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
