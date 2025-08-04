from browser_agent import get_facebook_page_content

def test_facebook_fetch():
    html = get_facebook_page_content("https://www.facebook.com/Magsetifel/?locale=ar_AR")
    assert isinstance(html, str)
    assert len(html) > 1000  # contenu minimal attendu
