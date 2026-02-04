import streamlit as st

def render_model_manager(all_models):
    if "benchmark_models" not in st.session_state:
        st.session_state.benchmark_models = []

    with st.sidebar:
        st.header("Model Manager")
        
        selected_to_add = st.selectbox("Select a Model:", all_models)
        
        col_add, col_clear = st.columns(2)
        
        with col_add:
            if st.button("➕ Add", use_container_width=True):
                st.session_state.benchmark_models.append(selected_to_add)
        
        with col_clear:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.benchmark_models = []

        st.divider()
        st.subheader("Selected Models:")
        
        if not st.session_state.benchmark_models:
            st.caption("No models added yet.")
        else:
            for i, model in enumerate(st.session_state.benchmark_models):
                st.markdown(f"**{i+1}.** {model}")