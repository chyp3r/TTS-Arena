import torch
from .base import BaseHandler
from chatterbox import Chatterbox

class ChatterboxHandler(BaseHandler):
    def load_model(self, model_id: str, device: str):
        model = Chatterbox.from_pretrained(model_id)
        model.to(device)
        return model

    def load_processor(self, model_id: str):
        return None

    def infer(self, model, inputs, text=None):
        if not text:
            raise ValueError("")

        audio_output = model.generate(text, language_id="tr")
        
        if isinstance(audio_output, torch.Tensor):
            audio_array = audio_output.cpu().numpy().squeeze()
        else:
            audio_array = audio_output

        sample_rate = getattr(model, "sr", 24000)

        return audio_array, sample_rate