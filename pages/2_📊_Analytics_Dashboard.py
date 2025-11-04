"""
Analytics Dashboard for Marketing Agencies and Event Promotion Companies
Provides deep insights into campaign performance and data analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# Import our modules
try:
    from backend.models import AreaDatabase, CampaignDatabase
    from backend.api_services import WeatherAPIService, TrafficAPIService
    from backend.business_logic import AdSuccessCalculator
    from frontend.styles import UNIVERSAL_CSS
    from frontend.components import UIComponents
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Import Stripe payment module
try:
    from backend.cookie_access import has_paid_cookie
    STRIPE_ENABLED = True
except ImportError:
    STRIPE_ENABLED = False
    has_paid_cookie = lambda: False

# Authentication check
def check_auth():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if STRIPE_ENABLED and has_paid_cookie():
        st.session_state.authenticated = True
    return st.session_state.authenticated or st.session_state.get('payment_completed', False)

def main():
    """Analytics Dashboard main page"""
    # Configure page
    st.set_page_config(
        page_title="Analytics Dashboard - BritMetrics",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Check authentication
    if not check_auth():
        st.error("🔒 Please authenticate on the Home page first")
        st.info("Go to the Home page to access BritMetrics")
        return
    
    # Apply CSS
    st.markdown(UNIVERSAL_CSS, unsafe_allow_html=True)
    
    # Header - pass True to indicate this is Analytics Dashboard page
    UIComponents.render_personalized_header(is_analytics_page=True)
    
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h1 style='color: #0078FF; font-size: clamp(1.5rem, 4vw, 2.5rem); margin-bottom: 0.5rem;'>📊 Analytics Dashboard</h1>
        <p style='color: #666; font-size: clamp(0.9rem, 2vw, 1.2rem);'>Deep insights for marketing agencies and event promotion companies</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Mobile-friendly styles
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .main-content { padding: 0.5rem; }
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.3rem !important; }
        h3 { font-size: 1.1rem !important; }
        h4 { font-size: 1rem !important; }
        .stMetric { font-size: 0.9rem; }
        .stDataFrame { font-size: 0.8rem; }
        /* Make charts responsive */
        .js-plotly-plot { width: 100% !important; }
        /* Stack columns on mobile */
        [data-testid="column"] { width: 100% !important; }
    }
    /* Hide sidebar on mobile, show as top menu */
    @media (max-width: 768px) {
        [data-testid="stSidebar"] {
            display: none;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Mobile-friendly navigation: selectbox works better on mobile than sidebar
    st.markdown("---")
    analytics_tab = st.selectbox(
        "📊 Choose Analytics View:",
        ["Demographic Insights", "ROI Calculator"],
        key="analytics_nav",
        label_visibility="visible"
    )
    
    # Initialize predictor
    if 'predictor' not in st.session_state:
        from backend.models import AreaDatabase, CampaignDatabase
        from backend.api_services import WeatherAPIService, TrafficAPIService
        
        class AdSuccessPredictor:
            """Main predictor class using organized structure"""
            def __init__(self):
                self.weather_service = WeatherAPIService()
                self.traffic_service = TrafficAPIService()
                self.manchester_areas = AreaDatabase.MANCHESTER_AREAS
                self.london_areas = AreaDatabase.LONDON_AREAS
            
            def predict_success(self, city_name: str, area_name: str, campaign_type=None) -> dict:
                """Predict ad success for a given area with optional campaign personalization"""
                if city_name == "Manchester":
                    area_data = self.manchester_areas[area_name]
                else:
                    area_data = self.london_areas[area_name]
                
                weather_data = self.weather_service.get_weather_data(
                    area_data.center.lat, area_data.center.lon
                )
                traffic_data = self.traffic_service.get_traffic_data(
                    area_data.center.lat, area_data.center.lon
                )
                
                result = AdSuccessCalculator.calculate_ad_success_score(
                    area_name, area_data, weather_data, traffic_data, campaign=campaign_type
                )
                
                return {
                    'result': result,
                    'weather_data': weather_data,
                    'traffic_data': traffic_data,
                    'area_data': area_data
                }
        
        st.session_state.predictor = AdSuccessPredictor()
    
    predictor = st.session_state.predictor
    
    # Main content based on selected tab
    if analytics_tab == "Demographic Insights":
        render_demographic_insights(predictor)
    elif analytics_tab == "ROI Calculator":
        render_roi_calculator(predictor)
    
    # Footer
    UIComponents.render_footer_personalized()




def render_demographic_insights(predictor):
    """Demographic insights and audience analysis"""
    st.markdown("### 👥 Demographic Insights & Audience Analysis")
    
    st.info("""
    **Analyze audience demographics across locations to find the best fit for your campaign.**
    This tool helps you understand where your target audience is most concentrated.
    """)
    
    # Campaign selection
    campaign_name = st.selectbox(
        "Select Campaign Type:",
        list(CampaignDatabase.CAMPAIGNS.keys()),
        key="demo_campaign"
    )
    
    campaign = CampaignDatabase.CAMPAIGNS[campaign_name]
    
    # Get all areas
    all_areas = {**AreaDatabase.MANCHESTER_AREAS, **AreaDatabase.LONDON_AREAS}
    
    # Calculate match scores for all areas
    match_scores = []
    for area_name, area_data in all_areas.items():
        match = AdSuccessCalculator._calculate_audience_match(area_data.success_factors, campaign)
        
        # Count matching factors
        factors_dict = {
            'affluent_audience': area_data.success_factors.affluent_audience,
            'business_district': area_data.success_factors.business_district,
            'shopping_area': area_data.success_factors.shopping_area,
            'brand_conscious': area_data.success_factors.brand_conscious,
            'student_area': area_data.success_factors.student_area,
            'creative_area': area_data.success_factors.creative_area,
            'university_district': area_data.success_factors.university_district,
            'young_audience': area_data.success_factors.young_audience,
            'transport_hub': area_data.success_factors.transport_hub,
            'high_traffic': area_data.success_factors.high_traffic,
        }
        
        matching_factors = [f for f in campaign.ideal_factors if factors_dict.get(f, False)]
        
        match_scores.append({
            'Location': area_name,
            'City': 'Manchester' if area_name in AreaDatabase.MANCHESTER_AREAS else 'London',
            'Match Score %': match,
            'Matching Factors': len(matching_factors),
            'Total Factors': len(campaign.ideal_factors),
            'Factors List': ', '.join(matching_factors) if matching_factors else 'None',
            'Footfall Daily': area_data.footfall_daily
        })
    
    df = pd.DataFrame(match_scores)
    df = df.sort_values('Match Score %', ascending=False)
    
    # Top locations
    st.markdown(f"#### 🎯 Top Locations for {campaign.name}")
    top_locations = df.head(10)
    
    fig = px.bar(
        top_locations,
        x='Match Score %',
        y='Location',
        orientation='h',
        color='Match Score %',
        color_continuous_scale='RdYlGn',
        title=f'Top 10 Locations by Audience Match for {campaign.name}',
        hover_data=['Matching Factors', 'Footfall Daily']
    )
    fig.update_layout(height=400, font=dict(size=11))
    st.plotly_chart(fig, use_container_width=True)
    
    # City comparison - mobile optimized
    st.markdown("#### 🏙️ City Comparison")
    city_comparison = df.groupby('City').agg({
        'Match Score %': 'mean',
        'Footfall Daily': 'sum'
    }).reset_index()
    
    # Stack charts vertically on mobile
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            city_comparison,
            x='City',
            y='Match Score %',
            title='Avg Match by City',
            color='City',
            color_discrete_map={'Manchester': '#0078FF', 'London': '#FF6B6B'}
        )
        fig.update_layout(height=300, font=dict(size=12))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            city_comparison,
            x='City',
            y='Footfall Daily',
            title='Total Footfall by City',
            color='City',
            color_discrete_map={'Manchester': '#0078FF', 'London': '#FF6B6B'}
        )
        fig.update_layout(height=300, font=dict(size=12))
        st.plotly_chart(fig, use_container_width=True)
    
    # Full table
    st.markdown("#### 📋 All Locations Analysis")
    st.dataframe(df, use_container_width=True)


def render_roi_calculator(predictor):
    """ROI Calculator for campaign planning"""
    st.markdown("### 💰 Campaign ROI Calculator")
    
    st.info("""
    **Calculate the potential ROI of your billboard campaign based on location, audience match, and campaign costs.**
    """)
    
    # Mobile-friendly: stack inputs vertically on small screens
    campaign_name = st.selectbox(
        "Campaign Type:",
        list(CampaignDatabase.CAMPAIGNS.keys()),
        key="roi_campaign"
    )
    city = st.selectbox("City:", ["Manchester", "London"], key="roi_city")
    location = st.selectbox(
        "Location:",
        list(AreaDatabase.MANCHESTER_AREAS.keys() if city == "Manchester" else AreaDatabase.LONDON_AREAS.keys()),
        key="roi_location"
    )
    
    st.markdown("---")
    st.markdown("**Campaign Details:**")
    
    col1, col2 = st.columns(2)
    with col1:
        campaign_duration_days = st.number_input("Duration (days):", min_value=1, max_value=365, value=30, key="duration")
        daily_cost = st.number_input("Daily Cost (£):", min_value=0.0, value=500.0, step=50.0, key="daily_cost")
    with col2:
        conversion_rate = st.number_input("Conversion Rate (%):", min_value=0.0, max_value=100.0, value=2.0, step=0.1, key="conversion")
        avg_order_value = st.number_input("Avg Order Value (£):", min_value=0.0, value=50.0, step=10.0, key="aov")
    
    # Get prediction
    campaign = CampaignDatabase.CAMPAIGNS[campaign_name]
    prediction = predictor.predict_success(city, location, campaign)
    result = prediction['result']
    
    # Calculate metrics
    total_cost = daily_cost * campaign_duration_days
    impressions_per_day = result.impressions_per_hour * 24
    total_impressions = impressions_per_day * campaign_duration_days
    target_impressions = result.target_audience_size * 24 * campaign_duration_days
    
    # ROI calculations
    conversions = (target_impressions * conversion_rate / 100)
    revenue = conversions * avg_order_value
    profit = revenue - total_cost
    roi_percentage = (profit / total_cost * 100) if total_cost > 0 else 0
    cpm = (total_cost / total_impressions * 1000) if total_impressions > 0 else 0
    cpc = (total_cost / conversions) if conversions > 0 else 0
    
    # Display results - mobile optimized (2 columns on mobile, 4 on desktop)
    st.markdown("---")
    st.markdown("### 📊 ROI Analysis Results")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Cost", f"£{total_cost:,.2f}")
        st.metric("Expected Revenue", f"£{revenue:,.2f}")
        st.metric("CPM", f"£{cpm:.2f}")
    with col2:
        st.metric("Expected Profit", f"£{profit:,.2f}", delta=f"{roi_percentage:.1f}% ROI")
        st.metric("Conversions", f"{conversions:.0f}")
        st.metric("CPC", f"£{cpc:.2f}")
    
    st.metric("Target Audience Reach", f"{target_impressions:,.0f}")
    
    # Visualizations - stack on mobile
    col1, col2 = st.columns(2)
    
    with col1:
        # Cost breakdown
        fig = go.Figure(data=[
            go.Bar(name='Cost', x=['Campaign'], y=[total_cost], marker_color='red'),
            go.Bar(name='Revenue', x=['Campaign'], y=[revenue], marker_color='green'),
            go.Bar(name='Profit', x=['Campaign'], y=[profit], marker_color='blue')
        ])
        fig.update_layout(title='Cost vs Revenue', barmode='group', height=300, font=dict(size=11))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # ROI gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = roi_percentage,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "ROI %", 'font': {'size': 14}},
            delta = {'reference': 0},
            gauge = {
                'axis': {'range': [-100, 200]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [-100, 0], 'color': "lightgray"},
                    {'range': [0, 100], 'color': "lightgreen"},
                    {'range': [100, 200], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 0
                }
            }
        ))
        fig.update_layout(height=300, font=dict(size=11))
        st.plotly_chart(fig, use_container_width=True)
    
    # Campaign performance context - mobile optimized
    st.markdown("---")
    st.markdown("### 📈 Campaign Performance Context")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Success Score", f"{result.success_score}/100")
        st.metric("Impressions/Hour", f"{result.impressions_per_hour:,}")
    with col2:
        st.metric("Audience Match", f"{result.audience_match_score}%")
        st.metric("Target Audience/HR", f"{result.target_audience_size:,}")




if __name__ == "__main__":
    main()

