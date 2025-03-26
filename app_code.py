import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import random
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Beem Billboard Optimizer", 
    page_icon="🚲", 
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
    "Spinningfields": {"latitude": 53.4802, "longitude": -2.2516, "zone_id": "spinningfields"}
}

def generate_route_data(area):
    """Generate sample route data for the given area"""
    return {
        'lat': [area_coordinates[area]["latitude"] + random.uniform(-0.01, 0.01) for _ in range(5)],
        'lon': [area_coordinates[area]["longitude"] + random.uniform(-0.01, 0.01) for _ in range(5)],
        'scores': [random.randint(60, 95) for _ in range(5)]
    }

def get_weather_data(area, day_type):
    """Generate simulated weather data for the area"""
    # More variation based on day type
    if day_type == "Weekend":
        temp = round(random.uniform(8, 18), 1)  # Slightly warmer on weekends for visualization
    else:
        temp = round(random.uniform(5, 15), 1)  # Cooler on weekdays
        
    conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Light Rain", "Moderate Rain"]
    weights = [0.2, 0.3, 0.3, 0.15, 0.05]  # Manchester is somewhat rainy
    
    return {
        "temperature": temp,
        "condition": random.choices(conditions, weights=weights)[0],
        "precipitation_chance": round(random.uniform(20, 60), 0),
        "wind_speed": round(random.uniform(5, 20), 1)
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
    """Generate simulated traffic density data"""
    if hour is None:
        hour = datetime.now().hour
    
    # Base traffic varies by area
    area_factor = {
        "Northern Quarter": 0.8,
        "City Centre": 0.95,
        "Ancoats": 0.7,
        "Piccadilly": 0.9,
        "Deansgate": 0.85,
        "Media City": 0.7,
        "Oxford Road": 0.9,
        "Spinningfields": 0.8
    }
    
    # Time-based factor - traffic peaks at rush hour
    if 7 <= hour <= 9 or 16 <= hour <= 18:  # Rush hours
        time_factor = 1.0
    elif 10 <= hour <= 15:  # Midday
        time_factor = 0.6
    elif hour < 6 or hour > 20:  # Early morning/late night
        time_factor = 0.3
    else:
        time_factor = 0.7
    
    # Day type factor
    if day_type == "Weekend":
        day_factor = 0.7  # Less traffic on weekends
    else:
        day_factor = 1.0  # Full traffic on weekdays
    
    # Calculate density with some randomness
    base_density = area_factor.get(area, 0.7) * time_factor * day_factor
    density = min(1.0, max(0.1, base_density + random.uniform(-0.1, 0.1)))
    
    return round(density * 100)

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
    
    # Update the layout - make it mobile-friendly
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=13
        ),
        margin=dict(l=0, r=0, t=10, b=0),  # Reduced top margin
        height=400,  # Slightly shorter for mobile
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
st.markdown("""
<div class="home-button">
    <form action="" method="get">
        <button type="submit">🏠 HOME</button>
    </form>
</div>
""", unsafe_allow_html=True)

# Handle home button click
if st.button("🏠", key="home_button_invisible", help="Go to home page"):
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

# Mobile-friendly notice 
st.markdown("""
<div style="background-color:#FFF1E6; padding:10px; border-radius:5px; margin-bottom:20px; text-align:center;">
    <h4 style="margin:0; color:#FF7E33;">📱 Optimized for mobile devices</h4>
    <p style="margin:5px 0;">Tap the top-left button to access settings</p>
</div>
""", unsafe_allow_html=True)

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
    # Welcome page - optimized for mobile
    st.title("beem.", anchor=False)
    
    # Banner with instructions
    st.error("## 👆 PRESS TOP LEFT MENU FIRST")
    
    st.header("🚲 Billboard Route Optimizer")
    
    # Help box - made more concise for mobile
    st.info("""
    **HOW TO USE:**
    1. Tap top left ≡ icon to open menu
    2. Select your area and day type
    3. Tap "ANALYZE ROUTE" button
    """)
    
    # App description - shortened
    st.markdown("""
    ### Optimize your mobile billboard routes
    Find the best times and locations for maximum engagement 📍
    """)
    
    # Direct analyze button - bigger for mobile
    st.markdown("""
    <div style="padding:20px 0;">
        <p style="text-align:center; font-weight:bold; margin-bottom:10px;">👇 OR START DIRECTLY 👇</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 ANALYZE NOW 🚀", type="primary", use_container_width=True):
        st.session_state.analyze = True
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:5px;">
    <p style="margin:0; color:#666;">beem. © 2025 Beem Mobile Billboard Solutions</p>
</div>
""", unsafe_allow_html=True)