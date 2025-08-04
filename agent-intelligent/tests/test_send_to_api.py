from send_to_api import send_price

def test_send_fake_price():
    produit_id = "fake-id"
    prix_info = {
        "produit": "test",
        "prix": 999,
        "unite": "kg",
        "source": "test-script",
        "date": "2025-07-13"
    }
    try:
        send_price(produit_id, prix_info)
    except Exception:
        assert False, "Envoi échoué"
