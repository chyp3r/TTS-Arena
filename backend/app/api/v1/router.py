from fastapi import APIRouter
from api.v1.endpoints import tts, system, check_cache

api_router = APIRouter()

api_router.include_router(tts.router, prefix="/tts", tags=["Text-to-Speech"])
api_router.include_router(system.router, prefix="/system", tags=["System"])
api_router.include_router(check_cache.router, prefix="/models", tags=["Models"])