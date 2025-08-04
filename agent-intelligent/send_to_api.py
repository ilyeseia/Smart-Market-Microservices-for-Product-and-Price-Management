import httpx
from config import PRIX_SERVICE_URL

def send_price(produit_id, prix_info):
    prix_info["produit_id"] = produit_id
    try:
        r = httpx.post(PRIX_SERVICE_URL, json=prix_info)
        print(f"[+]{prix_info['produit']} -> {r.status_code}")
    except Exception as e:
        print(f"Erreur d'envoi: {e}")
