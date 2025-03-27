import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import requests
import time as time_module
import random

# MAIN APP FILE - All functionality consolidated here

# Create a mock data collector class
class BeemDataCollector:
    def __init__(self, config):
        self.weather_api_key = config.get('weather_api_key', 'demo_key')
        self.traffic_api_key = config.get('traffic_api_key', 'demo_key')
    
    def get_weather_data(self, latitude, longitude, day=None):
        """Get real weather data from WeatherAPI.com"""
        # Check if we have an actual API key
        if self.weather_api_key and self.weather_api_key != 'demo_key':
            try:
                # WeatherAPI.com endpoint
                url = f"http://api.weatherapi.com/v1/forecast.json?key={self.weather_api_key}&q={latitude},{longitude}&days=1&aqi=no&alerts=no"
                
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    # Return the actual API response
                    return response.json()
            except Exception as e:
                st.error(f"Weather API error: {e}")
                # Fall back to mock data if there's an error
                pass
                
        # Fall back to mock data if API key is missing or API call failed
        weather_conditions = ["Sunny", "Cloudy", "Partly Cloudy", "Rainy", "Light Rain"]
        temps = [12, 15, 18, 20, 22, 24]
        wind_speeds = [5, 8, 10, 12, 15, 18]
        
        hourly_data = []
        
        # Generate data for 24 hours
        for hour in range(24):
            hourly_data.append({
                "time": f"{hour:02d}:00",
                "temp_c": random.choice(temps),
                "condition": random.choice(weather_conditions),
                "wind_kph": random.choice(wind_speeds),
                "chance_of_rain": random.randint(0, 100),
                "is_day": 1 if 6 <= hour <= 18 else 0
            })
        
        return {
            "current": {
                "temp_c": random.choice(temps),
                "condition": {"text": random.choice(weather_conditions)},
                "wind_kph": random.choice(wind_speeds),
                "feelslike_c": random.choice(temps) - 2,
                "is_day": 1
            },
            "forecast": {
                "forecastday": [{
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "day": {
                        "maxtemp_c": max(temps),
                        "mintemp_c": min(temps),
                        "avgtemp_c": sum(temps) // len(temps),
                        "daily_chance_of_rain": random.randint(0, 100),
                        "condition": {"text": random.choice(weather_conditions)}
                    },
                    "hour": hourly_data
                }]
            }
        }
    
    def get_traffic_data(self, latitude, longitude, radius=1000):
        """Get real traffic data from TomTom API"""
        # Check if we have an actual API key
        if self.traffic_api_key and self.traffic_api_key != 'demo_key':
            try:
                # TomTom Traffic Flow API
                url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={latitude},{longitude}&key={self.traffic_api_key}"
                
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract relevant traffic data
                    if 'flowSegmentData' in data:
                        flow_data = data['flowSegmentData']
                        current_speed = flow_data.get('currentSpeed', 40)
                        free_flow_speed = flow_data.get('freeFlowSpeed', 50) 
                        
                        # Calculate congestion level (0-1 range)
                        congestion_level = min(1.0, max(0.0, 1 - (current_speed / max(1, free_flow_speed))))
                        
                        # Convert numerical congestion to text for compatibility
                        congestion_text = "Low"
                        if congestion_level > 0.7:
                            congestion_text = "Very High"
                        elif congestion_level > 0.5:
                            congestion_text = "High"
                        elif congestion_level > 0.3:
                            congestion_text = "Moderate"
                        
                        return {
                            "congestion_level": congestion_text,
                            "flow_speed": current_speed,
                            "free_flow_speed": free_flow_speed,
                            "incidents": []
                        }
            except Exception as e:
                st.error(f"Traffic API error: {e}")
                # Fall back to mock data
                pass
        
        # Fall back to mock data if API key is missing or API call failed
        congestion_levels = ["Low", "Moderate", "High", "Very High"]
        incident_types = ["accident", "construction", "congestion"]
        
        return {
            "congestion_level": random.choice(congestion_levels),
            "flow_speed": random.randint(5, 60),
            "free_flow_speed": random.randint(40, 80),
            "incidents": [
                {
                    "type": random.choice(incident_types),
                    "severity": random.randint(1, 4),
                    "description": f"Mock incident {i+1}"
                } for i in range(random.randint(0, 3))
            ]
        }
    
    def get_pedestrian_density(self, area_id, time_of_day="morning"):
        """Mock pedestrian density data collection"""
        densities = {
            "morning": {"min": 40, "max": 80},
            "afternoon": {"min": 60, "max": 100},
            "evening": {"min": 70, "max": 120},
            "night": {"min": 10, "max": 30}
        }
        
        time_range = densities.get(time_of_day, {"min": 50, "max": 100})
        
        # Generate hourly mock data
        hourly_data = []
        peak_hour = 12 if time_of_day == "afternoon" else (8 if time_of_day == "morning" else 18)
        
        for hour in range(24):
            multiplier = 1.0
            # Increase density around peak hours
            if abs(hour - peak_hour) < 3:
                multiplier = 1.5
            
            base_density = random.randint(time_range["min"], time_range["max"])
            hourly_data.append({
                "hour": hour,
                "density": int(base_density * multiplier),
                "primary_demographic": random.choice(["commuters", "tourists", "students", "shoppers"])
            })
        
        return {
            "average_density": sum(item["density"] for item in hourly_data) // len(hourly_data),
            "peak_density": max(item["density"] for item in hourly_data),
            "hourly_breakdown": hourly_data,
            "area_type": random.choice(["commercial", "residential", "mixed", "entertainment"])
        }
        
    def integrate_data(self, zone, timestamp):
        """
        Integrate all data sources for a given zone and time
        Returns combined weather, traffic and pedestrian data
        """
        # Determine time of day for pedestrian density
        hour = timestamp.hour
        if 5 <= hour < 12:
            time_of_day = "morning"
        elif 12 <= hour < 17:
            time_of_day = "afternoon"
        elif 17 <= hour < 22:
            time_of_day = "evening"
        else:
            time_of_day = "night"
            
        # Get data from each source
        weather_data_full = self.get_weather_data(zone['latitude'], zone['longitude'])
        traffic_data_full = self.get_traffic_data(zone['latitude'], zone['longitude'])
        pedestrian_density = self.get_pedestrian_density(zone['zone_id'], time_of_day)
        
        # Extract current weather from the full response
        current_weather = weather_data_full['current']
        
        # Format traffic data
        congestion_level = 0.0
        if traffic_data_full["congestion_level"] == "Low":
            congestion_level = 0.2
        elif traffic_data_full["congestion_level"] == "Moderate":
            congestion_level = 0.5
        elif traffic_data_full["congestion_level"] == "High":
            congestion_level = 0.8
        elif traffic_data_full["congestion_level"] == "Very High":
            congestion_level = 0.95
        
        # Format simplified data for application use
        weather_data = {
            'temperature': current_weather['temp_c'],
            'condition': current_weather['condition']['text'],
            'wind_speed': current_weather['wind_kph'],
            'precipitation': 0 if 'rain' not in current_weather['condition']['text'].lower() else 1.0
        }
        
        traffic_data = {
            'congestion_level': congestion_level,
            'flow_speed': traffic_data_full['flow_speed'],
            'free_flow_speed': traffic_data_full['free_flow_speed']
        }
        
        # Calculate a normalized pedestrian density value between 0-1
        avg_density = pedestrian_density['average_density']
        normalized_density = min(1.0, max(0.0, avg_density / 100))
        
        return {
            'zone_id': zone['zone_id'],
            'timestamp': timestamp,
            'weather': weather_data,
            'traffic': traffic_data,
            'pedestrian_density': normalized_density,
            'latitude': zone['latitude'],
            'longitude': zone['longitude']
        }

