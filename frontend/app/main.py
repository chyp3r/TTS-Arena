import streamlit as st
from ui.dashboard.dashboard import render_dashboard

if __name__ == "__main__":
    st.set_page_config(
        page_title="TTS Arena",
        layout="wide",
        page_icon="🎙️"
    )
    render_dashboard()