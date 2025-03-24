import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time
from src.data.data_collector import BeemDataCollector
import json
import time as time_module

# Page configuration
st.set_page_config(
    page_title="Beem Billboard Bike Route Optimizer", 
    page_icon="🚲", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #1E88E5 !important;
        margin-bottom: 1rem !important;
    }
    .subheader {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #333 !important;
        margin-bottom: 1rem !important;
        padding-top: 1rem !important;
        border-top: 1px solid #eee !important;
    }
    .metric-container {
        background-color: #f7f7f7 !important;
        padding: 1rem !important;
        border-radius: 0.5rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1) !important;
    }
    .recommendation {
        padding: 0.5rem 1rem !important;
        margin-bottom: 0.5rem !important;
        border-left: 4px solid #1E88E5 !important;
        background-color: #f1f8fe !important;
        border-radius: 0.25rem !important;
    }
    .warning {
        border-left: 4px solid #ff9800 !important;
        background-color: #fff8e1 !important;
    }
    .success {
        border-left: 4px solid #4caf50 !important;
        background-color: #e8f5e9 !important;
    }
    .data-label {
        font-weight: 600 !important;
        color: #555 !important;
    }
    .footer {
        margin-top: 3rem !important;
        padding-top: 1rem !important;
        border-top: 1px solid #eee !important;
        font-size: 0.8rem !important;
        color: #888 !important;
        text-align: center !important;
    }
    .sidebar-content {
        padding: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<div class="main-header">🚲 Beem Billboard Bike Route Optimizer</div>', unsafe_allow_html=True)
st.markdown("""
This tool helps optimize bicycle routes for Beem's mobile billboards in Manchester. 
Get real-time weather, traffic, and pedestrian data to maximize engagement and plan your routes efficiently.
""")

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
        # Fallback to a placeholder
        st.image("https://placehold.co/200x100/3498db/FFFFFF?text=BEEM", width=200)
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.header("Route Configuration")
    
    # Area selection dropdown
    selected_area = st.selectbox(
        "📍 Choose an area in Manchester:",
        ["Northern Quarter", "City Centre", "Ancoats", "Piccadilly"]
    )
    
    # Time selection
    time_options = st.radio(
        "⏱️ When to display?",
        ["Now", "Select Time"]
    )
    
    if time_options == "Select Time":
        selected_date = st.date_input("Select date", datetime.now())
        selected_hour = st.slider("Select hour", 0, 23, datetime.now().hour)
        timestamp = datetime.combine(selected_date, time(hour=selected_hour))
    else:
        timestamp = datetime.now()
        st.write(f"Current time: {timestamp.strftime('%d %b %Y, %H:%M')}")
    
    # Analysis button
    analyze_button = st.button("📊 Analyze Route", type="primary", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    with st.expander("ℹ️ About Beem"):
        st.write("""
        Beem helps businesses reach their audience through eye-catching mobile billboards carried by cyclists.
        Our innovative approach is eco-friendly, cost-effective, and targets specific areas with precision.
        """)

# Define Manchester zones
manchester_zones = {
    "Northern Quarter": {
        'zone_id': 'northern_quarter',
        'latitude': 53.4831,
        'longitude': -2.2372,
        'description': 'A trendy, creative neighborhood with high foot traffic and many independent businesses.',
        'best_times': 'Evenings and weekends',
        'target_audience': 'Young professionals, creatives, tourists'
    },
    "City Centre": {
        'zone_id': 'city_centre',
        'latitude': 53.4808,
        'longitude': -2.2426,
        'description': 'The bustling heart of Manchester with shopping centers, offices, and attractions.',
        'best_times': 'Weekday lunchtimes and weekends',
        'target_audience': 'Shoppers, office workers, tourists'
    },
    "Ancoats": {
        'zone_id': 'ancoats',
        'latitude': 53.4836,
        'longitude': -2.2275,
        'description': 'An up-and-coming area with popular restaurants and apartment buildings.',
        'best_times': 'Evenings and weekends',
        'target_audience': 'Young professionals, foodies'
    },
    "Piccadilly": {
        'zone_id': 'piccadilly',
        'latitude': 53.4768,
        'longitude': -2.2351,
        'description': 'A major transportation hub with high commuter traffic.',
        'best_times': 'Rush hours (8-9 AM, 5-6 PM)',
        'target_audience': 'Commuters, travelers'
    }
}

# Progress indicator for analysis
def show_analysis_progress():
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = ["Collecting weather data", "Analyzing traffic conditions", 
             "Estimating pedestrian density", "Calculating optimal routes", 
             "Generating recommendations"]
    
    for i, step in enumerate(steps):
        progress_bar.progress((i+1)/len(steps))
        status_text.text(f"Step {i+1}/{len(steps)}: {step}...")
        time_module.sleep(0.5)
    
    progress_bar.empty()
    status_text.empty()

# When button is clicked, analyze the selected area
if analyze_button:
    # Get the selected zone
    selected_zone = manchester_zones[selected_area]
    
    # Show progress during analysis
    show_analysis_progress()
    
    # Collect integrated data
    integrated_data = data_collector.integrate_data(selected_zone, timestamp)
    
    # Main content divided into two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Display route analysis
        st.markdown(f'<div class="subheader">Route Analysis for {selected_area}</div>', unsafe_allow_html=True)
        
        # Area Information
        st.markdown("### 📌 Area Information")
        st.markdown(f"**Description:** {selected_zone['description']}")
        st.markdown(f"**Best Times:** {selected_zone['best_times']}")
        st.markdown(f"**Target Audience:** {selected_zone['target_audience']}")
        
        # Weather section
        st.markdown('<div class="subheader">☀️ Current Weather Conditions</div>', unsafe_allow_html=True)
        weather_data = integrated_data['weather']
        
        weather_cols = st.columns(4)
        with weather_cols[0]:
            st.metric("Temperature", f"{weather_data['temperature']:.1f}°C")
        with weather_cols[1]:
            st.metric("Condition", f"{weather_data['condition']}")
        with weather_cols[2]:
            st.metric("Wind Speed", f"{weather_data['wind_speed']:.1f} km/h")
        with weather_cols[3]:
            st.metric("Precipitation", f"{weather_data['precipitation']:.0f} mm")
        
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
        
        # Pedestrian density
        st.markdown('<div class="subheader">👥 Pedestrian Activity</div>', unsafe_allow_html=True)
        
        density_cols = st.columns(2)
        with density_cols[0]:
            density = integrated_data['pedestrian_density']
            density_status = "High" if density > 0.7 else "Medium" if density > 0.4 else "Low"
            st.metric("Current Level", f"{density:.2f}", delta=density_status)
        with density_cols[1]:
            hour = timestamp.hour
            expected_trend = "Increasing" if (hour >= 7 and hour <= 9) or (hour >= 16 and hour <= 18) else "Decreasing" if hour >= 19 or hour <= 5 else "Stable"
            st.metric("Expected Trend", expected_trend)
        
        # Overall score
        st.markdown('<div class="subheader">📊 Engagement Analysis</div>', unsafe_allow_html=True)
        
        # Calculate engagement score based on various factors
        engagement_score = (
            (0.4 * (1 - traffic_data['congestion_level'])) +  # Lower congestion is better
            (0.4 * integrated_data['pedestrian_density']) +   # Higher pedestrian density is better
            (0.2 * (1 - min(1, weather_data['precipitation'])))  # Less precipitation is better
        )
        
        engagement_percentage = min(100, max(0, engagement_score * 100))
        
        # Display engagement score
        score_cols = st.columns(2)
        with score_cols[0]:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            score_color = "green" if engagement_percentage >= 70 else "orange" if engagement_percentage >= 40 else "red"
            st.markdown(f"<h1 style='text-align: center; color: {score_color};'>{engagement_percentage:.1f}%</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Expected Engagement Score</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with score_cols[1]:
            # Recommendations based on conditions
            recommendations = []
            
            if traffic_data['congestion_level'] > 0.7:
                recommendations.append(("⚠️ High traffic congestion. Consider alternative routes.", "warning"))
            
            if integrated_data['pedestrian_density'] < 0.3:
                recommendations.append(("⚠️ Low pedestrian activity. Consider scheduling during peak hours.", "warning"))
            
            if weather_data['precipitation'] > 0.5:
                recommendations.append(("⚠️ Rain expected. Consider rescheduling or prepare weather protection.", "warning"))
            
            if weather_data['wind_speed'] > 15:
                recommendations.append(("⚠️ High winds may affect visibility. Take extra caution.", "warning"))
            
            if not recommendations:
                recommendations.append(("✅ Conditions are favorable for billboard display.", "success"))
            
            for rec, status in recommendations:
                st.markdown(f'<div class="recommendation {status}">{rec}</div>', unsafe_allow_html=True)
    
    with col2:
        # Display map with location marker
        st.markdown('<div class="subheader">🗺️ Route Map</div>', unsafe_allow_html=True)
        
        map_data = pd.DataFrame({
            'lat': [selected_zone['latitude']],
            'lon': [selected_zone['longitude']]
        })
        
        st.map(map_data)
        
        # Simulated historical data chart
        st.markdown('<div class="subheader">📈 Historical Patterns</div>', unsafe_allow_html=True)
        
        # Generate some sample historical data
        start_date = timestamp.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
        end_date = timestamp
        
        historical_data = data_collector.get_historical_engagement(start_date, end_date)
        
        # Plot the historical engagement data
        st.line_chart(historical_data.set_index('timestamp')['engagement_rate'])
        
        # Best times to display
        st.markdown('<div class="subheader">⏰ Best Times</div>', unsafe_allow_html=True)
        
        # Create a heatmap of best times
        hours = range(8, 22)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Create synthetic data for the heatmap
        if selected_area == "Northern Quarter":
            best_times = np.array([
                [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.7, 0.6, 0.5, 0.6, 0.7, 0.8, 0.9, 0.8],  # Mon
                [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.7, 0.6, 0.5, 0.6, 0.8, 0.9, 0.9, 0.8],  # Tue
                [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.7, 0.6, 0.5, 0.6, 0.8, 0.9, 0.9, 0.8],  # Wed
                [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.7, 0.6, 0.5, 0.7, 0.9, 1.0, 1.0, 0.9],  # Thu
                [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.7, 0.6, 0.6, 0.8, 0.9, 1.0, 1.0, 0.9],  # Fri
                [0.6, 0.7, 0.8, 0.9, 0.9, 0.8, 0.8, 0.7, 0.7, 0.8, 0.9, 1.0, 1.0, 0.9],  # Sat
                [0.5, 0.6, 0.7, 0.8, 0.8, 0.7, 0.6, 0.5, 0.5, 0.6, 0.7, 0.8, 0.7, 0.6],  # Sun
            ])
        elif selected_area == "City Centre":
            best_times = np.array([
                [0.7, 0.9, 1.0, 0.9, 0.8, 0.9, 0.8, 0.7, 0.6, 0.7, 0.8, 0.8, 0.6, 0.5],  # Mon
                [0.7, 0.9, 1.0, 0.9, 0.8, 0.9, 0.8, 0.7, 0.6, 0.7, 0.8, 0.8, 0.6, 0.5],  # Tue
                [0.7, 0.9, 1.0, 0.9, 0.8, 0.9, 0.8, 0.7, 0.6, 0.7, 0.8, 0.8, 0.6, 0.5],  # Wed
                [0.7, 0.9, 1.0, 0.9, 0.8, 0.9, 0.8, 0.7, 0.6, 0.7, 0.8, 0.8, 0.7, 0.6],  # Thu
                [0.7, 0.9, 1.0, 0.9, 0.8, 0.9, 0.8, 0.7, 0.7, 0.8, 0.8, 0.8, 0.8, 0.7],  # Fri
                [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.0, 0.9, 0.9, 0.9, 0.8, 0.8, 0.7, 0.6],  # Sat
                [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.8, 0.7, 0.6, 0.6, 0.5, 0.4, 0.3, 0.2],  # Sun
            ])
        elif selected_area == "Ancoats":
            best_times = np.array([
                [0.3, 0.4, 0.5, 0.5, 0.4, 0.6, 0.7, 0.6, 0.5, 0.7, 0.9, 0.9, 0.8, 0.7],  # Mon
                [0.3, 0.4, 0.5, 0.5, 0.4, 0.6, 0.7, 0.6, 0.5, 0.7, 0.9, 0.9, 0.8, 0.7],  # Tue
                [0.3, 0.4, 0.5, 0.5, 0.4, 0.6, 0.7, 0.6, 0.5, 0.7, 0.9, 0.9, 0.8, 0.7],  # Wed
                [0.3, 0.4, 0.5, 0.5, 0.4, 0.6, 0.7, 0.6, 0.5, 0.7, 0.9, 1.0, 0.9, 0.8],  # Thu
                [0.3, 0.4, 0.5, 0.5, 0.4, 0.6, 0.7, 0.6, 0.5, 0.7, 0.9, 1.0, 0.9, 0.8],  # Fri
                [0.4, 0.5, 0.6, 0.7, 0.8, 0.8, 0.8, 0.7, 0.7, 0.8, 0.9, 1.0, 0.9, 0.8],  # Sat
                [0.4, 0.5, 0.6, 0.7, 0.7, 0.7, 0.6, 0.6, 0.6, 0.7, 0.7, 0.6, 0.5, 0.4],  # Sun
            ])
        else:  # Piccadilly
            best_times = np.array([
                [0.9, 1.0, 0.8, 0.7, 0.6, 0.7, 0.8, 0.7, 0.6, 0.8, 0.9, 1.0, 0.8, 0.7],  # Mon
                [0.9, 1.0, 0.8, 0.7, 0.6, 0.7, 0.8, 0.7, 0.6, 0.8, 0.9, 1.0, 0.8, 0.7],  # Tue
                [0.9, 1.0, 0.8, 0.7, 0.6, 0.7, 0.8, 0.7, 0.6, 0.8, 0.9, 1.0, 0.8, 0.7],  # Wed
                [0.9, 1.0, 0.8, 0.7, 0.6, 0.7, 0.8, 0.7, 0.6, 0.8, 0.9, 1.0, 0.8, 0.7],  # Thu
                [0.9, 1.0, 0.8, 0.7, 0.6, 0.7, 0.8, 0.7, 0.6, 0.8, 0.9, 1.0, 0.9, 0.8],  # Fri
                [0.5, 0.6, 0.7, 0.8, 0.8, 0.7, 0.7, 0.6, 0.6, 0.7, 0.7, 0.8, 0.7, 0.6],  # Sat
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.4, 0.4, 0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3],  # Sun
            ])
        
        # Convert to dataframe for display
        hour_labels = [f"{h}:00" for h in hours]
        best_times_df = pd.DataFrame(best_times, index=days, columns=hour_labels)
        
        st.dataframe(best_times_df.style.background_gradient(cmap='Greens'), use_container_width=True)
        
        # Color scale explanation
        st.markdown("""
        <div style="display: flex; justify-content: space-between; margin-top: 5px; font-size: 0.8rem;">
            <span>Low Engagement</span>
            <span>High Engagement</span>
        </div>
        <div style="height: 10px; background: linear-gradient(to right, #f7fcf5, #e5f5e0, #c7e9c0, #a1d99b, #74c476, #41ab5d, #238b45, #005a32);"></div>
        """, unsafe_allow_html=True)

# Footer with disclaimer
st.markdown("""
<div class="footer">
    © 2023 Beem Mobile Billboard Solutions | Data updated in real-time from Weather and TomTom APIs<br>
    This tool is for informational purposes only. Actual conditions may vary.
</div>
""", unsafe_allow_html=True) 