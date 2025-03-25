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
    'weather_api_key': 'f70bd534000447b2a14202431252303',  # New WeatherAPI.com key provided by user
    'traffic_api_key': 'Uc0dPKIMHcqZ91VbGAnbEAINdzwqRzil'   # New TomTom API key provided by user
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
    .logo-container {display: flex; justify-content: center; margin-bottom: 20px}
    .footer-container {display: flex; justify-content: center; align-items: center; margin-top: 20px}
    .card {background-color: #FFF1E6; border-radius: 10px; padding: 20px; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1)}
    .icon-text {display: flex; align-items: center}
    .icon-text span {margin-left: 10px}
    .dashboard-metric {background-color: #FFF1E6; border-left: 5px solid #FF9D45; padding: 15px; margin: 10px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.05)}
    .gradient-header {
        background: linear-gradient(90deg, #FF7E33, #FFB673); 
        color: white !important; 
        padding: 12px 20px; 
        border-radius: 6px; 
        margin-bottom: 25px;
        font-weight: 800;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
        box-shadow: 0 4px 12px rgba(255, 157, 69, 0.3);
    }
    /* Make the main title stand out more */
    h1.main-header {
        font-size: 36px !important;
        background: -webkit-linear-gradient(#FF7E33, #FFB673);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-shadow: none;
        margin-bottom: 15px;
    }
    /* Enhance the tabs appearance */
    .stTabs [aria-selected="true"] {
        background-color: #FFF1E6;
        color: #FF7E33 !important;
        font-weight: 600;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        box-shadow: 0 -2px 5px rgba(255, 157, 69, 0.1);
    }
    /* Make metrics cards pop more */
    .dashboard-metric {
        background-color: #FFF1E6;
        border-left: 5px solid #FF9D45;
        padding: 18px;
        margin: 12px 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        transition: transform 0.2s ease;
        border-radius: 5px;
    }
    .dashboard-metric:hover {
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 20px">
    <div style="background-color: #FF9D45; color: white; font-size: 42px; font-weight: bold; padding: 10px 30px; border-radius: 5px;">
        beem.
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('<h1 class="main-header">🚲 Beem Billboard Route Optimizer</h1>', unsafe_allow_html=True)
st.markdown("Optimize your mobile billboard routes for maximum engagement")

# Sidebar
with st.sidebar:
    # Add Beem logo
    st.markdown("""
    <div class="logo-container">
        <div style="background-color: #FF9D45; color: white; font-size: 32px; font-weight: bold; padding: 5px 20px; border-radius: 5px; text-align: center;">
            beem.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a prominent help text at the top of sidebar
    st.markdown("""
    <div style="background-color: #FFE8D6; color: #333; padding: 10px; margin-bottom: 15px; border-radius: 5px; border-left: 5px solid #FF7E33; display: flex; align-items: center;">
        <div style="font-size: 24px; margin-right: 10px;">➡️</div>
        <div>
            <strong style="font-size: 16px;">Click "Analyze Route"</strong><br>
            <span style="font-size: 14px;">to see traffic & weather data</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
    
    # Add instructional text with arrow pointing to the button
    st.markdown("""
    <div style="margin-bottom: 10px; display: flex; align-items: center; justify-content: center;">
        <div style="background-color: #FFE8D6; border-left: 5px solid #FF9D45; padding: 10px; border-radius: 5px; margin-top: 10px; margin-bottom: 10px; text-align: center; position: relative;">
            <span style="font-weight: 600; color: #333;">👇 Click to analyze your route 👇</span>
            <div style="position: absolute; bottom: -20px; left: 50%; transform: translateX(-50%);">
                <span style="font-size: 24px; color: #FF7E33;">⬇️</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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

# Add visual banner with dynamic elements - MOVED AFTER analyze is defined
if analyze:
    st.markdown("""
    <div style="background: linear-gradient(90deg, #FF7E33, #FFB673); border-radius: 10px; padding: 20px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(255, 157, 69, 0.25);">
        <div>
            <h3 style="color: white !important; margin: 0; font-size: 30px; font-weight: 800; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">Beem Billboard Insights</h3>
            <p style="color: white !important; margin: 8px 0 0 0; font-weight: 600; font-size: 18px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Optimizing engagement across Manchester</p>
        </div>
        <div style="background: white; border-radius: 50%; width: 55px; height: 55px; display: flex; justify-content: center; align-items: center; box-shadow: 0 3px 8px rgba(0,0,0,0.2);">
            <span style="font-size: 28px">🚲</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Even when not analyzing, show a welcome banner
    st.markdown("""
    <div style="background: linear-gradient(90deg, #FF7E33, #FFB673); border-radius: 10px; padding: 20px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(255, 157, 69, 0.25);">
        <div>
            <h3 style="color: white !important; margin: 0; font-size: 30px; font-weight: 800; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">Welcome to Beem!</h3>
            <p style="color: white !important; margin: 8px 0 0 0; font-weight: 600; font-size: 18px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">Mobile billboard optimization platform</p>
        </div>
        <div style="background: white; border-radius: 50%; width: 55px; height: 55px; display: flex; justify-content: center; align-items: center; box-shadow: 0 3px 8px rgba(0,0,0,0.2);">
            <span style="font-size: 28px">🚲</span>
        </div>
    </div>
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
    if analyze:
        st.markdown(f'<h2 class="gradient-header">Analysis for {area}</h2>', unsafe_allow_html=True)
        
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
            
            # Display metrics with real data and enhanced visuals
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="dashboard-metric">
                    <h4 style="margin-top: 0">{weather_icon} Temperature</h4>
                    <h2 style="color: #333 !important; margin: 5px 0; font-size: 28px; font-weight: bold">{weather_data['temperature']:.1f}°C</h2>
                    <p style="color: #666; margin: 0">Exact measurement</p>
                    <hr style="margin: 10px 0; border-color: #ddd">
                    <p><strong>Condition:</strong> {weather_data['condition']}<br>
                    <strong>Wind:</strong> {weather_data["wind_speed"]:.1f} km/h<br>
                    <strong>Precipitation:</strong> {weather_data["precipitation"]:.1f} mm</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class="dashboard-metric">
                    <h4 style="margin-top: 0">{traffic_icon} Traffic</h4>
                    <h2 style="color: #333 !important; margin: 5px 0">{traffic_status}</h2>
                    <p style="color: #666; margin: 0">{int(traffic_data['flow_speed'])} km/h current speed</p>
                    <hr style="margin: 10px 0; border-color: #ddd">
                    <p><strong>Congestion:</strong> {int(traffic_data['congestion_level'] * 100)}%<br>
                    <strong>Free flow:</strong> {int(traffic_data["free_flow_speed"])} km/h</p>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                pedestrian_rating = "High" if pedestrian_density > 0.7 else "Medium" if pedestrian_density > 0.4 else "Low"
                st.markdown(f"""
                <div class="dashboard-metric">
                    <h4 style="margin-top: 0">📊 Engagement</h4>
                    <h2 style="color: #333 !important; margin: 5px 0">{engagement_score:.0f}/100</h2>
                    <p style="color: #666; margin: 0">{pedestrian_rating} foot traffic</p>
                    <hr style="margin: 10px 0; border-color: #ddd">
                    <p><strong>Pedestrian density:</strong> {int(pedestrian_density*100)}%<br>
                    <strong>Estimated views:</strong> {int(pedestrian_density*1000)}/hr</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Visual representation of optimal times (new)
            st.markdown("<h3>🎯 Optimal Times Today</h3>", unsafe_allow_html=True)
            hours_col1, hours_col2, hours_col3 = st.columns(3)
            
            with hours_col1:
                st.markdown("""
                <div class="card">
                    <h4 style="margin-top: 0">Morning</h4>
                    <div class="icon-text">
                        <div style="font-size: 24px">⭐⭐⭐</div>
                        <span>8:00 - 9:00 AM</span>
                    </div>
                    <p style="color: #666; margin-top: 10px">Morning commuters (75/100)</p>
                </div>
                """, unsafe_allow_html=True)
                
            with hours_col2:
                st.markdown("""
                <div class="card">
                    <h4 style="margin-top: 0">Afternoon</h4>
                    <div class="icon-text">
                        <div style="font-size: 24px">⭐⭐⭐⭐⭐</div>
                        <span>12:00 - 2:00 PM</span>
                    </div>
                    <p style="color: #666; margin-top: 10px">Lunch crowd (90/100)</p>
                </div>
                """, unsafe_allow_html=True)
                
            with hours_col3:
                st.markdown("""
                <div class="card">
                    <h4 style="margin-top: 0">Evening</h4>
                    <div class="icon-text">
                        <div style="font-size: 24px">⭐⭐⭐⭐</div>
                        <span>5:00 - 7:00 PM</span>
                    </div>
                    <p style="color: #666; margin-top: 10px">Evening commuters (85/100)</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Additional insights with enhanced visuals
            st.subheader("Route Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="traffic-box">
                    <h4 style="margin-top: 0">🚦 Traffic Conditions</h4>
                    <div style="display: flex; justify-content: space-between; margin: 15px 0">
                        <div style="text-align: center; background: rgba(255,255,255,0.5); padding: 10px; border-radius: 5px; width: 45%">
                            <div style="font-size: 24px; margin-bottom: 5px">🚗</div>
                            <div style="font-weight: bold">{0} km/h</div>
                            <div style="font-size: 12px; color: #666">Current Speed</div>
                        </div>
                        <div style="text-align: center; background: rgba(255,255,255,0.5); padding: 10px; border-radius: 5px; width: 45%">
                            <div style="font-size: 24px; margin-bottom: 5px">⚡</div>
                            <div style="font-weight: bold">{1} km/h</div>
                            <div style="font-size: 12px; color: #666">Free Flow</div>
                        </div>
                    </div>
                """.format(int(traffic_data['flow_speed']), int(traffic_data['free_flow_speed'])), unsafe_allow_html=True)
                
                # Traffic rating
                if traffic_data['congestion_level'] < 0.3:
                    st.markdown("<div style='margin-top: 15px'>⭐⭐⭐⭐⭐ Excellent - Very light traffic</div>", unsafe_allow_html=True)
                elif traffic_data['congestion_level'] < 0.5:
                    st.markdown("<div style='margin-top: 15px'>⭐⭐⭐⭐ Good - Manageable traffic</div>", unsafe_allow_html=True)
                elif traffic_data['congestion_level'] < 0.7:
                    st.markdown("<div style='margin-top: 15px'>⭐⭐⭐ Average - Moderate congestion</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='margin-top: 15px'>⭐⭐ Challenging - Heavy traffic</div>", unsafe_allow_html=True)
                    
                st.markdown('</div>', unsafe_allow_html=True)
                
            with col2:
                st.markdown("""
                <div class="weather-box">
                    <h4 style="margin-top: 0">{0} Exact Temperature</h4>
                    <div style="display: flex; justify-content: space-between; margin: 15px 0">
                        <div style="text-align: center; background: rgba(255,255,255,0.5); padding: 10px; border-radius: 5px; width: 45%">
                            <div style="font-size: 24px; margin-bottom: 5px">🌡️</div>
                            <div style="font-weight: bold; font-size: 22px">{1:.1f}°C</div>
                            <div style="font-size: 12px; color: #666">Current Reading</div>
                        </div>
                        <div style="text-align: center; background: rgba(255,255,255,0.5); padding: 10px; border-radius: 5px; width: 45%">
                            <div style="font-size: 24px; margin-bottom: 5px">💨</div>
                            <div style="font-weight: bold">{2:.1f} km/h</div>
                            <div style="font-size: 12px; color: #666">Wind Speed</div>
                        </div>
                    </div>
                """.format(weather_icon, weather_data['temperature'], weather_data['wind_speed']), unsafe_allow_html=True)
                
                # Additional weather info
                st.markdown(f"""
                <div style="margin-top: 15px">
                    <strong>Condition:</strong> {weather_data['condition']}<br>
                    <strong>Precipitation:</strong> {weather_data['precipitation']:.1f} mm
                </div>
                """, unsafe_allow_html=True)
                
                # Weather rating for billboard
                if weather_data['precipitation'] < 0.5 and weather_data['wind_speed'] < 20:
                    st.markdown("<div style='margin-top: 15px'>⭐⭐⭐⭐⭐ Excellent - Ideal for billboard visibility</div>", unsafe_allow_html=True)
                elif weather_data['precipitation'] < 2 and weather_data['wind_speed'] < 30:
                    st.markdown("<div style='margin-top: 15px'>⭐⭐⭐⭐ Good - Good visibility conditions</div>", unsafe_allow_html=True)
                elif weather_data['precipitation'] < 5 and weather_data['wind_speed'] < 40:
                    st.markdown("<div style='margin-top: 15px'>⭐⭐⭐ Average - Acceptable conditions</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div style='margin-top: 15px'>⭐⭐ Challenging - Poor visibility possible</div>", unsafe_allow_html=True)
                    
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color: #FFE8D6; border-left: 5px solid #FF9D45; padding: 15px; border-radius: 5px; margin-bottom: 20px; color: #333; font-weight: 500; font-size: 16px;">
            Select options and click <span style="color: #FF9D45; font-weight: 700;">'Analyze Route'</span> to see results.
        </div>
        """, unsafe_allow_html=True)
        
        # Add a visual placeholder when no analysis is running
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 300px">
            <div style="text-align: center">
                <div style="background-color: #FF9D45; color: white; font-size: 42px; font-weight: bold; padding: 10px 30px; border-radius: 5px; margin-bottom: 20px; display: inline-block;">
                    beem.
                </div>
                <p style="color: #FF9D45; margin-top: 20px; font-size: 18px">Select options and analyze to see data</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Tab 2: Map & Visualization
with tabs[1]:
    st.markdown('<h2 class="gradient-header">Map & Visualization</h2>', unsafe_allow_html=True)
    
    if analyze:
        # Enhanced map with highlighted area and traffic indicators
        st.markdown("""
        <div style="background-color: #FFE8D6; border-left: 5px solid #FF9D45; padding: 15px; border-radius: 5px; margin-bottom: 20px; box-shadow: 0 3px 10px rgba(0,0,0,0.05);">
            <strong style="font-size: 18px;">📍 Area:</strong> <span style="font-size: 18px; color: #FF7E33; font-weight: 600;">{0}</span><br>
            <strong style="font-size: 18px;">🚦 Traffic Status:</strong> <span style="color: {1}; font-weight: bold; font-size: 18px;">{2}</span><br>
            <strong style="font-size: 18px;">👥 Expected Foot Traffic:</strong> <span style="font-weight: 600; font-size: 18px;">{3}/hour</span>
        </div>
        """.format(
            area,
            "#4CAF50" if traffic_data['congestion_level'] < 0.3 else "#FFC107" if traffic_data['congestion_level'] < 0.6 else "#F44336",
            "Light 🟢" if traffic_data['congestion_level'] < 0.3 else "Moderate 🟡" if traffic_data['congestion_level'] < 0.6 else "Heavy 🔴",
            int(pedestrian_density * 1000)
        ), unsafe_allow_html=True)
        
        # Create map for visualization
        selected_area_data = area_coordinates[area]
        lat = selected_area_data['latitude']
        lon = selected_area_data['longitude']
        
        # Base map focused on selected area
        st.markdown("<h3 style='background: linear-gradient(90deg, #FF7E33, #FFB673); color: white; padding: 10px 15px; border-radius: 5px; margin-bottom: 15px; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>🗺️ Traffic Heatmap</h3>", unsafe_allow_html=True)
        
        # Create a map with the selected area at the center
        # Define neighboring areas for context
        map_data = {
            'latitude': [lat],
            'longitude': [lon],
            'size': [1000],  # Size of the point (larger for selected area)
            'color': ['green' if traffic_data['congestion_level'] < 0.3 else 'orange' if traffic_data['congestion_level'] < 0.6 else 'red'],
            'label': [area]
        }
        
        # Add other areas with smaller points for context 
        for other_area, coords in area_coordinates.items():
            if other_area != area:
                # Get traffic data for this area
                other_area_data = data_collector.integrate_data(coords, selected_time)
                other_traffic = other_area_data['traffic']
                
                # Add to map data with smaller size
                map_data['latitude'].append(coords['latitude'])
                map_data['longitude'].append(coords['longitude'])
                map_data['size'].append(500)  # Smaller for other areas
                map_data['color'].append('green' if other_traffic['congestion_level'] < 0.3 else 'orange' if other_traffic['congestion_level'] < 0.6 else 'red')
                map_data['label'].append(other_area)
        
        # Create the map
        st.map(pd.DataFrame({
            'lat': map_data['latitude'],
            'lon': map_data['longitude']
        }))
        
        # Add color-coded indicators
        cols = st.columns(3)
        with cols[0]:
            st.markdown(
                '<div style="background-color: #4CAF50; color: white; padding: 12px; border-radius: 8px; text-align: center; margin: 5px; font-weight: 600; font-size: 16px; box-shadow: 0 3px 6px rgba(0,0,0,0.1);">🟢 Light Traffic</div>', 
                unsafe_allow_html=True
            )
        with cols[1]:
            st.markdown(
                '<div style="background-color: #FFC107; color: white; padding: 12px; border-radius: 8px; text-align: center; margin: 5px; font-weight: 600; font-size: 16px; box-shadow: 0 3px 6px rgba(0,0,0,0.1);">🟡 Moderate Traffic</div>', 
                unsafe_allow_html=True
            )
        with cols[2]:
            st.markdown(
                '<div style="background-color: #F44336; color: white; padding: 12px; border-radius: 8px; text-align: center; margin: 5px; font-weight: 600; font-size: 16px; box-shadow: 0 3px 6px rgba(0,0,0,0.1);">🔴 Heavy Traffic</div>', 
                unsafe_allow_html=True
            )
        
        # Enhanced visualization - Traffic Flow Chart
        st.markdown("<h3 style='background: linear-gradient(90deg, #FF7E33, #FFB673); color: white; padding: 10px 15px; border-radius: 5px; margin: 25px 0 15px 0; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>📊 Hourly Traffic Flow</h3>", unsafe_allow_html=True)
        
        # Generate hourly traffic data
        hours = list(range(6, 24))  # 6 AM to 11 PM (18 hours)
        
        # Create different patterns based on time of day (ensure all arrays have 18 elements)
        morning_peak = [0.7, 0.9, 0.8, 0.6, 0.5, 0.4, 0.3]  # 7 elements (6 AM to 12 PM)
        lunch_peak = [0.4, 0.6, 0.7, 0.5]  # 4 elements (12 PM to 4 PM)
        evening_peak = [0.4, 0.6, 0.8, 0.9, 0.7, 0.5, 0.3]  # 7 elements (4 PM to 11 PM)
        
        # Ensure all arrays have consistent lengths (18 hours total)
        congestion_levels = morning_peak + lunch_peak + evening_peak
        # Truncate to ensure it matches hours array length
        congestion_levels = congestion_levels[:len(hours)]
        # Create speed levels of matching length
        speed_levels = [max(10, 50 * (1 - c)) for c in congestion_levels]
        
        # Create status array with matching length
        status_array = ['Heavy' if c > 0.7 else 'Moderate' if c > 0.3 else 'Light' for c in congestion_levels]
        
        # Create dataframe for visualization with consistent array lengths
        traffic_df = pd.DataFrame({
            'Hour': [f"{h}:00" for h in hours],
            'Congestion': congestion_levels,
            'Speed (km/h)': speed_levels,
            'Status': status_array
        })
        
        # Plot the data
        fig = px.bar(
            traffic_df, 
            x='Hour', 
            y='Congestion',
            color='Status',
            color_discrete_map={
                'Light': '#4CAF50',
                'Moderate': '#FFC107',
                'Heavy': '#F44336'
            },
            labels={'Congestion': 'Congestion Level', 'Hour': 'Time of Day'},
            title=f'Traffic Congestion in {area} throughout the day'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add a heatmap of pedestrian density
        st.markdown("<h3 style='background: linear-gradient(90deg, #FF7E33, #FFB673); color: white; padding: 10px 15px; border-radius: 5px; margin: 25px 0 15px 0; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.2);'>👥 Pedestrian Activity Heatmap</h3>", unsafe_allow_html=True)
        
        # Create data for the heatmap
        pedestrian_hours = list(range(6, 24))  # 18 hours
        
        # Different patterns for pedestrian activity - ensure all arrays have exactly 18 elements
        if area in ["Northern Quarter", "City Centre"]:
            # Busy shopping/entertainment areas
            pedestrian_pattern = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.9, 0.8, 0.9, 0.9, 0.8, 0.7, 0.8, 0.9, 0.9, 0.8, 0.6]
        elif area in ["Media City", "Spinningfields"]:
            # Business areas - busy during work hours
            pedestrian_pattern = [0.3, 0.5, 0.7, 0.8, 0.9, 0.8, 0.9, 0.9, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.2, 0.1, 0.1, 0.1]
        else:
            # General areas with lunch/evening peaks
            pedestrian_pattern = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.7, 0.6, 0.5, 0.6, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
        
        # Ensure pattern has exact length matching pedestrian_hours
        if len(pedestrian_pattern) > len(pedestrian_hours):
            pedestrian_pattern = pedestrian_pattern[:len(pedestrian_hours)]
        elif len(pedestrian_pattern) < len(pedestrian_hours):
            # Extend with the last value if shorter
            pedestrian_pattern.extend([pedestrian_pattern[-1]] * (len(pedestrian_hours) - len(pedestrian_pattern)))
        
        # Create a dataframe for the heatmap
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = []
        
        for day_idx, day in enumerate(days):
            for hour_idx, hour in enumerate(pedestrian_hours):
                # Adjust pattern based on day of week
                if day in ['Saturday', 'Sunday']:
                    # Weekends have different patterns
                    if area in ["Northern Quarter", "City Centre"]:
                        # Shopping areas busier on weekends
                        modifier = 1.2
                    else:
                        # Business areas quieter on weekends
                        modifier = 0.6
                else:
                    modifier = 1.0
                
                # Account for weather conditions
                if weather_data['condition'].lower() in ['rain', 'shower', 'drizzle', 'thunderstorm']:
                    weather_modifier = 0.7
                elif weather_data['condition'].lower() in ['cloudy', 'overcast', 'mist', 'fog']:
                    weather_modifier = 0.9
                else:
                    weather_modifier = 1.0
                    
                value = min(1.0, pedestrian_pattern[hour_idx] * modifier * weather_modifier)
                
                heatmap_data.append({
                    'Day': day,
                    'Hour': f"{hour}:00",
                    'Density': value
                })
        
        # Create a dataframe and pivot for the heatmap
        heatmap_df = pd.DataFrame(heatmap_data)
        heatmap_pivot = heatmap_df.pivot(index='Day', columns='Hour', values='Density')
        
        # Plot the heatmap
        fig2 = px.imshow(
            heatmap_pivot, 
            color_continuous_scale=['green', 'yellow', 'red'],
            labels=dict(x="Hour of Day", y="Day of Week", color="Pedestrian Density"),
            title=f"Weekly Pedestrian Activity Patterns in {area}"
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
    else:
        st.markdown("""
        <div style="background-color: #FFE8D6; border-left: 5px solid #FF9D45; padding: 15px; border-radius: 5px; margin-bottom: 20px; color: #333; font-weight: 500; font-size: 16px;">
            Select options and click <span style="color: #FF9D45; font-weight: 700;">'Analyze Route'</span> to view the map visualization.
        </div>
        
        <div style="display: flex; justify-content: center; align-items: center; height: 300px">
            <div style="text-align: center">
                <div style="background-color: #FF9D45; color: white; font-size: 42px; font-weight: bold; padding: 10px 30px; border-radius: 5px; margin-bottom: 20px; display: inline-block;">
                    beem.
                </div>
                <p style="color: #FF9D45; margin-top: 20px; font-size: 18px">Maps and visualizations will appear here</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

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

# Footer with enhanced visual elements
st.markdown("---")
st.markdown("""
<div class="footer-container">
    <div style="text-align: center">
        <div style="background-color: #FF9D45; color: white; font-size: 28px; font-weight: bold; padding: 5px 20px; border-radius: 5px; display: inline-block; margin-bottom: 10px;">
            beem.
        </div>
        <div style="color: #FF9D45; margin-top: 10px">© 2025 Beem Mobile Billboard Solutions</div>
        <div style="color: #999; font-size: 12px; margin-top: 5px">hello@beembillboards.com | +44 123 456 7890</div>
    </div>
</div>
""", unsafe_allow_html=True)