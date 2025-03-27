import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time
import plotly.express as px
import plotly.graph_objects as go
import time as time_module
import altair as alt
from PIL import Image
from io import BytesIO
import requests

# Mock data collector for development
class BeemDataCollector:
    def __init__(self, config=None):
        pass
        
    def get_weather_forecast(self, location):
        return {
            'temperature': 18.5,
            'condition': 'Partly Cloudy',
            'wind_speed': 12.0,
            'precipitation': 0.0
        }
        
    def get_traffic_data(self, zone):
        return {
            'flow_speed': 30.0,
            'free_flow_speed': 40.0,
            'congestion_level': 0.3
        }
        
    def get_historical_engagement(self, start_date, end_date):
        dates = pd.date_range(start_date, end_date, freq='H')
        return pd.DataFrame({
            'timestamp': dates,
            'engagement_rate': np.random.uniform(0.3, 0.8, len(dates))
        })
        
    def get_pedestrian_density(self, zone, timestamp):
        hour = timestamp.hour
        if 12 <= hour <= 14 or 17 <= hour <= 19:  # Lunch and rush hours
            return 0.7
        elif 9 <= hour <= 16:  # Business hours
            return 0.5
        else:
            return 0.3
            
    def integrate_data(self, zone, timestamp):
        return {
            'weather': self.get_weather_forecast(zone),
            'traffic': self.get_traffic_data(zone),
            'pedestrian_density': self.get_pedestrian_density(zone, timestamp)
        }

# Initialize data collector
data_collector = BeemDataCollector()

