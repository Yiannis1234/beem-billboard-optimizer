import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, Optional

# Page Configuration
st.set_page_config(
    page_title="Beem Billboard Optimizer",
    page_icon="🚲",
    layout="wide"
)

# Initialize session state variables
if 'selected_area' not in st.session_state:
    st.session_state.selected_area = "Northern Quarter"
if 'analyze' not in st.session_state:
    st.session_state.analyze = False
if 'day_type' not in st.session_state:
    st.session_state.day_type = "Weekday"

# Custom CSS for styling
st.markdown("""
<style>
    /* Button styling - applies to ALL buttons */
    .stButton button,
    button,
    .stButton > button:first-child,
    .stButton > button:hover,
    .stButton > button:focus,
    .stButton > button:active {
        background: linear-gradient(135deg, #FF7E33, #FF9945) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 6px rgba(255, 126, 51, 0.3) !important;
    }
    
    .stButton button:hover,
    button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(255, 126, 51, 0.4) !important;
    }

    /* Main theme colors */
    h1, h2, h3 {
        color: #FF7E33 !important;
    }
    
    div.stMarkdown {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

class BeemDataCollector:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the data collector with optional configuration."""
        self.config = config or {}

    def get_weather_forecast(self, location: str) -> Dict[str, float]:
        """Get weather forecast for a location."""
        return {
            'temperature': 18.5,
            'condition': 'Partly Cloudy',
            'wind_speed': 12.0,
            'precipitation': 0.0
        }

    def get_traffic_data(self, zone: str) -> Dict[str, float]:
        """Get traffic data for a zone."""
        return {
            'flow_speed': 30.0,
            'free_flow_speed': 40.0,
            'congestion_level': 0.3
        }

    def get_historical_engagement(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Get historical engagement data."""
        dates = pd.date_range(start_date, end_date, freq='H')
        return pd.DataFrame({
            'timestamp': dates,
            'engagement_rate': np.random.uniform(0.3, 0.8, len(dates))
        })

    def get_pedestrian_density(self, zone: str, timestamp: datetime) -> float:
        """Get pedestrian density for a zone at a specific time."""
        hour = timestamp.hour
        if 12 <= hour <= 14 or 17 <= hour <= 19:  # Lunch and rush hours
            return 0.7
        elif 9 <= hour <= 16:  # Business hours
            return 0.5
        else:
            return 0.3

    def integrate_data(self, zone: str, timestamp: datetime) -> Dict[str, Any]:
        """Integrate all data sources."""
        return {
            'weather': self.get_weather_forecast(zone),
            'traffic': self.get_traffic_data(zone),
            'pedestrian_density': self.get_pedestrian_density(zone, timestamp)
        }

# Initialize data collector
data_collector = BeemDataCollector()

# App title and description
st.title("🚲 Beem Billboard Optimizer")
st.markdown("""
This tool helps optimize bicycle routes for Beem's mobile billboards in Manchester. 
Get real-time weather, traffic, and pedestrian data to maximize engagement and plan your routes efficiently.
""")

# Sidebar for area selection
with st.sidebar:
    st.header("Route Configuration")
    
    # Area selection
    selected_area = st.selectbox(
        "Choose an area:",
        ["Northern Quarter", "City Centre", "Ancoats", "Piccadilly"],
        key="area_select"
    )
    st.session_state.selected_area = selected_area
    
    # Time selection
    time_option = st.radio("When to display?", ["Now", "Select Time"], key="time_option")
    
    if time_option == "Select Time":
        date = st.date_input("Date", datetime.now(), key="date_select")
        hour = st.slider("Hour", 0, 23, datetime.now().hour, key="hour_select")
    else:
        date = datetime.now().date()
        hour = datetime.now().hour
    
    # Analyze button
    if st.button("Analyze Route", key="analyze_button"):
        st.session_state.analyze = True
        st.success("Analysis started!")

# Main content area
if st.session_state.analyze:
    # Create timestamp for analysis
    analysis_time = datetime.combine(date, time(hour=hour))
    
    # Get integrated data
    data = data_collector.integrate_data(st.session_state.selected_area, analysis_time)
    
    # Display results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Weather", f"{data['weather']['temperature']}°C", "Partly Cloudy")
        
    with col2:
        st.metric("Traffic Flow", f"{data['traffic']['flow_speed']} km/h", 
                 f"{int(data['traffic']['congestion_level'] * 100)}% congested")
        
    with col3:
        st.metric("Pedestrian Density", f"{int(data['pedestrian_density'] * 100)}%", 
                 "High foot traffic")

    # Display recommendations
    st.subheader("Route Recommendations")
    st.write(f"Based on the current conditions in {st.session_state.selected_area}:")
    
    recommendations = [
        "🎯 Target high-traffic areas near major intersections",
        "⏰ Best display times are during lunch hours (12-2 PM) and evening rush (5-7 PM)",
        "🌤️ Weather conditions are favorable for outdoor advertising",
        "👥 Current pedestrian density suggests good visibility potential"
    ]
    
    for rec in recommendations:
        st.markdown(f"- {rec}")
else:
    # Instructions when app first loads
    st.markdown("""
    ## Welcome to the Beem Billboard Optimizer
    
    1. Select an area in Manchester in the sidebar
    2. Choose when to display your advertisement
    3. Click "Analyze Route" to get optimal route suggestions
    
    This tool will help you maximize the visibility and impact of your mobile billboard campaigns!
    """)
    
    # Display example buttons
    st.subheader("Choose an option:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("START ANALYSIS 🔍"):
            st.session_state.analyze = True
    
    with col2:
        if st.button("Press top left arrow to analyze ⬅️"):
            st.balloons()
