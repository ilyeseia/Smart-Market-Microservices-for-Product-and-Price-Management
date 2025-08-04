# Nouveau service: api-gateway
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import asyncio
from typing import Dict, Any

app = FastAPI(title="API Gateway")
security = HTTPBearer()

class ServiceRegistry:
    def __init__(self):
        self.services = {
            "prix": "http://prix-service:8000",
            "produits": "http://produits-service:8000",
            "agent": "http://agent-intelligent:8000"
        }
    
    async def route_request(self, service: str, path: str, method: str, **kwargs):
        if service not in self.services:
            raise HTTPException(status_code=404, detail="Service not found")
        
        url = f"{self.services[service]}/{path}"
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, **kwargs)
            return response.json()
