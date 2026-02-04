from pydantic import BaseModel

class SynthesisRequest(BaseModel):
    text: str
    model_id: str

class ModelListResponse(BaseModel):
    models: list[str]