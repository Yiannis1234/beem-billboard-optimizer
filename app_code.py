import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import requests
import time as time_module
import random

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

# Initialize analyze variable at the top of the script
if 'analyze' not in st.session_state:
    st.session_state.analyze = False

# Initialize the current tab in session state
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = 0

# Remove redundant active_tab variable
if 'active_tab' in st.session_state:
    # Transfer to current_tab if needed
    st.session_state.current_tab = st.session_state.active_tab
    del st.session_state.active_tab

# Set analyze from session state
analyze = st.session_state.analyze

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
            st.session_state.analyze = True
            st.session_state.current_tab = 0
            # Force a rerun to update the UI
            st.session_state.auto_scroll = True
            st.experimental_rerun()
    
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

# Add helper functions to generate data for each tab
def generate_route_data(area, time):
    """Generate sample route data for the given area and time"""
    # In a real implementation, this would fetch actual data
    return {
        'lat': [area_coordinates[area]['latitude'] + random.uniform(-0.01, 0.01) for _ in range(5)],
        'lon': [area_coordinates[area]['longitude'] + random.uniform(-0.01, 0.01) for _ in range(5)],
        'scores': [random.randint(60, 95) for _ in range(5)]
    }

def generate_density_heatmap(area, time, day_type):
    """Generate a heatmap of business density for the selected area"""
    # Create a grid of points around the selected area
    center_lat = area_coordinates[area]['latitude']
    center_lon = area_coordinates[area]['longitude']
    
    # Create a grid of points
    grid_size = 10
    lat_range = np.linspace(center_lat - 0.02, center_lat + 0.02, grid_size)
    lon_range = np.linspace(center_lon - 0.02, center_lon + 0.02, grid_size)
    
    # Generate random density values with higher values near the center
    densities = []
    lats = []
    lons = []
    for lat in lat_range:
        for lon in lon_range:
            distance = ((lat - center_lat)**2 + (lon - center_lon)**2)**0.5
            # Higher density closer to center, with some randomness
            density = max(0, 1 - (distance * 25)) + random.uniform(0, 0.3)
            lats.append(lat)
            lons.append(lon)
            densities.append(min(1.0, density))
    
    # Create the heatmap
    fig = px.density_mapbox(
        data_frame=pd.DataFrame({
            'lat': lats,
            'lon': lons,
            'density': densities
        }),
        lat='lat',
        lon='lon',
        z='density',
        radius=15,
        center=dict(lat=center_lat, lon=center_lon),
        zoom=13,
        mapbox_style="carto-positron",
        title=f"Business Density in {area}",
        color_continuous_scale=["green", "yellow", "orange", "red"]
    )
    
    return fig

def generate_route_map(area, data):
    """Generate a map showing the optimal route through the area"""
    center_lat = area_coordinates[area]['latitude']
    center_lon = area_coordinates[area]['longitude']
    
    # Create route points in a loop
    num_points = 10
    route_lats = [center_lat + 0.005 * np.cos(2 * np.pi * i / num_points) for i in range(num_points+1)]
    route_lons = [center_lon + 0.008 * np.sin(2 * np.pi * i / num_points) for i in range(num_points+1)]
    
    # Create the map
    fig = go.Figure()
    
    # Add the route line
    fig.add_trace(go.Scattermapbox(
        lat=route_lats,
        lon=route_lons,
        mode='lines',
        line=dict(width=4, color='#FF7E33'),
        name='Optimal Route'
    ))
    
    # Add markers for key locations
    fig.add_trace(go.Scattermapbox(
        lat=route_lats[::3],  # Take every 3rd point
        lon=route_lons[::3],
        mode='markers',
        marker=dict(size=15, color='#FF7E33'),
        name='Key Locations',
        text=['Start', 'Checkpoint 1', 'Checkpoint 2', 'End']
    ))
    
    # Update the layout
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=13
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=500
    )
    
    return fig

def generate_engagement_forecast():
    """Generate forecast data for engagement over time"""
    # Generate some sample data for hours of the day
    hours = list(range(6, 22))  # 6 AM to 9 PM
    
    # Create different patterns for engagement based on time of day
    engagement = []
    for hour in hours:
        if hour in [8, 9, 17, 18, 19]:  # Rush hours
            base = random.uniform(0.7, 0.9)
        elif hour in [12, 13, 14]:  # Lunch hours
            base = random.uniform(0.6, 0.8)
        else:
            base = random.uniform(0.3, 0.5)
        engagement.append(base)
    
    # Create a dataframe for the chart
    df = pd.DataFrame({
        'Hour': [f"{h}:00" for h in hours],
        'Engagement': engagement
    })
    
    return df.set_index('Hour')

