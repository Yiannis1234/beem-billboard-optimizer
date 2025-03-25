import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, time

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
    div.stMarkdown {color: white;}
    h1, h2, h3, h4, h5, h6 {color: #FF8C00;}
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

# Sidebar for area selection
with st.sidebar:
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

# Main content
tabs = st.tabs(["📊 Route Analysis", "🗺️ Map & Visualization", "📈 Historical Data", "⏰ Best Times"])

# Tab 1: Route Analysis
with tabs[0]:
    # Area Information 
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <div style="font-size: 2rem; margin-right: 15px;">📍</div>
        <div>
            <h2 style="margin: 0; color: #FF8C00;">{selected_area} Analysis</h2>
            <p style="margin: 5px 0 0 0; color: #FFFFFF;">Select an area and time, then click "Analyze Route" to see detailed insights.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if analyze_button:
        with st.spinner("Analyzing route data..."):
            # Simulate processing
            progress_bar = st.progress(0)
            for i in range(100):
                # Update progress bar
                progress_bar.progress(i + 1)
                time.sleep(0.01)
                
            st.success("Analysis complete!")
            
            # Display some sample metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Weather", "Sunny", "Favorable")
            with col2:
                st.metric("Foot Traffic", "High", "+12%")
            with col3:
                st.metric("Engagement Score", "85%", "+5%")
            
            # Sample recommendation
            st.info("**Recommendation:** Current conditions are optimal for billboard display in this area.")
    else:
        # Show placeholder when no analysis has been run
        st.markdown("""
        <div style="background-color: #333333; padding: 20px; border-radius: 10px; color: white; text-align: center;">
            <h3 style="margin-top: 0;">👆 Select an area and time, then click "Analyze Route" in the sidebar</h3>
            <p>You'll receive detailed insights on the best times and locations for your mobile billboard campaign.</p>
        </div>
        """, unsafe_allow_html=True)

# Tab 2: Map & Visualization
with tabs[1]:
    st.markdown("""
    <div style="background-color: #333333; padding: 20px; border-radius: 10px; color: white; text-align: center;">
        <h3 style="margin-top: 0;">🗺️ Interactive Map & Route Visualization</h3>
        <p>Select an area and analyze a route to see interactive maps and visualizations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display a sample map for demonstration
    if analyze_button:
        # Create a sample map centered on Manchester
        map_data = pd.DataFrame({
            'lat': [53.4808],
            'lon': [-2.2426]
        })
        st.map(map_data, zoom=13)

# Tab 3: Historical Data
with tabs[2]:
    st.markdown("""
    <div style="background-color: #333333; padding: 20px; border-radius: 10px; color: white; text-align: center;">
        <h3 style="margin-top: 0;">📈 Historical Engagement Data</h3>
        <p>Select an area and analyze a route to see historical data and trends.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display a sample chart for demonstration
    if analyze_button:
        # Create sample data
        chart_data = pd.DataFrame(
            np.random.randn(7, 3),
            columns=['Engagement', 'Foot Traffic', 'Weather Score']
        )
        st.line_chart(chart_data)

# Tab 4: Best Times
with tabs[3]:
    st.markdown("""
    <div style="background-color: #333333; padding: 20px; border-radius: 10px; color: white; text-align: center;">
        <h3 style="margin-top: 0;">⏰ Best Times to Display</h3>
        <p>Select an area and analyze a route to see the optimal display times.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display sample best times for demonstration
    if analyze_button:
        st.markdown("""
        <div style="background-color: #222222; padding: 15px; border-radius: 10px; margin-top: 20px; color: white;">
            <h4 style="margin-top: 0; color: #FF8C00;">Top Recommended Times:</h4>
            <ul>
                <li><strong>Friday at 5:00 PM</strong> - After-work crowds create high visibility opportunities</li>
                <li><strong>Saturday at 2:00 PM</strong> - Peak shopping hours with high pedestrian traffic</li>
                <li><strong>Sunday at 12:00 PM</strong> - Weekend lunch crowds in restaurant areas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="margin-top: 3rem; padding-top: 1.5rem; padding-bottom: 1.5rem; border-top: 1px solid #444444; 
            font-size: 0.85rem; color: #FFFFFF; text-align: center; background-color: #222222; border-radius: 0.5rem;">
    © 2025 Beem Mobile Billboard Solutions | This is a simplified version of the app with fixed indentation.
</div>
""", unsafe_allow_html=True)