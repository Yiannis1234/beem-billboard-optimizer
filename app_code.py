import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import requests
import time as time_module

# Import the BeemDataCollector from the src directory
from src.data.data_collector import BeemDataCollector

# Define config with API keys (you can replace 'demo_key' with actual keys later)
config = {
    'weather_api_key': 'demo_key',  # Replace with your WeatherAPI.com key
    'traffic_api_key': 'demo_key'   # Replace with your TomTom API key
}

# Initialize the data collector
data_collector = BeemDataCollector(config)

# Define area coordinates (Manchester areas)
area_coordinates = {
    "Northern Quarter": {"latitude": 53.4831, "longitude": -2.2367, "zone_id": "northern_quarter"},
    "City Centre": {"latitude": 53.4808, "longitude": -2.2426, "zone_id": "city_centre"},
    "Ancoats": {"latitude": 53.4841, "longitude": -2.2269, "zone_id": "ancoats"},
    "Piccadilly": {"latitude": 53.4779, "longitude": -2.2399, "zone_id": "piccadilly"},
    "Deansgate": {"latitude": 53.4772, "longitude": -2.2481, "zone_id": "deansgate"},
    "Media City": {"latitude": 53.4727, "longitude": -2.2984, "zone_id": "media_city"},
    "Oxford Road": {"latitude": 53.4710, "longitude": -2.2376, "zone_id": "oxford_road"},
    "Spinningfields": {"latitude": 53.4802, "longitude": -2.2516, "zone_id": "spinningfields"}
}

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
    .highlight {background-color: #FFF1E6; padding: 10px; border-radius: 5px}
    .time-card {background-color: #FFF1E6; padding: 15px; border-radius: 5px; margin-top: 10px}
    .time-title {color: #FF9D45; font-weight: bold; margin-bottom: 5px}
    .time-detail {margin-left: 20px; margin-bottom: 10px}
    .traffic-box {background-color: #FFF1E6; padding: 15px; border-radius: 5px; margin-top: 10px}
    .weather-box {background-color: #FFF1E6; padding: 15px; border-radius: 5px; margin-top: 10px}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🚲 Beem Billboard Route Optimizer</h1>', unsafe_allow_html=True)
st.markdown("Optimize your mobile billboard routes for maximum engagement")

# Sidebar
with st.sidebar:
    st.markdown('<h2 style="color: #FF9D45">Route Options</h2>', unsafe_allow_html=True)
    
    # Area selection - EXPANDED LIST
    areas = list(area_coordinates.keys())
    
    area = st.selectbox(
        "Select Area",
        areas
    )
    
    # Time selection
    st.markdown('<h3 style="color: #FF9D45; margin-top: 20px">Time Options</h3>', unsafe_allow_html=True)
    time_option = st.radio("Select time", ["Current time", "Custom time"])
    
    if time_option == "Custom time":
        date = st.date_input("Date", datetime.now())
        hour = st.slider("Hour", 0, 23, 12)
        selected_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=hour)
    else:
        selected_time = datetime.now()
    
    # Day type (new)
    day_type = st.radio("Day type", ["Weekday", "Weekend"])
    
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
        - 📱 Engaging
        - 📊 Data-driven
        """, unsafe_allow_html=True)

# Function to get weather icon based on condition
def get_weather_icon(condition):
    condition = condition.lower()
    if 'sunny' in condition or 'clear' in condition:
        return "☀️"  # Sunny
    elif 'cloud' in condition or 'overcast' in condition:
        return "☁️"  # Cloudy
    elif 'rain' in condition or 'drizzle' in condition:
        return "🌧️"  # Rainy
    elif 'snow' in condition:
        return "❄️"  # Snowy
    elif 'storm' in condition or 'thunder' in condition:
        return "⛈️"  # Storm
    elif 'fog' in condition or 'mist' in condition:
        return "🌫️"  # Foggy
    else:
        return "🌤️"  # Partly cloudy (default)

# Function to get traffic status icon and text
def get_traffic_status(congestion_level):
    if congestion_level < 0.3:
        return "🟢", "Light traffic"
    elif congestion_level < 0.6:
        return "🟡", "Moderate traffic"
    else:
        return "🔴", "Heavy traffic"

# Function to show analysis progress
def show_analysis_progress():
    progress = st.progress(0)
    # Show a series of steps for feedback
    steps = [
        "Collecting weather data...",
        "Analyzing traffic conditions...",
        "Calculating pedestrian density...",
        "Estimating engagement metrics...",
        "Optimizing route timing...",
        "Finalizing recommendations..."
    ]
    
    status_text = st.empty()
    details_text = st.empty()
    
    for i, step in enumerate(steps):
        status_text.text(f"Step {i+1}/{len(steps)}: {step}")
        details_text.text("Processing...")
        progress.progress((i+1)/len(steps))
        time_module.sleep(0.5)
        
    status_text.text("Analysis complete!")
    details_text.empty()
    return True

# Main content with expanded tabs
tabs = st.tabs(["Route Analysis", "Map & Visualization", "Historical Data", "Best Times", "Demographics"])

# Tab 1: Route Analysis
with tabs[0]:
    st.markdown(f'<h2 style="color: #FF9D45">Analysis for {area}</h2>', unsafe_allow_html=True)
    
    if analyze:
        with st.spinner("Analyzing route data..."):
            # Run the analysis progress simulation
            analysis_complete = show_analysis_progress()
            
            # Get actual data for the selected area
            selected_area_data = area_coordinates[area]
            
            # Fetch real weather and traffic data using the data collector
            integrated_data = data_collector.integrate_data(
                selected_area_data, 
                selected_time
            )
            
            weather_data = integrated_data['weather']
            traffic_data = integrated_data['traffic']
            pedestrian_density = integrated_data['pedestrian_density']
            
            # Calculate engagement score (example formula)
            base_score = 60
            weather_modifier = max(0, 20 - abs(weather_data['temperature'] - 20))  # Optimal around 20°C
            traffic_modifier = (1 - traffic_data['congestion_level']) * 15  # Lower congestion is better
            pedestrian_modifier = pedestrian_density * 25  # Higher density is better
            
            engagement_score = min(100, base_score + weather_modifier + traffic_modifier + pedestrian_modifier)
            
            # Weather status
            weather_icon = get_weather_icon(weather_data['condition'])
            
            # Traffic status
            traffic_icon, traffic_status = get_traffic_status(traffic_data['congestion_level'])
            
            st.success("Analysis complete!")
            
            # Display metrics with real data
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"Weather", 
                         f"{weather_data['temperature']:.1f}°C", 
                         f"{weather_data['condition']}")
                st.markdown(
                    f'<div class="highlight"><strong>Exact temperature:</strong> {weather_data["temperature"]:.1f}°C<br>Wind: {weather_data["wind_speed"]:.1f} km/h<br>Precipitation: {weather_data["precipitation"]:.1f} mm</div>', 
                    unsafe_allow_html=True
                )
                
            with col2:
                st.metric(f"Traffic {traffic_icon}", 
                          traffic_status, 
                          f"{int(traffic_data['flow_speed'])} km/h current speed")
                
                congestion_pct = int(traffic_data['congestion_level'] * 100)
                st.markdown(
                    f'<div class="highlight">Congestion: {congestion_pct}%<br>Free flow: {int(traffic_data["free_flow_speed"])} km/h</div>', 
                    unsafe_allow_html=True
                )
                
            with col3:
                pedestrian_rating = "High" if pedestrian_density > 0.7 else "Medium" if pedestrian_density > 0.4 else "Low"
                st.metric("Engagement Score", f"{engagement_score:.0f}/100", f"{pedestrian_rating} foot traffic")
                st.markdown(
                    f'<div class="highlight">Pedestrian density: {int(pedestrian_density*100)}%<br>Estimated views: {int(pedestrian_density*1000)}/hr</div>', 
                    unsafe_allow_html=True
                )
            
            # Additional insights
            st.subheader("Route Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="traffic-box">', unsafe_allow_html=True)
                st.markdown("#### 🚦 Traffic Conditions")
                st.markdown(f"**Current Speed:** {int(traffic_data['flow_speed'])} km/h")
                st.markdown(f"**Free Flow Speed:** {int(traffic_data['free_flow_speed'])} km/h")
                st.markdown(f"**Congestion Level:** {int(traffic_data['congestion_level']*100)}%")
                
                # Traffic rating
                if traffic_data['congestion_level'] < 0.3:
                    st.markdown("⭐⭐⭐⭐⭐ Excellent - Very light traffic")
                elif traffic_data['congestion_level'] < 0.5:
                    st.markdown("⭐⭐⭐⭐ Good - Manageable traffic")
                elif traffic_data['congestion_level'] < 0.7:
                    st.markdown("⭐⭐⭐ Average - Moderate congestion")
                else:
                    st.markdown("⭐⭐ Challenging - Heavy traffic")
                    
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col2:
                st.markdown('<div class="weather-box">', unsafe_allow_html=True)
                st.markdown(f"#### {weather_icon} Weather Conditions")
                st.markdown(f"**Exact Temperature:** {weather_data['temperature']:.1f}°C")
                st.markdown(f"**Condition:** {weather_data['condition']}")
                st.markdown(f"**Wind Speed:** {weather_data['wind_speed']:.1f} km/h")
                st.markdown(f"**Precipitation:** {weather_data['precipitation']:.1f} mm")
                
                # Weather rating for billboard
                if weather_data['precipitation'] < 0.5 and weather_data['wind_speed'] < 20:
                    st.markdown("⭐⭐⭐⭐⭐ Excellent - Ideal for billboard visibility")
                elif weather_data['precipitation'] < 2 and weather_data['wind_speed'] < 30:
                    st.markdown("⭐⭐⭐⭐ Good - Good visibility conditions")
                elif weather_data['precipitation'] < 5 and weather_data['wind_speed'] < 40:
                    st.markdown("⭐⭐⭐ Average - Acceptable conditions")
                else:
                    st.markdown("⭐⭐ Challenging - Poor visibility possible")
                    
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Select options and click 'Analyze Route' to see results.")

# Tab 2: Map & Visualization
with tabs[1]:
    st.markdown('<h2 style="color: #FF9D45">Map & Visualization</h2>', unsafe_allow_html=True)
    
    if analyze:
        # Enhanced map with multiple points
        map_data = pd.DataFrame({
            'lat': [53.4808, 53.4831, 53.4751, 53.4772, 53.4795],
            'lon': [-2.2426, -2.2362, -2.2282, -2.2387, -2.2451],
            'location': ['Start', 'Stop 1', 'Stop 2', 'Stop 3', 'End']
        })
        
        # Add the selected area as a highlighted point
        selected_coords = area_coordinates[area]
        highlighted_point = pd.DataFrame({
            'lat': [selected_coords['latitude']],
            'lon': [selected_coords['longitude']], 
            'location': [f"Selected: {area}"]
        })
        
        # Combine dataframes
        all_points = pd.concat([highlighted_point, map_data])
        
        st.map(all_points)
        
        # Engagement chart
        st.subheader("Hourly Engagement Forecast")
        hours = list(range(9, 21))
        engagement = [45, 50, 65, 75, 70, 68, 72, 85, 90, 87, 80, 60]
        
        chart_data = pd.DataFrame({
            'Hour': hours,
            'Engagement': engagement
        })
        
        st.line_chart(chart_data, x='Hour', y='Engagement')
    else:
        st.info("Select options and click 'Analyze Route' to see the map.")

# Tab 3: Historical Data
with tabs[2]:
    st.markdown('<h2 style="color: #FF9D45">Historical Engagement Data</h2>', unsafe_allow_html=True)
    
    if analyze:
        # Enhanced chart with labeled data
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        engagement = [65, 68, 70, 72, 85, 90, 80]
        foot_traffic = [70, 75, 70, 75, 85, 95, 85]
        weather = [60, 65, 70, 75, 80, 85, 75]
        
        chart_data = pd.DataFrame({
            'Day': days,
            'Engagement': engagement,
            'Foot Traffic': foot_traffic,
            'Weather Score': weather
        })
        
        st.line_chart(chart_data, x='Day')
        
        st.subheader("Top Performing Days")
        st.markdown("1. Saturday: 90/100")
        st.markdown("2. Friday: 85/100")
        st.markdown("3. Sunday: 80/100")
    else:
        st.info("Select options and click 'Analyze Route' to see historical data.")

# Tab 4: Best Times
with tabs[3]:
    st.markdown('<h2 style="color: #FF9D45">Best Times to Display</h2>', unsafe_allow_html=True)
    
    if analyze:
        st.markdown('<h3 style="color: #FF9D45">Recommended Times:</h3>', unsafe_allow_html=True)
        
        # Best times displayed correctly with CSS classes
        st.markdown('<div class="time-card">', unsafe_allow_html=True)
        
        # Time 1
        st.markdown('<div class="time-title">1. Friday at 5:00 PM - 7:00 PM</div>', unsafe_allow_html=True)
        st.markdown('<div class="time-detail">After-work crowds (95/100)</div>', unsafe_allow_html=True)
        
        # Time 2
        st.markdown('<div class="time-title">2. Saturday at 2:00 PM - 4:00 PM</div>', unsafe_allow_html=True)
        st.markdown('<div class="time-detail">Shopping hours (92/100)</div>', unsafe_allow_html=True)
        
        # Time 3
        st.markdown('<div class="time-title">3. Wednesday at 12:00 PM</div>', unsafe_allow_html=True)
        st.markdown('<div class="time-detail">Lunch break (88/100)</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add a daily engagement chart
        st.subheader("Daily Engagement Patterns")
        hours = list(range(7, 23))  # 7 AM to 10 PM
        
        # Different patterns for different days
        weekday_pattern = [30, 55, 65, 60, 70, 85, 80, 70, 65, 75, 85, 90, 75, 60, 40, 30]
        weekend_pattern = [20, 30, 45, 60, 75, 85, 90, 92, 88, 80, 70, 65, 55, 45, 35, 25]
        
        engagement_data = pd.DataFrame({
            'Hour': hours,
            'Weekday': weekday_pattern,
            'Weekend': weekend_pattern
        })
        
        st.line_chart(engagement_data, x='Hour', y=['Weekday', 'Weekend'])
        
    else:
        st.info("Select options and click 'Analyze Route' to see recommended times.")

# Tab 5: Demographics (New)
with tabs[4]:
    st.markdown('<h2 style="color: #FF9D45">Demographics Analysis</h2>', unsafe_allow_html=True)
    
    if analyze:
        st.subheader(f"Demographic Profile for {area}")
        
        # Demographics info based on area
        if area in ["Northern Quarter", "Oxford Road"]:
            audience = "Young, creative, students"
            age = "18-34 (65%)"
            interests = "Arts, Food, Music, Fashion"
        elif area in ["City Centre", "Deansgate"]:
            audience = "Mixed, tourists, shoppers"
            age = "25-45 (55%)"
            interests = "Shopping, Food, Entertainment"
        elif area in ["Media City", "Spinningfields"]:
            audience = "Professionals, business"
            age = "25-50 (75%)"
            interests = "Technology, Business, Food"
        else:
            audience = "Mixed urban"
            age = "25-45 (60%)"
            interests = "Various"
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="highlight">', unsafe_allow_html=True)
            st.markdown("#### Primary Audience")
            st.markdown(f"**Type:** {audience}")
            st.markdown(f"**Age Range:** {age}")
            st.markdown(f"**Key Interests:** {interests}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="highlight">', unsafe_allow_html=True)
            st.markdown("#### Recommended Targeting")
            st.markdown("- Digital products")
            st.markdown("- Food and dining")
            st.markdown("- Entertainment events")
            st.markdown("- Use QR codes for interaction")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Select options and click 'Analyze Route' to see demographic analysis.")

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #FF9D45">© 2025 Beem Mobile Billboard Solutions | hello@beembillboards.com</div>', unsafe_allow_html=True)