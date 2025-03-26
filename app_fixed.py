import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime
import requests
import os

# Define area coordinates (needed for examples)
area_coordinates = {
    "Northern Quarter": {"lat": 53.4831, "lon": -2.2317},
    "Ancoats": {"lat": 53.4847, "lon": -2.2248},
    "Spinningfields": {"lat": 53.4794, "lon": -2.2523},
    "Deansgate": {"lat": 53.4796, "lon": -2.2484},
    "Piccadilly": {"lat": 53.4808, "lon": -2.2426}
}

# Page Configuration - start with sidebar expanded
st.set_page_config(
    page_title="beem",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"  # Sidebar always expanded
)

# Initialize session state variables for analysis flow
if 'analyze' not in st.session_state:
    st.session_state.analyze = False

if 'selected_area' not in st.session_state:
    st.session_state.selected_area = "Northern Quarter"

if 'day_type' not in st.session_state:
    st.session_state.day_type = "Weekday"

# Basic CSS
st.markdown("""
<style>
    /* Main theme colors */
    h1, h2, h3 {
        color: #FF7E33 !important;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #FF7E33 !important;
        color: white !important;
        border: none !important;
    }
    
    /* Hero title styling */
    .hero-title {
        font-size: 72px !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #FF7E33, #FF9945);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.title("beem.")
    st.markdown("### ROUTE ANALYSIS CONTROLS")
    
    st.markdown('## Route Options')
    areas = list(area_coordinates.keys())
    selected_area = st.selectbox("Select your Area", areas)
    st.session_state.selected_area = selected_area
    
    st.markdown('### Time Options')
    day_type = st.radio("Day type", ["Weekday", "Weekend"])
    st.session_state.day_type = day_type
    
    st.info("**Click the button below to analyze!** ⬇️")
    
    if st.button("ANALYZE ROUTE", type="primary", use_container_width=True):
        st.session_state.analyze = True
        st.rerun()
    
    # About section in sidebar
    with st.expander("About Beem"):
        st.markdown("""
        **Beem Mobile Billboard Solutions**
        
        We help businesses reach their audience through eye-catching mobile billboards carried by cyclists.
        
        Our approach is:
        - 🌿 Eco-friendly
        - 💰 Cost-effective
        - 🎯 Highly targeted
        - 📱 Engaging
        - 📊 Data-driven
        """)

# Main content - Analysis or Home page
if st.session_state.analyze:
    # Analysis page
    st.title(f"Route Analysis for {st.session_state.selected_area}")
    st.subheader(f"Analysis for {st.session_state.day_type}")
    
    # Placeholder visualization and analysis
    st.write("Route analysis loaded successfully!")
    
    # Display map placeholder
    st.subheader("Route Map")
    map_placeholder = st.empty()
    map_placeholder.info("Map would display here in the full application.")
    
    # Display analytics placeholders
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Audience Reach")
        st.metric("Estimated Impressions", "4,250", "+15%")
    
    with col2:
        st.subheader("Optimal Times")
        st.metric("Best Hours", "12-2 PM, 5-7 PM")
    
    # Back to home button
    if st.button("Back to Home"):
        st.session_state.analyze = False
        st.rerun()
        
else:
    # Home page
    st.markdown('<h1 class="hero-title">beem.</h1>', unsafe_allow_html=True)
    
    # Start analysis button (no sidebar toggle button)
    if st.button("START ANALYSIS 🚀", type="primary", use_container_width=True):
        st.session_state.analyze = True
        st.rerun()
    
    # Features section
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📢 Optimize your advertising impact")
    
    # Feature cards in columns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 📍 Targeted Routes
        Identify the most effective cycling routes for maximum visibility based on pedestrian traffic.
        """)
        
    with col2:
        st.markdown("""
        ### ⏱️ Optimal Timing
        Determine the best times to deploy your mobile billboards for the highest impact.
        """)
