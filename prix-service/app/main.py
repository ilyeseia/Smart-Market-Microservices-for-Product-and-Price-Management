from fastapi import FastAPI
from app.routes import router
from app.database import connect_db

app = FastAPI(title="Service de Collecte des Prix")

@app.on_event("startup")
async def startup_db():
    await connect_db()

app.include_router(router)
