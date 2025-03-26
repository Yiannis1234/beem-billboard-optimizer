import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import random

# Page Configuration
st.set_page_config(
    page_title="Beem Billboard Optimizer", 
    page_icon="🚲", 
    layout="wide", 
    initial_sidebar_state="expanded"  # Start with sidebar expanded to avoid confusion
)

# Simple CSS without complex HTML or JavaScript
st.markdown("""
<style>
    /* Base theme */
    .stApp {
        background-color: #F9F9F9;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFF1E6;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #FF9D45 !important;
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
    "Spinningfields": {"latitude": 53.4802, "longitude": -2.2516, "zone_id": "spinningfields"}
}

# Initialize session state variables
if 'analyze' not in st.session_state:
    st.session_state.analyze = False
if 'selected_area' not in st.session_state:
    st.session_state.selected_area = list(area_coordinates.keys())[0]
if 'selected_time' not in st.session_state:
    st.session_state.selected_time = datetime.now()
if 'selected_day_type' not in st.session_state:
    st.session_state.selected_day_type = "Weekday"

# SIDEBAR - Define the sidebar first
with st.sidebar:
    st.title("beem.")
    st.markdown("### ROUTE ANALYSIS CONTROLS")
    
    # Area selection
    st.markdown('## Route Options')
    areas = list(area_coordinates.keys())
    selected_area = st.selectbox("Select your Area", areas, index=areas.index(st.session_state.selected_area))
    st.session_state.selected_area = selected_area
    
    # Time selection
    st.markdown('### Time Options')
    time_option = st.radio("Select time", ["Current time", "Custom time"])
    
    if time_option == "Custom time":
        date = st.date_input("Date", datetime.now())
        hour = st.slider("Hour", 0, 23, 12)
        selected_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=hour)
    else:
        selected_time = datetime.now()
    st.session_state.selected_time = selected_time
    
    # Day type
    selected_day_type = st.radio("Day type", ["Weekday", "Weekend"])
    st.session_state.selected_day_type = selected_day_type
    
    # Analysis button
    st.info("Click below to analyze your route ⬇️")
    if st.button("ANALYZE ROUTE", type="primary", use_container_width=True):
        st.session_state.analyze = True
    
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

# MAIN CONTENT
# Get the latest values from session state
area = st.session_state.selected_area
selected_time = st.session_state.selected_time
day_type = st.session_state.selected_day_type
analyze = st.session_state.analyze

# Display analysis or welcome page
if analyze:
    st.title(f"Beem Billboard Insights: {area}")
    st.subheader(f"Analysis for {area}")
    
    # Add a reset button at the top
    if st.button("Start New Analysis"):
        st.session_state.analyze = False
        st.rerun()
    
    # Display route data
    tabs = st.tabs(["Route Overview", "Map & Visualization", "Best Times", "Demographics"])
    
    # Tab 1: Route Overview
    with tabs[0]:
        # Basic route metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Estimated Impressions", f"{random.randint(12000, 18000):,}")
        with col2:
            st.metric("Route Length", f"{random.randint(8, 15)} km")
        with col3:
            st.metric("Estimated Time", f"{random.randint(45, 90)} mins")
        
        # Route map
        st.subheader("Optimal Route")
        st.plotly_chart(generate_route_map(area), use_container_width=True)
        
        # Engagement forecast
        st.subheader("Engagement Forecast")
        st.bar_chart(generate_engagement_forecast())
    
    # Tab 2: Map & Visualization
    with tabs[1]:
        # Density heatmap
        st.subheader("Business Density Heatmap")
        st.plotly_chart(generate_density_heatmap(area, day_type), use_container_width=True)
        
        # Key insights
        st.subheader("Key Area Insights")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Foot Traffic Density", f"{random.randint(75, 98)}%")
            st.metric("Business Concentration", f"{random.randint(65, 90)}%")
        with col2:
            st.metric("Average Dwell Time", f"{random.randint(12, 35)} min")
            st.metric("Area Popularity", f"{random.randint(7, 10)}/10")
    
    # Tab 3: Best Times
    with tabs[2]:
        st.subheader("Optimal Times")
        st.plotly_chart(generate_time_heatmap(), use_container_width=True)
        
        # Recommended time slots
        st.subheader("Recommended Time Slots")
        for i in range(3):
            day = random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            time = random.choice(["8:00 AM - 10:00 AM", "11:30 AM - 1:30 PM", "4:00 PM - 6:00 PM"])
            st.success(f"**{day}**: {time} - High business activity and foot traffic")
    
    # Tab 4: Demographics
    with tabs[3]:
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
    # Welcome page
    st.title("Welcome to Beem Billboard Optimizer")
    st.header("🚲 Optimize your mobile billboard routes")
    
    st.info("""
    **HOW TO USE:**
    1. Use the sidebar on the left to select your area and time options
    2. Click "ANALYZE ROUTE" to see detailed insights
    """)
    
    st.markdown("""
    ### Find the best times and locations for your advertising campaigns
    
    Beem helps businesses reach their target audience through:
    - 📍 Targeted geographical routing
    - ⏰ Optimal timing recommendations
    - 👥 Demographic insights
    - 📈 Engagement forecasts
    """)
    
    # Add a prominent analyze button in the main area too
    if st.button("ANALYZE ROUTE NOW", type="primary", use_container_width=False):
        st.session_state.analyze = True
        st.rerun()

# Simple footer
st.markdown("---")
st.markdown("### beem. © 2025 Beem Mobile Billboard Solutions")

# Helper functions to generate data
def generate_route_map(area):
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

def generate_density_heatmap(area, day_type):
    """Generate a heatmap of business density for the selected area"""
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