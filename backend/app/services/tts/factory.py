from services.tts.handlers.bark import BarkHandler
from services.tts.handlers.vits import VitsHandler

class HandlerFactory:
    _handlers = {
        "bark": BarkHandler(),
        "vits": VitsHandler(),
        "mms": VitsHandler(), 
        "chatterbox": VitsHandler(), 
    }
    
    _default = VitsHandler()

    @classmethod
    def get_handler(cls, model_type: str):
        return cls._handlers.get(model_type, cls._default)