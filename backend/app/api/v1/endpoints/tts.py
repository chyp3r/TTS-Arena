from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import Response
import uuid

from core.confing import settings
from schemas.tts import ModelListResponse 
from services.tts.engine import process_tts_background 
from core.store import get_job

router = APIRouter()

@router.get("/models", response_model=ModelListResponse)
async def list_models():
    return {"models": settings.AVAILABLE_MODELS}

@router.post("/generate")
async def generate_audio(payload: dict, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    text = payload.get("text")
    model = payload.get("model_id")

    if model not in settings.AVAILABLE_MODELS:
        raise HTTPException(status_code=400, detail="Invalid Model ID")

    background_tasks.add_task(process_tts_background, job_id, text, model)

    return {"job_id": job_id, "status": "QUEUED"}

@router.get("/status/{job_id}")
def check_status(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "status": job.get("status"),
        "message": job.get("message"),
        "error": job.get("error")
    }

@router.get("/result/{job_id}")
def get_result(job_id: str):
    job = get_job(job_id)
    if not job or job.get("status") != "COMPLETED":
        raise HTTPException(status_code=400, detail="Result not ready")
    
    return Response(content=job["result"], media_type="audio/wav")