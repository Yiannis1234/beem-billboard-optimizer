
import streamlit as st
import requests
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Configure Streamlit
st.set_page_config(
    page_title="Ad Success Predictor (Manchester & London)",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Universal CSS for Light and Dark Mode Compatibility
st.markdown("""
<style>
    /* Root variables for theme switching */
    :root {
        --primary-color: #00d4aa;
        --primary-dark: #00b894;
        --secondary-color: #0066cc;
        --text-primary: #2d3436;
        --text-secondary: #636e72;
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --border-color: #e9ecef;
        --shadow: rgba(0,0,0,0.1);
    }

    /* Dark mode variables */
    @media (prefers-color-scheme: dark) {
        :root {
            --text-primary: #ffffff;
            --text-secondary: #b2bec3;
            --bg-primary: #1a1a1a;
            --bg-secondary: #2d2d2d;
            --border-color: #404040;
            --shadow: rgba(255,255,255,0.1);
        }
    }

    /* Force dark mode detection and apply styles */
    .stApp {
        background-color: var(--bg-secondary) !important;
    }

    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: var(--secondary-color);
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Card styling with perfect visibility */
    .success-card {
        background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white !important;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 8px var(--shadow);
    }
    .success-card h2, .success-card h3, .success-card p { color: white !important; }
    .success-card .metric-highlight { color: white !important; }

    .warning-card {
        background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white !important;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 8px var(--shadow);
    }
    .warning-card h2, .warning-card h3, .warning-card p { color: white !important; }
    .warning-card .metric-highlight { color: white !important; }

    .danger-card {
        background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white !important;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 8px var(--shadow);
    }
    .danger-card h2, .danger-card h3, .danger-card p { color: white !important; }
    .danger-card .metric-highlight { color: white !important; }

    /* Reason box with theme-aware styling */
    .reason-box {
        background: var(--bg-primary);
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid var(--primary-color);
        margin: 0.5rem 0;
        color: var(--text-primary) !important;
        box-shadow: 0 2px 4px var(--shadow);
        border: 1px solid var(--border-color);
    }
    .reason-box strong { color: var(--text-primary) !important; }

    /* Metric highlight styling */
    .metric-highlight {
        font-size: 2rem;
        font-weight: bold;
        color: white !important;
    }

    /* Universal text visibility fixes */
    .main .block-container { 
        color: var(--text-primary) !important; 
        background: transparent !important; 
    }
    .main .block-container p, 
    .main .block-container h1, h2, h3, h4, h5, h6,
    .main .block-container div, 
    .main .block-container span, 
    .main .block-container label { 
        color: var(--text-primary) !important; 
    }

    /* Selectbox styling */
    .stSelectbox label, 
    .stSelectbox div { 
        color: var(--text-primary) !important; 
    }
    .stSelectbox > div > div { 
        background-color: var(--bg-primary) !important; 
        color: var(--text-primary) !important; 
        border: 2px solid var(--primary-color) !important; 
        border-radius: 8px !important; 
    }
    .stSelectbox > div > div > div, 
    .stSelectbox > div > div > div > div { 
        background-color: var(--bg-primary) !important; 
        color: var(--text-primary) !important; 
    }

    /* Button styling */
    .stButton button { 
        color: white !important; 
        background-color: var(--primary-color) !important; 
        border: none !important;
    }

    /* Metric containers */
    .stMetric, 
    .stMetric label, 
    .stMetric div { 
        color: var(--text-primary) !important; 
    }

    div[data-testid="metric-container"] {
        background-color: var(--bg-primary) !important; 
        color: var(--text-primary) !important; 
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important; 
        padding: 1rem !important;
    }
    div[data-testid="metric-container"] div, 
    div[data-testid="metric-container"] label, 
    div[data-testid="metric-container"] span { 
        color: var(--text-primary) !important; 
    }

    /* Data table styling */
    .stDataFrame { 
        background-color: var(--bg-primary) !important; 
        color: var(--text-primary) !important; 
        border: 2px solid var(--primary-color) !important; 
        border-radius: 10px !important; 
    }
    .stDataFrame table { 
        background-color: var(--bg-primary) !important; 
        color: var(--text-primary) !important; 
    }
    .stDataFrame th { 
        background-color: var(--primary-color) !important; 
        color: white !important; 
        font-weight: bold !important; 
        padding: 12px !important; 
    }
    .stDataFrame td { 
        background-color: var(--bg-primary) !important; 
        color: var(--text-primary) !important; 
        padding: 10px !important; 
        border-bottom: 1px solid var(--border-color) !important; 
    }
    .stDataFrame tr:nth-child(even) { 
        background-color: var(--bg-secondary) !important; 
    }
    .stDataFrame tr:hover { 
        background-color: rgba(0, 212, 170, 0.1) !important; 
    }

    /* Alert boxes */
    .stAlert {
        background-color: var(--bg-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 25px var(--shadow) !important;
    }
    .stAlert > div { 
        color: var(--text-primary) !important; 
    }

    /* Success, info, warning, error alerts */
    .stSuccess {
        background-color: rgba(0, 212, 170, 0.1) !important;
        border-left: 4px solid var(--primary-color) !important;
        color: var(--text-primary) !important;
    }
    .stInfo {
        background-color: rgba(0, 102, 204, 0.1) !important;
        border-left: 4px solid var(--secondary-color) !important;
        color: var(--text-primary) !important;
    }
    .stWarning {
        background-color: rgba(253, 203, 110, 0.1) !important;
        border-left: 4px solid #fdcb6e !important;
        color: var(--text-primary) !important;
    }
    .stError {
        background-color: rgba(253, 121, 168, 0.1) !important;
        border-left: 4px solid #fd79a8 !important;
        color: var(--text-primary) !important;
    }

    /* Container backgrounds */
    .main { 
        background-color: var(--bg-secondary) !important; 
    }
    .element-container, 
    .stColumn { 
        background-color: transparent !important; 
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .stDataFrame { 
            border-radius: 12px; 
            font-size: 0.9rem; 
        }
        .stDataFrame th, 
        .stDataFrame td { 
            padding: 0.6rem 0.8rem; 
        }
        .stAlert { 
            padding: 1.2rem; 
            border-radius: 12px; 
        }
        .main-header {
            font-size: 2rem;
        }
    }

    /* Force visibility for all text elements */
    * {
        color: inherit;
    }
    
    /* Override any Streamlit default colors */
    .stApp > div {
        color: var(--text-primary) !important;
    }
    
    /* Ensure all headings are visible */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
    }
    
    /* Ensure all paragraphs are visible */
    p {
        color: var(--text-primary) !important;
    }
    
    /* Ensure all labels are visible */
    label {
        color: var(--text-primary) !important;
    }
</style>
""", unsafe_allow_html=True)

class SimpleAdSuccessPredictor:
    def __init__(self):
        self.manchester_areas = {
            "Albert Square": {
                "center": {"lat": 53.4794, "lon": -2.2453},
                "population": 25000,
                "footfall_daily": 120000,
                "success_factors": {
                    "high_traffic": True,
                    "business_district": True,
                    "transport_hub": True,
                    "affluent_audience": True,
                    "shopping_area": True
                },
                "description": "Historic square with Town Hall - high foot traffic and prestige"
            },
            "Piccadilly": {
                "center": {"lat": 53.4808, "lon": -2.2308},
                "population": 10000,
                "footfall_daily": 400000,
                "success_factors": {
                    "high_traffic": True,
                    "transport_hub": True,
                    "commuter_area": True,
                    "business_district": False
                },
                "description": "Main transport hub - people wait here, perfect for ads"
            },
            "Oxford Road": {
                "center": {"lat": 53.4708, "lon": -2.2358},
                "population": 25000,
                "footfall_daily": 300000,
                "success_factors": {
                    "high_traffic": True,
                    "student_area": True,
                    "university_district": True,
                    "young_audience": True
                },
                "description": "University area - young, engaged audience"
            },
            "Northern Quarter": {
                "center": {"lat": 53.4858, "lon": -2.2358},
                "population": 8000,
                "footfall_daily": 120000,
                "success_factors": {
                    "high_traffic": False,
                    "creative_area": True,
                    "trendy_audience": True,
                    "nightlife": True
                },
                "description": "Creative district - trendy, brand-conscious audience"
            },
            "Deansgate": {
                "center": {"lat": 53.4758, "lon": -2.2508},
                "population": 7000,
                "footfall_daily": 180000,
                "success_factors": {
                    "high_traffic": True,
                    "shopping_area": True,
                    "affluent_audience": True,
                    "leisure_time": True
                },
                "description": "Shopping district - people with money and time to spend"
            },
            "Spinningfields": {
                "center": {"lat": 53.4788, "lon": -2.2508},
                "population": 5000,
                "footfall_daily": 200000,
                "success_factors": {
                    "high_traffic": True,
                    "business_district": True,
                    "affluent_audience": True,
                    "corporate_area": True
                },
                "description": "Financial district - high-earning professionals"
            },
            "Chorlton": {
                "center": {"lat": 53.4508, "lon": -2.2708},
                "population": 18000,
                "footfall_daily": 90000,
                "success_factors": {
                    "high_traffic": False,
                    "affluent_suburb": True,
                    "family_area": True,
                    "local_businesses": True
                },
                "description": "Trendy suburb - affluent families and professionals"
            },
            "Didsbury": {
                "center": {"lat": 53.4208, "lon": -2.2308},
                "population": 22000,
                "footfall_daily": 75000,
                "success_factors": {
                    "high_traffic": False,
                    "affluent_suburb": True,
                    "family_area": True,
                    "local_community": True
                },
                "description": "Affluent suburb - wealthy families and professionals"
            },
            "Stockport": {
                "center": {"lat": 53.4106, "lon": -2.1575},
                "population": 35000,
                "footfall_daily": 45000,
                "success_factors": {
                    "high_traffic": True,
                    "shopping_area": True,
                    "transport_hub": True,
                    "affluent_audience": False,
                    "student_area": False
                },
                "description": "Historic market town - good shopping and transport links"
            },
            "Bolton": {
                "center": {"lat": 53.5767, "lon": -2.4282},
                "population": 40000,
                "footfall_daily": 55000,
                "success_factors": {
                    "high_traffic": True,
                    "shopping_area": True,
                    "business_district": True,
                    "affluent_audience": False,
                    "student_area": False
                },
                "description": "Large town with shopping center and business district"
            },
            "Bury": {
                "center": {"lat": 53.5928, "lon": -2.2981},
                "population": 28000,
                "footfall_daily": 38000,
                "success_factors": {
                    "high_traffic": True,
                    "shopping_area": True,
                    "transport_hub": True,
                    "affluent_audience": False,
                    "student_area": False
                },
                "description": "Market town with good shopping and transport connections"
            },
            "Rochdale": {
                "center": {"lat": 53.6097, "lon": -2.1561},
                "population": 32000,
                "footfall_daily": 42000,
                "success_factors": {
                    "high_traffic": True,
                    "shopping_area": True,
                    "business_district": True,
                    "affluent_audience": False,
                    "student_area": False
                },
                "description": "Historic town with shopping center and business activity"
            },
            "Oldham": {
                "center": {"lat": 53.5409, "lon": -2.1114},
                "population": 30000,
                "footfall_daily": 40000,
                "success_factors": {
                    "high_traffic": True,
                    "shopping_area": True,
                    "transport_hub": True,
                    "affluent_audience": False,
                    "student_area": False
                },
                "description": "Town center with shopping and transport hub"
            }
        }

        self.london_areas = {
            "Oxford Circus": {
                "center": {"lat": 51.5154, "lon": -0.1410},
                "population": 20000,
                "footfall_daily": 450000,
                "success_factors": {
                    "high_traffic": True,
                    "shopping_area": True,
                    "affluent_audience": True,
                    "transport_hub": False
                },
                "description": "Iconic West End shopping junction with extremely high footfall"
            },
            "Piccadilly Circus": {
                "center": {"lat": 51.5098, "lon": -0.1340},
                "population": 15000,
                "footfall_daily": 400000,
                "success_factors": {
                    "high_traffic": True,
                    "shopping_area": True,
                    "tourist_area": True
                },
                "description": "Tourist hotspot with giant screens and constant pedestrian flow"
            },
            "Liverpool Street": {
                "center": {"lat": 51.5178, "lon": -0.0824},
                "population": 18000,
                "footfall_daily": 380000,
                "success_factors": {
                    "high_traffic": True,
                    "transport_hub": True,
                    "business_district": True
                },
                "description": "Major commuter hub in the City with strong professional audience"
            },
            "Canary Wharf": {
                "center": {"lat": 51.5054, "lon": -0.0235},
                "population": 12000,
                "footfall_daily": 300000,
                "success_factors": {
                    "business_district": True,
                    "affluent_audience": True,
                    "high_traffic": True
                },
                "description": "Financial district with affluent professionals and premium brands"
            },
            "Shoreditch": {
                "center": {"lat": 51.5260, "lon": -0.0803},
                "population": 10000,
                "footfall_daily": 180000,
                "success_factors": {
                    "creative_area": True,
                    "nightlife": True,
                    "high_traffic": True
                },
                "description": "Trendy creative area with young, brand-conscious audience"
            },
            "South Bank": {
                "center": {"lat": 51.5066, "lon": -0.1163},
                "population": 8000,
                "footfall_daily": 220000,
                "success_factors": {
                    "tourist_area": True,
                    "shopping_area": True,
                    "high_traffic": True
                },
                "description": "Riverside cultural district with heavy tourist footfall"
            },
            "King's Cross": {
                "center": {"lat": 51.5308, "lon": -0.1238},
                "population": 11000,
                "footfall_daily": 320000,
                "success_factors": {
                    "transport_hub": True,
                    "business_district": True,
                    "high_traffic": True
                },
                "description": "Major rail hub with offices and retail – long dwell times"
            },
            "Camden Town": {
                "center": {"lat": 51.5416, "lon": -0.1420},
                "population": 9000,
                "footfall_daily": 160000,
                "success_factors": {
                    "creative_area": True,
                    "shopping_area": True,
                    "nightlife": True
                },
                "description": "Market and music area – strong youth and tourist traffic"
            }
        }

    def get_weather_data(self, lat, lon):
        """Get real weather data from WeatherAPI.com with fallback"""
        try:
            url = f"http://api.weatherapi.com/v1/forecast.json?key=f70bd534000447b2a14202431252303&q={lat},{lon}&days=1&aqi=no&alerts=no"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                current = data.get('current', {})
                condition = current.get('condition', {}) or {}
                return {
                    'temperature': current.get('temp_c', 12),
                    'condition': condition.get('text', 'Partly Cloudy'),
                    'visibility': current.get('vis_km', 10),
                    'wind_kph': current.get('wind_kph', 8),
                    'humidity': current.get('humidity', 70),
                    'uv': current.get('uv', 2),
                    'precip_mm': current.get('precip_mm', 0.0),
                    'is_day': current.get('is_day', 1)
                }
            else:
                return {
                    'temperature': 12, 'condition': 'Partly Cloudy', 'visibility': 10,
                    'wind_kph': 8, 'humidity': 70, 'uv': 2, 'precip_mm': 0.0, 'is_day': 1
                }
        except Exception:
            return {
                'temperature': 12, 'condition': 'Partly Cloudy', 'visibility': 10,
                'wind_kph': 8, 'humidity': 70, 'uv': 2, 'precip_mm': 0.0, 'is_day': 1
            }

    def get_traffic_data(self, lat, lon):
        """Get comprehensive traffic data from TomTom API with enhanced fallback"""
        try:
            # TomTom Traffic Flow API endpoint
            url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key=sljp3YAvFa7J3EalnGslYfnSCZg6VQUg"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if we have valid flow data
                if 'flowSegmentData' in data and data['flowSegmentData']:
                    flow_data = data['flowSegmentData']
                    current_speed = flow_data.get('currentSpeed', 0)
                    free_flow_speed = flow_data.get('freeFlowSpeed', 50)
                    confidence = flow_data.get('confidence', 0)
                    
                    # Calculate congestion level with more granular levels
                    speed_ratio = current_speed / free_flow_speed if free_flow_speed > 0 else 0
                    
                    if speed_ratio >= 0.9:
                        congestion_level = 'Free Flow'
                        congestion_color = '🟢'
                    elif speed_ratio >= 0.7:
                        congestion_level = 'Light'
                        congestion_color = '🟡'
                    elif speed_ratio >= 0.5:
                        congestion_level = 'Moderate'
                        congestion_color = '🟠'
                    elif speed_ratio >= 0.3:
                        congestion_level = 'Heavy'
                        congestion_color = '🔴'
                    else:
                        congestion_level = 'Very Heavy'
                        congestion_color = '🛑'
                    
                    # Calculate additional metrics
                    delay_minutes = max(0, (free_flow_speed - current_speed) / 60 * 10)  # Rough delay estimate
                    traffic_density = min(100, (1 - speed_ratio) * 100)  # Density percentage
                    
                    return {
                        'current_speed': round(current_speed, 1),
                        'free_flow_speed': round(free_flow_speed, 1),
                        'congestion_level': congestion_level,
                        'congestion_color': congestion_color,
                        'speed_ratio': round(speed_ratio, 2),
                        'confidence': confidence,
                        'delay_minutes': round(delay_minutes, 1),
                        'traffic_density': round(traffic_density, 1),
                        'api_status': 'Live Data',
                        'last_updated': datetime.now().strftime('%H:%M')
                    }
                else:
                    # No flow data available
                    return self._get_fallback_traffic_data("No traffic data available")
            else:
                # API error
                return self._get_fallback_traffic_data(f"API Error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            return self._get_fallback_traffic_data("Request timeout")
        except requests.exceptions.RequestException as e:
            return self._get_fallback_traffic_data(f"Network error: {str(e)[:50]}")
        except Exception as e:
            return self._get_fallback_traffic_data(f"Unexpected error: {str(e)[:50]}")
    
    def _get_fallback_traffic_data(self, reason):
        """Provide fallback traffic data when API is unavailable"""
        return {
            'current_speed': 28.0,
            'free_flow_speed': 50.0,
            'congestion_level': 'Light',
            'congestion_color': '🟡',
            'speed_ratio': 0.56,
            'confidence': 0,
            'delay_minutes': 3.7,
            'traffic_density': 44.0,
            'api_status': f'Fallback ({reason})',
            'last_updated': datetime.now().strftime('%H:%M')
        }

    def _weather_adjustments(self, weather):
        """Derive score and impression adjustments from detailed weather."""
        condition = (weather['condition'] or '').lower()
        temp = weather['temperature']
        vis = weather['visibility']
        wind = weather['wind_kph']
        precip = weather['precip_mm']
        uv = weather['uv']

        score_delta = 0
        impression_pct = 0  # percent change

        notes = []

        # Visibility impact
        if vis >= 9:
            score_delta += 4
            notes.append("☀️ Very clear visibility = creative pops")
        elif vis >= 6:
            score_delta += 2
            notes.append("⛅ Good visibility")
        elif vis >= 3:
            score_delta -= 3
            impression_pct -= 5
            notes.append("🌫️ Low visibility reduces readability")
        else:
            score_delta -= 6
            impression_pct -= 10
            notes.append("🌁 Very poor visibility significantly hurts viewing")

        # Precipitation / condition impact
        raining = "rain" in condition or precip >= 0.5
        snowing = "snow" in condition
        storm = "storm" in condition or "thunder" in condition

        if storm:
            score_delta -= 6
            impression_pct -= 12
            notes.append("⛈️ Storms: people rush / hide indoors")
        elif snowing:
            score_delta -= 5
            impression_pct -= 10
            notes.append("❄️ Snow: travel disruption reduces exposure")
        elif raining:
            score_delta -= 3
            impression_pct -= 6
            notes.append("🌧️ Rain: shorter dwell time outdoors")
        elif "sunny" in condition or "clear" in condition:
            score_delta += 3
            impression_pct += 4
            notes.append("🌞 Sunny: higher dwell time and mood boost")

        # Wind impact
        if wind >= 40:
            score_delta -= 4
            notes.append("🌬️ Strong wind: people move quickly")
        elif wind <= 10:
            score_delta += 1
            notes.append("🍃 Calm wind: comfortable dwell time")

        # Temperature comfort band
        if 12 <= temp <= 22:
            score_delta += 3
            impression_pct += 3
            notes.append("🌡️ Comfortable temperature increases linger time")
        elif temp < 3:
            score_delta -= 4
            impression_pct -= 8
            notes.append("🥶 Very cold: people minimize time outside")
        elif temp > 28:
            score_delta -= 2
            impression_pct -= 4
            notes.append("🥵 Hot: shade-seeking reduces ad viewing angles")

        # UV (daytime readability for non-backlit prints)
        if uv >= 7:
            score_delta -= 1
            notes.append("🕶️ High UV/glare may reduce print readability")

        return score_delta, impression_pct, notes

    def calculate_ad_success_score(self, area_name, area_data, weather_data, traffic_data):
        """Calculate realistic ad success score (0-100) with visible weather effects"""
        base_score = min(60, (area_data['footfall_daily'] / 10000))  # Max 60 from footfall

        factor_boost = 0
        factors = area_data['success_factors']
        if factors.get('high_traffic', False): factor_boost += 15
        if factors.get('business_district', False): factor_boost += 12
        if factors.get('transport_hub', False): factor_boost += 12
        if factors.get('affluent_audience', False): factor_boost += 8
        if factors.get('student_area', False): factor_boost += 8
        if factors.get('shopping_area', False): factor_boost += 8
        if factors.get('creative_area', False): factor_boost += 5

        weather_score_delta, impression_pct_delta, weather_notes = self._weather_adjustments(weather_data)

        traffic_boost = 0
        if traffic_data['congestion_level'] == 'Heavy':
            traffic_boost = 8
        elif traffic_data['congestion_level'] == 'Moderate':
            traffic_boost = 5

        raw_score = base_score + factor_boost + weather_score_delta + traffic_boost
        success_score = int(min(95, max(0, raw_score)))

        base_impressions_per_hour = int((area_data['footfall_daily'] / 24) * 0.15)
        adjusted_impressions_per_hour = int(base_impressions_per_hour * (1 + (impression_pct_delta / 100.0)))

        return {
            'area_name': area_name,
            'success_score': success_score,
            'impressions_per_hour': max(0, adjusted_impressions_per_hour),
            'success_level': self.get_success_level(success_score),
            'key_reasons': self.get_success_reasons(factors, weather_data, traffic_data, weather_notes),
            'description': area_data['description'],
            'weather_notes': weather_notes,
            'weather_score_delta': weather_score_delta,
            'impression_pct_delta': impression_pct_delta,
            'base_impressions_per_hour': base_impressions_per_hour
        }

    def get_success_level(self, score):
        if score >= 75:
            return "EXCELLENT"
        elif score >= 55:
            return "GOOD"
        elif score >= 35:
            return "MODERATE"
        else:
            return "POOR"

    def get_success_reasons(self, factors, weather_data, traffic_data, weather_notes):
        reasons = []
        if factors.get('high_traffic', False):
            reasons.append("🚶 High foot traffic = More people see your ad")
        if factors.get('business_district', False):
            reasons.append("🏢 Business area = Professional audience with money")
        if factors.get('transport_hub', False):
            reasons.append("🚉 Transport hub = People wait here = More ad time")
        if factors.get('affluent_audience', False):
            reasons.append("💰 Affluent area = People with money to spend")
        if factors.get('student_area', False):
            reasons.append("🎓 Student area = Young, engaged audience")
        if factors.get('shopping_area', False):
            reasons.append("🛍️ Shopping area = People in buying mood")
        if factors.get('creative_area', False):
            reasons.append("🎨 Creative area = Brand-conscious audience")

        if weather_notes:
            reasons.append(weather_notes[0])
        if traffic_data['congestion_level'] in ['Heavy', 'Moderate']:
            reasons.append("🚦 Traffic congestion = People stuck = More ad views")

        return reasons[:3]

def main():
    st.markdown('<h1 class="main-header">🎯 Ad Success Predictor — Manchester & London</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h3 style='color: #2d3436;'>Choose Manchester or London and get instant ad success predictions.</h3>
        <p style='color: #636e72;'>We analyze real traffic, audience and <strong>current weather</strong>. Separate buttons keep it crystal clear.</p>
    </div>
    """, unsafe_allow_html=True)

    st.info("""
    **💡 How it works:** 
    - Select any Manchester area from the dropdown
    - Click "Predict Ad Success" to get instant results
    - See your success score (0-100), how many people will see your ad, and why
    - Weather now visibly adjusts scores and impressions (e.g., rain reduces dwell time)
    - Compare all areas in the table below
    """)

    predictor = SimpleAdSuccessPredictor()

    left, right = st.columns(2)
    with left:
        m_area = st.selectbox("📍 Manchester Area", list(predictor.manchester_areas.keys()), index=0, help="Select a Manchester area")
        manchester_clicked = st.button("🔍 Predict Manchester", type="primary", use_container_width=True)
    with right:
        l_area = st.selectbox("📍 London Area", list(predictor.london_areas.keys()), index=0, help="Select a London area")
        london_clicked = st.button("🔍 Predict London", type="primary", use_container_width=True)

    selected_city = None
    if manchester_clicked:
        selected_city = ("Manchester", m_area, predictor.manchester_areas[m_area])
    elif london_clicked:
        selected_city = ("London", l_area, predictor.london_areas[l_area])

    if selected_city is not None:
        city_name, selected_area, area_data = selected_city
        weather_data = predictor.get_weather_data(area_data['center']['lat'], area_data['center']['lon'])
        traffic_data = predictor.get_traffic_data(area_data['center']['lat'], area_data['center']['lon'])
        success_data = predictor.calculate_ad_success_score(selected_area, area_data, weather_data, traffic_data)

        st.markdown("---")

        if success_data['success_level'] == "EXCELLENT":
            st.markdown(f"""
            <div class="success-card">
                <h2>🎉 EXCELLENT AD SUCCESS!</h2>
                <div class="metric-highlight">{success_data['success_score']}/100</div>
                <h3>{selected_area}</h3>
                <p>{success_data['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        elif success_data['success_level'] == "GOOD":
            st.markdown(f"""
            <div class="warning-card">
                <h2>👍 GOOD AD SUCCESS</h2>
                <div class="metric-highlight">{success_data['success_score']}/100</div>
                <h3>{selected_area}</h3>
                <p>{success_data['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="danger-card">
                <h2>⚠️ MODERATE AD SUCCESS</h2>
                <div class="metric-highlight">{success_data['success_score']}/100</div>
                <h3>{selected_area}</h3>
                <p>{success_data['description']}</p>
            </div>
            """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Ad Success Score", f"{success_data['success_score']}/100", help="Higher score = Better ad success")
        with col2:
            delta_txt = f"{success_data['impression_pct_delta']:+.0f}% from weather"
            st.metric("People See Ad/Hour", f"{success_data['impressions_per_hour']:,}", delta=delta_txt, help="Weather now adjusts impressions")
        with col3:
            st.metric("Success Level", success_data['success_level'], help="Overall success rating")

        st.subheader("🌦️ Weather & 🚦 Traffic Impact")
        wcol1, wcol2, wcol3, wcol4 = st.columns(4)
        with wcol1:
            st.metric("Condition", weather_data['condition'])
        with wcol2:
            st.metric("Temp (°C)", f"{weather_data['temperature']:.0f}")
        with wcol3:
            st.metric("Visibility (km)", f"{weather_data['visibility']}")
        with wcol4:
            st.metric("Wind (kph)", f"{weather_data['wind_kph']:.0f}")

        tcol1, tcol2 = st.columns(2)
        with tcol1:
            w_delta = f"{success_data['weather_score_delta']:+d} pts on score"
            st.info("**Weather effect**\n\n" + "\n".join([f"- {n}" for n in success_data['weather_notes'][:3]]) + f"\n\n**Net:** {w_delta}")
        with tcol2:
            # Enhanced traffic display with more details
            traffic_status = f"{traffic_data['congestion_color']} {traffic_data['congestion_level']}"
            st.info(f"**Traffic Status:** {traffic_status}\n\n"
                    f"- Current speed: {traffic_data['current_speed']} km/h\n"
                    f"- Free-flow: {traffic_data['free_flow_speed']} km/h\n"
                    f"- Traffic density: {traffic_data['traffic_density']}%\n"
                    f"- Data source: {traffic_data['api_status']}\n"
                    f"- Updated: {traffic_data['last_updated']}")

        st.subheader("🤔 Why This Area is Good for Ads:")
        for reason in success_data['key_reasons']:
            st.markdown(f"""<div class="reason-box"><strong>{reason}</strong></div>""", unsafe_allow_html=True)

        st.subheader("📈 What This Means for Your Ad:")
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"""
            **🎯 Expected Results:**
            - **{success_data['impressions_per_hour']:,} people** will see your ad every hour
            - **Success rate:** {success_data['success_score']}% chance of good performance
            - **Best time:** Peak hours (8-10am, 5-7pm)
            """)
        with col2:
            if success_data['success_score'] >= 75:
                st.info("""
                **💡 Pro Tips:**
                - This is an **excellent** location!
                - Consider premium ad placement
                - Run ads during peak hours
                - Monitor performance closely
                """)
            elif success_data['success_score'] >= 55:
                st.warning("""
                **💡 Pro Tips:**
                - This is a **good** location
                - Focus on peak traffic times
                - Consider A/B testing
                - Monitor competitor activity
                """)
            else:
                st.error("""
                **💡 Pro Tips:**
                - This area has **moderate** potential
                - Consider other locations first
                - If using this area, focus on weekends
                - Lower your ad spend expectations
                """)

        st.subheader(f"📊 Quick Area Comparison — {city_name}")
        all_scores = []
        city_dict = predictor.manchester_areas if city_name == "Manchester" else predictor.london_areas
        for area_name, a_data in city_dict.items():
            weather = predictor.get_weather_data(a_data['center']['lat'], a_data['center']['lon'])
            traffic = predictor.get_traffic_data(a_data['center']['lat'], a_data['center']['lon'])
            success = predictor.calculate_ad_success_score(area_name, a_data, weather, traffic)
            all_scores.append({
                'Area': area_name,
                'Success Score': success['success_score'],
                'Impressions/Hour': success['impressions_per_hour'],
                'Level': success['success_level']
            })

        df = pd.DataFrame(all_scores).sort_values('Success Score', ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.subheader("🏆 Top 3 Best Areas for Ads:")
        top_3 = df.head(3)
        for i, (_, row) in enumerate(top_3.iterrows(), 1):
            if row['Level'] == 'EXCELLENT':
                color_class = 'success-card'; emoji = '🥇'
            elif row['Level'] == 'GOOD':
                color_class = 'warning-card'; emoji = '🥈'
            else:
                color_class = 'danger-card'; emoji = '🥉'
            st.markdown(f"""
            <div class="{color_class}">
                <h3>{emoji} #{i} {row['Area']}</h3>
                <div class="metric-highlight">{row['Success Score']}/100</div>
                <p>{row['Impressions/Hour']:,} people see ads per hour</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📚 Understanding Your Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("""
        **🎯 Success Score (0-100):**
        - **90-100:** Exceptional location
        - **75-89:** Excellent location  
        - **55-74:** Good location
        - **35-54:** Moderate location
        - **0-34:** Poor location
        """)
    with col2:
        st.success("""
        **👥 Impressions/Hour:**
        - **3000+:** Very high visibility
        - **2000-2999:** High visibility
        - **1000-1999:** Good visibility
        - **500-999:** Moderate visibility
        - **<500:** Low visibility
        """)
    with col3:
        st.warning("""
        **⏰ Best Times to Advertise:**
        - **Morning:** 8:00-10:00 AM
        - **Lunch:** 12:00-2:00 PM
        - **Evening:** 5:00-7:00 PM
        - **Weekends:** Higher footfall
        """)

    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #636e72;'>
        <p><strong>🎯 Manchester Ad Success Predictor</strong> | 🏙️ Powered by Real-Time Data</p>
        <p>💡 Higher score = More successful ads | 📊 Based on traffic, audience, and <strong>live weather</strong></p>
        <p>🔄 Data updates every hour | ⚡ Instant predictions</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()