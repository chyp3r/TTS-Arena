import streamlit as st
from ui.dashboard.component.status import poll_and_wait

def render_results_grid(active_jobs):
    for i in range(0, len(active_jobs), 2):
        cols = st.columns(2)
        
        model_1, job_1 = active_jobs[i]
        with cols[0]:
            st.subheader(f"#{i+1} {model_1}")
            audio_bytes = poll_and_wait(job_1, model_1, cols[0])
            
            if audio_bytes:
                st.audio(audio_bytes, format="audio/wav")

        if i + 1 < len(active_jobs):
            model_2, job_2 = active_jobs[i+1]
            with cols[1]:
                st.subheader(f"#{i+2} {model_2}")
                audio_bytes = poll_and_wait(job_2, model_2, cols[1])
                
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/wav")
        
        st.markdown("---")