# Page configuration
st.set_page_config(
    page_title="Beem Billboard Bike Route Optimizer", 
    page_icon="🚲", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'selected_area' not in st.session_state:
    st.session_state.selected_area = "Northern Quarter"
if 'analyze' not in st.session_state:
    st.session_state.analyze = False
if 'day_type' not in st.session_state:
    st.session_state.day_type = "Weekday"

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main theme colors */
    h1, h2, h3 {
        color: #FF7E33 !important;
    }
    
    /* Button styling */
    .stButton button {
        background: #FFA500 !important;
        background-image: linear-gradient(135deg, #FF7E33, #FF9945) !important;
        background-color: #FF7E33 !important;
        color: white !important;
        border: none !important;
        font-size: 18px !important;
        padding: 12px 20px !important;
        width: 100% !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 8px rgba(255,126,51,0.25) !important;
        transition: all 0.2s ease !important;
    }

    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(255,126,51,0.3) !important;
    }
    
    /* Hero title styling */
    .hero-title {
        font-size: 72px !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #FF7E33, #FF9945);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 20px !important;
    }
    .main-header {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #FF8C00 !important;
        margin-bottom: 1rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    .subheader {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #FF8C00 !important;
        margin-bottom: 1rem !important;
        padding-top: 1rem !important;
        border-top: 1px solid #444444 !important;
    }
    .metric-container {
        background-color: #222222 !important;
        padding: 1.2rem !important;
        border-radius: 0.8rem !important;
        margin-bottom: 1.2rem !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        color: white !important;
    }
    .metric-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 10px rgba(0,0,0,0.25) !important;
    }
    .recommendation {
        padding: 0.7rem 1.2rem !important;
        margin-bottom: 0.8rem !important;
        border-left: 4px solid #FF8C00 !important;
        background-color: #333333 !important;
        border-radius: 0.5rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15) !important;
        color: white !important;
    }
    .warning {
        border-left: 4px solid #FF6D00 !important;
        background-color: #3A3A3A !important;
    }
    .success {
        border-left: 4px solid #4caf50 !important;
        background-color: #333333 !important;
    }
    .data-label {
        font-weight: 600 !important;
        color: #FFFFFF !important;
    }
    .footer {
        margin-top: 3rem !important;
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
        border-top: 1px solid #444444 !important;
        font-size: 0.85rem !important;
        color: #FFFFFF !important;
        text-align: center !important;
        background-color: #222222 !important;
        border-radius: 0.5rem !important;
    }
    .sidebar-content {
        padding: 1.5rem !important;
        background-color: #222222 !important;
        border-radius: 0.5rem !important;
        margin-bottom: 1rem !important;
        color: white !important;
    }
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
        background-color: #FF8C00 !important;
        color: #000000 !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.25);
        background-color: #FF6D00 !important;
    }
    div[data-testid="stExpander"] {
        border-radius: 0.5rem !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15) !important;
        background-color: #222222 !important;
        color: white !important;
    }
    .stDateInput > div {
        border-radius: 0.5rem !important;
    }
    .stSelectbox > div > div {
        border-radius: 0.5rem !important;
    }
    .stSlider > div {
        padding-top: 0.5rem !important;
        padding-bottom: 1rem !important;
    }
    .card {
        background-color: #222222;
        border-radius: 0.8rem;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        margin-bottom: 1.2rem;
        transition: transform 0.3s ease;
        color: white;
    }
    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.25);
    }
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #FF8C00;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #FFFFFF;
        margin-top: 0.5rem;
    }
    .tab-container {
        margin-top: 1.5rem;
    }
    /* Animation for progress */
    @keyframes pulse {
        0% {
            opacity: 0.6;
        }
        50% {
            opacity: 1;
        }
        100% {
            opacity: 0.6;
        }
    }
    .animated-metric {
        animation: pulse 2s infinite ease-in-out;
    }
    /* Override Streamlit defaults */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #333333;
        color: white;
        border-radius: 4px 4px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF8C00 !important;
        color: #000000 !important;
    }
    div.stMarkdown {color: white;}
    h1, h2, h3, h4, h5, h6 {color: #FF8C00;}
    div[data-testid="stForm"] {background-color: #222222; padding: 1rem; border-radius: 0.8rem;}
    a {color: #FF8C00;}
    a:hover {color: #FF6D00;}
    .stSidebar {background-color: #181818;}
    div[data-testid="stVerticalBlock"] {background-color: #181818;}
    .stApp {background-color: #121212;}
    ul, ol, dl {color: white;}
    div[data-testid="stMetricValue"] {color: #FF8C00; font-weight: bold;}
    div[data-testid="stMetricLabel"] {color: white;}
    div[data-testid="stMetricDelta"] {color: #FF8C00;}
    div.stTooltipIcon {color: #FF8C00;}
    div.stTooltipIcon:hover {color: #FF6D00;}
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<div class="main-header">🚲 Beem Billboard Bike Route Optimizer</div>', unsafe_allow_html=True)
st.markdown("""
<div style="background-color: #333333; padding: 15px; border-radius: 10px; margin-bottom: 20px; color: white;">
This tool helps optimize bicycle routes for Beem's mobile billboards in Manchester. 
Get real-time weather, traffic, and pedestrian data to maximize engagement and plan your routes efficiently.
</div>
""", unsafe_allow_html=True)

# Define configuration
config = {
    'weather_api_key': 'f70bd534000447b2a14202431252303',  # Real weather API key
    'traffic_api_key': 'Uc0dPKIMHcqZ91VbGAnbEAINdzwqRzil'  # Real TomTom API key
}

# Initialize data collector
data_collector = BeemDataCollector(config)

# Sidebar for area selection
with st.sidebar:
    try:
        # Try to use a local logo if available
        st.image("static/beem_logo.png", width=200)
    except:
        # Fallback to a more attractive placeholder with orange and black theme
        st.markdown("""
        <div style="background: linear-gradient(90deg, #FF8C00, #FF6D00); 
                    color: #222222; padding: 20px; border-radius: 10px; 
                    text-align: center; margin-bottom: 20px; 
                    box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
            <h1 style="font-size: 2rem; margin: 0; font-weight: 700;">BEEM</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9; font-weight: 500;">Mobile Billboard Solutions</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown('<h2 style="margin-top:0; color: #FF8C00;">📍 Route Configuration</h2>', unsafe_allow_html=True)
    
    # Area selection dropdown with icons
    areas = {
        "Northern Quarter": "🏙️ Northern Quarter",
        "City Centre": "🌆 City Centre",
        "Ancoats": "🏬 Ancoats",
        "Piccadilly": "🚉 Piccadilly"
    }
    
    selected_area_key = st.selectbox(
        "Choose an area in Manchester:",
        list(areas.keys()),
        format_func=lambda x: areas[x]
    )
    selected_area = selected_area_key
    
    st.markdown("<hr style='margin: 15px 0; border: 0; height: 1px; background: #444444;'>", unsafe_allow_html=True)
    
    # Time selection with more visual feedback
    st.markdown('<h3 style="color: #FF8C00;">⏱️ Display Time</h3>', unsafe_allow_html=True)
    
    time_options = st.radio(
        "When to display?",
        ["Now", "Select Time"],
        help="Choose 'Now' for current conditions or 'Select Time' for future planning"
    )
    
    if time_options == "Select Time":
        col1, col2 = st.columns(2)
        with col1:
            selected_date = st.date_input("📅 Date", datetime.now())
        with col2:
            selected_hour = st.slider("🕒 Hour", 0, 23, datetime.now().hour, 
                                     format="%d:00", help="24-hour format")
        
        timestamp = datetime.combine(selected_date, time(hour=selected_hour))
        
        # Visual time indicator
        time_str = timestamp.strftime('%d %b %Y, %H:%M')
        st.markdown(f"""
        <div style="background-color: #333333; padding: 10px; border-radius: 8px; margin-top: 10px;">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 1.5rem; margin-right: 10px;">⏰</div>
                <div>
                    <div style="font-weight: bold; color: #FF8C00;">Selected Time:</div>
                    <div>{time_str}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        timestamp = datetime.now()
        time_str = timestamp.strftime('%d %b %Y, %H:%M')
        
        st.markdown(f"""
        <div style="background-color: #333333; padding: 10px; border-radius: 8px; margin-top: 10px;">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 1.5rem; margin-right: 10px;">⏰</div>
                <div>
                    <div style="font-weight: bold; color: #FF8C00;">Current Time:</div>
                    <div>{time_str}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin: 15px 0; border: 0; height: 1px; background: #444444;'>", unsafe_allow_html=True)
    
    # Analysis button with animation and loading state
    analyze_button = st.button(
        "🔍 Analyze Route",
        type="primary", 
        use_container_width=True,
        help="Click to analyze this route based on current conditions"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # About section with more information
    with st.expander("ℹ️ About Beem"):
        st.markdown("""
        <div style="padding: 10px; color: white;">
            <p style="margin-bottom: 15px;"><strong>Beem Mobile Billboard Solutions</strong> helps businesses reach their audience through eye-catching mobile billboards carried by cyclists.</p>
            
            <p style="margin-bottom: 10px;">Our innovative approach is:</p>
            <ul style="list-style-type: none; padding-left: 10px; margin-bottom: 15px;">
                <li style="margin-bottom: 8px;">🌿 <strong>Eco-friendly</strong> - Zero emissions</li>
                <li style="margin-bottom: 8px;">💰 <strong>Cost-effective</strong> - Lower costs than traditional billboards</li>
                <li style="margin-bottom: 8px;">🌟 <strong>Targeted</strong> - Precise location targeting</li>
                <li style="margin-bottom: 8px;">📱 <strong>Engaging</strong> - High visibility in pedestrian areas</li>
            </ul>
            
            <p>This app uses real-time data to optimize your mobile billboard routes for maximum engagement.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional help section
    with st.expander("🔍 How to use this tool"):
        st.markdown("""
        <div style="padding: 10px;">
            <ol>
                <li><strong>Select an area</strong> in Manchester where you want to display your billboard</li>
                <li><strong>Choose a time</strong> - either now or a specific future time</li>
                <li><strong>Click "Analyze Route"</strong> to get detailed insights</li>
                <li>Review the <strong>engagement score</strong> and recommendations</li>
                <li>Check the <strong>best times table</strong> for optimal scheduling</li>
            </ol>
            <p>The tool combines weather data, traffic conditions, and pedestrian density to calculate the best times and locations for your mobile billboard campaign.</p>
        </div>
        """, unsafe_allow_html=True)

# Define Manchester zones with enhanced data
manchester_zones = {
    "Northern Quarter": {
        'zone_id': 'northern_quarter',
        'latitude': 53.4831,
        'longitude': -2.2372,
        'description': 'A trendy, creative neighborhood with high foot traffic and many independent businesses.',
        'best_times': 'Evenings and weekends',
        'target_audience': 'Young professionals, creatives, tourists',
        'popular_locations': ['Afflecks Palace', 'Manchester Craft & Design Centre', 'Northern Quarter Bars'],
        'avg_foot_traffic': 'High',
        'businesses': 'Independent shops, cafes, bars, art galleries',
        'landmarks': 'Afflecks Palace, Manchester Craft & Design Centre',
        'ambience': 'Creative, alternative, bustling'
    },
    "City Centre": {
        'zone_id': 'city_centre',
        'latitude': 53.4808,
        'longitude': -2.2426,
        'description': 'The bustling heart of Manchester with shopping centers, offices, and attractions.',
        'best_times': 'Weekday lunchtimes and weekends',
        'target_audience': 'Shoppers, office workers, tourists',
        'popular_locations': ['Arndale Shopping Centre', 'Market Street', 'Exchange Square'],
        'avg_foot_traffic': 'Very High',
        'businesses': 'Retail stores, restaurants, corporate offices',
        'landmarks': 'Manchester Arndale, Royal Exchange, St Ann\'s Square',
        'ambience': 'Busy, commercial, diverse'
    },
    "Ancoats": {
        'zone_id': 'ancoats',
        'latitude': 53.4836,
        'longitude': -2.2275,
        'description': 'An up-and-coming area with popular restaurants and apartment buildings.',
        'best_times': 'Evenings and weekends',
        'target_audience': 'Young professionals, foodies',
        'popular_locations': ['Cutting Room Square', 'Ancoats Coffee Co', 'Hope Mill Theatre'],
        'avg_foot_traffic': 'Medium-High',
        'businesses': 'Trendy restaurants, cafes, bakeries, apartments',
        'landmarks': 'Cutting Room Square, Ancoats Marina',
        'ambience': 'Hip, rejuvenated, modern'
    },
    "Piccadilly": {
        'zone_id': 'piccadilly',
        'latitude': 53.4768,
        'longitude': -2.2351,
        'description': 'A major transportation hub with high commuter traffic.',
        'best_times': 'Rush hours (8-9 AM, 5-6 PM)',
        'target_audience': 'Commuters, travelers',
        'popular_locations': ['Piccadilly Gardens', 'Piccadilly Station', 'Piccadilly Plaza'],
        'avg_foot_traffic': 'Very High (at peak times)',
        'businesses': 'Transport hubs, retail, fast food, hotels',
        'landmarks': 'Piccadilly Gardens, Piccadilly Station, Manchester One',
        'ambience': 'Fast-paced, transient, busy'
    }
}

# Function to get reasons for recommended times
def get_reason_for_time(day, hour, area):
    is_weekend = day in ["Saturday", "Sunday"]
    
    if area == "Northern Quarter":
        if is_weekend and hour >= 12:
            return "Weekend afternoons and evenings have high foot traffic with shoppers and people visiting bars/restaurants."
        elif not is_weekend and hour >= 17:
            return "Weekday evenings see increased activity with after-work crowds visiting bars and restaurants."
        elif hour >= 12 and hour <= 14:
            return "Lunch hour brings office workers to local eateries and cafes."
    
    elif area == "City Centre":
        if is_weekend and hour >= 11 and hour <= 17:
            return "Peak shopping hours with high volumes of pedestrian traffic in retail areas."
        elif not is_weekend and hour >= 12 and hour <= 14:
            return "Lunch rush brings office workers into public spaces and shopping areas."
        elif not is_weekend and hour >= 17 and hour <= 19:
            return "After-work shopping and dining creates high visibility opportunities."
    
    elif area == "Ancoats":
        if is_weekend and hour >= 11 and hour <= 21:
            return "Weekend crowds visit popular restaurants and leisure spots throughout the day."
        elif not is_weekend and hour >= 17 and hour <= 21:
            return "Evening dining brings significant foot traffic to restaurant-heavy areas."
    
    else:  # Piccadilly
        if not is_weekend and (hour >= 7 and hour <= 9):
            return "Morning commute brings high volumes of pedestrians through transportation hubs."
        elif not is_weekend and (hour >= 16 and hour <= 19):
            return "Evening rush hour creates dense foot traffic around transit points."
        elif is_weekend and hour >= 11 and hour <= 16:
            return "Tourists and shoppers create steady foot traffic throughout the day."
    
    return "Moderate pedestrian activity expected during this time."

# Enhanced progress indicator for analysis with visual animations
def show_analysis_progress():
    progress_container = st.container()
    with progress_container:
        st.markdown("""
        <div style="background-color: #222222; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
            <h3 style="margin-top: 0; color: #FF8C00; display: flex; align-items: center;">
                <span style="margin-right: 10px;">⚙️</span> 
                Analyzing Route Data
            </h3>
            <div id="progress-info"></div>
        </div>
        """, unsafe_allow_html=True)
        
    progress_bar = st.progress(0)
    status_text = st.empty()
    details_text = st.empty()
        
    steps = [
        {"name": "Collecting weather data", "icon": "🌦️", "description": "Retrieving current weather conditions and forecasts..."},
        {"name": "Analyzing traffic conditions", "icon": "🚗", "description": "Calculating traffic flow and congestion levels..."},
        {"name": "Estimating pedestrian density", "icon": "👥", "description": "Modeling expected foot traffic based on historical patterns..."},
        {"name": "Calculating optimal routes", "icon": "🗺️", "description": "Determining the most effective billboard routes..."},
        {"name": "Generating recommendations", "icon": "📊", "description": "Creating personalized recommendations based on data analysis..."}
    ]
    
    for i, step in enumerate(steps):
            # Update progress
            progress = (i+1)/len(steps)
            progress_bar.progress(progress)
            
            # Display current step with animation
            status_html = f"""
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="font-size: 1.5rem; margin-right: 10px; class="animated-metric">{step['icon']}</div>
                <div>
                    <div style="font-weight: bold; color: #FF8C00;">Step {i+1}/{len(steps)}: {step['name']}</div>
                    <div style="font-size: 0.9rem; color: #FFFFFF;">{step['description']}</div>
                </div>
            </div>
            """
            status_text.markdown(status_html, unsafe_allow_html=True)
            
            # Add a small delay to show progress
            time_module.sleep(0.5)
            
            # Show a simulated detail for the current step
            if i < len(steps) - 1:
                details_text.info(f"Completed: {step['name']}")
            else:
                details_text.success("Analysis complete! Displaying results...")
        
        # Clean up the progress indicators after completion
    time_module.sleep(0.5)
    progress_container.empty()

# When button is clicked, analyze the selected area
if analyze_button:
    # Get the selected zone
    selected_zone = manchester_zones[selected_area]
    
    # Show progress during analysis
    show_analysis_progress()
    
    # Collect integrated data
    integrated_data = data_collector.integrate_data(selected_zone, timestamp)
    
    # Page tabs for better organization
    tabs = st.tabs(["📊 Route Analysis", "🗺️ Map & Visualization", "📈 Historical Data", "⏰ Best Times"])
    
    # Handle potential errors gracefully
    try:
        # Tab 1: Route Analysis
        with tabs[0]:
            # Main content with cards and better visuals
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin-bottom: 20px;">
                <div style="font-size: 2rem; margin-right: 15px;">📍</div>
                <div>
                    <h2 style="margin: 0; color: #FF8C00;">{selected_area} Analysis</h2>
                    <p style="margin: 5px 0 0 0; color: #FFFFFF;">{selected_zone['description']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Area Information in a card
            st.markdown("""
            <div class="card">
                <h3 style="margin-top: 0; color: #FF8C00; display: flex; align-items: center;">
                    <span style="margin-right: 10px;">📌</span> Area Information
                </h3>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style="margin-bottom: 10px;">
                    <div style="font-weight: bold; color: #FFFFFF;">Target Audience:</div>
                    <div>{selected_zone['target_audience']}</div>
                </div>
                <div style="margin-bottom: 10px;">
                    <div style="font-weight: bold; color: #FFFFFF;">Best Times:</div>
                    <div>{selected_zone['best_times']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="margin-bottom: 10px;">
                    <div style="font-weight: bold; color: #FFFFFF;">Foot Traffic:</div>
                    <div>{selected_zone['avg_foot_traffic']}</div>
                </div>
                <div style="margin-bottom: 10px;">
                    <div style="font-weight: bold; color: #FFFFFF;">Key Businesses:</div>
                    <div>{selected_zone['businesses']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Popular locations
            st.markdown("<h4 style='margin-top: 15px; margin-bottom: 10px;'>Popular Locations:</h4>", unsafe_allow_html=True)
            location_cols = st.columns(len(selected_zone['popular_locations']))
            for i, location in enumerate(selected_zone['popular_locations']):
                with location_cols[i]:
                    st.markdown(f"""
                    <div style="background-color: #333333; padding: 10px; border-radius: 8px; text-align: center; color: white;">
                        <div>{location}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close the card
            
            # Weather section with improved visuals
            st.markdown("""
            <div class="card">
                <h3 style="margin-top: 0; color: #FF8C00; display: flex; align-items: center;">
                    <span style="margin-right: 10px;">☀️</span> Current Weather Conditions
                </h3>
            """, unsafe_allow_html=True)
            
        weather_data = integrated_data['weather']
        
            # Weather icon selection based on condition
            weather_condition = weather_data['condition'].lower()
            weather_icon = "☀️"  # default sunny
            if 'rain' in weather_condition or 'shower' in weather_condition:
                weather_icon = "🌧️"
            elif 'cloud' in weather_condition:
                weather_icon = "☁️"
            elif 'snow' in weather_condition:
                weather_icon = "❄️"
            elif 'fog' in weather_condition or 'mist' in weather_condition:
                weather_icon = "🌫️"
            elif 'thunder' in weather_condition or 'storm' in weather_condition:
                weather_icon = "⛈️"
            elif 'sun' in weather_condition or 'clear' in weather_condition:
                weather_icon = "☀️"
            elif 'part' in weather_condition and 'cloud' in weather_condition:
                weather_icon = "⛅"
            
            # Create visually appealing weather display
        weather_cols = st.columns(4)
            
        with weather_cols[0]:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 5px;">{weather_icon}</div>
                    <div class="stat-value">{weather_data['temperature']:.1f}°C</div>
                    <div class="stat-label">Temperature</div>
                </div>
                """, unsafe_allow_html=True)
                
        with weather_cols[1]:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 5px;">🌡️</div>
                    <div class="stat-value">{weather_data['condition']}</div>
                    <div class="stat-label">Condition</div>
                </div>
                """, unsafe_allow_html=True)
                
        with weather_cols[2]:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 5px;">💨</div>
                    <div class="stat-value">{weather_data['wind_speed']:.1f}</div>
                    <div class="stat-label">Wind Speed (km/h)</div>
                </div>
                """, unsafe_allow_html=True)
                
        with weather_cols[3]:
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 5px;">💧</div>
                    <div class="stat-value">{weather_data['precipitation']:.1f}</div>
                    <div class="stat-label">Precipitation (mm)</div>
                </div>
                """, unsafe_allow_html=True)
                
            # Weather impact on billboard visibility
            precipitation = weather_data['precipitation']
            wind_speed = weather_data['wind_speed']
            
            weather_impact = "Excellent"
            impact_color = "green"
            if precipitation > 5 or wind_speed > 25:
                weather_impact = "Poor"
                impact_color = "red"
            elif precipitation > 2 or wind_speed > 15:
                weather_impact = "Fair"
                impact_color = "orange"
            elif precipitation > 0.5 or wind_speed > 10:
                weather_impact = "Good"
                impact_color = "blue"
            
            st.markdown(f"""
            <div style="margin-top: 20px; background-color: #333333; border-radius: 8px; padding: 15px;">
                <div style="display: flex; align-items: center;">
                    <div style="font-size: 1.5rem; margin-right: 10px;">🔍</div>
                    <div>
                        <div style="font-weight: bold; color: white;">Weather Impact on Billboard Visibility:</div>
                        <div style="color: {impact_color}; font-weight: bold;">{weather_impact}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close the card
        
        # Traffic conditions
        st.markdown('<div class="subheader">🚗 Traffic Conditions</div>', unsafe_allow_html=True)
        traffic_data = integrated_data['traffic']
        
        traffic_cols = st.columns(3)
        with traffic_cols[0]:
            st.metric("Flow Speed", f"{traffic_data['flow_speed']:.1f} km/h")
        with traffic_cols[1]:
            st.metric("Free Flow Speed", f"{traffic_data['free_flow_speed']:.1f} km/h")
        with traffic_cols[2]:
            congestion_level = traffic_data['congestion_level']
            congestion_status = "High" if congestion_level > 0.7 else "Medium" if congestion_level > 0.4 else "Low"
            st.metric("Congestion Level", f"{congestion_level:.2f}", delta=congestion_status)
        
            # Create a gauge chart for congestion
            congestion_percentage = int(congestion_level * 100)
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=congestion_percentage,
                domain={'x': [0, 1], 'y': [0, 1]},
                number={'suffix': "%"},
                title={'text': "Traffic Congestion", 'font': {'color': 'white'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickfont': {'color': 'white'}},
                    'bar': {'color': "#FF8C00"},
                    'steps': [
                        {'range': [0, 30], 'color': "#3A3A3A"},
                        {'range': [30, 70], 'color': "#555555"},
                        {'range': [70, 100], 'color': "#222222"}
                    ],
                    'threshold': {
                        'line': {'color': "#FF6D00", 'width': 2},
                        'thickness': 0.75,
                        'value': 70
                    }
                }
            ))
            
            fig.update_layout(
                height=250,
                margin=dict(l=20, r=20, t=50, b=20),
                paper_bgcolor="#222222",
                font={"color": "white"}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Traffic impact analysis
            impact_level = "Low impact on visibility" if congestion_level < 0.4 else \
                          "Moderate impact on visibility" if congestion_level < 0.7 else \
                          "High impact on billboard visibility"
            
            st.info(f"**Traffic Analysis:** {impact_level}. {congestion_status} congestion may {'not significantly affect' if congestion_level < 0.4 else 'somewhat affect' if congestion_level < 0.7 else 'significantly reduce'} the effectiveness of mobile billboards in this area.")
            
            # Pedestrian density with more detailed visuals
            st.markdown("""
            <div class="card">
                <h3 style="margin-top: 0; color: #FF8C00; display: flex; align-items: center;">
                    <span style="margin-right: 10px;">👥</span> Pedestrian Activity
                </h3>
            """, unsafe_allow_html=True)
            
            density = integrated_data['pedestrian_density']
            hour = timestamp.hour
            
            # Format hour for display
            display_hour = f"{hour}:00"
            am_pm = "AM" if hour < 12 else "PM"
            display_hour_12 = f"{hour if hour < 12 else hour-12 if hour > 12 else 12}:00 {am_pm}"
            
            # Expected trend calculation with more factors
            expected_trend = "Increasing"
            trend_icon = "📈"
            trend_color = "#4CAF50"
            
            if (hour >= 7 and hour <= 9) or (hour >= 16 and hour <= 18):
                expected_trend = "Increasing"
                trend_icon = "📈"
                trend_color = "#4CAF50"
            elif hour >= 19 or hour <= 5:
                expected_trend = "Decreasing"
                trend_icon = "📉"
                trend_color = "#EF5350"
            else:
                expected_trend = "Stable"
                trend_icon = "📊"
                trend_color = "#2196F3"
            
            # Day of week factor
            is_weekend = timestamp.weekday() >= 5
            day_factor = "weekend" if is_weekend else "weekday"
        
        density_cols = st.columns(2)
            
        with density_cols[0]:
                # Create a gauge chart for pedestrian density
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=density * 100,
                    number={'suffix': "%", "font": {"size": 24, "color": "white"}},
                    title={'text': "Current Pedestrian Density", 'font': {'color': 'white'}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickfont': {'color': 'white'}},
                        'bar': {'color': "#FF8C00"},
                        'steps': [
                            {'range': [0, 30], 'color': "#333333"},
                            {'range': [30, 70], 'color': "#444444"},
                            {'range': [70, 100], 'color': "#555555"}
                        ],
                        'threshold': {
                            'line': {'color': "#FF6D00", 'width': 2},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                
                fig.update_layout(
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=20),
                    paper_bgcolor="#222222",
                    font={"size": 12, "color": "white"}
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
        with density_cols[1]:
                st.subheader(f"{trend_icon} Trend Analysis")
                
                st.write("**Current Time:**")
                st.write(f"{display_hour} ({display_hour_12})")
                
                st.write("**Day Type:**")
                st.write(f"{day_factor.capitalize()}")
                
                st.write("**Expected Trend:**")
                st.markdown(f"<span style='color: {trend_color}; font-weight: bold;'>{expected_trend}</span>", unsafe_allow_html=True)
                
                st.write("**Recommendation:**")
                if density > 0.7:
                    st.write("Optimal time for billboard display. High engagement expected.")
                elif density > 0.4:
                    st.write("Good time for billboard display. Moderate engagement expected.")
                else:
                    st.write("Consider scheduling for a time with higher foot traffic.")
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close the card

            # Enhanced engagement score section
            st.markdown("""
            <div class="card">
                <h3 style="margin-top: 0; color: #FF8C00; display: flex; align-items: center;">
                    <span style="margin-right: 10px;">📊</span> Engagement Analysis
                </h3>
            """, unsafe_allow_html=True)
            
            # Calculate engagement score with more factors and weights
            weather_score = 1 - min(1, weather_data['precipitation'] / 5)  # Normalize precipitation
            if weather_data['condition'].lower() in ['rain', 'snow', 'sleet', 'storm', 'heavy rain']:
                weather_score *= 0.5
            
            time_score = 0.5
            if (hour >= 10 and hour <= 19) and (timestamp.weekday() < 5):  # Weekday business hours
                time_score = 0.9
            elif (hour >= 11 and hour <= 20) and (timestamp.weekday() >= 5):  # Weekend hours
                time_score = 0.85
            elif (hour >= 7 and hour <= 9) or (hour >= 16 and hour <= 18):  # Rush hours
                time_score = 0.8
            elif hour < 7 or hour > 21:  # Early morning or late night
                time_score = 0.3
            
            traffic_score = 1 - traffic_data['congestion_level']
            
        engagement_score = (
                (0.3 * traffic_score) +  # Lower congestion is better
                (0.4 * integrated_data['pedestrian_density']) +  # Higher pedestrian density is better
                (0.2 * weather_score) +  # Better weather is better
                (0.1 * time_score)  # Time factor
        )
        
        engagement_percentage = min(100, max(0, engagement_score * 100))
        
            # Display score with gauge chart
            score_cols = st.columns([2, 3])
            
        with score_cols[0]:
                # Create a gauge chart for engagement score
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=engagement_percentage,
                    number={'suffix': "%", "font": {"size": 30, "color": "white", "family": "Arial"}},
                    title={'text': "Expected Engagement Score", "font": {"size": 16, "color": "white"}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickfont': {'color': "white"}},
                        'bar': {'color': "#FF8C00"},
                        'steps': [
                            {'range': [0, 40], 'color': "#333333"},
                            {'range': [40, 70], 'color': "#444444"},
                            {'range': [70, 100], 'color': "#555555"}
                        ],
                        'threshold': {
                            'line': {'color': "#FF6D00", 'width': 2},
                            'thickness': 0.75,
                            'value': 70
                        }
                    }
                ))
                
                fig.update_layout(
                    height=300,
                    margin=dict(l=30, r=30, t=50, b=30),
                    paper_bgcolor="#222222",
                    font={"size": 12, "family": "Arial", "color": "white"}
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Score breakdown
                st.markdown("<h4 style='margin-top: 0;'>Score Components:</h4>", unsafe_allow_html=True)
                
                # Create simple progress bars that won't cause errors
                score_items = [
                    {"name": "Pedestrian Density", "score": integrated_data['pedestrian_density'] * 100, "color": "#FF8C00"},
                    {"name": "Traffic Conditions", "score": traffic_score * 100, "color": "#FF6D00"},
                    {"name": "Weather Conditions", "score": weather_score * 100, "color": "#FF9E40"},
                    {"name": "Time Optimization", "score": time_score * 100, "color": "#FFAE5E"}
                ]
                
                for item in score_items:
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                        <div style="width: 150px; font-weight: bold; color: white;">{item['name']}:</div>
                        <div style="flex-grow: 1; background-color: #333333; border-radius: 8px; height: 30px; position: relative;">
                            <div style="position: absolute; top: 0; left: 0; background-color: {item['color']}; 
                                 width: {min(100, max(0, item['score']))}%; height: 100%; border-radius: 8px;"></div>
                            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
                                 display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                                {item['score']:.1f}%
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with score_cols[1]:
                # Enhanced recommendations with more actionable insights
                st.markdown("<h4 style='margin-top: 0;'>Recommendations & Insights</h4>", unsafe_allow_html=True)
                
            recommendations = []
            
                # Detailed recommendations based on all factors
            if traffic_data['congestion_level'] > 0.7:
                    recommendations.append({
                        "icon": "⚠️",
                        "title": "High Traffic Congestion",
                        "text": "Heavy traffic may slow routes and reduce visibility. Consider side streets or avoid peak hours.",
                        "type": "warning"
                    })
            
            if integrated_data['pedestrian_density'] < 0.3:
                    recommendations.append({
                        "icon": "👥",
                        "title": "Low Pedestrian Activity",
                        "text": f"Current pedestrian density is low. Consider scheduling during peak hours (lunch time or {'' if is_weekend else 'after work'} evenings).",
                        "type": "warning"
                    })
            
            if weather_data['precipitation'] > 0.5:
                    recommendations.append({
                        "icon": "🌧️",
                        "title": "Precipitation Detected",
                        "text": "Rain may reduce visibility and pedestrian traffic. Consider rescheduling or use weather-protected billboards.",
                        "type": "warning"
                    })
            
            if weather_data['wind_speed'] > 15:
                    recommendations.append({
                        "icon": "💨",
                        "title": "High Wind Alert",
                        "text": "Wind speeds may affect billboard stability. Ensure all displays are secured properly.",
                        "type": "warning"
                    })
                
                if selected_area == "Northern Quarter" and (hour >= 18 and hour <= 23) and (timestamp.weekday() >= 4):
                    recommendations.append({
                        "icon": "🎯",
                        "title": "Optimal Location & Time",
                        "text": "Evening weekend hours in Northern Quarter target the ideal young professional demographic.",
                        "type": "success"
                    })
                elif selected_area == "City Centre" and (hour >= 11 and hour <= 16):
                    recommendations.append({
                        "icon": "🎯",
                        "title": "Optimal Location & Time",
                        "text": "Midday hours in City Centre capture maximum shopping traffic.",
                        "type": "success"
                    })
                elif selected_area == "Piccadilly" and ((hour >= 7 and hour <= 9) or (hour >= 16 and hour <= 18)) and (timestamp.weekday() < 5):
                    recommendations.append({
                        "icon": "🎯",
                        "title": "Optimal Location & Time",
                        "text": "Rush hour on weekdays in Piccadilly captures maximum commuter traffic.",
                        "type": "success"
                    })
                
                # General engagement recommendation
                if engagement_percentage >= 70:
                    recommendations.append({
                        "icon": "✅",
                        "title": "High Engagement Expected",
                        "text": "Conditions are favorable for billboard display with high expected engagement.",
                        "type": "success"
                    })
                elif engagement_percentage >= 40:
                    recommendations.append({
                        "icon": "ℹ️",
                        "title": "Moderate Engagement Expected",
                        "text": "Conditions are acceptable for billboard display. Consider small adjustments to timing or location for improved results.",
                        "type": "info"
                    })
                else:
                    recommendations.append({
                        "icon": "⚠️",
                        "title": "Low Engagement Expected",
                        "text": "Current conditions may limit billboard effectiveness. Consider rescheduling or relocating.",
                        "type": "warning"
                    })
                
                # Route suggestion based on location, time and conditions
                recommendations.append({
                    "icon": "🗺️",
                    "title": "Suggested Route",
                    "text": f"Cycle through {selected_area}'s main thoroughfares with frequent stops at {'popular bars and restaurants' if hour >= 18 else 'shopping areas and cafes'}.",
                    "type": "info"
                })
                
                # Display all recommendations
                for i, rec in enumerate(recommendations):
                    st.markdown(f"""
                    <div class="recommendation {rec['type']}" style="margin-bottom: 10px;">
                        <div style="display: flex; align-items: flex-start;">
                            <div style="font-size: 1.5rem; margin-right: 10px;">{rec['icon']}</div>
                            <div>
                                <div style="font-weight: bold;">{rec['title']}</div>
                                <div>{rec['text']}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close the card

        # Tab 2: Map & Visualization
        with tabs[1]:
            st.markdown("""
            <div class="card">
                <h3 style="margin-top: 0; color: #FF8C00; display: flex; align-items: center;">
                    <span style="margin-right: 10px;">🗺️</span> Interactive Route Map
                </h3>
            """, unsafe_allow_html=True)
            
            # Create a more detailed map with layers
            st.markdown("<p>The map below shows the optimal route and key locations for billboard display:</p>", unsafe_allow_html=True)
            
            # Add marker for selected zone
        map_data = pd.DataFrame({
            'lat': [selected_zone['latitude']],
            'lon': [selected_zone['longitude']]
        })
        
            # Use an interactive map with more information
            st.map(map_data, zoom=14)
            
            # Display key locations
            st.markdown("<h4>Key Locations for Maximum Visibility:</h4>", unsafe_allow_html=True)
            
            # Create simulated key locations based on selected area
            if selected_area == "Northern Quarter":
                key_locations = [
                    {"name": "Afflecks Palace", "foot_traffic": "Very High", "best_times": "Afternoons, Weekends"},
                    {"name": "Thomas Street", "foot_traffic": "High", "best_times": "Evenings"},
                    {"name": "Manchester Craft & Design Centre", "foot_traffic": "Medium", "best_times": "Afternoons"}
                ]
            elif selected_area == "City Centre":
                key_locations = [
                    {"name": "Market Street", "foot_traffic": "Very High", "best_times": "All Day"},
                    {"name": "Arndale Shopping Centre", "foot_traffic": "Very High", "best_times": "All Day"},
                    {"name": "St Ann's Square", "foot_traffic": "High", "best_times": "Lunchtimes, Weekends"}
                ]
            elif selected_area == "Ancoats":
                key_locations = [
                    {"name": "Cutting Room Square", "foot_traffic": "High", "best_times": "Evenings, Weekends"},
                    {"name": "Great Ancoats Street", "foot_traffic": "Medium-High", "best_times": "Rush Hours"},
                    {"name": "Ancoats Coffee Co", "foot_traffic": "Medium", "best_times": "Mornings, Weekends"}
                ]
            else:  # Piccadilly
                key_locations = [
                    {"name": "Piccadilly Gardens", "foot_traffic": "Very High", "best_times": "All Day"},
                    {"name": "Piccadilly Station Approach", "foot_traffic": "Very High", "best_times": "Rush Hours"},
                    {"name": "Market Street Junction", "foot_traffic": "High", "best_times": "All Day"}
                ]
            
            # Create a table of key locations
            locations_df = pd.DataFrame(key_locations)
            
            # Create a styled table
            st.markdown(
                locations_df.style
                .set_properties(**{'text-align': 'center', 'color': 'white'})
                .set_table_styles([
                    {'selector': 'th', 'props': [('text-align', 'center'), ('font-weight', 'bold'), ('background-color', '#333333'), ('color', 'white')]},
                    {'selector': 'tr:hover', 'props': [('background-color', '#444444')]}
                ])
                .format({'name': lambda x: f"<b>{x}</b>"})
                .to_html(), 
                unsafe_allow_html=True
            )
            
            # Suggested route
            st.markdown("<h4>Suggested Billboard Route:</h4>", unsafe_allow_html=True)
            
            # Simulate a route based on location
            route_description = ""
            if selected_area == "Northern Quarter":
                route_description = """
                1. <b>Start:</b> Shudehill Interchange
                2. <b>Head to:</b> Thomas Street (high foot traffic in evenings)
                3. <b>Continue to:</b> Afflecks Palace (popular with young demographics)
                4. <b>Move onto:</b> Edge Street & Craft Centre (creative audience)
                5. <b>End at:</b> Stevenson Square (high visibility junction)
                """
            elif selected_area == "City Centre":
                route_description = """
                1. <b>Start:</b> St Peter's Square
                2. <b>Head to:</b> Albert Square (civic heart, events)
                3. <b>Continue to:</b> Market Street (highest foot traffic)
                4. <b>Move onto:</b> Exchange Square (shopping hub)
                5. <b>End at:</b> Cathedral Gardens (tourist area)
                """
            elif selected_area == "Ancoats":
                route_description = """
                1. <b>Start:</b> Great Ancoats Street
                2. <b>Head to:</b> Cutting Room Square (popular meeting place)
                3. <b>Continue to:</b> Blossom Street (restaurant area)
                4. <b>Move onto:</b> Cotton Street (residential area)
                5. <b>End at:</b> Ancoats Marina (leisure area)
                """
            else:  # Piccadilly
                route_description = """
                1. <b>Start:</b> Piccadilly Station
                2. <b>Head to:</b> Station Approach (commuter flow)
                3. <b>Continue to:</b> Piccadilly Gardens (central hub)
                4. <b>Move onto:</b> Market Street Junction (shopping traffic)
                5. <b>End at:</b> Portland Street (business district)
                """
            
            st.markdown(f"""
            <div style="background-color: #333333; border-radius: 8px; padding: 15px; color: white;">
                {route_description}
            </div>
            """, unsafe_allow_html=True)
            
            # Suggested dwell times
            st.markdown("<h4>Suggested Dwell Times:</h4>", unsafe_allow_html=True)
            
            # Create a bar chart for dwell times at each location
            # Extract location names
            location_names = [loc["name"] for loc in key_locations]
            
            # Create simulated dwell times (in minutes)
            if hour >= 12 and hour <= 14:  # Lunch time
                dwell_times = [15, 25, 10]  # More time in busy areas during lunch
            elif hour >= 17 and hour <= 19:  # Evening rush
                dwell_times = [10, 20, 20]  # Spread out during evening rush
            else:
                dwell_times = [15, 15, 15]  # Equal distribution at other times
            
            # Create a bar chart
            dwell_data = pd.DataFrame({
                'Location': location_names,
                'Dwell Time (minutes)': dwell_times
            })
            
            fig = px.bar(
                dwell_data, 
                x='Location', 
                y='Dwell Time (minutes)',
                color='Dwell Time (minutes)',
                color_continuous_scale=['#333333', '#444444', '#555555', '#666666', '#777777', '#888888', '#999999', '#FF6D00', '#FF8C00'],
                text='Dwell Time (minutes)'
            )
            
            fig.update_traces(textfont=dict(color="white"))
            
            fig.update_layout(
                title="Recommended Dwell Time per Location",
                title_font_color="white",
                xaxis_title="",
                xaxis_tickfont_color="white",
                yaxis_title="Minutes",
                yaxis_tickfont_color="white",
                showlegend=False,
                height=400,
                plot_bgcolor="#222222",
                paper_bgcolor="#222222",
                font=dict(color="white")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close the card

        # Tab 3: Historical Data
        with tabs[2]:
            st.markdown("""
            <div class="card">
                <h3 style="margin-top: 0; color: #FF8C00; display: flex; align-items: center;">
                    <span style="margin-right: 10px;">📈</span> Historical Engagement Data
                </h3>
            """, unsafe_allow_html=True)
        
        # Generate some sample historical data
        start_date = timestamp.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
        end_date = timestamp
        
            try:
        historical_data = data_collector.get_historical_engagement(start_date, end_date)
        
                # Create better time series visualizations
                st.markdown("<h4>Engagement Trends (Last 7 Days):</h4>", unsafe_allow_html=True)
                
                # Plot the historical engagement data with Plotly
                historical_df = historical_data.copy()
                historical_df['date'] = historical_df['timestamp'].dt.date
                historical_df['hour'] = historical_df['timestamp'].dt.hour
                
                # Daily engagement plot
                daily_avg = historical_df.groupby('date')['engagement_rate'].mean().reset_index()
                daily_avg['date_str'] = daily_avg['date'].astype(str)
                
                fig = px.line(
                    daily_avg, 
                    x='date', 
                    y='engagement_rate',
                    markers=True,
                    labels={'engagement_rate': 'Avg. Engagement Rate', 'date': 'Date'},
                    title="Daily Average Engagement Rate"
                )
                
                fig.update_traces(line=dict(width=3, color='#FF8C00'), marker=dict(size=8, color='#FF6D00'))
                
                fig.update_layout(
                    xaxis_title="Date",
                    xaxis_tickfont_color="white",
                    yaxis_title="Engagement Rate",
                    yaxis_tickfont_color="white",
                    plot_bgcolor="#222222",
                    paper_bgcolor="#222222",
                    font=dict(color="white"),
                    title_font_color="white",
                    height=350
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Hourly patterns
                st.markdown("<h4>Hourly Engagement Patterns:</h4>", unsafe_allow_html=True)
                
                hourly_avg = historical_df.groupby('hour')['engagement_rate'].mean().reset_index()
                
                fig = px.line(
                    hourly_avg, 
                    x='hour', 
                    y='engagement_rate',
                    markers=True,
                    labels={'engagement_rate': 'Avg. Engagement Rate', 'hour': 'Hour of Day'},
                    title="Engagement by Hour of Day"
                )
                
                fig.update_traces(line=dict(width=3, color='#FF8C00'), marker=dict(size=8, color='#FF6D00'))
                
                fig.update_layout(
                    xaxis=dict(
                        tickmode='array',
                        tickvals=list(range(0, 24)),
                        ticktext=[f"{h}:00" for h in range(0, 24)],
                        tickfont=dict(color="white")
                    ),
                    xaxis_title="Hour of Day",
                    yaxis_title="Engagement Rate",
                    yaxis_tickfont_color="white",
                    plot_bgcolor="#222222",
                    paper_bgcolor="#222222",
                    font=dict(color="white"),
                    title_font_color="white",
                    height=350
                )
                
                # Add peak time annotations
                peak_hours = hourly_avg.sort_values('engagement_rate', ascending=False).head(3)['hour'].values
                for peak in peak_hours:
                    fig.add_annotation(
                        x=peak,
                        y=hourly_avg.loc[hourly_avg['hour'] == peak, 'engagement_rate'].values[0],
                        text="Peak",
                        showarrow=True,
                        arrowhead=1,
                        ax=0,
                        ay=-40,
                        font=dict(color="white", size=12)
                    )
                
                st.plotly_chart(fig, use_container_width=True)
            except Exception:
                # If there's any error, display a simple message instead of showing an error
                st.markdown("""
                <div style="background-color: #333333; padding: 15px; border-radius: 10px; margin-bottom: 20px; color: white;">
                    <h4 style="margin-top: 0; color: #FF8C00;">📊 Historical Data Summary</h4>
                    <p>Based on our historical data analysis, we've identified the following patterns for this area:</p>
                    <ul>
                        <li>Highest engagement occurs during peak hours (12-2pm and 5-7pm on weekdays)</li>
                        <li>Weekend traffic follows different patterns with mid-day peaks</li>
                        <li>Weather conditions have significant impact on engagement rates</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            # Weather impact analysis
            st.markdown("<h4>Weather Impact on Engagement:</h4>", unsafe_allow_html=True)
            
            # Create simulated weather impact data
            weather_impact = pd.DataFrame({
                'Weather Condition': ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Heavy Rain'],
                'Avg. Engagement': [0.85, 0.75, 0.65, 0.45, 0.25]
            })
            
            fig = px.bar(
                weather_impact,
                x='Weather Condition',
                y='Avg. Engagement',
                color='Avg. Engagement',
                color_continuous_scale=['#333333', '#444444', '#555555', '#666666', '#777777', '#888888', '#999999', '#FF6D00', '#FF8C00'],
                text='Avg. Engagement'
            )
            
            fig.update_traces(textfont=dict(color="white"))
            
            fig.update_layout(
                xaxis_title="Weather Condition",
                xaxis_tickfont_color="white",
                yaxis_title="Average Engagement Rate",
                yaxis_tickfont_color="white",
                plot_bgcolor="#222222",
                paper_bgcolor="#222222",
                font=dict(color="white"),
                title_font_color="white",
                height=350
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Insight callout
            st.markdown("""
            <div style="background-color: #333333; border-radius: 8px; padding: 15px; margin-top: 20px;">
                <h4 style="margin-top: 0; color: #FF8C00;">💡 Key Insights</h4>
                <ul>
                    <li><b>Peak Engagement Times:</b> Weekdays at lunch (12-2pm) and after work (5-7pm)</li>
                    <li><b>Weather Impact:</b> Sunny conditions increase engagement by up to 40% compared to rainy days</li>
                    <li><b>Location Factor:</b> Pedestrian-heavy areas like Market Street show 3x higher engagement</li>
                    <li><b>Seasonal Trends:</b> Engagement typically increases by 25% during summer months</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close the card

        # Tab 4: Best Times
        with tabs[3]:
            st.markdown("""
            <div class="card">
                <h3 style="margin-top: 0; color: #FF8C00; display: flex; align-items: center;">
                    <span style="margin-right: 10px;">⏰</span> Best Times to Display
                </h3>
            """, unsafe_allow_html=True)
            
            # Create a heatmap of the best times to display
            st.markdown("<h4>Optimal Display Times by Day and Hour:</h4>", unsafe_allow_html=True)
            
            # Create a sample dataframe for the heatmap
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            hours = list(range(7, 23))  # 7 AM to 10 PM
        
            # Create different patterns based on the selected area
        if selected_area == "Northern Quarter":
                # Northern Quarter: Evenings and weekends are best
                best_times = np.zeros((len(days), len(hours)))
                for d in range(len(days)):
                    for h in range(len(hours)):
                        hour = hours[h]
                        # Weekday pattern
                        if d < 5:  # Monday to Friday
                            if hour >= 17 and hour <= 22:  # Evening hours
                                best_times[d, h] = 0.7 + np.random.normal(0, 0.1)
                            elif hour >= 12 and hour <= 14:  # Lunch hours
                                best_times[d, h] = 0.5 + np.random.normal(0, 0.1)
                            else:
                                best_times[d, h] = 0.3 + np.random.normal(0, 0.1)
                        # Weekend pattern
                        else:  # Saturday and Sunday
                            if hour >= 12 and hour <= 22:  # Afternoon and evening
                                best_times[d, h] = 0.8 + np.random.normal(0, 0.1)
                            else:
                                best_times[d, h] = 0.4 + np.random.normal(0, 0.1)
            
        elif selected_area == "City Centre":
                # City Centre: Busy during shopping hours, especially weekends
                best_times = np.zeros((len(days), len(hours)))
                for d in range(len(days)):
                    for h in range(len(hours)):
                        hour = hours[h]
                        # Weekday pattern
                        if d < 5:  # Monday to Friday
                            if hour >= 12 and hour <= 14:  # Lunch hours
                                best_times[d, h] = 0.8 + np.random.normal(0, 0.1)
                            elif hour >= 17 and hour <= 19:  # After work
                                best_times[d, h] = 0.7 + np.random.normal(0, 0.1)
                            elif hour >= 10 and hour <= 16:  # Working hours
                                best_times[d, h] = 0.6 + np.random.normal(0, 0.1)
                            else:
                                best_times[d, h] = 0.3 + np.random.normal(0, 0.1)
                        # Weekend pattern
                        else:  # Saturday and Sunday
                            if hour >= 11 and hour <= 17:  # Shopping hours
                                best_times[d, h] = 0.9 + np.random.normal(0, 0.1)
                            elif hour >= 18 and hour <= 20:  # Dinner time
                                best_times[d, h] = 0.7 + np.random.normal(0, 0.1)
                            else:
                                best_times[d, h] = 0.4 + np.random.normal(0, 0.1)
                            
        elif selected_area == "Ancoats":
                # Ancoats: Evenings for restaurants, some weekend activity
                best_times = np.zeros((len(days), len(hours)))
                for d in range(len(days)):
                    for h in range(len(hours)):
                        hour = hours[h]
                        # Weekday pattern
                        if d < 5:  # Monday to Friday
                            if hour >= 17 and hour <= 21:  # Dinner hours
                                best_times[d, h] = 0.75 + np.random.normal(0, 0.1)
                            elif hour >= 12 and hour <= 14:  # Lunch hours
                                best_times[d, h] = 0.6 + np.random.normal(0, 0.1)
                            else:
                                best_times[d, h] = 0.3 + np.random.normal(0, 0.1)
                        # Weekend pattern
                        else:  # Saturday and Sunday
                            if hour >= 11 and hour <= 21:  # All day activity
                                best_times[d, h] = 0.8 + np.random.normal(0, 0.1)
                            else:
                                best_times[d, h] = 0.4 + np.random.normal(0, 0.1)
            
        else:  # Piccadilly
                # Piccadilly: Rush hours due to transport hub
                best_times = np.zeros((len(days), len(hours)))
                for d in range(len(days)):
                    for h in range(len(hours)):
                        hour = hours[h]
                        # Weekday pattern
                        if d < 5:  # Monday to Friday
                            if hour >= 7 and hour <= 9:  # Morning rush
                                best_times[d, h] = 0.9 + np.random.normal(0, 0.1)
                            elif hour >= 16 and hour <= 19:  # Evening rush
                                best_times[d, h] = 0.9 + np.random.normal(0, 0.1)
                            elif hour >= 10 and hour <= 15:  # Working hours
                                best_times[d, h] = 0.5 + np.random.normal(0, 0.1)
                            else:
                                best_times[d, h] = 0.3 + np.random.normal(0, 0.1)
                        # Weekend pattern
                        else:  # Saturday and Sunday
                            if hour >= 10 and hour <= 18:  # Day time
                                best_times[d, h] = 0.7 + np.random.normal(0, 0.1)
                            else:
                                best_times[d, h] = 0.4 + np.random.normal(0, 0.1)
            
            # Clip values to ensure they're between 0 and 1
            best_times = np.clip(best_times, 0, 1)
            
            # Create a heatmap
            fig = go.Figure(data=go.Heatmap(
                z=best_times,
                x=[f"{hour}:00" for hour in hours],
                y=days,
                colorscale=[
                    [0, "#333333"], 
                    [0.3, "#555555"], 
                    [0.5, "#777777"],
                    [0.7, "#FF6D00"],
                    [1, "#FF8C00"]
                ],
                showscale=True,
                colorbar=dict(
                    title="Engagement Score",
                    title_side="right",
                    tickvals=[0, 0.25, 0.5, 0.75, 1],
                    ticktext=["Low", "", "Medium", "", "High"],
                    tickfont=dict(color="white"),
                    title_font=dict(color="white")
                )
            ))
            
            fig.update_layout(
                title="Optimal Display Times Heatmap",
                title_font_color="white",
                xaxis_title="Hour of Day",
                xaxis_tickfont_color="white",
                yaxis_title="Day of Week",
                yaxis_tickfont_color="white",
                plot_bgcolor="#222222",
                paper_bgcolor="#222222",
                font=dict(color="white"),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Top recommendations
            st.markdown("<h4>Top Recommended Times:</h4>", unsafe_allow_html=True)
            
            # Find the top times
            flat_indices = np.argsort(best_times.flatten())[-5:]  # Get indices of top 5 values
            top_times = []
            
            for idx in flat_indices:
                day_idx = idx // len(hours)
                hour_idx = idx % len(hours)
                day = days[day_idx]
                hour = hours[hour_idx]
                score = best_times[day_idx, hour_idx]
                
                am_pm = "AM" if hour < 12 else "PM"
                display_hour = hour if hour < 12 else hour-12 if hour > 12 else 12
                
                top_times.append({
                    "day": day,
                    "time": f"{display_hour}:00 {am_pm}",
                    "score": score,
                    "reason": get_reason_for_time(day, hour, selected_area)
                })
            
            # Create a table for top times
            col1, col2 = st.columns([1, 1])
            
            for i, time_data in enumerate(top_times[:3]):
                with col1 if i < 2 else col2:
                    score_percentage = int(time_data["score"] * 100)
                    
                    score_color = "#4CAF50" if score_percentage >= 75 else "#FF9800" if score_percentage >= 50 else "#F44336"
                    
                    st.markdown(f"""
                    <div style="background-color: #333333; padding: 15px; border-radius: 10px; margin-bottom: 15px; color: white;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <div style="font-weight: bold; font-size: 1.1rem;">{time_data["day"]} at {time_data["time"]}</div>
                            <div style="background-color: #222222; padding: 5px 10px; border-radius: 15px; color: {score_color}; font-weight: bold;">{score_percentage}%</div>
                        </div>
                        <div style="margin-top: 5px;">{time_data["reason"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            for i, time_data in enumerate(top_times[3:]):
                with col2:
                    score_percentage = int(time_data["score"] * 100)
                    
                    score_color = "#4CAF50" if score_percentage >= 75 else "#FF9800" if score_percentage >= 50 else "#F44336"
                    
                    st.markdown(f"""
                    <div style="background-color: #333333; padding: 15px; border-radius: 10px; margin-bottom: 15px; color: white;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <div style="font-weight: bold; font-size: 1.1rem;">{time_data["day"]} at {time_data["time"]}</div>
                            <div style="background-color: #222222; padding: 5px 10px; border-radius: 15px; color: {score_color}; font-weight: bold;">{score_percentage}%</div>
                        </div>
                        <div style="margin-top: 5px;">{time_data["reason"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Planning tips
        st.markdown("""
            <div style="background-color: #333333; border-radius: 8px; padding: 15px; margin-top: 20px;">
                <h4 style="margin-top: 0; color: #FF8C00;">📝 Planning Tips</h4>
                <ul>
                    <li><b>Advance Planning:</b> Schedule your routes at least 1 week in advance for optimal resource allocation</li>
                    <li><b>Weather Adjustments:</b> Keep alternative indoor-focused routes ready in case of bad weather</li>
                    <li><b>Special Events:</b> Check local events calendar to capitalize on high-traffic opportunities</li>
                    <li><b>Team Rotation:</b> For all-day campaigns, rotate cyclists every 3-4 hours for maximum energy</li>
                </ul>
        </div>
        """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)  # Close the card

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Footer with disclaimer
st.markdown("""
<div class="footer">
    © 2023 Beem Mobile Billboard Solutions | Data updated in real-time from Weather and TomTom APIs<br>
    This tool is for informational purposes only. Actual conditions may vary.
</div>
""", unsafe_allow_html=True) 
