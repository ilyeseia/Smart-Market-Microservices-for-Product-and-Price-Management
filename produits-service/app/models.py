from beanie import Document

class Produit(Document):
    nom: str
    unite: str
    region: str
    categorie: str
