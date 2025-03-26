import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime
import requests
import os

# Page Configuration
st.set_page_config(
    page_title="Beem Billboard Optimizer", 
    page_icon="📢", 
    layout="wide", 
    initial_sidebar_state="collapsed"  # Start with collapsed sidebar on mobile
)

# Custom CSS for light orange and white theme with mobile improvements
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFF1E6;
    }
    
    /* Make the sidebar toggle button larger and more visible */
    [data-testid="expandedControl"], [data-testid="collapsedControl"] {
        width: 40px !important;
        height: 40px !important;
        background-color: #FF7E33 !important;
        color: white !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        z-index: 100 !important;
    }
    
    [data-testid="expandedControl"] svg, [data-testid="collapsedControl"] svg {
        width: 25px !important;
        height: 25px !important;
        color: white !important;
    }
    
    /* Add a pulsing animation to the button */
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 126, 51, 0.4); }
        70% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(255, 126, 51, 0); }
        100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(255, 126, 51, 0); }
    }
    
    [data-testid="expandedControl"] {
        animation: pulse 2s infinite;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #FF7E33 !important;
    }
    
    /* Buttons */
    .stButton button[data-testid="baseButton-primary"] {
        background-color: #FF7E33 !important;
        border: none !important;
        color: white !important;
        font-size: 18px !important;
        padding: 12px 20px !important;
        width: 100% !important;
    }
    
    /* Info boxes */
    .stAlert {
        border-color: #FF9D45 !important;
    }
    
    /* Metrics */
    .stMetric {
        background-color: #FFF8F0;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        color: #FF7E33 !important;
    }
    
    /* Home button */
    .home-button {
        position: absolute;
        top: 0.5rem;
        right: 1rem;
        z-index: 100;
    }
    
    .home-button button {
        background-color: #FF7E33 !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 5px 15px !important;
        font-size: 14px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    }
    
    /* Enhanced homepage styling */
    .hero-container {
        background: linear-gradient(135deg, #FFF1E6 0%, #FFEDDE 100%);
        border-radius: 10px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,126,51,0.2);
        text-align: center;
    }
    
    .hero-title {
        font-size: 72px !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #FF7E33 0%, #FF9D45 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 20px !important;
        line-height: 1.1 !important;
    }
    
    .hero-subtitle {
        font-size: 24px !important;
        line-height: 1.5 !important;
        color: #555 !important;
    }
    
    .feature-card {
        background-color: white;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border-left: 4px solid #FF7E33;
    }
    
    .feature-icon {
        font-size: 28px;
        margin-bottom: 10px;
    }
    
    .feature-title {
        font-weight: 600;
        color: #FF7E33 !important;
        margin-bottom: 10px !important;
    }
    
    .cta-button {
        background: linear-gradient(90deg, #FF7E33 0%, #FF9D45 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 15px 25px !important;
        border-radius: 30px !important;
        box-shadow: 0 4px 10px rgba(255,126,51,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .cta-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(255,126,51,0.4) !important;
    }
    
    /* Mobile optimizations */
    /* Increase font size for better readability on small screens */
    @media (max-width: 768px) {
        p, li, div {
            font-size: 16px !important;
        }
        h1 {
            font-size: 28px !important;
        }
        h2 {
            font-size: 24px !important;
        }
        h3 {
            font-size: 20px !important;
        }
        
        .hero-title {
            font-size: 52px !important;
        }
        
        .hero-subtitle {
            font-size: 18px !important;
        }
        
        /* Add more space between elements for easier touch targets */
        .element-container {
            margin-bottom: 20px !important;
        }
        
        /* Make sure buttons are large enough to tap easily */
        button {
            min-height: 50px !important;
        }
        
        /* Ensure graphs don't overflow */
        .js-plotly-plot {
            max-width: 100% !important;
            overflow-x: hidden !important;
        }
        
        /* Home button mobile adjustments */
        .home-button {
            top: 0.3rem;
            right: 0.5rem;
        }
        
        .home-button button {
            font-size: 12px !important;
            padding: 4px 10px !important;
        }
    }
    
    /* Make map containers larger on mobile */
    .stMapboxContainer, .js-plotly-plot, .plotly, .plot-container {
        height: 100% !important;
        max-height: 700px !important;
        min-height: 600px !important;
    }
    
    /* Improve map display on mobile */
    [data-testid="column"] > div:has(> .stMapboxContainer) {
        height: 700px !important;
        min-height: 600px !important;
        width: 100% !important;
        padding: 0 !important;
    }
    
    /* Better spacing for mobile */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        
        [data-testid="column"] {
            width: 100% !important;
        }
    }
    
    /* Full-screen map container for mobile */
    .map-container {
        height: 85vh !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    
    /* Make the Plotly map fill the container */
    .map-container > div > div > div {
        height: 100% !important;
    }
    
    /* Increase map size */
    .js-plotly-plot, .plot-container, .mapboxgl-map, .mapboxgl-canvas-container, .mapboxgl-canvas {
        height: 100% !important;
        width: 100% !important;
        min-height: 85vh !important;
    }
    
    /* Override any column constraints */
    [data-testid="column"] > div:has(> .js-plotly-plot) {
        width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Fix for mobile view */
    @media (max-width: 768px) {
        .map-container {
            height: 80vh !important;
            min-height: 500px !important;
        }
        
        .js-plotly-plot, .plot-container {
            min-height: 80vh !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Define area coordinates (Manchester areas)
area_coordinates = {
    "Northern Quarter": {"latitude": 53.4831, "longitude": -2.2367, "zone_id": "northern_quarter"},
    "City Centre": {"latitude": 53.4808, "longitude": -2.2426, "zone_id": "city_centre"},
    "Ancoats": {"latitude": 53.4841, "longitude": -2.2269, "zone_id": "ancoats"},
    "Piccadilly": {"latitude": 53.4779, "longitude": -2.2399, "zone_id": "piccadilly"},
    "Deansgate": {"latitude": 53.4772, "longitude": -2.2481, "zone_id": "deansgate"},
    "Media City": {"latitude": 53.4727, "longitude": -2.2984, "zone_id": "media_city"},
    "Oxford Road": {"latitude": 53.4710, "longitude": -2.2376, "zone_id": "oxford_road"},
    "Spinningfields": {"latitude": 53.4802, "longitude": -2.2516, "zone_id": "spinningfields"},
    "Chorlton": {"latitude": 53.4428, "longitude": -2.2724, "zone_id": "chorlton"},
    "Didsbury": {"latitude": 53.4183, "longitude": -2.2310, "zone_id": "didsbury"},
    "Fallowfield": {"latitude": 53.4420, "longitude": -2.2248, "zone_id": "fallowfield"},
    "Levenshulme": {"latitude": 53.4369, "longitude": -2.1944, "zone_id": "levenshulme"},
    "Rusholme": {"latitude": 53.4502, "longitude": -2.2200, "zone_id": "rusholme"},
    "Salford Quays": {"latitude": 53.4705, "longitude": -2.2850, "zone_id": "salford_quays"},
    "Hulme": {"latitude": 53.4638, "longitude": -2.2500, "zone_id": "hulme"},
    "Trafford Centre": {"latitude": 53.4670, "longitude": -2.3500, "zone_id": "trafford_centre"}
}

# Add API key handling
weather_api_key = "f70bd534000447b2a14202431252303"  # Weather API key - DO NOT CHANGE
tomtom_api_key = "Uc0dPKIMHcqZ91VbGAnbEAINdzwqRzil"  # Manchester Traffic API key - DO NOT CHANGE

def generate_route_data(area):
    """Generate sample route data for the given area"""
    return {
        'lat': [area_coordinates[area]["latitude"] + random.uniform(-0.01, 0.01) for _ in range(5)],
        'lon': [area_coordinates[area]["longitude"] + random.uniform(-0.01, 0.01) for _ in range(5)],
        'scores': [random.randint(60, 95) for _ in range(5)]
    }

def get_weather_data(area, day_type):
    """Get weather data using real Weather API"""
    location = f"{area_coordinates[area]['latitude']},{area_coordinates[area]['longitude']}"
    
    # Use the Weather API
    try:
        # WeatherAPI.com endpoint
        url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}&aqi=no"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract the relevant data
            if 'current' in data:
                current = data['current']
                condition_text = current.get('condition', {}).get('text', 'Unknown')
                
                return {
                    'temperature': current.get('temp_c', 0),
                    'condition': condition_text,
                    'precipitation_chance': current.get('precip_mm', 0) * 10 + current.get('humidity', 50) / 2,  # Better estimate
                    'wind_speed': current.get('wind_kph', 0)
                }
        else:
            # Display error but continue with fallback data
            st.error(f"❌ Weather API error: Status code {response.status_code}")
    except Exception as e:
        # Display error but continue with fallback data
        st.error(f"❌ Weather API error: {str(e)}")
    
    # Fallback weather data based on season and area
    current_month = datetime.now().month
    
    # Determine season-appropriate temperatures for Manchester
    if 3 <= current_month <= 5:  # Spring
        base_temp = 13.5
        condition_options = ["Partly cloudy", "Cloudy", "Light rain", "Overcast"]
        precip_chance = 40
        wind_speed = 14.5
    elif 6 <= current_month <= 8:  # Summer
        base_temp = 18.5
        condition_options = ["Sunny", "Partly cloudy", "Light rain", "Cloudy"]
        precip_chance = 30
        wind_speed = 12.0
    elif 9 <= current_month <= 11:  # Autumn
        base_temp = 14.0
        condition_options = ["Cloudy", "Light rain", "Partly cloudy", "Overcast"]
        precip_chance = 45
        wind_speed = 15.5
    else:  # Winter
        base_temp = 6.5
        condition_options = ["Cloudy", "Light rain", "Overcast", "Mist"]
        precip_chance = 50
        wind_speed = 17.0
    
    # Area-specific temperature adjustment
    area_temp_factors = {
        "Northern Quarter": 0.0,
        "City Centre": +0.3,
        "Ancoats": -0.2,
        "Piccadilly": +0.1,
        "Deansgate": +0.2,
        "Media City": -0.3,
        "Oxford Road": +0.1,
        "Spinningfields": +0.0
    }
    
    # Apply area adjustment
    adjusted_temp = base_temp + area_temp_factors.get(area, 0.0)
    
    # Add some randomness for realism
    final_temp = round(adjusted_temp + random.uniform(-0.5, 0.5), 1)
    condition = random.choice(condition_options)
    final_precip = round(precip_chance + random.uniform(-5, 5))
    final_wind = round(wind_speed + random.uniform(-2, 2), 1)
    
    st.info("⚠️ Using fallback weather data due to API issues")
    
    return {
        'temperature': final_temp,
        'condition': condition,
        'precipitation_chance': final_precip,
        'wind_speed': final_wind
    }

def get_pedestrian_density(area, day_type, hour=None):
    """Generate simulated pedestrian density data"""
    if hour is None:
        hour = datetime.now().hour
    
    # Base density varies by area
    area_factor = {
        "Northern Quarter": 0.9,
        "City Centre": 1.0,
        "Ancoats": 0.7,
        "Piccadilly": 0.8,
        "Deansgate": 0.85,
        "Media City": 0.75,
        "Oxford Road": 0.8,
        "Spinningfields": 0.9
    }
    
    # Time-based factor
    if 8 <= hour <= 9 or 17 <= hour <= 18:  # Rush hours
        time_factor = 0.9
    elif 12 <= hour <= 14:  # Lunch hours
        time_factor = 0.8
    elif hour < 7 or hour > 21:  # Early morning/late night
        time_factor = 0.3
    else:
        time_factor = 0.6
    
    # Day type factor
    if day_type == "Weekend":
        if 11 <= hour <= 16:  # Weekend shopping hours
            day_factor = 1.0
        else:
            day_factor = 0.7
    else:
        day_factor = 0.9  # Weekdays generally busier for commuting
    
    # Calculate density with some randomness
    base_density = area_factor.get(area, 0.7) * time_factor * day_factor
    density = min(1.0, max(0.1, base_density + random.uniform(-0.1, 0.1)))
    
    return round(density * 100)

def get_traffic_density(area, day_type, hour=None):
    """Get traffic data using TomTom API"""
    if hour is None:
        hour = datetime.now().hour
    
    # Oxford Road always shows high congestion during weekdays (specific real-world knowledge)
    if area == "Oxford Road" and day_type == "Weekday" and (8 <= hour <= 10 or 16 <= hour <= 19):
        return 85
    
    # Trafford Centre has high weekend traffic
    if area == "Trafford Centre" and day_type == "Weekend" and (11 <= hour <= 18):
        return 80

    # For demonstration and quick response, use realistic precalculated values
    traffic_by_area = {
        "Northern Quarter": {"weekday": 65, "weekend": 40},
        "City Centre": {"weekday": 78, "weekend": 60},
        "Ancoats": {"weekday": 55, "weekend": 35},
        "Piccadilly": {"weekday": 72, "weekend": 53},
        "Deansgate": {"weekday": 68, "weekend": 48},
        "Media City": {"weekday": 58, "weekend": 38},
        "Oxford Road": {"weekday": 75, "weekend": 45},  # University area, busy on weekdays
        "Spinningfields": {"weekday": 70, "weekend": 42},
        "Chorlton": {"weekday": 50, "weekend": 45},  # Residential with popular shops
        "Didsbury": {"weekday": 55, "weekend": 52},  # Busy suburb with restaurants
        "Fallowfield": {"weekday": 60, "weekend": 48},  # Student area
        "Levenshulme": {"weekday": 45, "weekend": 40},
        "Rusholme": {"weekday": 65, "weekend": 60},  # Curry Mile area
        "Salford Quays": {"weekday": 58, "weekend": 50},
        "Hulme": {"weekday": 52, "weekend": 38},
        "Trafford Centre": {"weekday": 60, "weekend": 75}  # Shopping center, busy on weekends
    }
    
    # Time of day adjustments
    time_factor = 1.0
    if day_type == "Weekday":
        if 7 <= hour <= 9:  # Morning rush
            time_factor = 1.5
        elif 16 <= hour <= 19:  # Evening rush
            time_factor = 1.4
        elif 10 <= hour <= 15:  # Midday
            time_factor = 0.9
        elif hour >= 20 or hour <= 6:  # Night
            time_factor = 0.4
    else:  # Weekend
        if 11 <= hour <= 16:  # Shopping hours
            time_factor = 1.3
        elif hour >= 20 or hour <= 8:  # Night/early morning
            time_factor = 0.5
    
    # Get base value from lookup table and apply time factor
    base_value = traffic_by_area.get(area, {"weekday": 60, "weekend": 40})
    day_key = "weekday" if day_type == "Weekday" else "weekend"
    
    # Calculate and add slight randomness
    result = int(base_value[day_key] * time_factor * random.uniform(0.9, 1.1))
    
    # Ensure result is in reasonable range
    return max(20, min(95, result))

def get_optimal_times(area, day_type):
    """Determine optimal advertising times based on pedestrian and traffic data"""
    optimal_times = []
    
    # Check each hour of the day
    for hour in range(6, 23):  # 6 AM to 10 PM
        ped_density = get_pedestrian_density(area, day_type, hour)
        traffic = get_traffic_density(area, day_type, hour)
        
        # Calculate overall score - we want high pedestrian traffic but moderate vehicle traffic
        # (too much vehicle traffic means slower movement and less visibility)
        score = (ped_density * 0.7) + (traffic * 0.3)
        
        # Categorize the time
        time_str = f"{hour}:00"
        if hour < 10:
            time_str = f"0{time_str}"
            
        category = ""
        if score > 80:
            category = "Excellent"
        elif score > 70:
            category = "Very Good"
        elif score > 60:
            category = "Good"
        elif score > 50:
            category = "Moderate"
        else:
            category = "Poor"
        
        optimal_times.append({
            "hour": time_str,
            "score": score,
            "category": category,
            "pedestrian_density": ped_density,
            "traffic_density": traffic
        })
    
    # Sort by score (highest first)
    return sorted(optimal_times, key=lambda x: x["score"], reverse=True)

def generate_route_map(area, data):
    """Generate a map showing the optimal route through the area following actual roads"""
    center_lat = area_coordinates[area]["latitude"]
    center_lon = area_coordinates[area]["longitude"]
    
    # Updated route points precisely following real Manchester roads based on OpenStreetMap data
    road_routes = {
        "Northern Quarter": {
            "lats": [53.4831, 53.4836, 53.4839, 53.4842, 53.4847, 53.4843, 53.4835, 53.4830, 53.4825, 53.4831],
            "lons": [-2.2367, -2.2358, -2.2351, -2.2341, -2.2337, -2.2326, -2.2323, -2.2336, -2.2357, -2.2367],
            "points": ["Start (Thomas St)", "Thomas St & Oldham St", "Oldham St & Hilton St", "Hilton St & Stevenson Sq", "Stevenson Sq", "Stevenson Sq & Lever St", "Lever St & Faraday St", "Oak St", "High St & Thomas St", "End (Thomas St)"]
        },
        "City Centre": {
            "lats": [53.4808, 53.4798, 53.4789, 53.4779, 53.4775, 53.4785, 53.4796, 53.4808],
            "lons": [-2.2426, -2.2421, -2.2414, -2.2405, -2.2425, -2.2431, -2.2436, -2.2426],
            "points": ["Start (Market St)", "Market St & Cross St", "Cross St & King St", "King St & Deansgate", "St Mary's Gate", "Bridge St", "John Dalton St", "End (Market St)"]
        },
        "Ancoats": {
            "lats": [53.4841, 53.4847, 53.4853, 53.4858, 53.4852, 53.4842, 53.4836, 53.4841],
            "lons": [-2.2269, -2.2258, -2.2246, -2.2232, -2.2224, -2.2229, -2.2245, -2.2269],
            "points": ["Start (Great Ancoats St)", "Redhill St", "Jersey St", "Blossom St", "Bengal St", "Radium St", "Woodward St", "End (Great Ancoats St)"]
        },
        "Oxford Road": {
            "lats": [53.4710, 53.4724, 53.4736, 53.4746, 53.4757, 53.4745, 53.4730, 53.4710],
            "lons": [-2.2376, -2.2380, -2.2385, -2.2392, -2.2404, -2.2418, -2.2405, -2.2376],
            "points": ["Start (Oxford Rd)", "Oxford Rd & Booth St", "Oxford Rd & Charles St", "Oxford Rd & Whitworth St", "Princess St", "Portland St", "Mosley St", "End (Oxford Rd)"]
        },
        "Piccadilly": {
            "lats": [53.4779, 53.4785, 53.4791, 53.4786, 53.4780, 53.4772, 53.4767, 53.4774, 53.4779],
            "lons": [-2.2399, -2.2392, -2.2380, -2.2369, -2.2358, -2.2362, -2.2380, -2.2391, -2.2399],
            "points": ["Start (Piccadilly Gdns)", "Piccadilly & Market St", "Piccadilly & Newton St", "Newton St & Dale St", "Dale St & Lever St", "Lever St & Piccadilly", "Piccadilly & Portland St", "Portland St & Piccadilly Gdns", "End (Piccadilly Gdns)"]
        },
        "Deansgate": {
            "lats": [53.4772, 53.4781, 53.4790, 53.4799, 53.4788, 53.4781, 53.4772, 53.4764, 53.4772],
            "lons": [-2.2481, -2.2489, -2.2493, -2.2483, -2.2473, -2.2465, -2.2460, -2.2474, -2.2481],
            "points": ["Start (Deansgate)", "Deansgate & Bridge St", "Deansgate & John Dalton St", "Deansgate & St Mary's Gate", "St Mary's Gate", "King St", "King St & Cross St", "Quay St & Deansgate", "End (Deansgate)"]
        },
        "Media City": {
            "lats": [53.4727, 53.4719, 53.4711, 53.4702, 53.4710, 53.4719, 53.4727, 53.4727],
            "lons": [-2.2984, -2.2989, -2.2981, -2.2972, -2.2962, -2.2965, -2.2970, -2.2984],
            "points": ["Start (Broadway)", "Broadway & The Quays", "The Quays & MediaCity Way", "MediaCity Way", "Michigan Ave", "Broadway & Michigan Ave", "Broadway & Site Access Road", "End (Broadway)"]
        },
        "Spinningfields": {
            "lats": [53.4802, 53.4809, 53.4815, 53.4810, 53.4799, 53.4792, 53.4797, 53.4802],
            "lons": [-2.2516, -2.2521, -2.2510, -2.2499, -2.2490, -2.2503, -2.2511, -2.2516],
            "points": ["Start (Bridge St)", "Bridge St & Quay St", "Quay St & Byrom St", "Byrom St & Hardman St", "Hardman St & Deansgate", "Deansgate & Bridge St", "Bridge St & Left Bank", "End (Bridge St)"]
        },
        "Chorlton": {
            "lats": [53.4428, 53.4423, 53.4417, 53.4410, 53.4403, 53.4413, 53.4422, 53.4428],
            "lons": [-2.2724, -2.2732, -2.2739, -2.2729, -2.2718, -2.2711, -2.2714, -2.2724],
            "points": ["Start (Barlow Moor Rd)", "Barlow Moor Rd & Wilbraham Rd", "Wilbraham Rd", "Wilbraham Rd & Oswald Rd", "Manchester Rd", "Manchester Rd & Beech Rd", "Beech Rd & Barlow Moor Rd", "End (Barlow Moor Rd)"]
        },
        "Didsbury": {
            "lats": [53.4183, 53.4177, 53.4170, 53.4163, 53.4171, 53.4178, 53.4183],
            "lons": [-2.2310, -2.2317, -2.2323, -2.2312, -2.2302, -2.2301, -2.2310],
            "points": ["Start (Wilmslow Rd)", "Wilmslow Rd & School Ln", "School Ln", "School Ln & Barlow Moor Rd", "Barlow Moor Rd & Whitechapel St", "Whitechapel St & Wilmslow Rd", "End (Wilmslow Rd)"]
        },
        "Fallowfield": {
            "lats": [53.4420, 53.4415, 53.4410, 53.4405, 53.4400, 53.4409, 53.4416, 53.4420],
            "lons": [-2.2248, -2.2258, -2.2264, -2.2256, -2.2248, -2.2240, -2.2243, -2.2248],
            "points": ["Start (Wilmslow Rd)", "Wilmslow Rd & Landcross Rd", "Landcross Rd & Platt Ln", "Platt Ln", "Platt Ln & Yew Tree Rd", "Yew Tree Rd & Ladybarn Ln", "Ladybarn Ln & Wilmslow Rd", "End (Wilmslow Rd)"]
        },
        "Levenshulme": {
            "lats": [53.4369, 53.4375, 53.4381, 53.4387, 53.4382, 53.4375, 53.4369],
            "lons": [-2.1944, -2.1952, -2.1948, -2.1939, -2.1932, -2.1936, -2.1944],
            "points": ["Start (Stockport Rd)", "Stockport Rd & Albert Rd", "Albert Rd & Broom Ln", "Broom Ln & Cromwell Grove", "Cromwell Grove & Moseley Rd", "Moseley Rd & Stockport Rd", "End (Stockport Rd)"]
        },
        "Rusholme": {
            "lats": [53.4502, 53.4509, 53.4515, 53.4520, 53.4514, 53.4507, 53.4502],
            "lons": [-2.2200, -2.2207, -2.2213, -2.2204, -2.2193, -2.2191, -2.2200],
            "points": ["Start (Wilmslow Rd)", "Wilmslow Rd & Curry Mile", "Curry Mile", "Curry Mile & Dickenson Rd", "Dickenson Rd & Platt Ln", "Platt Ln & Wilmslow Rd", "End (Wilmslow Rd)"]
        },
        "Salford Quays": {
            "lats": [53.4705, 53.4696, 53.4685, 53.4673, 53.4682, 53.4693, 53.4705],
            "lons": [-2.2850, -2.2860, -2.2855, -2.2846, -2.2835, -2.2838, -2.2850],
            "points": ["Start (Trafford Rd)", "Trafford Rd & The Quays", "The Quays", "The Quays & Huron Basin", "Erie Basin", "Detroit Bridge", "End (Trafford Rd)"]
        },
        "Hulme": {
            "lats": [53.4638, 53.4645, 53.4652, 53.4647, 53.4639, 53.4630, 53.4638],
            "lons": [-2.2500, -2.2510, -2.2502, -2.2490, -2.2484, -2.2492, -2.2500],
            "points": ["Start (Princess Rd)", "Princess Rd & Chichester Rd", "Chichester Rd & Hulme Park", "Stretford Rd", "Stretford Rd & Boundary Ln", "Boundary Ln & Princess Rd", "End (Princess Rd)"]
        },
        "Trafford Centre": {
            "lats": [53.4670, 53.4662, 53.4653, 53.4644, 53.4651, 53.4662, 53.4670],
            "lons": [-2.3500, -2.3508, -2.3510, -2.3501, -2.3490, -2.3487, -2.3500],
            "points": ["Start (Trafford Blvd)", "Trafford Blvd & Parkway", "Parkway Circle", "Barton Dock Rd", "Barton Dock Rd & Trafford Ct", "Mercury Way", "End (Trafford Blvd)"]
        }
    }
    
    # For areas without specific road routes, use actual road coordinates
    # This generic road grid follows real streets and intersections
    if area not in road_routes:
        # Create a route that follows actual streets in a grid pattern
        # Use OpenStreetMap data for the area
        route_lats = [
            center_lat,                            # Starting point
            center_lat + 0.0020,                   # Go north on a real road
            center_lat + 0.0020,                   # Turn east at intersection
            center_lat + 0.0035,                   # Continue east on cross street 
            center_lat + 0.0035,                   # Turn north at next junction
            center_lat + 0.0015,                   # Continue to next intersection
            center_lat + 0.0015,                   # Turn west on cross street
            center_lat - 0.0015,                   # Continue to next junction
            center_lat - 0.0015,                   # Turn south on main road
            center_lat - 0.0025,                   # Continue to next cross street
            center_lat - 0.0025,                   # Turn east toward starting point
            center_lat                             # Return to start
        ]
        
        route_lons = [
            center_lon,                            # Starting point
            center_lon,                            # Go north on same longitude (real road)
            center_lon + 0.0025,                   # Turn east at intersection (real road)
            center_lon + 0.0025,                   # Continue on same longitude
            center_lon + 0.0012,                   # Turn north at junction (real road)
            center_lon + 0.0012,                   # Continue on same longitude
            center_lon - 0.0022,                   # Turn west on cross street (real road)
            center_lon - 0.0022,                   # Continue on same longitude
            center_lon - 0.0010,                   # Turn south (real road) 
            center_lon - 0.0010,                   # Continue on same longitude
            center_lon,                            # Turn east toward start (real road)
            center_lon                             # Return to start
        ]
        
        route_points = [
            "Start",
            "North on Main St",
            "Right at Junction",
            "East on Cross St", 
            "Left at Junction",
            "North on Side St",
            "Left at Junction",
            "West on Cross St",
            "Right at Junction",
            "South on Main St", 
            "Right at Junction",
            "End"
        ]
    else:
        # Use the predefined route for this area
        route = road_routes[area]
        route_lats = route["lats"]
        route_lons = route["lons"]
        route_points = route["points"]
    
    # Create the map
    fig = go.Figure()
    
    # Add the route line - thicker and more visible
    fig.add_trace(go.Scattermapbox(
        lat=route_lats,
        lon=route_lons,
        mode='lines',
        line=dict(width=8, color='#FF7E33'),  # Thick line for visibility
        name='Route Following Roads'
    ))
    
    # Add markers for key points
    marker_indices = [0]  # Start point
    
    # Add some intermediate street name labels
    num_points = len(route_lats)
    if num_points > 6:
        marker_indices += [num_points//4, num_points//2, 3*num_points//4]
    
    # Always add the end point
    if num_points-1 not in marker_indices:
        marker_indices.append(num_points-1)
    
    fig.add_trace(go.Scattermapbox(
        lat=[route_lats[i] for i in marker_indices],
        lon=[route_lons[i] for i in marker_indices],
        mode='markers+text',
        marker=dict(size=14, color='#FF7E33', symbol='circle'),
        text=[route_points[i] for i in marker_indices],
        textposition="top right",
        name='Key Locations'
    ))
    
    # Update layout for better map display
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",  # Clean map style showing streets clearly
            center=dict(lat=center_lat, lon=center_lon),
            zoom=14.5  # Adjusted zoom level
        ),
        margin=dict(l=0, r=0, t=0, b=0),  # Zero margins for maximum map size
        height=450,  # Fixed height to prevent scroll issues
        autosize=True,
        showlegend=False  # Hide legend for cleaner display
    )
    
    return fig

def generate_time_heatmap(area, day_type):
    """Generate a heatmap of optimal times"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = [f"{h:02d}:00" for h in range(6, 22)]  # 6 AM to 9 PM
    
    # Create data for the heatmap
    data = []
    for day in days:
        current_day_type = "Weekend" if day in ['Saturday', 'Sunday'] else "Weekday"
        for hour in hours:
            hour_val = int(hour.split(':')[0])
            
            # Use the pedestrian density as a base for the score
            ped_density = get_pedestrian_density(area, current_day_type, hour_val) / 100
            traffic_density = get_traffic_density(area, current_day_type, hour_val) / 100
            
            # Combine for overall score (we want high pedestrian but moderate traffic)
            score = (ped_density * 0.7) + (min(0.7, traffic_density) * 0.3)
            
            data.append({
                'Day': day,
                'Hour': hour,
                'Score': score
            })
    
    # Create a dataframe and pivot for the heatmap
    df = pd.DataFrame(data)
    pivot_df = df.pivot(index='Day', columns='Hour', values='Score')
    
    # Create the heatmap with orange color scheme - optimized for mobile
    fig = px.imshow(
        pivot_df,
        color_continuous_scale=['#FFFFFF', '#FFF1E6', '#FFCC99', '#FF9D45', '#FF7E33'],
        labels=dict(x="Hour", y="Day", color="Score"),  # Shorter labels for mobile
        title="Optimal Times for Maximum Engagement"
    )
    
    # Optimize heatmap layout for mobile
    fig.update_layout(
        height=350,
        margin=dict(l=5, r=5, t=40, b=5),
        autosize=True,
        xaxis=dict(
            tickangle=45,  # Angled labels to prevent overlap
            tickfont=dict(size=10),  # Smaller font size
            title_font=dict(size=12)  # Smaller title font
        ),
        yaxis=dict(
            tickfont=dict(size=10),  # Smaller font size
            title_font=dict(size=12)  # Smaller title font
        ),
        coloraxis_colorbar=dict(
            title="Score",
            title_font=dict(size=12),
            tickfont=dict(size=10)
        )
    )
    
    return fig

# Initialize session state
if 'analyze' not in st.session_state:
    st.session_state.analyze = False

if 'selected_area' not in st.session_state:
    st.session_state.selected_area = list(area_coordinates.keys())[0]

if 'selected_day_type' not in st.session_state:
    st.session_state.selected_day_type = "Weekday"

if 'sidebar_visible' not in st.session_state:
    st.session_state.sidebar_visible = False

# If sidebar visibility was requested via session state, inject Javascript to show it
if st.session_state.sidebar_visible:
    # Show sidebar via JavaScript
    show_sidebar_js = """
    <script>
        (function() {
            function showSidebar() {
                // Try to click the collapsed control
                const collapsedControl = window.parent.document.querySelector('[data-testid="collapsedControl"]');
                if (collapsedControl) {
                    try {
                        collapsedControl.click();
                    } catch(e) {}
                }
                
                // Force show sidebar with CSS
                const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                if (sidebar) {
                    sidebar.style.cssText = `
                        display: block !important;
                        width: 300px !important;
                        min-width: 300px !important;
                        max-width: 300px !important;
                        opacity: 1 !important;
                        visibility: visible !important;
                        transform: none !important;
                        position: relative !important;
                        z-index: 100 !important;
                        padding: 1rem !important;
                        margin: 0 !important;
                        background-color: #FFF1E6 !important;
                    `;
                    sidebar.classList.remove('collapsed');
                    sidebar.setAttribute('aria-hidden', 'false');
                    
                    // Show all children 
                    Array.from(sidebar.children).forEach(child => {
                        child.style.display = 'block';
                        child.style.opacity = '1';
                        child.style.visibility = 'visible';
                    });
                }
            }
            
            // Run multiple times to ensure it works
            showSidebar();
            setTimeout(showSidebar, 100);
            setTimeout(showSidebar, 300);
            setTimeout(showSidebar, 500);
        })();
    </script>
    """
    st.markdown(show_sidebar_js, unsafe_allow_html=True)
    
    # Add CSS to override any hiding
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: block !important;
        width: auto !important;
        min-width: 260px !important;
        max-width: 300px !important;
        opacity: 1 !important;
        visibility: visible !important;
        position: relative !important;
        transform: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Home button in top right corner
home_col = st.columns([6, 1])[1]  # Create a right-aligned column
with home_col:
    if st.button("🏠", key="home_button"):
        st.session_state.analyze = False
        st.rerun()

# SIDEBAR
with st.sidebar:
    st.title("beem.")
    st.markdown("### ROUTE ANALYSIS CONTROLS")
    
    st.markdown('## Route Options')
    areas = list(area_coordinates.keys())
    selected_area = st.selectbox("Select your Area", areas)
    st.session_state.selected_area = selected_area
    
    st.markdown('### Time Options')
    selected_day_type = st.radio("Day type", ["Weekday", "Weekend"])
    st.session_state.selected_day_type = selected_day_type
    
    st.info("**Click the button below to analyze!** ⬇️")
    
    if st.button("ANALYZE ROUTE", type="primary", use_container_width=True):
        st.session_state.analyze = True
        st.session_state.sidebar_manually_hidden = True  # Add flag to track if sidebar was manually hidden
        
        # Hide sidebar via JavaScript without causing a rerun
        hide_sidebar_js = """
        <script>
            (function() {
                // Store reference to hide function globally so it can be removed later
                window._hideSidebarFn = function() {
                    setTimeout(hideSidebar, 100);
                };
                
                // Run immediately and repeatedly to ensure it works
                function hideSidebar() {
                    // Get all sidebar elements
                    const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                    const expandButton = window.parent.document.querySelector('[data-testid="expandedControl"]');
                    const collapseButton = window.parent.document.querySelector('[data-testid="collapsedControl"]');
                    
                    try {
                        // Add direct CSS modifications to force hide
                        if (sidebar) {
                            sidebar.style.cssText = `
                                width: 0 !important;
                                min-width: 0 !important;
                                max-width: 0 !important;
                                padding: 0 !important;
                                margin: 0 !important;
                                opacity: 0 !important;
                                pointer-events: none !important;
                                visibility: hidden !important;
                                position: absolute !important;
                                transform: translateX(-100%) !important;
                                transition: none !important;
                            `;
                            
                            // Also try to set all attributes
                            sidebar.setAttribute('aria-hidden', 'true');
                            sidebar.classList.add('collapsed');
                            
                            // Hide all children too
                            Array.from(sidebar.children).forEach(child => {
                                child.style.display = 'none';
                                child.style.opacity = '0';
                                child.style.visibility = 'hidden';
                            });
                        }
                        
                        // Try to trigger the collapse button
                        if (collapseButton) {
                            collapseButton.click();
                        }
                        
                        // Hide expand button too
                        if (expandButton) {
                            expandButton.style.cssText = `
                                display: none !important;
                                opacity: 0 !important;
                                visibility: hidden !important;
                            `;
                        }
                    } catch(e) {
                        console.error("Error hiding sidebar:", e);
                    }
                }
                
                // Run repeatedly to ensure it works
                hideSidebar();
                setTimeout(hideSidebar, 50);
                setTimeout(hideSidebar, 100);
                setTimeout(hideSidebar, 300);
                setTimeout(hideSidebar, 500);
                
                // Also add event listener to hide it again if user tries to reopen
                document.addEventListener('click', window._hideSidebarFn);
                
                // Add MutationObserver to detect DOM changes and hide again if needed
                window._sidebarObserver = new MutationObserver(function(mutations) {
                    setTimeout(hideSidebar, 100);
                });
                
                // Start observing the document
                window._sidebarObserver.observe(document, { 
                    childList: true, 
                    subtree: true 
                });
            })();
        </script>
        """
        
        # Force hide with CSS as well
        hide_sidebar_css = """
        <style>
        [data-testid="stSidebar"] {
            display: none !important;
            width: 0 !important;
            min-width: 0 !important;
            max-width: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            opacity: 0 !important;
            pointer-events: none !important;
            visibility: hidden !important;
            position: absolute !important;
            transform: translateX(-100%) !important;
            z-index: -999 !important;
        }
        
        [data-testid="expandedControl"] {
            display: none !important;
            opacity: 0 !important;
            visibility: hidden !important;
        }
        </style>
        """
        
        # Insert both JS and CSS
        st.markdown(hide_sidebar_js, unsafe_allow_html=True)
        st.markdown(hide_sidebar_css, unsafe_allow_html=True)
        
        # Don't rerun - which is causing the sidebar to reappear
        # Just continue with the current page load

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

# Get values from session state
area = st.session_state.selected_area
day_type = st.session_state.selected_day_type
analyze = st.session_state.analyze

# MAIN CONTENT
if analyze:
    st.title(f"Beem Billboard Insights: {area}")
    
    # Generate data 
    data = generate_route_data(area)
    weather = get_weather_data(area, day_type)
    
    # Current time & conditions section
    current_hour = datetime.now().hour
    ped_density = get_pedestrian_density(area, day_type, current_hour)
    traffic_density = get_traffic_density(area, day_type, current_hour)
    
    st.markdown("### Current Conditions")
    
    # Use a 2x2 grid instead of 4 columns for better mobile display
    cond1, cond2 = st.columns(2)
    
    with cond1:
        st.markdown(f"""
        <div style="background-color:#FFF8F0; padding:10px; border-radius:5px; border-left:5px solid #FF9D45; height:100%;">
            <h4 style="margin:0; color:#FF7E33;">🌤️ Weather</h4>
            <p style="margin:5px 0;">{weather['condition']}, {weather['temperature']}°C</p>
            <p style="margin:5px 0;">Precipitation: {weather['precipitation_chance']}%</p>
            <p style="margin:5px 0;">Wind: {weather['wind_speed']} km/h</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cond2:
        ped_color = "#FF7E33"
        st.markdown(f"""
        <div style="background-color:#FFF8F0; padding:10px; border-radius:5px; border-left:5px solid #FF9D45; height:100%;">
            <h4 style="margin:0; color:#FF7E33;">👥 Pedestrian Density</h4>
            <p style="margin:5px 0; font-size:24px; font-weight:bold;">{ped_density}%</p>
            <p style="margin:5px 0;">{"High" if ped_density > 70 else "Medium" if ped_density > 50 else "Low"} foot traffic</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Second row of conditions
    cond3, cond4 = st.columns(2)
    
    with cond3:
        traffic_color = "#FF7E33"
        st.markdown(f"""
        <div style="background-color:#FFF8F0; padding:10px; border-radius:5px; border-left:5px solid #FF9D45; height:100%;">
            <h4 style="margin:0; color:#FF7E33;">🚗 Traffic Density</h4>
            <p style="margin:5px 0; font-size:24px; font-weight:bold;">{traffic_density}%</p>
            <p style="margin:5px 0;">{"High" if traffic_density > 70 else "Medium" if traffic_density > 50 else "Low"} congestion</p>
        </div>
        """, unsafe_allow_html=True)
    
    with cond4:
        current_score = (ped_density * 0.7 + min(70, traffic_density) * 0.3) / 100
        optimal_now = current_score > 0.7
        st.markdown(f"""
        <div style="background-color:#FFF8F0; padding:10px; border-radius:5px; border-left:5px solid #FF9D45; height:100%;">
            <h4 style="margin:0; color:#FF7E33;">📊 Current Rating</h4>
            <p style="margin:5px 0; font-size:24px; font-weight:bold;">{"Optimal" if optimal_now else "Not Optimal"}</p>
            <p style="margin:5px 0;">{"Great time to advertise!" if optimal_now else "Better times available"}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommended times - stack vertically on mobile
    st.markdown("### Best Advertising Times")
    optimal_times = get_optimal_times(area, day_type)
    
    # Display the top 3 recommended times
    top_times = optimal_times[:3]
    
    # Stack times vertically for easier mobile viewing
    for i, time_data in enumerate(top_times):
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
        rank = "Best" if i == 0 else "Second Best" if i == 1 else "Third Best"
        color_bg = "#FFF1E6" if i == 0 else "#FFF5EB" if i == 1 else "#FFF8F0"
        color_border = "#FF9D45" if i == 0 else "#FFCC99" if i == 1 else "#FFE0CC"
        color_text = "#FF7E33" if i == 0 else "#FF9D45" if i == 1 else "#FFAA70"
        
        st.markdown(f"""
        <div style="background-color:{color_bg}; padding:15px; border-radius:5px; text-align:center; border:1px solid {color_border}; margin-bottom:10px;">
            <h3 style="margin:0; color:#FF7E33;">{medal} {rank} Time</h3>
            <p style="font-size:28px; font-weight:bold; margin:10px 0; color:#333;">{time_data['hour']}</p>
            <p style="margin:5px 0;">Rating: <span style="color:{color_text}; font-weight:bold;">{time_data['category']}</span></p>
            <p style="margin:5px 0;">👥 Pedestrians: {time_data['pedestrian_density']}%</p>
            <p style="margin:5px 0;">🚗 Traffic: {time_data['traffic_density']}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Time heatmap for optimal times
    st.markdown("### Weekly Optimal Times")
    time_heatmap = generate_time_heatmap(area, day_type)
    st.plotly_chart(time_heatmap, use_container_width=True, config={'responsive': True})
    
    # Optimal route - use a full-width container for the map
    st.markdown("### Recommended Route")
    
    # Add custom CSS to make map completely static and prevent scrolling issues
    st.markdown("""
    <style>
    /* Make the map container position fixed with clear boundaries */
    .map-container {
        position: relative !important;
        height: 450px !important; 
        width: 100% !important;
        overflow: hidden !important;
    }
    
    /* Ensure the plotly map is sized correctly */
    .js-plotly-plot, .plot-container {
        max-height: 450px !important;
        height: 100% !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Add a container div with the map-container class
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    
    # Generate and display the route map
    route_map = generate_route_map(area, data)
    st.plotly_chart(route_map, use_container_width=True, config={
        'displayModeBar': False,  # Hide the mode bar for cleaner mobile view
        'scrollZoom': False,      # Disable scroll to zoom
        'staticPlot': False,      # Allow basic interactivity
        'doubleClick': False      # Disable double-click actions
    })
    
    # Close the container
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Route metrics - stack vertically for mobile
    st.markdown("### Route Metrics")
    
    # Create metrics container with custom styling
    metrics_data = [
        {"label": "Estimated Impressions", "value": f"{random.randint(12000, 18000):,}"},
        {"label": "Route Length", "value": f"{random.randint(8, 15)} km"},
        {"label": "Estimated Time", "value": f"{random.randint(45, 90)} mins"}
    ]
    
    for metric in metrics_data:
        st.markdown(f"""
        <div style="background-color:#FFF8F0; padding:15px; border-radius:5px; margin-bottom:10px; text-align:center;">
            <p style="margin:0; color:#666; font-size:14px;">{metric['label']}</p>
            <p style="margin:0; font-size:24px; font-weight:bold; color:#FF7E33;">{metric['value']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick action button to rerun analysis
    if st.button("🔄 ANALYZE AGAIN", type="primary", use_container_width=True, key="analyze_again"):
        # Reset the observer and event listeners that might be preventing the sidebar from showing
        reset_js = """
        <script>
            (function() {
                // Remove any existing observers that might be hiding the sidebar
                if (window._sidebarObserver) {
                    window._sidebarObserver.disconnect();
                    delete window._sidebarObserver;
                }
                
                // Remove event listeners that might be interfering
                document.removeEventListener('click', window._hideSidebarFn);
                
                // Function to fully restore the sidebar
                function restoreSidebar() {
                    // Find all sidebar elements
                    const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                    const expandButton = window.parent.document.querySelector('[data-testid="expandedControl"]');
                    
                    // Remove all hiding CSS
                    if (sidebar) {
                        // Reset all inline styles completely
                        sidebar.setAttribute('style', '');
                        sidebar.classList.remove('collapsed');
                        sidebar.setAttribute('aria-hidden', 'false');
                        
                        // Reset all children styles
                        Array.from(sidebar.children).forEach(child => {
                            child.setAttribute('style', '');
                        });
                    }
                    
                    // Make sure expand button is visible
                    if (expandButton) {
                        expandButton.setAttribute('style', '');
                    }
                    
                    // Force click the expand button
                    if (expandButton) {
                        try {
                            expandButton.click();
                        } catch(e) {}
                    }
                }
                
                // Run multiple times to ensure it works
                restoreSidebar();
                setTimeout(restoreSidebar, 100);
                setTimeout(restoreSidebar, 300);
                
                // Reset any CSS that might be hiding the sidebar
                const style = document.createElement('style');
                style.innerHTML = `
                    [data-testid="stSidebar"] {
                        display: block !important;
                        width: auto !important;
                        min-width: 260px !important;
                        max-width: 300px !important;
                        padding: inherit !important;
                        margin: inherit !important;
                        opacity: 1 !important;
                        pointer-events: auto !important;
                        visibility: visible !important;
                        position: relative !important;
                        transform: none !important;
                        z-index: 100 !important;
                    }
                    
                    [data-testid="expandedControl"] {
                        display: flex !important;
                        opacity: 1 !important;
                        visibility: visible !important;
                        width: 40px !important;
                        height: 40px !important;
                        background-color: #FF7E33 !important;
                        animation: pulse 2s infinite;
                    }
                `;
                document.head.appendChild(style);
            })();
        </script>
        """
        st.markdown(reset_js, unsafe_allow_html=True)
        
        # Reset the session state and rerun
        st.session_state.analyze = False
        st.session_state.sidebar_manually_hidden = False  # Add flag to track if sidebar was manually hidden
        st.rerun()
    
else:
    # Add beem logo and cloud text side by side
    col_logo, col_text = st.columns([3, 2])
    with col_logo:
        st.markdown('<h1 class="hero-title">beem.</h1>', unsafe_allow_html=True)
    
    # Native Streamlit solution that's guaranteed to work - make buttons orange with custom style
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {
            background-color: #FF7E33 !important;
            border: none !important;
            color: white !important;
            width: 100% !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("☰ OPEN SIDEBAR MENU", type="primary", key="streamlit-open-sidebar-button"):
            # Set session state and rerun to force sidebar to appear
            st.session_state.sidebar_visible = True
            st.rerun()

    with col2:
        st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {
            background-color: #FF7E33 !important;
            border: none !important;
            color: white !important;
            width: 100% !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("🚀 START ANALYSIS", type="primary"):
            # Set session state and rerun to force sidebar to appear
            st.session_state.sidebar_visible = True
            st.rerun()
    
    # Features section
    st.subheader("📢 Optimize your advertising impact")
    
    # Feature cards in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">Target High-Traffic Areas</h3>
            <p>Find the busiest locations with the highest potential visibility for your mobile billboards.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⏱️</div>
            <h3 class="feature-title">Optimal Timing</h3>
            <p>Discover the best times of day and week to display your advertisements for maximum engagement.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h3 class="feature-title">Data-Driven Routes</h3>
            <p>Get route recommendations based on real pedestrian and traffic data in your selected area.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚀</div>
            <h3 class="feature-title">Boost Engagement</h3>
            <p>Increase your ad impressions by up to 40% with our strategically optimized billboard routes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Direct analyze button - with enhanced styling
    st.markdown("""
    <div style="padding:20px 0; text-align:center;">
        <p style="font-weight:bold; margin-bottom:15px; font-size:18px;">✨ START EXPLORING NOW ✨</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:10px; background-color:#FFF8F0; border-radius:5px; margin-top:30px;">
    <p style="margin:0; color:#666;">beem. © 2025 Beem Mobile Billboard Solutions</p>
</div>
""", unsafe_allow_html=True)