import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Beem Billboard Optimizer",
    page_icon="🚲",
    layout="wide"
)

# Simple orange button styling
st.markdown("""
<style>
.stButton > button {
    background-color: #FF7E33 !important;
    color: white !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# App title
st.title("🚲 Beem Billboard Optimizer")

# Sidebar
with st.sidebar:
    st.header("Route Configuration")
    
    # Area selection
    area = st.selectbox("Choose an area:", ["Northern Quarter", "City Centre", "Ancoats", "Piccadilly"])
    
    # Analyze button
    if st.button("Analyze Route"):
        st.success("Analysis started!")

# Main screen buttons
st.subheader("Choose an option:")

col1, col2 = st.columns(2)
with col1:
    if st.button("START ANALYSIS 🔍"):
        st.success("Analysis button clicked!")
with col2:
    if st.button("Press top left arrow to analyze ⬅️"):
        st.balloons() 