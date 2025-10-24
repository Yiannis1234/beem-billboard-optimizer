"""
Main application file for Ad Success Predictor.
Uses the organized backend and frontend structure.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Import our organized modules
try:
    from backend.models import AreaDatabase
    from backend.api_services import WeatherAPIService, TrafficAPIService
    from backend.business_logic import AdSuccessCalculator
    from frontend.styles import UNIVERSAL_CSS
    from frontend.components import UIComponents
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()


class AdSuccessPredictor:
    """Main predictor class using organized structure"""
    
    def __init__(self):
        self.weather_service = WeatherAPIService()
        self.traffic_service = TrafficAPIService()
        self.manchester_areas = AreaDatabase.MANCHESTER_AREAS
        self.london_areas = AreaDatabase.LONDON_AREAS
    
    def predict_success(self, city_name: str, area_name: str) -> dict:
        """Predict ad success for a given area"""
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
        
        # Calculate success
        result = AdSuccessCalculator.calculate_ad_success_score(
            area_name, area_data, weather_data, traffic_data
        )
        
        return {
            'result': result,
            'weather_data': weather_data,
            'traffic_data': traffic_data,
            'area_data': area_data
        }
    
    def get_all_predictions(self, city_name: str) -> list:
        """Get predictions for all areas in a city"""
        areas = self.manchester_areas if city_name == "Manchester" else self.london_areas
        results = []
        
        for area_name, area_data in areas.items():
            prediction = self.predict_success(city_name, area_name)
            results.append(prediction)
        
        return results


def main():
    """Main application function"""
    # Configure Streamlit
    st.set_page_config(
        page_title="Ad Success Predictor (Manchester & London)",
        page_icon="🎯",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Apply universal CSS
    st.markdown(UNIVERSAL_CSS, unsafe_allow_html=True)
    
    # Initialize predictor
    if 'predictor' not in st.session_state:
        st.session_state.predictor = AdSuccessPredictor()
    
    predictor = st.session_state.predictor
    
    # Render UI
    UIComponents.render_header()
    UIComponents.render_info_section()
    
    # City selection
    selected_city = UIComponents.render_city_selection()
    
    if selected_city is not None:
        city_name, selected_area, area_data = selected_city
        
        # Get prediction
        prediction = predictor.predict_success(city_name, selected_area)
        result = prediction['result']
        weather_data = prediction['weather_data']
        traffic_data = prediction['traffic_data']
        
        st.markdown("---")
        
        # Render results
        UIComponents.render_success_card(result, selected_area)
        UIComponents.render_metrics(result)
        UIComponents.render_weather_traffic_data(weather_data, traffic_data, result)
        UIComponents.render_success_reasons(result)
        UIComponents.render_pro_tips(result)
        
        # Comparison table
        all_predictions = predictor.get_all_predictions(city_name)
        all_results = [p['result'] for p in all_predictions]
        df = UIComponents.render_comparison_table(city_name, all_results)
        UIComponents.render_top_areas(df)
    
    # Help and footer
    UIComponents.render_help_section()
    UIComponents.render_footer()


if __name__ == "__main__":
    main()
