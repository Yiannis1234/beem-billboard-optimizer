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
st.set_page_config(page_title="Beem Billboard Optimizer", page_icon="🚲", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for orange theme and to fix sidebar visibility
st.markdown("""
<style>
    /* Base styling improvements */
    .stApp {
        background-color: #F9F9F9;
        background-color: rgba(255, 157, 69, 0.05);
    }
    
    /* Force sidebar to be expanded */
    .css-1d391kg {
        width: 250px !important;
    }
    
    /* Make sure sidebar is visible */
    section[data-testid="stSidebar"] {
        width: 250px !important;
        min-width: 250px !important;
        max-width: 250px !important;
        display: flex !important;
        flex-direction: column !important;
        opacity: 1 !important;
        visibility: visible !important;
        transform: none !important;
    }
    
    /* Sidebar background */
    .css-6qob1r {
        background-color: #FFF1E6 !important;
    }
    
    /* Main header and banner styling */
    h1.main-header {
        font-size: 38px !important;
        background: -webkit-linear-gradient(#FF7E33, #FFB673);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        margin-bottom: 15px;
        position: relative;
    }
    h1.main-header:after {
        content: '';
        display: block;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #FF7E33, transparent);
        margin-top: 10px;
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
    
    /* Enhanced button styling */
    .stButton button {
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    .stButton button[data-testid="baseButton-primary"] {
        background: linear-gradient(to bottom, #FF7E33, #FF9D45) !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        padding: 12px 24px !important;
        font-size: 18px !important;
        box-shadow: 0 4px 8px rgba(255, 126, 51, 0.3) !important;
    }
    .stButton button[data-testid="baseButton-primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255, 126, 51, 0.4) !important;
    }
    
    /* Map-themed containers */
    .map-card {
        background-color: white;
        background: linear-gradient(145deg, #ffffff, #fff8f2);
        border-radius: 8px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        border: 1px solid #eaeaea;
    }
    
    /* Additional utility classes */
    .time-card {background-color: #FFF1E6; padding: 15px; border-radius: 5px; margin-top: 10px}
    .time-title {color: #FF9D45; font-weight: bold; margin-bottom: 5px}
    .time-detail {margin-left: 20px; margin-bottom: 10px}
    .traffic-box {background-color: #FFF1E6; padding: 15px; border-radius: 5px; margin-top: 10px}
    .weather-box {background-color: #FFF1E6; padding: 15px; border-radius: 5px; margin-top: 10px}
    .highlight {background-color: #FFF1E6; padding: 10px; border-radius: 5px}
    .logo-container {display: flex; justify-content: center; margin-bottom: 20px}
    .footer-container {display: flex; justify-content: center; align-items: center; margin-top: 20px}
    .card {background-color: #FFF1E6; border-radius: 10px; padding: 20px; margin: 10px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1)}
    .icon-text {display: flex; align-items: center}
    .icon-text span {margin-left: 10px}
    
    /* Tab styling */
    .stTabs [aria-selected="true"] {
        background-color: #FFF1E6 !important;
        color: #FF7E33 !important;
        font-weight: 600 !important;
    }
    
    /* Ensure all headers are orange */
    h1, h2, h3, h4 {color: #FF9D45 !important}
    
    /* Progress bar color */
    .stProgress .st-bo {background-color: #FF9D45 !important}
</style>
""", unsafe_allow_html=True)

# Title with prominent instruction about the arrow - using Streamlit native instead of HTML
st.title("beem.", anchor=False)

# Banner with instructions - using Streamlit native components
st.warning("👉 **CLICK THE ARROW TOP LEFT** TO ANALYZE YOUR ROUTE 👈")

st.markdown('<h1 class="main-header">🚲 Beem Billboard Route Optimizer</h1>', unsafe_allow_html=True)

# Help box using Streamlit native components
st.info("""
### HOW TO USE THIS APP:

1. **Click the gray ">" button** in the top left corner to open the sidebar menu
2. Select your area and time options in the sidebar
3. Click the "ANALYZE ROUTE" button to see results
""")

# App description using Streamlit native
st.markdown("""
### Optimize your mobile billboard routes for maximum engagement
Find the best times and locations for your advertising campaigns 📍
""")

# Initialize analyze variable at the top
analyze = False

# ROUTE ANALYSIS CONTROLS using Streamlit native components instead of HTML
st.success("### ROUTE ANALYSIS CONTROLS\n⬅️ Use the controls in the sidebar to select your options")

# Add a direct analyze button in the main content area - HUGE and unmissable
st.markdown("### Click this button to see results:")

analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 2, 1])
with analyze_col2:
    # Remove the custom button styling that's causing issues
    main_analyze = st.button("🚀 ANALYZE ROUTE NOW 🚀", type="primary", use_container_width=True)
    if main_analyze:
        analyze = True

