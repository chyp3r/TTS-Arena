from huggingface_hub import try_to_load_from_cache
from fastapi import APIRouter

router = APIRouter()

@router.get("/check_cache")
def check_if_model_cached(model_id: str):
    filepath = try_to_load_from_cache(repo_id=model_id, filename="config.json")
    
    if filepath:
        return {"cached": True}
    else:
        return {"cached": False}