from extract_logic import extract_prices_from_html

# مثال HTML بسيط (simulation)
sample_html = """
<div>سعر البطاطا 120 دينار</div>
<div>طماطم بـ 150 دج.</div>
"""

def test_extract_prices():
    results = extract_prices_from_html(sample_html)
    assert isinstance(results, list)
    assert len(results) >= 2
    for item in results:
        assert "produit" in item
        assert "prix" in item
