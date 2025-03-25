import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(page_title="Beem Billboard Optimizer", page_icon="🚲", layout="wide")

# Title
st.title("🚲 Beem Billboard Route Optimizer")
st.markdown("Optimize your mobile billboard routes for maximum engagement")

# Sidebar
with st.sidebar:
    st.header("Route Options")
    
    # Area selection
    area = st.selectbox(
        "Select Area",
        ["Northern Quarter", "City Centre", "Ancoats", "Piccadilly"]
    )
    
    # Time selection
    st.subheader("Time Options")
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
        Beem Mobile Billboard Solutions helps businesses reach their 
        audience through eye-catching mobile billboards carried by cyclists.
        
        Our approach is:
        - Eco-friendly
        - Cost-effective
        - Highly targeted
        """)

# Main content
tabs = st.tabs(["Route Analysis", "Map & Visualization", "Historical Data", "Best Times"])

# Tab 1: Route Analysis
with tabs[0]:
    st.header(f"Analysis for {area}")
    
    if analyze:
        with st.spinner("Analyzing route data..."):
            # Simple progress simulation
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
    st.header("Map & Visualization")
    
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
    st.header("Historical Engagement Data")
    
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
    st.header("Best Times to Display")
    
    if analyze:
        st.subheader("Recommended Times:")
        st.write("1. Friday at 5:00 PM")
        st.write("2. Saturday at 2:00 PM")
        st.write("3. Sunday at 12:00 PM")
    else:
        st.info("Select options and click 'Analyze Route' to see recommended times.")

# Footer
st.markdown("---")
st.caption("© 2025 Beem Mobile Billboard Solutions")