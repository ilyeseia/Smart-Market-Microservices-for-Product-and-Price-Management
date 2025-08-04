from pydantic import BaseModel
from datetime import date

class PrixModel(BaseModel):
    produit_id: str
    prix: float
    unite: str
    source: str
    date: date
