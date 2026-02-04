import requests
import os

BASE_URL = os.getenv("BACKEND_URL", "http://backend:8000")
API_V1_PREFIX = "/api/v1/tts" 

class APIClient:
    @staticmethod
    def get_models():
        url = f"{BASE_URL}{API_V1_PREFIX}/models"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json().get("models", [])
            return []
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []

    @staticmethod
    def start_generation(text: str, model_id: str):
        url = f"{BASE_URL}{API_V1_PREFIX}/generate"
        payload = {"text": text, "model_id": model_id}
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                return response.json().get("job_id")
            else:
                print(f"Start Error: {response.text}")
                return None
        except Exception as e:
            print(f"Connection Error (Start): {e}")
            return None

    @staticmethod
    def get_job_status(job_id: str):
        url = f"{BASE_URL}{API_V1_PREFIX}/status/{job_id}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "FAILED", "error": "Status check failed"}
        except Exception as e:
            print(f"Connection Error (Status): {e}")
            return {"status": "FAILED", "error": str(e)}

    @staticmethod
    def get_audio_result(job_id: str):
        url = f"{BASE_URL}{API_V1_PREFIX}/result/{job_id}"
        try:
            response = requests.get(url, timeout=60) 
            if response.status_code == 200:
                return response.content
            else:
                print(f"Result Error: {response.text}")
                return None
        except Exception as e:
            print(f"Connection Error (Result): {e}")
            return None