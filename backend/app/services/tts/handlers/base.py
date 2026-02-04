from abc import ABC, abstractmethod

class BaseHandler(ABC):
    @abstractmethod
    def load_model(self, model_id: str, device: str):
        pass

    @abstractmethod
    def load_processor(self, model_id: str):
        pass

    @abstractmethod
    def infer(self, model, inputs, text=None):
        pass