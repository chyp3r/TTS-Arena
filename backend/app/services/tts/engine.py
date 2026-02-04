import torch
import io
import scipy.io.wavfile
import logging
from core.confing import settings
from core.store import update_job
from services.tts.factory import HandlerFactory 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        self.model_cache = {}
        self.processor_cache = {}
        self.handler_cache = {}  
        self.device = settings.DEVICE

    def _load_resources(self, model_id: str, job_id: str = None):
        if model_id in self.model_cache:
            if job_id:
                update_job(job_id, "PROCESSING", "Loading model from cache...")
            return self.handler_cache[model_id], self.processor_cache[model_id], self.model_cache[model_id]

        logger.info(f"Loading resources for: {model_id}")
        
        if job_id:
            update_job(job_id, "DOWNLOADING", "Downloading model resources...")

        try:
            handler = HandlerFactory.get_handler(model_id)

            processor = handler.load_processor(model_id)
            model = handler.load_model(model_id, self.device)
            
            if job_id:
                update_job(job_id, "PROCESSING", "Model loaded into memory")
            
            self.model_cache[model_id] = model
            self.processor_cache[model_id] = processor
            self.handler_cache[model_id] = handler
            
            return handler, processor, model

        except Exception as e:
            logger.error(f"Error loading model {model_id}: {e}")
            raise RuntimeError(f"Failed to load model: {str(e)}")

    def synthesize_audio(self, model_id: str, text: str, job_id: str = None) -> io.BytesIO:
        handler, processor, model = self._load_resources(model_id, job_id)
        
        if job_id:
            update_job(job_id, "GENERATING", "Generating audio... 🎧")
        
        inputs = processor(text=text, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            audio_array, sample_rate = handler.infer(model, inputs, text=text)
        
        buffer = io.BytesIO()
        scipy.io.wavfile.write(buffer, rate=sample_rate, data=audio_array)
        buffer.seek(0)
        
        return buffer

tts_service = TTSService()

def process_tts_background(job_id: str, text: str, model_name: str):
    try:
        update_job(job_id, "QUEUED", "Processing queued")
        audio_buffer = tts_service.synthesize_audio(model_name, text, job_id)
        update_job(job_id, "COMPLETED", "Operation completed", result=audio_buffer.getvalue())
    except Exception as e:
        print(f"Error at Job {job_id}: {e}")
        update_job(job_id, "FAILED", error=str(e))