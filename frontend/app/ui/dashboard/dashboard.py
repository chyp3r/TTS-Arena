import streamlit as st
from service.clinent import APIClient

from ui.dashboard.component.sidebar import render_model_manager
from ui.dashboard.component.grid import render_results_grid

def render_dashboard():
    st.title("TTS Benchmark Arena")

    with st.spinner("Loading models..."):
        all_models = APIClient.get_models()
    
    if not all_models:
        st.error("Backend unreachable. Is Docker running?")
        st.stop()
    
    render_model_manager(all_models)

    text_input = st.text_area("Enter Text:", "Yapay zeka sistemleri artık insan gibi konuşabiliyor.", height=100)
    
    selected_models = st.session_state.get("benchmark_models", [])
    model_count = len(selected_models)
    
    if st.button(f"Run Benchmark ({model_count} Models)", use_container_width=True, type="primary"):
        
        if model_count == 0:
            st.warning("Please add at least one model from the sidebar!")
            st.stop()

        active_jobs = [] 
        for model in selected_models:
            job_id = APIClient.start_generation(text_input, model)
            active_jobs.append((model, job_id))
            
        render_results_grid(active_jobs)