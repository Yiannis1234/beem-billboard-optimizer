import streamlit as st
import pandas as pd
import numpy as np

# Define area coordinates (needed for examples)
area_coordinates = {
    "Northern Quarter": {"lat": 53.4831, "lon": -2.2317},
    "Ancoats": {"lat": 53.4847, "lon": -2.2248},
    "Spinningfields": {"lat": 53.4794, "lon": -2.2523},
    "Deansgate": {"lat": 53.4796, "lon": -2.2484},
    "Piccadilly": {"lat": 53.4808, "lon": -2.2426}
}

# IMPORTANT: This app must be run with:
#   streamlit run fresh_app.py
# NOT with:
#   python fresh_app.py

# Simple page config
st.set_page_config(
    page_title="beem",
    page_icon="🚲",
    initial_sidebar_state="expanded"  # Start with sidebar expanded
)

# Basic CSS
st.markdown("""
<style>
    h1, h2, h3 {
        color: #FF7E33 !important;
    }
    
    .stButton button {
        background-color: #FF7E33 !important;
        color: white !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Setup sidebar content
with st.sidebar:
    st.title("beem")
    st.header("Menu Options")
    
    # Sidebar options
    selected_area = st.selectbox("Select Area:", 
                         list(area_coordinates.keys()))
    
    day_type = st.radio("Day Type:", ["Weekday", "Weekend"])
    
    analyze = st.button("Analyze Route", use_container_width=True)
    if analyze:
        st.success("Analysis started!")

# Main page content
st.title("beem")
st.subheader("Mobile Advertising Platform")

# Main content
st.write("Welcome to the beem advertising platform!")
st.write("Use the sidebar to configure your advertising routes.")

# Just a simple hint about the sidebar
st.info("💡 The sidebar on the left contains all your options and controls.") 