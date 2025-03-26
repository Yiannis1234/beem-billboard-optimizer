import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random

# Page Configuration
st.set_page_config(
    page_title="Beem Billboard Optimizer", 
    page_icon="🚲", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

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

def generate_route_data(area):
    """Generate sample route data for the given area"""
    return {
        'lat': [area_coordinates[area]["latitude"] + random.uniform(-0.01, 0.01) for _ in range(5)],
        'lon': [area_coordinates[area]["longitude"] + random.uniform(-0.01, 0.01) for _ in range(5)],
        'scores': [random.randint(60, 95) for _ in range(5)]
    }

def generate_density_heatmap(area, day_type):
    """Generate a heatmap of business density for the selected area"""
    center_lat = area_coordinates[area]["latitude"]
    center_lon = area_coordinates[area]["longitude"]
    
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
    center_lat = area_coordinates[area]["latitude"]
    center_lon = area_coordinates[area]["longitude"]
    
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
        lon=route_lons[::3],  # This was a bug! Should be route_lons
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

# Initialize session state
if 'analyze' not in st.session_state:
    st.session_state.analyze = False

if 'selected_area' not in st.session_state:
    st.session_state.selected_area = list(area_coordinates.keys())[0]

if 'selected_day_type' not in st.session_state:
    st.session_state.selected_day_type = "Weekday"

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
    st.subheader(f"Analysis for {area}")
    
    # Generate data 
    data = generate_route_data(area)
    
    # Business density heatmap
    st.subheader("Business Density Heatmap")
    density_heatmap = generate_density_heatmap(area, day_type)
    st.plotly_chart(density_heatmap, use_container_width=True)
    
    # Optimal route
    st.subheader("Optimal Route")
    route_map = generate_route_map(area, data)
    st.plotly_chart(route_map, use_container_width=True)
    
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
    forecast = generate_engagement_forecast()
    st.bar_chart(forecast)
else:
    # Welcome page
    st.title("beem.", anchor=False)
    
    # Banner with instructions
    st.error("## 👉 PRESS TOP LEFT TO ANALYZE YOUR ROUTE 👈")
    
    st.header("🚲 Beem Billboard Route Optimizer")
    
    # Help box
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("""
        **HOW TO USE:**
        1. Press the top left options to select your area and time
        2. Click "ANALYZE ROUTE" to see results
        """)
    
    # App description
    st.markdown("""
    ### Optimize your mobile billboard routes for maximum engagement
    Find the best times and locations for your advertising campaigns 📍
    """)
    
    # Direct analyze button
    st.markdown("### Click the button below to see results:")
    
    analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 2, 1])
    with analyze_col2:
        if st.button("🚀 ANALYZE ROUTE NOW 🚀", type="primary", use_container_width=True):
            st.session_state.analyze = True
            st.rerun()

# Footer
st.markdown("---")
st.markdown("### beem. © 2025 Beem Mobile Billboard Solutions")