"""
Main application file for Ad Success Predictor.
Uses the organized backend and frontend structure.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Import our organized modules
try:
    from backend.models import AreaDatabase, CampaignDatabase
    from backend.api_services import WeatherAPIService, TrafficAPIService, GooglePlacesService, EventbriteService
    from backend.business_logic import AdSuccessCalculator
    from frontend.styles import UNIVERSAL_CSS
    from frontend.components import UIComponents
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Import Stripe payment module
try:
    from backend.stripe_payment import render_stripe_payment_button, check_payment_status
    from backend.cookie_access import has_paid_cookie, save_access_to_cookie
    STRIPE_ENABLED = True
except ImportError:
    STRIPE_ENABLED = False
    has_paid_cookie = lambda: False
    save_access_to_cookie = lambda x: None

# Authentication system
ACCESS_CODE = "9797"
PAYMENT_AMOUNT = 5.00

def check_authentication():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'payment_completed' not in st.session_state:
        st.session_state.payment_completed = False
    
    # Check if user has paid via cookie
    if STRIPE_ENABLED and has_paid_cookie():
        st.session_state.payment_completed = True
        st.session_state.authenticated = True
        return True
    
    # Check payment status if Stripe is enabled
    if STRIPE_ENABLED:
        # This will check and save email automatically
        if check_payment_status():
            st.session_state.payment_completed = True
            st.session_state.authenticated = True
            return True
    
    return st.session_state.authenticated or st.session_state.payment_completed

def render_login_page():
    """Render login/payment page"""
    st.markdown(UNIVERSAL_CSS, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; padding: 3rem;'>
        <h1 style='color: #0078FF; font-size: 3rem; margin-bottom: 1rem;'>🔒 BritMetrics</h1>
        <h2 style='color: #333; font-size: 2rem; margin-bottom: 2rem;'>Access Required</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Free temporary access button
    col0 = st.columns(1)[0]
    with col0:
        st.markdown("### 🎁 Try Free (Limited Time)")
        st.markdown("Get temporary free access to explore BritMetrics:")
        
        if st.button("🚀 Start Free Trial", type="primary", use_container_width=True):
            st.session_state.authenticated = True
            st.success("✅ Free access granted! Enjoy...")
            st.rerun()
    
    st.markdown("---")
    
    # Check if returning paid customer
    with st.form("paid_customer_login"):
        st.markdown("### 💳 Returning Customer")
        st.markdown("Enter your email to access your account:")
        
        email = st.text_input("Email Address", placeholder="your-email@example.com")
        
        if st.form_submit_button("🔓 Login", type="primary", use_container_width=True):
            if email and has_paid_cookie():
                from backend.cookie_access import is_customer_paid
                if is_customer_paid(email):
                    st.session_state.authenticated = True
                    st.session_state.payment_completed = True
                    st.success("✅ Welcome back! Redirecting...")
                    st.rerun()
                else:
                    st.warning(f"❌ Email {email} is not registered. Please purchase access below.")
            else:
                st.error("❌ Please enter a valid email")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔑 Access Code")
        st.markdown("Enter the access code to unlock BritMetrics:")
        
        access_code = st.text_input("Access Code", type="password", placeholder="Enter code...", key="access_code_input")
        
        if st.button("🔓 Unlock with Code", type="primary", use_container_width=True, key="unlock_button"):
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
        - Instant access
        """)
        
        if STRIPE_ENABLED:
            render_stripe_payment_button(PAYMENT_AMOUNT, "BritMetrics Premium Access")
        else:
            st.warning("⚠️ Stripe not configured. Contact admin for access code.")
            if st.button("🔑 Get Access Code", type="secondary"):
                st.info(f"💡 Access code: **{ACCESS_CODE}**")
    
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
        self.places_service = GooglePlacesService()
        self.events_service = EventbriteService()
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
        
        # Get Google Places data (footfall/popularity indicators)
        places_data = self.places_service.get_places_data(
            area_name, area_data.center.lat, area_data.center.lon
        )
        
        # Get Eventbrite events data (upcoming events in the area)
        events_data = self.events_service.get_events_near_location(
            area_name, area_data.center.lat, area_data.center.lon
        )
        
        # Calculate success with campaign personalization
        result = AdSuccessCalculator.calculate_ad_success_score(
            area_name, area_data, weather_data, traffic_data, campaign=campaign_type, places_data=places_data
        )
        
        return {
            'result': result,
            'weather_data': weather_data,
            'traffic_data': traffic_data,
            'places_data': places_data,
            'events_data': events_data,
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
        
        UIComponents.render_weather_traffic_data(weather_data, traffic_data, result, prediction.get('places_data'))
        UIComponents.render_events_data(prediction.get('events_data'))
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
