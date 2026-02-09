from services.tts.handlers.bark import BarkHandler
from services.tts.handlers.vits import VitsHandler
from services.tts.handlers.chatterbox import ChatterboxHandler
from services.tts.handlers.default import AutoTTSHandler
from transformers import AutoConfig

class HandlerFactory:
    _handlers = {
        "bark": BarkHandler,
        "vits": VitsHandler,
        "mms": VitsHandler, 
        "chatterbox": ChatterboxHandler, 
        "generic": AutoTTSHandler
    }
    
    @classmethod
    def get_handler(cls, model_id: str):
        try:
            config = AutoConfig.from_pretrained(model_id)
            model_type = getattr(config, "model_type", "generic")
            
            handler_class = cls._handlers.get(model_type, cls._handlers["generic"])
            return handler_class()
            
        except Exception:
            return cls._handlers["generic"]()