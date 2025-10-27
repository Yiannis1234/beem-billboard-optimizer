"""
UI components for the Ad Success Predictor application.
Contains reusable Streamlit components.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any

# Import backend models - handle both relative and absolute imports
try:
    from ..backend.models import AdSuccessResult, AreaData, WeatherData, TrafficData, CampaignType
except ImportError:
    from backend.models import AdSuccessResult, AreaData, WeatherData, TrafficData, CampaignType


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
    
    # NEW PERSONALIZED CAMPAIGN UI METHODS
    
    @staticmethod
    def render_personalized_header():
        """Render personalized campaign header with logo"""
        st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem; padding: 2rem;'>
            <div style='background: #0078FF; padding: 2rem; border-radius: 15px;'>
                <!-- Logo next to title -->
                <div style='display: flex; align-items: center; justify-content: center; gap: 20px; flex-wrap: wrap;'>
                    <div style='width: 80px; height: 80px; background: url("./logo.png") center/contain no-repeat;'></div>
                    <div style='text-align: left;'>
                        <h1 style='color: #FFFFFF; font-size: 3.5rem; font-weight: 900; margin: 0; font-family: "Arial", sans-serif; letter-spacing: 3px;'>BRITMETRICS</h1>
                        <p style='color: #FFFFFF; font-size: 1.2rem; margin-top: 0.5rem; font-weight: 500;'>Billboard Intelligence Platform</p>
                    </div>
                </div>
                <p style='color: #FFFFFF; font-size: 0.95rem; margin-top: 1rem;'>Campaign-specific recommendations tailored to YOUR brand</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_info_section_personalized(campaign):
        """Render personalized how it works section"""
        if campaign:
            st.info(f"""
            **💡 Personalized for {campaign.name}:**
            - We analyze audience match specifically for {', '.join(campaign.target_demographics[:2])}
            - Get creative recommendations based on current weather and area demographics
            - See which areas have the highest concentration of your target audience
            - Receive tactical tips for maximizing campaign ROI
            """)
        else:
            st.info("""
            **💡 How it works:** 
            - Select your campaign type in the sidebar to get personalized insights
            - Choose Manchester or London and pick an area
            - Get audience match scores, creative recommendations, and tactical tips
            - Compare areas based on YOUR specific target audience
            """)
    
    @staticmethod
    def render_personalized_success_card(result: AdSuccessResult, area_name: str, campaign: CampaignType):
        """Render personalized success card with audience match"""
        match_score = result.audience_match_score
        overall_score = result.success_score
        
        # Card color and title based on OVERALL SCORE (not just match)
        if overall_score >= 80:
            card_class = "success-card"
            emoji = "🎉"
            title = "EXCELLENT FOR YOUR CAMPAIGN!"
        elif overall_score >= 65:
            card_class = "warning-card"
            emoji = "✅"
            title = "GOOD FOR YOUR CAMPAIGN"
        elif overall_score >= 50:
            card_class = "warning-card"
            emoji = "⚠️"
            title = "MODERATE FOR YOUR CAMPAIGN"
        else:
            card_class = "danger-card"
            emoji = "❌"
            title = "LOW SUCCESS FOR YOUR CAMPAIGN"
        
        # Add match context in subtitle
        if match_score >= 80:
            match_context = f"Perfect audience match ({match_score}%)"
        elif match_score >= 60:
            match_context = f"Strong audience match ({match_score}%)"
        elif match_score >= 40:
            match_context = f"Moderate audience match ({match_score}%)"
        else:
            match_context = f"Low audience match ({match_score}%)"
        
        st.markdown(f"""
        <div class="{card_class}">
            <h2>{emoji} {title}</h2>
            <div class="metric-highlight">{overall_score}/100</div>
            <h3>{area_name}</h3>
            <p style="font-size: 1.1rem; margin: 0.5rem 0;"><strong>{match_context}</strong></p>
            <p>{result.description}</p>
            <p style="margin-top: 1rem; opacity: 0.9;"><strong>Campaign:</strong> {campaign.name}</p>
            <p style="opacity: 0.9;"><strong>Target:</strong> {', '.join(campaign.target_demographics)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_personalized_metrics(result: AdSuccessResult):
        """Render personalized campaign metrics"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Calculate what the boost/penalty was
            if result.audience_match_score >= 80:
                score_indicator = "📈 Boosted by campaign match!"
            elif result.audience_match_score >= 60:
                score_indicator = "↗️ Slightly boosted"
            elif result.audience_match_score >= 40:
                score_indicator = "→ Neutral"
            else:
                score_indicator = "📉 Reduced by poor match"
            
            st.metric("Overall Score", f"{result.success_score}/100", 
                     help=f"Campaign-adjusted score. {score_indicator}")
        
        with col2:
            # Show the match with helpful context
            if result.audience_match_score >= 80:
                match_emoji = "🎯"
            elif result.audience_match_score >= 60:
                match_emoji = "✅"
            elif result.audience_match_score >= 40:
                match_emoji = "⚠️"
            else:
                match_emoji = "❌"
            
            st.metric(f"{match_emoji} Audience Match", f"{result.audience_match_score}%", 
                     help="How well this area matches your target demographics - this affects the Overall Score!")
        
        with col3:
            st.metric("Total Impressions/Hr", f"{result.impressions_per_hour:,}", 
                     help="Total people passing by per hour")
        
        with col4:
            st.metric("Target Audience/Hr", f"{result.target_audience_size:,}", 
                     help="YOUR target demographic per hour", delta=f"{result.audience_match_score}% of total")
    
    @staticmethod
    def render_personalized_tips(result: AdSuccessResult):
        """Render personalized campaign tips"""
        if result.personalized_tips:
            st.subheader("💡 Personalized Campaign Strategy")
            
            for tip in result.personalized_tips:
                st.markdown(f"""<div class="reason-box">{tip}</div>""", unsafe_allow_html=True)
    
    @staticmethod
    def render_creative_recommendations(result: AdSuccessResult):
        """Render creative recommendations"""
        if result.creative_recommendations:
            st.subheader("🎨 Creative & Design Recommendations")
            
            col1, col2 = st.columns(2)
            
            for i, rec in enumerate(result.creative_recommendations):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""<div class="reason-box">{rec}</div>""", unsafe_allow_html=True)
    
    @staticmethod
    def render_comparison_table_personalized(city_name: str, results: List[AdSuccessResult], campaign):
        """Render personalized area comparison table"""
        if campaign:
            st.subheader(f"📊 Area Ranking for {campaign.name} — {city_name}")
        else:
            st.subheader(f"📊 Quick Area Comparison — {city_name}")
        
        # Prepare data for table
        table_data = []
        for result in results:
            data = {
                'Area': result.area_name,
                'Overall Score': result.success_score,
                'Total Impressions/Hr': result.impressions_per_hour,
            }
            
            if campaign:
                data['Audience Match'] = f"{result.audience_match_score}%"
                data['Target Audience/Hr'] = result.target_audience_size
            
            data['Level'] = result.success_level
            table_data.append(data)
        
        # Sort by audience match if campaign selected, otherwise by overall score
        sort_by = 'Audience Match' if campaign else 'Overall Score'
        df = pd.DataFrame(table_data)
        
        if campaign:
            # Convert audience match to numeric for sorting
            df['_match_numeric'] = df['Audience Match'].str.rstrip('%').astype(int)
            df = df.sort_values('_match_numeric', ascending=False).drop('_match_numeric', axis=1)
        else:
            df = df.sort_values('Overall Score', ascending=False)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        return df
    
    @staticmethod
    def render_top_areas_personalized(df: pd.DataFrame, campaign):
        """Render top 3 areas with personalization context"""
        if campaign:
            st.subheader(f"🏆 Top 3 Areas for {campaign.name}:")
        else:
            st.subheader("🏆 Top 3 Best Areas for Ads:")
        
        top_3 = df.head(3)
        
        for i, (_, row) in enumerate(top_3.iterrows(), 1):
            if row['Level'] == 'EXCELLENT' or (campaign and int(str(row.get('Audience Match', '0%')).rstrip('%')) >= 80):
                color_class = 'success-card'
                emoji = '🥇'
            elif row['Level'] == 'GOOD' or (campaign and int(str(row.get('Audience Match', '0%')).rstrip('%')) >= 60):
                color_class = 'warning-card'
                emoji = '🥈'
            else:
                color_class = 'danger-card'
                emoji = '🥉'
            
            if campaign:
                st.markdown(f"""
                <div class="{color_class}">
                    <h3>{emoji} #{i} {row['Area']}</h3>
                    <div class="metric-highlight">{row['Audience Match']} Audience Match</div>
                    <p>{row['Target Audience/Hr']:,} target audience members per hour</p>
                    <p style="font-size: 0.9em; opacity: 0.8;">Overall Score: {row['Overall Score']}/100 | Total: {row['Total Impressions/Hr']:,}/hr</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="{color_class}">
                    <h3>{emoji} #{i} {row['Area']}</h3>
                    <div class="metric-highlight">{row['Overall Score']}/100</div>
                    <p>{row['Total Impressions/Hr']:,} people see ads per hour</p>
                </div>
                """, unsafe_allow_html=True)
    
    @staticmethod
    def render_help_section_personalized():
        """Render personalized help section"""
        st.markdown("---")
        st.markdown("### 📚 How Personalization Works")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **🎯 Audience Matching:**
            - We analyze each area's demographics
            - Match them to YOUR target audience
            - Higher match = more relevant viewers
            - Focus on quality over quantity
            """)
        
        with col2:
            st.success("""
            **🎨 Creative Recommendations:**
            - Weather-responsive suggestions
            - Area-specific design tips
            - Brand-aligned creative direction
            - Context-aware messaging
            """)
        
        with col3:
            st.warning("""
            **💡 Tactical Tips:**
            - Campaign-specific strategies
            - Timing recommendations
            - Budget optimization advice
            - ROI maximization tactics
            """)
    
    @staticmethod
    def render_footer_personalized():
        """Render personalized footer"""
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: var(--text-secondary); padding: 2rem 0;'>
            <h2 style='color: var(--primary-color); font-size: 1.8rem; margin-bottom: 0.5rem;'>📊 BritMetrics</h2>
            <p style='color: var(--text-primary); font-size: 1.1rem; margin-bottom: 1rem;'><strong>Billboard Intelligence Platform</strong></p>
            <p>💡 Go beyond generic analytics | 🎨 Campaign-specific insights | 📊 Match your exact target audience</p>
            <p>🔄 Real-time weather & traffic | ⚡ AI-powered recommendations | 🎯 Maximize campaign ROI</p>
            <p style='margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;'>Powered by Real-Time Data + AI | Manchester & London</p>
        </div>
        """, unsafe_allow_html=True)
