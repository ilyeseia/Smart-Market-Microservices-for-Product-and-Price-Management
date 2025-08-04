from beanie import Document
from datetime import date

class Prix(Document):
    produit_id: str
    prix: float
    unite: str
    source: str
    date: date
