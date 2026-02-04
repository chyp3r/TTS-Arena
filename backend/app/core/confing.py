import torch
import os

class Settings:
    PROJECT_NAME = "TTS Benchmark API"
    VERSION = "1.0.0"
    DEVICE = "cpu"
    
    AVAILABLE_MODELS = [
        "facebook/mms-tts-tur",
        "suno/bark-small",
        "suno/bark",
        "ResembleAI/chatterbox"
    ]

settings = Settings()