def generate_interactive_map(area):
    """Generate an interactive map of the area with key points"""
    center_lat = area_coordinates[area]['latitude']
    center_lon = area_coordinates[area]['longitude']
    
    # Create sample points of interest
    num_points = 8
    poi_names = [
        "Shopping Center", "Business District", 
        "University", "Tourist Attraction",
        "Public Park", "Transport Hub", 
        "Entertainment Venue", "Food Court"
    ]
    
    poi_lats = [center_lat + random.uniform(-0.015, 0.015) for _ in range(num_points)]
    poi_lons = [center_lon + random.uniform(-0.015, 0.015) for _ in range(num_points)]
    poi_scores = [random.randint(60, 95) for _ in range(num_points)]
    
    # Create map
    fig = go.Figure()
    
    # Add area boundary (circle)
    theta = np.linspace(0, 2*np.pi, 100)
    radius = 0.012
    boundary_lats = [center_lat + radius * np.cos(t) for t in theta]
    boundary_lons = [center_lon + radius * np.sin(t) for t in theta]
    
    fig.add_trace(go.Scattermapbox(
        lat=boundary_lats,
        lon=boundary_lons,
        mode='lines',
        line=dict(width=2, color='rgba(255, 126, 51, 0.5)'),
        name='Area Boundary'
    ))
    
    # Add points of interest
    fig.add_trace(go.Scattermapbox(
        lat=poi_lats,
        lon=poi_lons,
        mode='markers',
        marker=dict(
            size=14,
            color=poi_scores,
            colorscale='YlOrRd',
            showscale=True,
            colorbar=dict(title="Engagement Score")
        ),
        name='Points of Interest',
        text=poi_names,
        hoverinfo='text+name'
    ))
    
    # Update the layout
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=13
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=500
    )
    
    return fig

def generate_historical_data():
    """Generate historical engagement data"""
    # Create a dataframe with days of the week
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # Generate random engagement data with higher values on weekends
    engagement = []
    foot_traffic = []
    weather_impact = []
    
    for day in days:
        if day in ['Sat', 'Sun']:
            # Weekends have higher engagement
            eng = random.uniform(0.7, 0.9)
            traffic = random.uniform(0.7, 0.95)
            weather = random.uniform(0.6, 0.8)
        else:
            # Weekdays have various patterns
            if day in ['Mon', 'Fri']:
                eng = random.uniform(0.6, 0.8)
            else:
                eng = random.uniform(0.5, 0.7)
            traffic = random.uniform(0.5, 0.8)
            weather = random.uniform(0.5, 0.7)
        
        engagement.append(eng)
        foot_traffic.append(traffic)
        weather_impact.append(weather)
    
    # Create a dataframe for the chart
    df = pd.DataFrame({
        'Day': days,
        'Engagement': engagement,
        'Foot Traffic': foot_traffic,
        'Weather Impact': weather_impact
    })
    
    return df.set_index('Day')

