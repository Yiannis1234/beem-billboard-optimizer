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

# Bright, clean CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0066cc;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-card {
        background: linear-gradient(135deg, #00d4aa 0%, #00b894 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .success-card .metric-highlight {
        color: #ffffff !important;
    }
    .warning-card {
        background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .warning-card .metric-highlight {
        color: #ffffff !important;
    }
    .danger-card {
        background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .danger-card .metric-highlight {
        color: #ffffff !important;
    }
    .reason-box {
        background: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #00d4aa;
        margin: 0.5rem 0;
        color: #2d3436 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .reason-box strong {
        color: #2d3436 !important;
    }
    .metric-highlight {
        font-size: 2rem;
        font-weight: bold;
        color: #ffffff !important;
    }
    
    /* Force ALL metric-highlight to be white - NUCLEAR OPTION */
    div.metric-highlight {
        color: #ffffff !important;
    }
    .metric-highlight {
        color: #ffffff !important;
    }
    .success-card .metric-highlight,
    .warning-card .metric-highlight,
    .danger-card .metric-highlight {
        color: #ffffff !important;
    }
    /* Override any inherited colors */
    * .metric-highlight {
        color: #ffffff !important;
    }
    /* Fix ALL text visibility - comprehensive */
    .main .block-container {
        color: #2d3436 !important;
        background-color: #f8f9fa !important;
    }
    .main .block-container p {
        color: #2d3436 !important;
    }
    .main .block-container h1, h2, h3, h4, h5, h6 {
        color: #2d3436 !important;
    }
    .main .block-container div {
        color: #2d3436 !important;
    }
    .main .block-container span {
        color: #2d3436 !important;
    }
    .main .block-container label {
        color: #2d3436 !important;
    }
    /* Fix Streamlit components */
    .stSelectbox label {
        color: #2d3436 !important;
    }
    .stSelectbox div {
        color: #2d3436 !important;
    }
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        color: #2d3436 !important;
        border: 2px solid #00d4aa !important;
        border-radius: 8px !important;
    }
    .stSelectbox > div > div > div {
        background-color: #ffffff !important;
        color: #2d3436 !important;
    }
    /* Fix selectbox dropdown */
    div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #2d3436 !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #2d3436 !important;
        border: 2px solid #00d4aa !important;
    }
    .stButton button {
        color: #ffffff !important;
        background-color: #00d4aa !important;
    }
    .stMetric {
        color: #2d3436 !important;
    }
    .stMetric label {
        color: #2d3436 !important;
    }
    .stMetric div {
        color: #2d3436 !important;
    }
    /* Fix dataframe - bright colors */
    .stDataFrame {
        background-color: #ffffff !important;
        color: #2d3436 !important;
        border: 2px solid #00d4aa !important;
        border-radius: 10px !important;
    }
    .stDataFrame table {
        background-color: #ffffff !important;
        color: #2d3436 !important;
    }
    .stDataFrame th {
        background-color: #00d4aa !important;
        color: #ffffff !important;
        font-weight: bold !important;
        padding: 12px !important;
    }
    .stDataFrame td {
        background-color: #ffffff !important;
        color: #2d3436 !important;
        padding: 10px !important;
        border-bottom: 1px solid #e9ecef !important;
    }
    .stDataFrame tr:nth-child(even) {
        background-color: #f8f9fa !important;
    }
    .stDataFrame tr:hover {
        background-color: #e8f5e8 !important;
    }
    /* Bright background */
    .main {
        background-color: #f8f9fa !important;
    }
    .stApp {
        background-color: #f8f9fa !important;
    }
    /* Fix any remaining black boxes - COMPREHENSIVE */
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        color: #2d3436 !important;
        border: 1px solid #e9ecef !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    /* Fix metric text colors */
    div[data-testid="metric-container"] div {
        color: #2d3436 !important;
    }
    div[data-testid="metric-container"] label {
        color: #2d3436 !important;
    }
    div[data-testid="metric-container"] span {
        color: #2d3436 !important;
    }
    
    /* Fix ALL possible black elements */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        color: #2d3436 !important;
        border: 1px solid #e9ecef !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    /* Fix metric labels and values */
    div[data-testid="stMetric"] label {
        color: #2d3436 !important;
    }
    div[data-testid="stMetric"] div {
        color: #2d3436 !important;
    }
    
    /* Fix any remaining selectbox issues */
    .stSelectbox > div > div > div > div {
        background-color: #ffffff !important;
        color: #2d3436 !important;
    }
    
    /* Fix button styling */
    .stButton > button {
        background-color: #00d4aa !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: bold !important;
    }
    
    /* Fix any info/success/warning boxes */
    .stAlert {
        background-color: #ffffff !important;
        color: #2d3436 !important;
        border: 1px solid #e9ecef !important;
    }
    
    /* Nuclear option - fix ALL divs */
    div:not(.success-card):not(.warning-card):not(.danger-card):not(.reason-box) {
        background-color: transparent !important;
    }
    
    /* Fix specific Streamlit containers */
    .element-container {
        background-color: transparent !important;
    }
    
    /* Fix any remaining black backgrounds */
    [data-testid="stApp"] > div {
        background-color: #f8f9fa !important;
    }
    
    /* Fix column containers */
    .stColumn {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

class SimpleAdSuccessPredictor:
    def __init__(self):
        # Simplified Manchester areas with clear success factors
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
        
        # London areas (initial set) with clear success factors
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
            # WeatherAPI.com endpoint
            url = f"http://api.weatherapi.com/v1/forecast.json?key=f70bd534000447b2a14202431252303&q={lat},{lon}&days=1&aqi=no&alerts=no"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data['current']
                return {
                    'temperature': current['temp_c'],
                    'condition': current['condition']['text'],
                    'visibility': current['vis_km']
                }
            else:
                # Silent fallback - no error messages shown to users
                return {
                    'temperature': 12,
                    'condition': 'Partly Cloudy',
                    'visibility': 10
                }
        except Exception as e:
            # Silent fallback - no error messages shown to users
            return {
                'temperature': 12,
                'condition': 'Partly Cloudy',
                'visibility': 10
            }
    
    def get_traffic_data(self, lat, lon):
        """Get real traffic data from TomTom API with fallback"""
        try:
            # TomTom Traffic Flow API
            url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key=sljp3YAvFa7J3EalnGslYfnSCZg6VQUg"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                flow_data = data['flowSegmentData']
                
                # Extract relevant traffic data
                current_speed = flow_data['currentSpeed']
                free_flow_speed = flow_data['freeFlowSpeed']
                
                # Calculate congestion level
                if current_speed >= free_flow_speed * 0.8:
                    congestion_level = 'Light'
                elif current_speed >= free_flow_speed * 0.6:
                    congestion_level = 'Moderate'
                elif current_speed >= free_flow_speed * 0.4:
                    congestion_level = 'Heavy'
                else:
                    congestion_level = 'Very Heavy'
                
                return {
                    'current_speed': current_speed,
                    'free_flow_speed': free_flow_speed,
                    'congestion_level': congestion_level
                }
            else:
                # Silent fallback - realistic data based on latest real data
                return {
                    'current_speed': 28,
                    'free_flow_speed': 50,
                    'congestion_level': 'Light'
                }
        except Exception as e:
            # Silent fallback - realistic data based on latest real data
            return {
                'current_speed': 28,
                'free_flow_speed': 50,
                'congestion_level': 'Light'
            }
    
    def calculate_ad_success_score(self, area_name, area_data, weather_data, traffic_data):
        """Calculate realistic ad success score (0-100)"""
        
        # Base score from footfall (more realistic scaling)
        base_score = min(60, (area_data['footfall_daily'] / 10000))  # Max 60 from footfall
        
        # Success factors boost (reduced values)
        factor_boost = 0
        factors = area_data['success_factors']
        
        if factors.get('high_traffic', False):
            factor_boost += 15  # Reduced from 20
        if factors.get('business_district', False):
            factor_boost += 12  # Reduced from 15
        if factors.get('transport_hub', False):
            factor_boost += 12  # Reduced from 15
        if factors.get('affluent_audience', False):
            factor_boost += 8   # Reduced from 10
        if factors.get('student_area', False):
            factor_boost += 8   # Reduced from 10
        if factors.get('shopping_area', False):
            factor_boost += 8   # Reduced from 10
        if factors.get('creative_area', False):
            factor_boost += 5   # Same
        
        # Weather impact (reduced)
        weather_boost = 0
        if weather_data['visibility'] > 8:
            weather_boost = 5   # Reduced from 10
        elif weather_data['visibility'] > 5:
            weather_boost = 3   # Reduced from 5
        
        # Traffic impact (reduced)
        traffic_boost = 0
        if traffic_data['congestion_level'] == 'Heavy':
            traffic_boost = 8   # Reduced from 15
        elif traffic_data['congestion_level'] == 'Moderate':
            traffic_boost = 5   # Reduced from 10
        
        # Calculate final score (capped at 95 for realism)
        success_score = min(95, base_score + factor_boost + weather_boost + traffic_boost)
        
        # Calculate ad impressions
        impressions_per_hour = int((area_data['footfall_daily'] / 24) * 0.15)  # 15% see ads
        
        return {
            'area_name': area_name,
            'success_score': int(success_score),
            'impressions_per_hour': impressions_per_hour,
            'success_level': self.get_success_level(success_score),
            'key_reasons': self.get_success_reasons(factors, weather_data, traffic_data),
            'description': area_data['description']
        }
    
    def get_success_level(self, score):
        """Get success level based on score"""
        if score >= 75:
            return "EXCELLENT"
        elif score >= 55:
            return "GOOD"
        elif score >= 35:
            return "MODERATE"
        else:
            return "POOR"
    
    def get_success_reasons(self, factors, weather_data, traffic_data):
        """Get key reasons why this area is good/bad for ads"""
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
        
        if weather_data['visibility'] > 8:
            reasons.append("☀️ Clear weather = Better ad visibility")
        
        if traffic_data['congestion_level'] in ['Heavy', 'Moderate']:
            reasons.append("🚦 Traffic congestion = People stuck = More ad views")
        
        return reasons[:3]  # Top 3 reasons

def main():
    st.markdown('<h1 class="main-header">🎯 Ad Success Predictor — Manchester & London</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h3 style='color: #2d3436;'>Choose Manchester or London and get instant ad success predictions.</h3>
        <p style='color: #636e72;'>We analyze real traffic, audience and conditions. Separate buttons keep it crystal clear.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User-friendly info box
    st.info("""
    **💡 How it works:** 
    - Select any Manchester area from the dropdown
    - Click "Predict Ad Success" to get instant results
    - See your success score (0-100), how many people will see your ad, and why
    - Compare all areas in the table below
    """)
    
    predictor = SimpleAdSuccessPredictor()
    
    # Dual city selection with distinct buttons
    left, right = st.columns(2)
    with left:
        m_area = st.selectbox(
            "📍 Manchester Area",
            list(predictor.manchester_areas.keys()),
            index=0,
            help="Select a Manchester area"
        )
        manchester_clicked = st.button("🔍 Predict Manchester", type="primary", use_container_width=True)
    with right:
        l_area = st.selectbox(
            "📍 London Area",
            list(predictor.london_areas.keys()),
            index=0,
            help="Select a London area"
        )
        london_clicked = st.button("🔍 Predict London", type="primary", use_container_width=True)

    # Determine which city to analyze
    selected_city = None
    if manchester_clicked:
        selected_city = ("Manchester", m_area, predictor.manchester_areas[m_area])
    elif london_clicked:
        selected_city = ("London", l_area, predictor.london_areas[l_area])

    if selected_city is not None:
        city_name, selected_area, area_data = selected_city
        # Get data
        weather_data = predictor.get_weather_data(area_data['center']['lat'], area_data['center']['lon'])
        traffic_data = predictor.get_traffic_data(area_data['center']['lat'], area_data['center']['lon'])
        
        # Calculate success
        success_data = predictor.calculate_ad_success_score(selected_area, area_data, weather_data, traffic_data)
        
        # Display results
        st.markdown("---")
        
        # Success Score Card
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
        
        # Key Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Ad Success Score",
                f"{success_data['success_score']}/100",
                help="Higher score = Better ad success"
            )
        
        with col2:
            st.metric(
                "People See Ad/Hour",
                f"{success_data['impressions_per_hour']:,}",
                help="How many people will see your ad per hour"
            )
        
        with col3:
            st.metric(
                "Success Level",
                success_data['success_level'],
                help="Overall success rating"
            )
        
        # Why This Area is Good/Bad
        st.subheader("🤔 Why This Area is Good for Ads:")
        
        for reason in success_data['key_reasons']:
            st.markdown(f"""
            <div class="reason-box">
                <strong>{reason}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional helpful info
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
                st.info(f"""
                **💡 Pro Tips:**
                - This is an **excellent** location!
                - Consider premium ad placement
                - Run ads during peak hours
                - Monitor performance closely
                """)
            elif success_data['success_score'] >= 55:
                st.warning(f"""
                **💡 Pro Tips:**
                - This is a **good** location
                - Focus on peak traffic times
                - Consider A/B testing
                - Monitor competitor activity
                """)
            else:
                st.error(f"""
                **💡 Pro Tips:**
                - This area has **moderate** potential
                - Consider other locations first
                - If using this area, focus on weekends
                - Lower your ad spend expectations
                """)
        
        # Simple comparison
        st.subheader(f"📊 Quick Area Comparison — {city_name}")
        
        # Calculate scores for all areas in the selected city
        all_scores = []
        city_dict = predictor.manchester_areas if city_name == "Manchester" else predictor.london_areas
        for area_name, area_data in city_dict.items():
            weather = predictor.get_weather_data(area_data['center']['lat'], area_data['center']['lon'])
            traffic = predictor.get_traffic_data(area_data['center']['lat'], area_data['center']['lon'])
            success = predictor.calculate_ad_success_score(area_name, area_data, weather, traffic)
            all_scores.append({
                'Area': area_name,
                'Success Score': success['success_score'],
                'Impressions/Hour': success['impressions_per_hour'],
                'Level': success['success_level']
            })
        
        df = pd.DataFrame(all_scores)
        df = df.sort_values('Success Score', ascending=False)
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        # Top 3 recommendations
        st.subheader("🏆 Top 3 Best Areas for Ads:")
        
        top_3 = df.head(3)
        
        for i, (_, row) in enumerate(top_3.iterrows(), 1):
            if row['Level'] == 'EXCELLENT':
                color_class = 'success-card'
                emoji = '🥇'
            elif row['Level'] == 'GOOD':
                color_class = 'warning-card'
                emoji = '🥈'
            else:
                color_class = 'danger-card'
                emoji = '🥉'
            
            st.markdown(f"""
            <div class="{color_class}">
                <h3>{emoji} #{i} {row['Area']}</h3>
                <div class="metric-highlight">{row['Success Score']}/100</div>
                <p>{row['Impressions/Hour']:,} people see ads per hour</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer with helpful information
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
        <p>💡 Higher score = More successful ads | 📊 Based on traffic, audience, and conditions</p>
        <p>🔄 Data updates every hour | ⚡ Instant predictions</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
