import httpx

async def check_produit_exists(produit_id: str) -> bool:
    PRODUIT_SERVICE_URL = "http://produits-api:8000/produits"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{PRODUIT_SERVICE_URL}/{produit_id}")
            return resp.status_code == 200
    except Exception as e:
        return False
