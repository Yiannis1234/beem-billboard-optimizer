import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(page_title="Beem Billboard Optimizer", page_icon="🚲", layout="wide")

# Custom CSS for orange theme
st.markdown("""
<style>
    .main-header {color: #FF9D45 !important; font-weight: 600}
    div.stButton > button {background-color: #FF9D45; color: white; border: none}
    div.stButton > button:hover {background-color: #FFB673}
    .css-1aumxhk {background-color: #FFF1E6} /* Sidebar background */
    .css-18e3th9 {padding-top: 2rem; padding-bottom: 10rem; padding-left: 5rem; padding-right: 5rem}
    h1, h2, h3, h4 {color: #FF9D45 !important}
    .stProgress .st-bo {background-color: #FF9D45}
    .stTabs [aria-selected="true"] {background-color: #FFF1E6; color: #FF9D45 !important}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🚲 Beem Billboard Route Optimizer</h1>', unsafe_allow_html=True)
st.markdown("Optimize your mobile billboard routes for maximum engagement")

# Sidebar
with st.sidebar:
    st.markdown('<h2 style="color: #FF9D45">Route Options</h2>', unsafe_allow_html=True)
    
    # Area selection
    area = st.selectbox(
        "Select Area",
        ["Northern Quarter", "City Centre", "Ancoats", "Piccadilly"]
    )
    
    # Time selection
    st.markdown('<h3 style="color: #FF9D45; margin-top: 20px">Time Options</h3>', unsafe_allow_html=True)
    time_option = st.radio("Select time", ["Current time", "Custom time"])
    
    if time_option == "Custom time":
        date = st.date_input("Date", datetime.now())
        hour = st.slider("Hour", 0, 23, 12)
        selected_time = f"{date} at {hour}:00"
    else:
        selected_time = "Current time"
    
    # Analysis button
    analyze = st.button("Analyze Route", type="primary")
    
    # About section
    with st.expander("About Beem"):
        st.markdown("""
        <div style="color: #FF9D45; font-weight: bold; margin-bottom: 10px">Beem Mobile Billboard Solutions</div>
        
        We help businesses reach their audience through eye-catching mobile billboards carried by cyclists.
        
        Our approach is:
        - 🌿 Eco-friendly
        - 💰 Cost-effective
        - 🎯 Highly targeted
        """, unsafe_allow_html=True)

# Main content
tabs = st.tabs(["Route Analysis", "Map & Visualization", "Historical Data", "Best Times"])

# Tab 1: Route Analysis
with tabs[0]:
    st.markdown(f'<h2 style="color: #FF9D45">Analysis for {area}</h2>', unsafe_allow_html=True)
    
    if analyze:
        with st.spinner("Analyzing route data..."):
            # Simple progress simulation with orange color
            progress = st.progress(0)
            for i in range(100):
                # Update progress bar
                progress.progress(i + 1)
                import time
                time.sleep(0.01)
            
            st.success("Analysis complete!")
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Weather", "Sunny", "+2°C")
            with col2:
                st.metric("Foot Traffic", "High", "+15%")
            with col3:
                st.metric("Engagement Score", "87/100", "+5")
    else:
        st.info("Select options and click 'Analyze Route' to see results.")

# Tab 2: Map & Visualization
with tabs[1]:
    st.markdown('<h2 style="color: #FF9D45">Map & Visualization</h2>', unsafe_allow_html=True)
    
    if analyze:
        # Sample map
        map_data = pd.DataFrame(
            {'lat': [53.4808], 'lon': [-2.2426]}
        )
        st.map(map_data)
    else:
        st.info("Select options and click 'Analyze Route' to see the map.")

# Tab 3: Historical Data
with tabs[2]:
    st.markdown('<h2 style="color: #FF9D45">Historical Engagement Data</h2>', unsafe_allow_html=True)
    
    if analyze:
        # Sample chart
        chart_data = pd.DataFrame(
            np.random.randn(7, 3),
            columns=['Engagement', 'Foot Traffic', 'Weather Score']
        )
        st.line_chart(chart_data)
    else:
        st.info("Select options and click 'Analyze Route' to see historical data.")

# Tab 4: Best Times
with tabs[3]:
    st.markdown('<h2 style="color: #FF9D45">Best Times to Display</h2>', unsafe_allow_html=True)
    
    if analyze:
        st.markdown('<h3 style="color: #FF9D45">Recommended Times:</h3>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background-color: #FFF1E6; padding: 15px; border-radius: 5px; margin-top: 10px">
            <div style="color: #FF9D45; font-weight: bold">1. Friday at 5:00 PM</div>
            <div style="color: #FF9D45; font-weight: bold; margin-top: 10px">2. Saturday at 2:00 PM</div>
            <div style="color: #FF9D45; font-weight: bold; margin-top: 10px">3. Sunday at 12:00 PM</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Select options and click 'Analyze Route' to see recommended times.")

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #FF9D45">© 2025 Beem Mobile Billboard Solutions</div>', unsafe_allow_html=True)