# services/analytics-service
from fastapi import FastAPI
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

app = FastAPI(title="Analytics Service")

class PriceAnalytics:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
    
    async def predict_price_trend(self, product_id: str, days: int = 30):
        """Prédiction des tendances de prix"""
        # Récupération des données historiques
        historical_data = await self.get_historical_prices(product_id)
        
        # Préparation des données
        df = pd.DataFrame(historical_data)
        df['date'] = pd.to_datetime(df['date'])
        df['days_since_start'] = (df['date'] - df['date'].min()).dt.days
        
        # Entraînement du modèle
        X = df[['days_since_start']].values
        y = df['price'].values
        
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        
        # Prédiction
        future_days = np.arange(df['days_since_start'].max() + 1, 
                              df['days_since_start'].max() + days + 1)
        future_X = self.scaler.transform(future_days.reshape(-1, 1))
        predictions = self.model.predict(future_X)
        
        return {
            "product_id": product_id,
            "predictions": predictions.tolist(),
            "trend": "increasing" if predictions[-1] > predictions[0] else "decreasing"
        }
    
    async def analyze_market_volatility(self, product_id: str):
        """Analyse de la volatilité du marché"""
        data = await self.get_historical_prices(product_id)
        df = pd.DataFrame(data)
        
        # Calcul de la volatilité
        df['price_change'] = df['price'].pct_change()
        volatility = df['price_change'].std()
        
        return {
            "product_id": product_id,
            "volatility": volatility,
            "risk_level": "high" if volatility > 0.1 else "low"
        }
