"""
Main application file for Ad Success Predictor.
Uses the organized backend and frontend structure.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import time

# Import our organized modules
try:
    from backend.models import AreaDatabase, CampaignDatabase
    from backend.api_services import WeatherAPIService, TrafficAPIService
    from backend.business_logic import AdSuccessCalculator
    from frontend.styles import UNIVERSAL_CSS
    from frontend.components import UIComponents
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Authentication system
ACCESS_CODE = "tatakas101"
PAYMENT_AMOUNT = 5.00  # £5
PAYMENT_DESCRIPTION = "BritMetrics Premium Access"

def check_authentication():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'payment_completed' not in st.session_state:
        st.session_state.payment_completed = False
    return st.session_state.authenticated or st.session_state.payment_completed

def render_login_page():
    """Render login/payment page"""
    st.markdown(UNIVERSAL_CSS, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; padding: 3rem;'>
        <h1 style='color: #0078FF; font-size: 3rem; margin-bottom: 1rem;'>🔒 BritMetrics</h1>
        <h2 style='color: #333; font-size: 2rem; margin-bottom: 2rem;'>Premium Access Required</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔑 Access Code")
        st.markdown("Enter the access code to unlock BritMetrics:")
        
        access_code = st.text_input("Access Code", type="password", placeholder="Enter code...")
        
        if st.button("🔓 Unlock with Code", type="primary", use_container_width=True):
            if access_code == ACCESS_CODE:
                st.session_state.authenticated = True
                st.success("✅ Access granted! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid access code")
    
    with col2:
        st.markdown("### 💳 Premium Access")
        st.markdown(f"**Get instant access for £{PAYMENT_AMOUNT}**")
        
        st.markdown("""
        **What you get:**
        - Full campaign optimization
        - Personalized recommendations
        - Real-time analytics
        - Priority support
        """)
        
        if st.button(f"💳 Pay £{PAYMENT_AMOUNT} for Access", type="secondary", use_container_width=True):
            # Simulate payment processing
            with st.spinner("Processing payment..."):
                time.sleep(2)
                st.session_state.payment_completed = True
                st.success("✅ Payment successful! Redirecting...")
                st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>🔐 Your data is secure and encrypted</p>
        <p>💡 Need help? Contact support</p>
    </div>
    """, unsafe_allow_html=True)


class AdSuccessPredictor:
    """Main predictor class using organized structure"""
    
    def __init__(self):
        self.weather_service = WeatherAPIService()
        self.traffic_service = TrafficAPIService()
        self.manchester_areas = AreaDatabase.MANCHESTER_AREAS
        self.london_areas = AreaDatabase.LONDON_AREAS
    
    def predict_success(self, city_name: str, area_name: str, campaign_type=None) -> dict:
        """Predict ad success for a given area with optional campaign personalization"""
        # Get area data
        if city_name == "Manchester":
            area_data = self.manchester_areas[area_name]
        else:
            area_data = self.london_areas[area_name]
        
        # Get external data
        weather_data = self.weather_service.get_weather_data(
            area_data.center.lat, area_data.center.lon
        )
        traffic_data = self.traffic_service.get_traffic_data(
            area_data.center.lat, area_data.center.lon
        )
        
        # Calculate success with campaign personalization
        result = AdSuccessCalculator.calculate_ad_success_score(
            area_name, area_data, weather_data, traffic_data, campaign=campaign_type
        )
        
        return {
            'result': result,
            'weather_data': weather_data,
            'traffic_data': traffic_data,
            'area_data': area_data
        }
    
    def get_all_predictions(self, city_name: str, campaign_type=None) -> list:
        """Get predictions for all areas in a city"""
        areas = self.manchester_areas if city_name == "Manchester" else self.london_areas
        results = []
        
        for area_name, area_data in areas.items():
            prediction = self.predict_success(city_name, area_name, campaign_type)
            results.append(prediction)
        
        return results


def main():
    """Main application function"""
    # Configure Streamlit
    st.set_page_config(
        page_title="BritMetrics - Billboard Intelligence Platform",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Check authentication first
    if not check_authentication():
        render_login_page()
        return
    
    # Apply universal CSS
    st.markdown(UNIVERSAL_CSS, unsafe_allow_html=True)
    
    # Initialize predictor
    if 'predictor' not in st.session_state:
        st.session_state.predictor = AdSuccessPredictor()
    
    predictor = st.session_state.predictor
    
    # Add logout button in top right
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.authenticated = False
            st.session_state.payment_completed = False
            st.rerun()
    
    # Render personalized header with logo
    UIComponents.render_personalized_header()
    
    # Campaign selection at the top
    st.markdown("### 🎨 Step 1: Select Your Campaign Type")
    campaign_names = ["None (Generic Analysis)"] + list(CampaignDatabase.CAMPAIGNS.keys())
    
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_campaign_name = st.selectbox(
            "What type of campaign are you running?",
            campaign_names,
            help="Select your brand/campaign type for personalized insights"
        )
    
    if selected_campaign_name != "None (Generic Analysis)":
        campaign = CampaignDatabase.CAMPAIGNS[selected_campaign_name]
        with col2:
            st.success(f"✅ Target: {', '.join(campaign.target_demographics[:2])}")
        
        st.info(f"""
        **💡 Personalized for {campaign.name}:**
        - We analyze audience match specifically for {', '.join(campaign.target_demographics[:2])}
        - Get creative recommendations based on current weather and area demographics
        - See which areas have the highest concentration of your target audience
        """)
    else:
        campaign = None
        st.info("""
        **💡 Select a campaign type above to unlock:**
        - Audience match scores for YOUR target demographic
        - Personalized creative recommendations
        - Tactical tips for maximizing campaign ROI
        """)
    
    st.markdown("---")
    st.markdown("### 📍 Step 2: Choose Your Location")
    
    # City and area selection
    selected_city = UIComponents.render_city_selection()
    
    if selected_city is not None:
        city_name, selected_area, area_data = selected_city
        
        # Get prediction with campaign personalization
        prediction = predictor.predict_success(city_name, selected_area, campaign)
        result = prediction['result']
        weather_data = prediction['weather_data']
        traffic_data = prediction['traffic_data']
        
        st.markdown("---")
        
        # Render personalized results
        if campaign:
            UIComponents.render_personalized_success_card(result, selected_area, campaign)
            UIComponents.render_personalized_metrics(result)
            UIComponents.render_personalized_tips(result)
            UIComponents.render_creative_recommendations(result)
        else:
            UIComponents.render_success_card(result, selected_area)
            UIComponents.render_metrics(result)
        
        UIComponents.render_weather_traffic_data(weather_data, traffic_data, result)
        UIComponents.render_success_reasons(result)
        
        # Comparison table with campaign context
        all_predictions = predictor.get_all_predictions(city_name, campaign)
        all_results = [p['result'] for p in all_predictions]
        df = UIComponents.render_comparison_table_personalized(city_name, all_results, campaign)
        UIComponents.render_top_areas_personalized(df, campaign)
    
    # Help and footer
    UIComponents.render_help_section_personalized()
    UIComponents.render_footer_personalized()


if __name__ == "__main__":
    main()
