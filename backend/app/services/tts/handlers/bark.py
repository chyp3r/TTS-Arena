import torch
from transformers import BarkModel, AutoProcessor
from .base import BaseHandler

class BarkHandler(BaseHandler):
    def load_model(self, model_id: str, device: str):
        return BarkModel.from_pretrained(
            model_id, 
            torch_dtype=torch.float32, 
            low_cpu_mem_usage=True
        ).to(device)

    def load_processor(self, model_id: str):
        return AutoProcessor.from_pretrained(model_id)

    def infer(self, model, inputs, text=None):
        voice_preset = "v2/tr_speaker_0" 

        audio_array = model.generate(
            **inputs, 
            history_prompt=voice_preset, 
            do_sample=True
        ).cpu().numpy().squeeze()
        
        sample_rate = model.generation_config.sample_rate
        return audio_array, sample_rate