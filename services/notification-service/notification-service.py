# services/notification-service
from fastapi import FastAPI
from typing import List, Dict
import aioredis
import asyncio

app = FastAPI(title="Notification Service")

class NotificationService:
    def __init__(self):
        self.redis = None
        self.subscribers = {}
    
    async def send_price_alert(self, product_id: str, old_price: float, new_price: float):
        """Envoi d'alerte de changement de prix"""
        alert = {
            "type": "price_change",
            "product_id": product_id,
            "old_price": old_price,
            "new_price": new_price,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.redis.publish("price_alerts", json.dumps(alert))
    
    async def send_stock_alert(self, product_id: str, status: str):
        """Envoi d'alerte de stock"""
        alert = {
            "type": "stock_alert",
            "product_id": product_id,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.redis.publish("stock_alerts", json.dumps(alert))
