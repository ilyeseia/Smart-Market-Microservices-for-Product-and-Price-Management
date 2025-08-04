from browser_agent import get_facebook_page_content
from extract_logic import extract_prices_from_html
from send_to_api import send_price
import time

# Mapping produits à remplacer par vos IDs réels de produits
produit_map = {
    "?????": "666a123abc11112223334444",
    "?????": "666a123abc11112223335555",
}

def main():
    print("[*] Lancement de l'agent IA...")
    html = get_facebook_page_content("https://www.facebook.com/Magsetifel/?locale=ar_AR")
    if not html:
        print("Erreur de récupération de la page.")
        return
    prix_list = extract_prices_from_html(html)
    for prix in prix_list:
        produit = prix["produit"]
        if produit in produit_map:
            send_price(produit_map[produit], prix)
        else:
            print(f"[!] Produit non trouvé dans la map: {produit}")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(86400)  # toutes les 24h
