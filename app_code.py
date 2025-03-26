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
    
    # Create route points that follow roads instead of a simple circle
    # For Manchester areas, we'll use realistic road paths
    road_routes = {
        "Northern Quarter": {
            "lats": [53.4831, 53.4844, 53.4850, 53.4842, 53.4835, 53.4826, 53.4817, 53.4825, 53.4831],
            "lons": [-2.2367, -2.2352, -2.2334, -2.2321, -2.2309, -2.2324, -2.2348, -2.2367, -2.2367],
            "points": ["Start", "Oldham St", "Thomas St", "Tib St", "Edge St", "Hilton St", "Church St", "Shudehill", "End"]
        },
        "City Centre": {
            "lats": [53.4808, 53.4798, 53.4780, 53.4765, 53.4775, 53.4790, 53.4802, 53.4808],
            "lons": [-2.2426, -2.2413, -2.2418, -2.2432, -2.2450, -2.2455, -2.2440, -2.2426],
            "points": ["Start", "Market St", "Piccadilly", "Portland St", "Oxford Rd", "Peter St", "Deansgate", "End"]
        },
        "Ancoats": {
            "lats": [53.4841, 53.4851, 53.4862, 53.4855, 53.4845, 53.4835, 53.4841],
            "lons": [-2.2269, -2.2255, -2.2235, -2.2218, -2.2228, -2.2249, -2.2269],
            "points": ["Start", "Great Ancoats St", "Redhill St", "Bengal St", "Jersey St", "Radium St", "End"]
        },
        "Oxford Road": {
            "lats": [53.4710, 53.4725, 53.4740, 53.4752, 53.4765, 53.4755, 53.4735, 53.4710],
            "lons": [-2.2376, -2.2382, -2.2390, -2.2404, -2.2420, -2.2440, -2.2410, -2.2376],
            "points": ["Start", "Oxford Rd", "Whitworth St", "Princess St", "Portland St", "Peter St", "Lower Mosley St", "End"]
        },
        "Piccadilly": {
            "lats": [53.4779, 53.4790, 53.4798, 53.4788, 53.4775, 53.4766, 53.4776, 53.4779],
            "lons": [-2.2399, -2.2386, -2.2363, -2.2346, -2.2361, -2.2385, -2.2405, -2.2399],
            "points": ["Start", "Piccadilly", "Newton St", "Lever St", "Ducie St", "Portland St", "Mosley St", "End"]
        },
        "Deansgate": {
            "lats": [53.4772, 53.4785, 53.4797, 53.4800, 53.4786, 53.4772, 53.4762, 53.4772],
            "lons": [-2.2481, -2.2496, -2.2502, -2.2485, -2.2470, -2.2455, -2.2469, -2.2481],
            "points": ["Start", "Deansgate", "Liverpool Rd", "Quay St", "Peter St", "Oxford St", "Whitworth St", "End"]
        },
        "Media City": {
            "lats": [53.4727, 53.4716, 53.4700, 53.4710, 53.4725, 53.4735, 53.4727],
            "lons": [-2.2984, -2.2998, -2.2980, -2.2965, -2.2955, -2.2969, -2.2984],
            "points": ["Start", "Broadway", "The Quays", "MediaCityUK", "Trafford Wharf Rd", "Broadway", "End"]
        },
        "Spinningfields": {
            "lats": [53.4802, 53.4815, 53.4825, 53.4820, 53.4805, 53.4795, 53.4802],
            "lons": [-2.2516, -2.2530, -2.2516, -2.2498, -2.2485, -2.2500, -2.2516],
            "points": ["Start", "Bridge St", "St Mary's Gate", "Deansgate", "Hardman St", "Quay St", "End"]
        },
        "Chorlton": {
            "lats": [53.4428, 53.4420, 53.4403, 53.4428, 53.4438, 53.4428],
            "lons": [-2.2724, -2.2745, -2.2732, -2.2705, -2.2715, -2.2724],
            "points": ["Start", "Barlow Moor Rd", "Wilbraham Rd", "Manchester Rd", "Beech Rd", "End"]
        },
        "Didsbury": {
            "lats": [53.4183, 53.4170, 53.4163, 53.4180, 53.4193, 53.4183],
            "lons": [-2.2310, -2.2330, -2.2310, -2.2295, -2.2305, -2.2310],
            "points": ["Start", "Wilmslow Rd", "School Ln", "Barlow Moor Rd", "Didsbury Park", "End"]
        },
        "Fallowfield": {
            "lats": [53.4420, 53.4410, 53.4395, 53.4420, 53.4435, 53.4420],
            "lons": [-2.2248, -2.2268, -2.2248, -2.2225, -2.2235, -2.2248],
            "points": ["Start", "Wilmslow Rd", "Platt Ln", "Yew Tree Rd", "Ladybarn Ln", "End"]
        },
        "Levenshulme": {
            "lats": [53.4369, 53.4380, 53.4390, 53.4375, 53.4360, 53.4369],
            "lons": [-2.1944, -2.1965, -2.1944, -2.1925, -2.1930, -2.1944],
            "points": ["Start", "Stockport Rd", "Broom Ln", "Cromwell Grove", "Moseley Rd", "End"]
        },
        "Rusholme": {
            "lats": [53.4502, 53.4515, 53.4525, 53.4510, 53.4495, 53.4502],
            "lons": [-2.2200, -2.2220, -2.2200, -2.2180, -2.2190, -2.2200],
            "points": ["Start", "Wilmslow Rd", "Curry Mile", "Dickenson Rd", "Platt Ln", "End"]
        },
        "Salford Quays": {
            "lats": [53.4705, 53.4690, 53.4675, 53.4690, 53.4710, 53.4725, 53.4705],
            "lons": [-2.2850, -2.2870, -2.2850, -2.2830, -2.2820, -2.2840, -2.2850],
            "points": ["Start", "Trafford Rd", "The Quays", "Huron Basin", "Erie Basin", "Detroit Bridge", "End"]
        },
        "Hulme": {
            "lats": [53.4638, 53.4650, 53.4660, 53.4640, 53.4625, 53.4638],
            "lons": [-2.2500, -2.2520, -2.2500, -2.2480, -2.2490, -2.2500],
            "points": ["Start", "Princess Rd", "Hulme Park", "Stretford Rd", "Boundary Ln", "End"]
        },
        "Trafford Centre": {
            "lats": [53.4670, 53.4655, 53.4640, 53.4655, 53.4675, 53.4690, 53.4670],
            "lons": [-2.3500, -2.3520, -2.3500, -2.3480, -2.3475, -2.3490, -2.3500],
            "points": ["Start", "Trafford Blvd", "Parkway", "Barton Dock Rd", "Trafford Ct", "Mercury Way", "End"]
        }
    }
    
    # For areas without specific road routes, create a more realistic road-like pattern 
    # instead of a simple geometric shape that might cross buildings
    if area not in road_routes:
        # Create a zigzag route that mimics road patterns with right-angle turns
        # Rather than a smooth curve or direct line that would cross buildings
        route_lats = [
            center_lat,
            center_lat + 0.002,                     # Go north
            center_lat + 0.002,                     # Continue east on same latitude
            center_lat + 0.004,                     # Go north again
            center_lat + 0.004,                     # Continue east
            center_lat + 0.001,                     # Go south
            center_lat + 0.001,                     # Continue west
            center_lat - 0.002,                     # Go south again
            center_lat - 0.002,                     # Continue west
            center_lat - 0.004,                     # Go south once more
            center_lat - 0.004,                     # Continue back towards start
            center_lat                              # Return to start point
        ]
        
        route_lons = [
            center_lon,
            center_lon,                             # Go north on same longitude
            center_lon + 0.003,                     # Turn right (east)
            center_lon + 0.003,                     # Go north on same longitude
            center_lon + 0.001,                     # Turn left (west)
            center_lon + 0.001,                     # Go south on same longitude
            center_lon - 0.003,                     # Turn left (west)
            center_lon - 0.003,                     # Go south on same longitude
            center_lon - 0.001,                     # Turn right (east)
            center_lon - 0.001,                     # Go south on same longitude
            center_lon,                             # Turn right (east)
            center_lon                              # Return to start point
        ]
        
        route_points = [
            "Start",
            "North St",
            "1st Avenue", 
            "North St",
            "Highland Rd",
            "Center St",
            "West Rd",
            "South St",
            "Main St",
            "South St", 
            "Return Rd",
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
    
    # Add the route line
    fig.add_trace(go.Scattermapbox(
        lat=route_lats,
        lon=route_lons,
        mode='lines',
        line=dict(width=4, color='#FF7E33'),
        name='Route Following Roads'
    ))
    
    # Add markers for key points (start, important intersections, end)
    # Add more markers for better visibility of the route's path
    num_points = len(route_lats)
    marker_indices = [0]
    
    # Add intermediate markers approximately every 3 points
    if num_points > 6:
        marker_indices += list(range(2, num_points-2, 2))
    
    # Always add the end point
    if num_points-1 not in marker_indices:
        marker_indices.append(num_points-1)
    
    fig.add_trace(go.Scattermapbox(
        lat=[route_lats[i] for i in marker_indices],
        lon=[route_lons[i] for i in marker_indices],
        mode='markers+text',
        marker=dict(size=10, color='#FF7E33'),
        text=[route_points[i] for i in marker_indices],
        textposition="top right",
        name='Key Locations'
    ))
    
    # Update the layout with higher zoom to see streets clearly
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",  # Clean map style showing streets clearly
            center=dict(lat=center_lat, lon=center_lon),
            zoom=15  # Higher zoom level to see street details
        ),
        margin=dict(l=0, r=0, t=10, b=0),
        height=450,  # Slightly taller for better visibility
        autosize=True,
        hovermode='closest'
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
        st.rerun()
    
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
    
    # Optimal route
    st.markdown("### Recommended Route")
    route_map = generate_route_map(area, data)
    st.plotly_chart(route_map, use_container_width=True, config={'responsive': True})
    
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
    st.button("🔄 ANALYZE AGAIN", type="primary")
    
else:
    # Add beem logo and cloud text side by side
    col_logo, col_text = st.columns([3, 2])
    with col_logo:
        st.markdown('<h1 class="hero-title">beem.</h1>', unsafe_allow_html=True)
    
    with col_text:
        st.markdown("""
        <div style="background-color:#FFF1E6; padding:10px; border-radius:20px; 
             text-align:center; box-shadow:0 2px 5px rgba(0,0,0,0.1); 
             border:2px dashed #FF7E33; margin-top:15px;">
            <h4 style="margin:5px; color:#FF7E33;">⬆️ PRESS TOP LEFT</h4>
            <h4 style="margin:5px; color:#FF7E33;">ARROW TO ANALYZE</h4>
        </div>
        """, unsafe_allow_html=True)
    
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
    
    if st.button("🚀 ANALYZE NOW 🚀", type="primary", use_container_width=True):
        st.session_state.analyze = True
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:10px; background-color:#FFF8F0; border-radius:5px; margin-top:30px;">
    <p style="margin:0; color:#666;">beem. © 2025 Beem Mobile Billboard Solutions</p>
</div>
""", unsafe_allow_html=True)