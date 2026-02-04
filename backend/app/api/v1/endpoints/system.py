from fastapi import APIRouter
from core.confing import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "active",
        "version": settings.VERSION,
        "device": settings.DEVICE
    }