from pydantic import BaseModel

class ProduitModel(BaseModel):
    nom: str
    unite: str
    region: str
    categorie: str
