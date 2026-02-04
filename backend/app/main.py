from fastapi import FastAPI
from core.confing import settings
from api.v1.router import api_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "TTS Benchmark API is running. Go to /docs for Swagger UI."}