import time
import streamlit as st
from service.clinent import APIClient

def poll_and_wait(job_id, model_name, status_container):
    if not job_id:
        status_container.error(f"{model_name}: Failed to start!")
        return None

    progress_bar = status_container.progress(0)
    status_text = status_container.empty()
    
    while True:
        status_data = APIClient.get_job_status(job_id)
        status = status_data.get("status")
        msg = status_data.get("message", "Waiting...")
        err = status_data.get("error")

        if status == "QUEUED":
            status_text.info(f"⏳ {model_name}: {msg}")
            progress_bar.progress(10)
        elif status == "PROCESSING" or status == "DOWNLOADING":
            status_text.warning(f"⬇️ {model_name}: {msg}")
            progress_bar.progress(40)
        elif status == "GENERATING":
            status_text.warning(f"⚙️ {model_name}: {msg}")
            progress_bar.progress(70)
        elif status == "COMPLETED":
            status_text.success(f"✅ {model_name}: Ready!")
            progress_bar.progress(100)
            time.sleep(0.5)
            status_text.empty() 
            progress_bar.empty()
            return APIClient.get_audio_result(job_id)
        elif status == "FAILED":
            status_text.error(f"{model_name} Error: {err}")
            return None
        
        time.sleep(1)