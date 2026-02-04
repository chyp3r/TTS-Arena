from transformers import AutoModel, AutoTokenizer, AutoProcessor
from .base import BaseHandler

class VitsHandler(BaseHandler):
    def load_model(self, model_id: str, device: str):
        return AutoModel.from_pretrained(model_id).to(device)

    def load_processor(self, model_id: str):
        try:
            return AutoProcessor.from_pretrained(model_id)
        except:
            return AutoTokenizer.from_pretrained(model_id)

    def infer(self, model, inputs, text=None):
        output = model(**inputs).waveform
        audio_array = output.cpu().numpy().squeeze()
        sample_rate = model.config.sampling_rate
        return audio_array, sample_rate