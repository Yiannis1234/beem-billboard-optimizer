"""
UI components for the Ad Success Predictor application.
Contains reusable Streamlit components.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any

# Import backend models - handle both relative and absolute imports
try:
    from ..backend.models import AdSuccessResult, AreaData, WeatherData, TrafficData
except ImportError:
    from backend.models import AdSuccessResult, AreaData, WeatherData, TrafficData


class UIComponents:
    """Reusable UI components for the application"""
    
    @staticmethod
    def render_header():
        """Render the main application header"""
        st.markdown('<h1 class="main-header">🎯 Ad Success Predictor — Manchester & London</h1>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <h3 style='color: var(--text-primary);'>Choose Manchester or London and get instant ad success predictions.</h3>
            <p style='color: var(--text-secondary);'>We analyze real traffic, audience and <strong>current weather</strong>. Separate buttons keep it crystal clear.</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_info_section():
        """Render the how it works information section"""
        st.info("""
        **💡 How it works:** 
        - Select any Manchester area from the dropdown
        - Click "Predict Ad Success" to get instant results
        - See your success score (0-100), how many people will see your ad, and why
        - Weather now visibly adjusts scores and impressions (e.g., rain reduces dwell time)
        - Compare all areas in the table below
        """)
    
    @staticmethod
    def render_city_selection() -> tuple:
        """Render city selection interface and return selected city data"""
        predictor = st.session_state.get('predictor')
        if not predictor:
            st.error("Predictor not initialized")
            return None
        
        left, right = st.columns(2)
        
        with left:
            m_area = st.selectbox("📍 Manchester Area", list(predictor.manchester_areas.keys()), index=0, help="Select a Manchester area")
            manchester_clicked = st.button("🔍 Predict Manchester", type="primary", use_container_width=True)
        
        with right:
            l_area = st.selectbox("📍 London Area", list(predictor.london_areas.keys()), index=0, help="Select a London area")
            london_clicked = st.button("🔍 Predict London", type="primary", use_container_width=True)
        
        if manchester_clicked:
            return ("Manchester", m_area, predictor.manchester_areas[m_area])
        elif london_clicked:
            return ("London", l_area, predictor.london_areas[l_area])
        
        return None
    
    @staticmethod
    def render_success_card(result: AdSuccessResult, area_name: str):
        """Render the main success card based on success level"""
        if result.success_level == "EXCELLENT":
            st.markdown(f"""
            <div class="success-card">
                <h2>🎉 EXCELLENT AD SUCCESS!</h2>
                <div class="metric-highlight">{result.success_score}/100</div>
                <h3>{area_name}</h3>
                <p>{result.description}</p>
            </div>
            """, unsafe_allow_html=True)
        elif result.success_level == "GOOD":
            st.markdown(f"""
            <div class="warning-card">
                <h2>👍 GOOD AD SUCCESS</h2>
                <div class="metric-highlight">{result.success_score}/100</div>
                <h3>{area_name}</h3>
                <p>{result.description}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="danger-card">
                <h2>⚠️ MODERATE AD SUCCESS</h2>
                <div class="metric-highlight">{result.success_score}/100</div>
                <h3>{area_name}</h3>
                <p>{result.description}</p>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_metrics(result: AdSuccessResult):
        """Render key metrics"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Ad Success Score", f"{result.success_score}/100", help="Higher score = Better ad success")
        
        with col2:
            delta_txt = f"{result.impression_pct_delta:+.0f}% from weather"
            st.metric("People See Ad/Hour", f"{result.impressions_per_hour:,}", delta=delta_txt, help="Weather now adjusts impressions")
        
        with col3:
            st.metric("Success Level", result.success_level, help="Overall success rating")
    
    @staticmethod
    def render_weather_traffic_data(weather_data: WeatherData, traffic_data: TrafficData, result: AdSuccessResult):
        """Render weather and traffic impact section"""
        st.subheader("🌦️ Weather & 🚦 Traffic Impact")
        
        # Weather metrics
        wcol1, wcol2, wcol3, wcol4 = st.columns(4)
        with wcol1:
            st.metric("Condition", weather_data.condition)
        with wcol2:
            st.metric("Temp (°C)", f"{weather_data.temperature:.0f}")
        with wcol3:
            st.metric("Visibility (km)", f"{weather_data.visibility}")
        with wcol4:
            st.metric("Wind (kph)", f"{weather_data.wind_kph:.0f}")
        
        # Weather and traffic effects
        tcol1, tcol2 = st.columns(2)
        with tcol1:
            w_delta = f"{result.weather_score_delta:+d} pts on score"
            st.info("**Weather effect**\n\n" + "\n".join([f"- {n}" for n in result.weather_notes[:3]]) + f"\n\n**Net:** {w_delta}")
        
        with tcol2:
            traffic_status = f"{traffic_data.congestion_color} {traffic_data.congestion_level}"
            st.info(f"**Traffic Status:** {traffic_status}\n\n"
                    f"- Current speed: {traffic_data.current_speed} km/h\n"
                    f"- Free-flow: {traffic_data.free_flow_speed} km/h\n"
                    f"- Traffic density: {traffic_data.traffic_density}%\n"
                    f"- Data source: {traffic_data.api_status}\n"
                    f"- Updated: {traffic_data.last_updated}")
    
    @staticmethod
    def render_success_reasons(result: AdSuccessResult):
        """Render success reasons"""
        st.subheader("🤔 Why This Area is Good for Ads:")
        for reason in result.key_reasons:
            st.markdown(f"""<div class="reason-box"><strong>{reason}</strong></div>""", unsafe_allow_html=True)
    
    @staticmethod
    def render_pro_tips(result: AdSuccessResult):
        """Render pro tips based on success level"""
        st.subheader("📈 What This Means for Your Ad:")
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"""
            **🎯 Expected Results:**
            - **{result.impressions_per_hour:,} people** will see your ad every hour
            - **Success rate:** {result.success_score}% chance of good performance
            - **Best time:** Peak hours (8-10am, 5-7pm)
            """)
        
        with col2:
            if result.success_score >= 75:
                st.info("""
                **💡 Pro Tips:**
                - This is an **excellent** location!
                - Consider premium ad placement
                - Run ads during peak hours
                - Monitor performance closely
                """)
            elif result.success_score >= 55:
                st.warning("""
                **💡 Pro Tips:**
                - This is a **good** location
                - Focus on peak traffic times
                - Consider A/B testing
                - Monitor competitor activity
                """)
            else:
                st.error("""
                **💡 Pro Tips:**
                - This area has **moderate** potential
                - Consider other locations first
                - If using this area, focus on weekends
                - Lower your ad spend expectations
                """)
    
    @staticmethod
    def render_comparison_table(city_name: str, results: List[AdSuccessResult]):
        """Render area comparison table"""
        st.subheader(f"📊 Quick Area Comparison — {city_name}")
        
        # Prepare data for table
        table_data = []
        for result in results:
            table_data.append({
                'Area': result.area_name,
                'Success Score': result.success_score,
                'Impressions/Hour': result.impressions_per_hour,
                'Level': result.success_level
            })
        
        df = pd.DataFrame(table_data).sort_values('Success Score', ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        return df
    
    @staticmethod
    def render_top_areas(df: pd.DataFrame):
        """Render top 3 areas"""
        st.subheader("🏆 Top 3 Best Areas for Ads:")
        top_3 = df.head(3)
        
        for i, (_, row) in enumerate(top_3.iterrows(), 1):
            if row['Level'] == 'EXCELLENT':
                color_class = 'success-card'
                emoji = '🥇'
            elif row['Level'] == 'GOOD':
                color_class = 'warning-card'
                emoji = '🥈'
            else:
                color_class = 'danger-card'
                emoji = '🥉'
            
            st.markdown(f"""
            <div class="{color_class}">
                <h3>{emoji} #{i} {row['Area']}</h3>
                <div class="metric-highlight">{row['Success Score']}/100</div>
                <p>{row['Impressions/Hour']:,} people see ads per hour</p>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_help_section():
        """Render help and understanding section"""
        st.markdown("---")
        st.markdown("### 📚 Understanding Your Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **🎯 Success Score (0-100):**
            - **90-100:** Exceptional location
            - **75-89:** Excellent location  
            - **55-74:** Good location
            - **35-54:** Moderate location
            - **0-34:** Poor location
            """)
        
        with col2:
            st.success("""
            **👥 Impressions/Hour:**
            - **3000+:** Very high visibility
            - **2000-2999:** High visibility
            - **1000-1999:** Good visibility
            - **500-999:** Moderate visibility
            - **<500:** Low visibility
            """)
        
        with col3:
            st.warning("""
            **⏰ Best Times to Advertise:**
            - **Morning:** 8:00-10:00 AM
            - **Lunch:** 12:00-2:00 PM
            - **Evening:** 5:00-7:00 PM
            - **Weekends:** Higher footfall
            """)
    
    @staticmethod
    def render_footer():
        """Render application footer"""
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: var(--text-secondary);'>
            <p><strong>🎯 Manchester Ad Success Predictor</strong> | 🏙️ Powered by Real-Time Data</p>
            <p>💡 Higher score = More successful ads | 📊 Based on traffic, audience, and <strong>live weather</strong></p>
            <p>🔄 Data updates every hour | ⚡ Instant predictions</p>
        </div>
        """, unsafe_allow_html=True)
