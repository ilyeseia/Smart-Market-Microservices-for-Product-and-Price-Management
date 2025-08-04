# services/recommendation-service
from fastapi import FastAPI
from typing import List, Dict
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="Recommendation Service")

class RecommendationEngine:
    def __init__(self):
        self.kmeans = KMeans(n_clusters=5)
        self.product_features = {}
    
    async def get_similar_products(self, product_id: str, limit: int = 5):
        """Recommandation de produits similaires"""
        # Récupération des caractéristiques du produit
        product_features = await self.get_product_features(product_id)
        
        # Calcul de similarité
        similarities = {}
        for other_id, other_features in self.product_features.items():
            if other_id != product_id:
                similarity = cosine_similarity([product_features], [other_features])[0][0]
                similarities[other_id] = similarity
        
        # Tri par similarité
        sorted_products = sorted(similarities.items(), 
                               key=lambda x: x[1], 
                               reverse=True)[:limit]
        
        return [{"product_id": pid, "similarity": sim} 
                for pid, sim in sorted_products]
    
    async def get_seasonal_recommendations(self, season: str):
        """Recommandations saisonnières"""
        seasonal_products = await self.get_seasonal_products(season)
        
        # Analyse des tendances saisonnières
        recommendations = []
        for product in seasonal_products:
            trend = await self.analyze_seasonal_trend(product['id'], season)
            recommendations.append({
                "product_id": product['id'],
                "name": product['name'],
                "seasonal_score": trend['score'],
                "expected_price_range": trend['price_range']
            })
        
        return sorted(recommendations, 
                     key=lambda x: x['seasonal_score'], 
                     reverse=True)