# Sidebar
with st.sidebar:
    # Add Beem logo
    st.title("beem.")
    
    # Add a prominent header for the sidebar
    st.markdown("### ROUTE ANALYSIS CONTROLS")
    
    st.markdown('## Route Options')
    
    # Area selection - EXPANDED LIST
    areas = list(area_coordinates.keys())
    
    area = st.selectbox(
        "Select your Area",
        areas
    )
    
    # Time selection
    st.markdown('### Time Options')
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
    st.info("**Click the button below to analyze!** ⬇️")
    
    # Add spacing
    st.markdown("")
    
    # Analysis button - Make it much more prominent
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        sidebar_analyze = st.button("ANALYZE ROUTE", type="primary", use_container_width=True)
        if sidebar_analyze:
            analyze = True
    
    # About section
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

# Add visual banner with dynamic elements - MOVED AFTER analyze is defined
if analyze:
    # Analysis banner - keep simple to avoid HTML showing
    st.markdown("""
    <div style="background: linear-gradient(90deg, #FF7E33, #FFB673); border-radius: 10px; padding: 20px; margin-bottom: 25px;">
        <h3 style="color: white !important; margin: 0; font-size: 30px; font-weight: 800;">Beem Billboard Insights</h3>
        <p style="color: white !important; margin: 8px 0 0 0; font-weight: 600; font-size: 18px;">Optimizing engagement across Manchester</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Welcome banner - extremely simplified to avoid HTML issues
    st.header("Welcome to Beem!", anchor=False)
    st.subheader("Mobile billboard optimization platform", anchor=False)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("📣 Find the best times and locations for your advertising campaigns")
    with col2:
        st.markdown("### 🚲")

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
        st.info("Select area and time options in the sidebar, then click 'Analyze Route' to see results.")
        
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
    st.markdown('<h2 style="color: #FF9D45;">Map & Visualization</h2>', unsafe_allow_html=True)
    
    if analyze:
        # Create map for visualization
        selected_area_data = area_coordinates[area]
        lat = selected_area_data['latitude']
        lon = selected_area_data['longitude']
        
        # Show area details
        st.success(f"**Area:** {area}")
        
        traffic_status = "Light 🟢" if traffic_data['congestion_level'] < 0.3 else "Moderate 🟡" if traffic_data['congestion_level'] < 0.6 else "Heavy 🔴"
        st.info(f"**Traffic Status:** {traffic_status}")
        
        st.warning(f"**Expected Foot Traffic:** {int(pedestrian_density * 1000)}/hour")
        
        # Base map focused on selected area
        st.subheader("🗺️ Traffic Heatmap")
        
        # Create the map with selected area
        map_df = pd.DataFrame({
            'lat': [lat],
            'lon': [lon]
        })
        
        st.map(map_df)
        
        # Add color-coded indicators in a cleaner way
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success("🟢 Light Traffic")
        with col2:
            st.warning("🟡 Moderate Traffic")
        with col3:
            st.error("🔴 Heavy Traffic")
        
        # Simplified traffic chart
        st.subheader("📊 Hourly Traffic Flow")
        
        # Generate sample data
        hours = list(range(6, 24))  # 6 AM to 11 PM
        congestion = [0.7, 0.9, 0.8, 0.6, 0.5, 0.4, 0.3, 0.4, 0.6, 0.7, 0.5, 0.4, 0.6, 0.8, 0.9, 0.7, 0.5, 0.3]
        
        # Create dataframe for hourly traffic
        traffic_df = pd.DataFrame({
            'Hour': [f"{h}:00" for h in hours],
            'Congestion': congestion[:len(hours)]
        })
        
        st.bar_chart(traffic_df.set_index('Hour'))
        
        # Pedestrian activity
        st.subheader("👥 Pedestrian Activity")
        
        # Sample data for pedestrian activity
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        activity = [0.5, 0.6, 0.6, 0.7, 0.8, 0.9, 0.7]
        
        # Create dataframe
        activity_df = pd.DataFrame({
            'Day': days,
            'Activity': activity
        })
        
        st.line_chart(activity_df.set_index('Day'))
        
    else:
        st.info("Select area and time options in the sidebar, then click 'Analyze Route' to view the map visualization.")

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
        st.info("Select area and time options in the sidebar, then click 'Analyze Route' to see historical data.")

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
        st.info("Select area and time options in the sidebar, then click 'Analyze Route' to see recommended times.")

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
        st.info("Select area and time options in the sidebar, then click 'Analyze Route' to see demographic analysis.")

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