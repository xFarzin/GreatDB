from fastapi import FastAPI
from src.core.config import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