def generate_time_heatmap():
    """Generate a heatmap of optimal times"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = [f"{h}:00" for h in range(6, 22)]  # 6 AM to 9 PM
    
    # Create data for the heatmap
    data = []
    for day in days:
        for hour in hours:
            hour_val = int(hour.split(':')[0])
            
            # Set different patterns for different days and times
            if day in ['Saturday', 'Sunday']:
                if hour_val in [11, 12, 13, 14, 15, 16]:
                    score = random.uniform(0.7, 0.95)  # Weekends midday
                else:
                    score = random.uniform(0.4, 0.7)   # Other times weekends
            else:
                if hour_val in [8, 9, 17, 18, 19]:
                    score = random.uniform(0.7, 0.9)   # Rush hours
                elif hour_val in [12, 13, 14]:
                    score = random.uniform(0.6, 0.8)   # Lunch
                else:
                    score = random.uniform(0.3, 0.6)   # Other times
            
            data.append({
                'Day': day,
                'Hour': hour,
                'Score': score
            })
    
    # Create a dataframe and pivot for the heatmap
    df = pd.DataFrame(data)
    pivot_df = df.pivot(index='Day', columns='Hour', values='Score')
    
    # Create the heatmap
    fig = px.imshow(
        pivot_df,
        color_continuous_scale=['green', 'yellow', 'orange', 'red'],
        labels=dict(x="Hour of Day", y="Day of Week", color="Engagement Score"),
        title="Optimal Times for Maximum Engagement"
    )
    
    fig.update_layout(height=500)
    
    return fig

def generate_age_distribution():
    """Generate age distribution data for the selected area"""
    age_groups = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    
    # Random distribution with preference for younger ages
    values = [random.uniform(0.7, 0.9), random.uniform(0.6, 0.8), 
              random.uniform(0.4, 0.6), random.uniform(0.3, 0.5),
              random.uniform(0.2, 0.4), random.uniform(0.1, 0.3)]
    
    # Create a dataframe
    df = pd.DataFrame({
        'Age Group': age_groups,
        'Percentage': values
    })
    
    return df.set_index('Age Group')

def generate_income_distribution():
    """Generate income distribution data for the selected area"""
    income_levels = ['Under £20k', '£20k-£30k', '£30k-£40k', '£40k-£50k', '£50k-£70k', 'Over £70k']
    
    # Random distribution favoring middle incomes
    values = [random.uniform(0.3, 0.5), random.uniform(0.5, 0.7), 
              random.uniform(0.6, 0.8), random.uniform(0.5, 0.7),
              random.uniform(0.3, 0.5), random.uniform(0.2, 0.4)]
    
    # Create a dataframe
    df = pd.DataFrame({
        'Income Level': income_levels,
        'Percentage': values
    })
    
    return df.set_index('Income Level')

def generate_interest_chart():
    """Generate interest category distribution for the selected area"""
    categories = ['Food & Dining', 'Retail Shopping', 'Entertainment', 
                 'Technology', 'Health & Fitness', 'Education', 
                 'Travel', 'Fashion']
    
    # Random values for each category
    values = [random.uniform(0.5, 0.9) for _ in range(len(categories))]
    
    # Create the radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(255, 126, 51, 0.5)',
        line=dict(color='#FF7E33')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        title="Interest Categories",
        height=400
    )
    
    return fig

# Create a container at the top for the analysis content with an anchor
if analyze:
    st.markdown('<div id="analysis-content"></div>', unsafe_allow_html=True)
    # Use JavaScript to scroll to the analysis content when analyze button is clicked
    st.markdown("""
    <script>
        // Function to scroll to the analysis content
        function scrollToAnalysis() {
            var element = document.getElementById('analysis-content');
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        }
        
        // Call the function after the page loads
        window.addEventListener('load', function() {
            setTimeout(scrollToAnalysis, 500);
        });
    </script>
    """, unsafe_allow_html=True)

# Title with prominent instruction about the arrow - only display when not analyzing
if not analyze:
    # Only show the intro content if we're not analyzing
    st.title("beem.", anchor=False)
    
    # Banner with instructions - using Streamlit native components
    st.warning("👉 **CLICK THE ARROW TOP LEFT** TO ANALYZE YOUR ROUTE 👈")
    
    st.markdown('<h1 class="main-header">🚲 Beem Billboard Route Optimizer</h1>', unsafe_allow_html=True)
    
    # Help box using Streamlit native components - make this smaller
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("""
        **HOW TO USE:** Click the gray ">" button in the top left to open the sidebar menu, 
        select your options, then click "ANALYZE ROUTE"
        """)
    
    # App description using Streamlit native
    st.markdown("""
    ### Optimize your mobile billboard routes for maximum engagement
    Find the best times and locations for your advertising campaigns 📍
    """)
    
    # ROUTE ANALYSIS CONTROLS using Streamlit native components instead of HTML
    st.success("### ROUTE ANALYSIS CONTROLS\n⬅️ Use the controls in the sidebar to select your options")
    
    # Add a direct analyze button in the main content area - HUGE and unmissable
    st.markdown("### Click this button to see results:")
    
    analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 2, 1])
    with analyze_col2:
        main_analyze = st.button("🚀 ANALYZE ROUTE NOW 🚀", type="primary", use_container_width=True)
        if main_analyze:
            st.session_state.analyze = True
            st.session_state.current_tab = 0
            # Force a rerun to update the UI
            st.session_state.auto_scroll = True
            st.experimental_rerun()

    # Welcome banner - extremely simplified to avoid HTML issues
    st.header("Welcome to Beem!", anchor=False)
    st.subheader("Mobile billboard optimization platform", anchor=False)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("📣 Find the best times and locations for your advertising campaigns")
    with col2:
        st.markdown("### 🚲")

# Welcome or Analysis banner based on state - simplified for analysis
if analyze:
    # Analysis banner - keep simple to avoid HTML showing
    st.markdown("""
    <div style="background: linear-gradient(90deg, #FF7E33, #FFB673); border-radius: 10px; padding: 10px; margin-bottom: 15px;" id="scroll-target">
        <h3 style="color: white !important; margin: 0; font-size: 22px; font-weight: 800;">Beem Billboard Insights: {0}</h3>
    </div>
    """.format(area), unsafe_allow_html=True)

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

# Create tabs based on the current tab in session state
tab_names = ["Route Analysis", "Map & Visualization", "Historical Data", "Best Times", "Demographics"]

# Create the tabs
tabs = st.tabs(tab_names)

# Display content in the currently selected tab
with tabs[st.session_state.current_tab]:
    # Tab 1: Route Analysis
    if st.session_state.current_tab == 0:
        if analyze:
            st.markdown(f'<h2 class="gradient-header">Analysis for {area}</h2>', unsafe_allow_html=True)
            
            # Simulate loading time for now (remove this in production)
            # Generate placeholder data
            placeholder_data = generate_route_data(area, selected_time)
            
            # Business density heatmap
            st.subheader("Business Density Heatmap")
            st.plotly_chart(generate_density_heatmap(area, selected_time, day_type), use_container_width=True)
            
            # Optimal route
            st.subheader("Optimal Route")
            st.plotly_chart(generate_route_map(area, placeholder_data), use_container_width=True)
            
            # Route metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Estimated Impressions", f"{random.randint(12000, 18000):,}")
            with col2:
                st.metric("Route Length", f"{random.randint(8, 15)} km")
            with col3:
                st.metric("Estimated Time", f"{random.randint(45, 90)} mins")
                
            # Detailed metrics
            st.subheader("Engagement Forecast")
            st.bar_chart(generate_engagement_forecast())
        else:
            st.info("Click the ANALYZE ROUTE button to see results")
    
    # Tab 2: Map & Visualization
    elif st.session_state.current_tab == 1:
        st.subheader("Interactive Area Map")
        if analyze:
            # Display map of the selected area with key metrics
            st.plotly_chart(generate_interactive_map(area), use_container_width=True)
            
            # Key area insights
            st.subheader("Key Area Insights")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Foot Traffic Density", f"{random.randint(75, 98)}%")
                st.metric("Business Concentration", f"{random.randint(65, 90)}%")
            with col2:
                st.metric("Average Dwell Time", f"{random.randint(12, 35)} min")
                st.metric("Area Popularity", f"{random.randint(7, 10)}/10")
        else:
            st.info("Run the analysis first to see visualizations")
    
    # Tab 3: Historical Data
    elif st.session_state.current_tab == 2:
        st.subheader("Historical Performance")
        if analyze:
            # Display comparison charts
            st.line_chart(generate_historical_data())
            
            # Insights
            st.subheader("Trend Analysis")
            st.write("Based on historical data, we predict a 23% increase in engagement compared to last month in this area.")
        else:
            st.info("Run the analysis first to see historical data")
    
    # Tab 4: Best Times
    elif st.session_state.current_tab == 3:
        st.subheader("Optimal Times")
        if analyze:
            # Heat calendar for best times
            st.plotly_chart(generate_time_heatmap(), use_container_width=True)
            
            # Recommended time slots
            st.subheader("Recommended Time Slots")
            for i in range(3):
                day = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
                time = random.choice(["8:00 AM - 10:00 AM", "11:30 AM - 1:30 PM", "4:00 PM - 6:00 PM"])
                st.success(f"**{day}**: {time} - High business activity and foot traffic")
        else:
            st.info("Run the analysis first to see optimal times")
    
    # Tab 5: Demographics
    elif st.session_state.current_tab == 4:
        st.subheader("Demographic Insights")
        if analyze:
            # Age distribution
            st.subheader("Age Distribution")
            st.bar_chart(generate_age_distribution())
            
            # Income levels
            st.subheader("Income Levels")
            st.bar_chart(generate_income_distribution())
            
            # Interest categories
            st.subheader("Interest Categories")
            st.plotly_chart(generate_interest_chart(), use_container_width=True)
        else:
            st.info("Run the analysis first to see demographic insights")

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

# Add button to return to the top if scrolled down
if analyze:
    # Initialize auto scroll if needed
    if 'auto_scroll' not in st.session_state:
        st.session_state.auto_scroll = False
        
    # Auto-scroll implementation
    if st.session_state.auto_scroll:
        # Scroll to the top of the analysis section - higher priority than anchor
        js = f"""
        <script>
            function scrollToTop() {{
                window.scrollTo(0, 0);
            }}
            // Execute with a small delay to ensure page is rendered
            setTimeout(scrollToTop, 100);
        </script>
        """
        st.markdown(js, unsafe_allow_html=True)
        # Reset flag to avoid continuous scrolling
        st.session_state.auto_scroll = False
    
    # Add a button to jump to top
    st.sidebar.markdown("---")
    if st.sidebar.button("Return to Top ⬆️"):
        st.session_state.auto_scroll = True
        st.experimental_rerun()