# Define config with API keys (you can replace 'demo_key' with actual keys later)
config = {
    'weather_api_key': 'c43d5e7fe8694a7d879125624230208',  # WeatherAPI.com key
    'traffic_api_key': 'UpJxQZe4G5KVzlBvM53wRuCcXC2H8BDc'   # TomTom API key
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
st.set_page_config(
    page_title="Beem Billboard Optimizer", 
    page_icon="🚲", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Completely replace all custom sidebar and button CSS with a much simpler approach
st.markdown("""
<style>
/* MAKE EVERYTHING ORANGE - BRUTE FORCE METHOD */
button,
.st-bq,
.st-bm, 
.st-bn,
.st-bo,
.st-bp,
.st-c3,
.st-c4,
.stButton > button,
[data-testid="baseButton-secondary"],
[data-testid="baseButton-primary"],
[data-baseweb="button"],
[kind="primary"],
[kind="secondary"],
header button,
div.stButton button,
button.css-jggiw1,
button.css-1d3q4k7,
.css-1cpxqw2, 
[aria-label="Close"],
.stApp button {
    background-color: #FF6600 !important;
    color: white !important;
    border: none !important;
    font-weight: bold !important;
}

/* Make sidebar collapse control ORANGE */
[data-testid="collapsedControl"] {
    background-color: #FF6600 !important;
    color: white !important;
    visibility: visible !important;
    border-radius: 0 4px 4px 0 !important;
    padding: 10px 5px !important;
    opacity: 1 !important;
    border: none !important;
    padding: 7px 0 !important;
    width: 24px !important;
    height: 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
}

[data-testid="collapsedControl"] svg {
    color: white !important;
    fill: white !important;
}

/* HIDE ALL toggle button attempts */
#sidebar-button-container,
.custom-sidebar-toggle,
#custom-sidebar-toggle,
#dummy-target,
iframe#dummy-target,
button[id="custom-sidebar-toggle"] {
    display: none !important;
}

/* Global resets for light theme */
body {
    background-color: #FFFFFF !important;
    color: #333333 !important;
}

.stApp {
    background-color: #FFFFFF !important;
}

/* Main styles with better contrast on light background */
.main-header {color: #FF6600 !important; font-weight: 600}

/* Sidebar styling for light theme */
section[data-testid="stSidebar"] {
    background-color: #FFF6F0 !important;
}

/* Headers */
h1, h2, h3, h4 {color: #FF6600 !important}

/* Progress bar color */
.stProgress .st-bo {background-color: #FF6600}

/* Card elements with light backgrounds */
.highlight {background-color: #FFF6F0; padding: 10px; border-radius: 5px; color: #333333 !important; box-shadow: 0 2px 5px rgba(0,0,0,0.05);}
.highlight p, .highlight li {color: #333333 !important; font-weight: 500 !important}

.time-card {background-color: #FFF6F0; padding: 15px; border-radius: 5px; margin-top: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);}
.time-title {color: #FF6600; font-weight: bold; margin-bottom: 5px}
.time-detail {margin-left: 20px; margin-bottom: 10px; color: #333333 !important; font-weight: 500 !important}

.traffic-box {background-color: #FFF6F0; padding: 15px; border-radius: 5px; margin-top: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);}
.traffic-box p, .traffic-box div {color: #333333 !important; font-weight: 500 !important}

.weather-box {background-color: #FFF6F0; padding: 15px; border-radius: 5px; margin-top: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);}
.weather-box p, .weather-box div {color: #333333 !important; font-weight: 500 !important}

.logo-container {display: flex; justify-content: center; margin-bottom: 20px}
.footer-container {display: flex; justify-content: center; align-items: center; margin-top: 20px}

.card {background-color: #FFF6F0; border-radius: 10px; padding: 20px; margin: 10px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05);}
.card p, .card div, .card span {color: #333333 !important; font-weight: 500 !important}

.dashboard-metric {background-color: #FFF6F0; border-left: 5px solid #FF6600; padding: 15px; margin: 10px 0; box-shadow: 0 2px 5px rgba(0,0,0,0.05);}
.dashboard-metric p, .dashboard-metric div {color: #333333 !important; font-weight: 500 !important}

.gradient-header {background: linear-gradient(90deg, #FF6600, #FF8533); color: white !important; padding: 10px; border-radius: 5px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
.gradient-header p, .gradient-header div {color: white !important; font-weight: 500 !important}

/* Fix for radio button text color */
.stRadio > div {
    background-color: transparent !important;
}
.stRadio input {
    display: inline-block !important;
}

/* Override any radio button label colors */
label[data-baseweb="radio"] div,
label[data-testid="stRadioLabel"] span {
    color: #333333 !important;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🚲 Beem Billboard Route Optimizer</h1>', unsafe_allow_html=True)

# Add an unmissable banner that is absolutely impossible to miss
st.markdown("""
<div style="background: linear-gradient(90deg, #FF6600, #FF8533); color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.3); border: 3px solid white; animation: pulse 2s infinite;">
    <h2 style="color: white !important; margin: 0; text-transform: uppercase; font-size: 28px;">🔥 APP UPDATED ON MARCH 27, 2024 🔥</h2>
    <p style="font-size: 20px; font-weight: bold; margin: 10px 0 0 0;">All buttons are now ORANGE and using real Weather + TomTom APIs</p>
</div>
<style>
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.03); }
  100% { transform: scale(1); }
}
</style>
""", unsafe_allow_html=True)

st.markdown("Optimize your mobile billboard routes for maximum engagement")

# Homepage button
if st.button("HOMEPAGE", key="main_homepage"):
    st.markdown("""
    <script>
    window.location.href = 'https://beem-billboard-optimizer-lvvnqjcpqucrxzvnhg3vc6.streamlit.app/';
    </script>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Add Beem logo
    st.markdown("""
    <div class="logo-container">
        <img src="https://raw.githubusercontent.com/ioannisvamvakas/beem_resources/main/beem_logo.png" width="180">
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 style="color: #FF6600; font-weight: 600;">Route Options</h2>', unsafe_allow_html=True)
    
    # Area selection - EXPANDED LIST
    areas = list(area_coordinates.keys())
    
    area = st.selectbox(
        "Select Area",
        areas
    )
    
    # Time selection
    st.markdown('<h3 style="color: #FF6600; font-weight: 600; margin-top: 20px">Time Options</h3>', unsafe_allow_html=True)
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
        <div style="color: #FF6600; font-weight: bold; margin-bottom: 10px">Beem Mobile Billboard Solutions</div>
        
        We help businesses reach their audience through eye-catching mobile billboards carried by cyclists.
        
        Our approach is:
        - 🌿 Eco-friendly
        - 💰 Cost-effective
        - 🎯 Highly targeted
        - 📱 Engaging
        - 📊 Data-driven
        """, unsafe_allow_html=True)
        
    # Homepage button in sidebar too
    if st.button("HOMEPAGE", key="sidebar_homepage"):
        st.markdown("""
        <script>
        window.location.href = 'https://beem-billboard-optimizer-lvvnqjcpqucrxzvnhg3vc6.streamlit.app/';
        </script>
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
                    <h4 style="margin-top: 0">{weather_icon} Weather</h4>
                    <h2 style="color: #333 !important; margin: 5px 0">{weather_data['temperature']:.1f}°C</h2>
                    <p style="color: #666; margin: 0">{weather_data['condition']}</p>
                    <hr style="margin: 10px 0; border-color: #ddd">
                    <p><strong>Exact temperature:</strong> {weather_data["temperature"]:.1f}°C<br>
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
                    <h4 style="margin-top: 0">{0} Weather Conditions</h4>
                    <div style="display: flex; justify-content: space-between; margin: 15px 0">
                        <div style="text-align: center; background: rgba(255,255,255,0.5); padding: 10px; border-radius: 5px; width: 45%">
                            <div style="font-size: 24px; margin-bottom: 5px">🌡️</div>
                            <div style="font-weight: bold">{1:.1f}°C</div>
                            <div style="font-size: 12px; color: #666">Exact Temperature</div>
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
        st.info("Select options and click 'Analyze Route' to see results.")
        
        # Add a visual placeholder when no analysis is running
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 300px">
            <div style="text-align: center">
                <img src="https://raw.githubusercontent.com/ioannisvamvakas/beem_resources/main/beem_logo.png" width="200">
                <p style="color: #FF9D45; margin-top: 20px; font-size: 18px">Select options and analyze to see data</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

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

# Footer with enhanced visual elements
st.markdown("---")
st.markdown("""
<div class="footer-container">
    <div style="text-align: center">
        <img src="https://raw.githubusercontent.com/ioannisvamvakas/beem_resources/main/beem_logo.png" width="100">
        <div style="color: #FF9D45; margin-top: 10px">© 2025 Beem Mobile Billboard Solutions</div>
        <div style="color: #999; font-size: 12px; margin-top: 5px">hello@beembillboards.com | +44 123 456 7890</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Add visual banner with dynamic elements
if analyze:
    st.markdown("""
    <div style="background: linear-gradient(90deg, #FF9D45, #FFB673); border-radius: 10px; padding: 15px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center">
        <div>
            <h3 style="color: white !important; margin: 0">Beem Billboard Insights</h3>
            <p style="color: white; margin: 5px 0 0 0">Optimizing engagement across Manchester</p>
        </div>
        <div style="background: white; border-radius: 50%; width: 50px; height: 50px; display: flex; justify-content: center; align-items: center">
            <span style="font-size: 24px">🚲</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Even when not analyzing, show a welcome banner
    st.markdown("""
    <div style="background: linear-gradient(90deg, #FF9D45, #FFB673); border-radius: 10px; padding: 15px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center">
        <div>
            <h3 style="color: white !important; margin: 0">Welcome to Beem</h3>
            <p style="color: white; margin: 5px 0 0 0">Mobile billboard optimization platform</p>
        </div>
        <div style="background: white; border-radius: 50%; width: 50px; height: 50px; display: flex; justify-content: center; align-items: center">
            <span style="font-size: 24px">🚲</span>
        </div>
    </div>
    """, unsafe_allow_html=True)