"""
Business logic for ad success prediction.
Contains the core prediction algorithms and calculations.
"""

from typing import List, Tuple, Optional
from .models import AreaData, WeatherData, TrafficData, AdSuccessResult, SuccessFactors, CampaignType


class AdSuccessCalculator:
    """Core business logic for ad success prediction"""
    
    @staticmethod
    def calculate_ad_success_score(area_name: str, area_data: AreaData, 
                                 weather_data: WeatherData, traffic_data: TrafficData,
                                 campaign: Optional[CampaignType] = None) -> AdSuccessResult:
        """Calculate realistic ad success score (0-100) with personalized campaign matching"""
        
        # Base score from footfall
        base_score = min(60, (area_data.footfall_daily / 10000))  # Max 60 from footfall
        
        # Factor boost from area characteristics
        factor_boost = AdSuccessCalculator._calculate_factor_boost(area_data.success_factors)
        
        # Weather adjustments
        weather_score_delta, impression_pct_delta, weather_notes = AdSuccessCalculator._weather_adjustments(weather_data)
        
        # Traffic boost
        traffic_boost = AdSuccessCalculator._calculate_traffic_boost(traffic_data)
        
        # Calculate base success score (without campaign matching)
        raw_score = base_score + factor_boost + weather_score_delta + traffic_boost
        base_success_score = int(min(95, max(0, raw_score)))
        
        # Calculate impressions
        base_impressions_per_hour = int((area_data.footfall_daily / 24) * 0.15)
        adjusted_impressions_per_hour = int(base_impressions_per_hour * (1 + (impression_pct_delta / 100.0)))
        
        # NEW: Campaign-specific personalization
        audience_match_score = 0
        personalized_tips = []
        creative_recommendations = []
        target_audience_size = adjusted_impressions_per_hour
        final_success_score = base_success_score
        
        if campaign:
            # Calculate audience match
            audience_match_score = AdSuccessCalculator._calculate_audience_match(
                area_data.success_factors, campaign
            )
            
            # BOOST THE SUCCESS SCORE based on audience match!
            # High match = higher score, low match = lower score
            match_multiplier = audience_match_score / 100.0
            
            # Apply campaign relevance boost/penalty to the success score
            # Perfect match (100%) can add up to +15 points
            # Poor match (30%) can reduce by -10 points
            if match_multiplier >= 0.8:  # 80%+ match
                campaign_boost = int((match_multiplier - 0.5) * 30)  # +9 to +15 points
            elif match_multiplier >= 0.6:  # 60-79% match
                campaign_boost = int((match_multiplier - 0.5) * 20)  # +2 to +9 points
            elif match_multiplier >= 0.4:  # 40-59% match
                campaign_boost = 0  # Neutral
            else:  # <40% match
                campaign_boost = int((match_multiplier - 0.5) * 20)  # -2 to -10 points
            
            final_success_score = int(min(98, max(25, base_success_score + campaign_boost)))
            
            # Adjust target audience size based on match
            target_audience_size = int(adjusted_impressions_per_hour * match_multiplier)
            
            # Generate personalized tips
            personalized_tips = AdSuccessCalculator._generate_personalized_tips(
                campaign, area_data, weather_data, audience_match_score
            )
            
            # Generate creative recommendations
            creative_recommendations = AdSuccessCalculator._generate_creative_recommendations(
                campaign, weather_data, area_data
            )
        
        return AdSuccessResult(
            area_name=area_name,
            success_score=final_success_score,
            impressions_per_hour=max(0, adjusted_impressions_per_hour),
            success_level=AdSuccessCalculator.get_success_level(final_success_score),
            key_reasons=AdSuccessCalculator.get_success_reasons(area_data.success_factors, weather_data, traffic_data, weather_notes),
            description=area_data.description,
            weather_notes=weather_notes,
            weather_score_delta=weather_score_delta,
            impression_pct_delta=impression_pct_delta,
            base_impressions_per_hour=base_impressions_per_hour,
            audience_match_score=audience_match_score,
            personalized_tips=personalized_tips,
            creative_recommendations=creative_recommendations,
            target_audience_size=target_audience_size
        )
    
    @staticmethod
    def _calculate_factor_boost(factors: SuccessFactors) -> int:
        """Calculate boost from area success factors"""
        boost = 0
        if factors.high_traffic: boost += 15
        if factors.business_district: boost += 12
        if factors.transport_hub: boost += 12
        if factors.affluent_audience: boost += 8
        if factors.student_area: boost += 8
        if factors.shopping_area: boost += 8
        if factors.creative_area: boost += 5
        return boost
    
    @staticmethod
    def _calculate_traffic_boost(traffic_data: TrafficData) -> int:
        """Calculate boost from traffic conditions"""
        if traffic_data.congestion_level == 'Heavy':
            return 8
        elif traffic_data.congestion_level == 'Moderate':
            return 5
        return 0
    
    @staticmethod
    def _weather_adjustments(weather: WeatherData) -> Tuple[int, float, List[str]]:
        """Derive score and impression adjustments from detailed weather"""
        condition = (weather.condition or '').lower()
        temp = weather.temperature
        vis = weather.visibility
        wind = weather.wind_kph
        precip = weather.precip_mm
        uv = weather.uv
        
        score_delta = 0
        impression_pct = 0  # percent change
        notes = []
        
        # Visibility impact
        if vis >= 9:
            score_delta += 4
            notes.append("☀️ Very clear visibility = creative pops")
        elif vis >= 6:
            score_delta += 2
            notes.append("⛅ Good visibility")
        elif vis >= 3:
            score_delta -= 3
            impression_pct -= 5
            notes.append("🌫️ Low visibility reduces readability")
        else:
            score_delta -= 6
            impression_pct -= 10
            notes.append("🌁 Very poor visibility significantly hurts viewing")
        
        # Precipitation / condition impact
        raining = "rain" in condition or precip >= 0.5
        snowing = "snow" in condition
        storm = "storm" in condition or "thunder" in condition
        
        if storm:
            score_delta -= 6
            impression_pct -= 12
            notes.append("⛈️ Storms: people rush / hide indoors")
        elif snowing:
            score_delta -= 5
            impression_pct -= 10
            notes.append("❄️ Snow: travel disruption reduces exposure")
        elif raining:
            score_delta -= 3
            impression_pct -= 6
            notes.append("🌧️ Rain: shorter dwell time outdoors")
        elif "sunny" in condition or "clear" in condition:
            score_delta += 3
            impression_pct += 4
            notes.append("🌞 Sunny: higher dwell time and mood boost")
        
        # Wind impact
        if wind >= 40:
            score_delta -= 4
            notes.append("🌬️ Strong wind: people move quickly")
        elif wind <= 10:
            score_delta += 1
            notes.append("🍃 Calm wind: comfortable dwell time")
        
        # Temperature comfort band
        if 12 <= temp <= 22:
            score_delta += 3
            impression_pct += 3
            notes.append("🌡️ Comfortable temperature increases linger time")
        elif temp < 3:
            score_delta -= 4
            impression_pct -= 8
            notes.append("🥶 Very cold: people minimize time outside")
        elif temp > 28:
            score_delta -= 2
            impression_pct -= 4
            notes.append("🥵 Hot: shade-seeking reduces ad viewing angles")
        
        # UV (daytime readability for non-backlit prints)
        if uv >= 7:
            score_delta -= 1
            notes.append("🕶️ High UV/glare may reduce print readability")
        
        return score_delta, impression_pct, notes
    
    @staticmethod
    def get_success_level(score: int) -> str:
        """Get success level based on score"""
        if score >= 75:
            return "EXCELLENT"
        elif score >= 55:
            return "GOOD"
        elif score >= 35:
            return "MODERATE"
        else:
            return "POOR"
    
    @staticmethod
    def get_success_reasons(factors: SuccessFactors, weather_data: WeatherData, 
                          traffic_data: TrafficData, weather_notes: List[str]) -> List[str]:
        """Get key reasons for success"""
        reasons = []
        
        if factors.high_traffic:
            reasons.append("🚶 High foot traffic = More people see your ad")
        if factors.business_district:
            reasons.append("🏢 Business area = Professional audience with money")
        if factors.transport_hub:
            reasons.append("🚉 Transport hub = People wait here = More ad time")
        if factors.affluent_audience:
            reasons.append("💰 Affluent area = People with money to spend")
        if factors.student_area:
            reasons.append("🎓 Student area = Young, engaged audience")
        if factors.shopping_area:
            reasons.append("🛍️ Shopping area = People in buying mood")
        if factors.creative_area:
            reasons.append("🎨 Creative area = Brand-conscious audience")
        
        if weather_notes:
            reasons.append(weather_notes[0])
        if traffic_data.congestion_level in ['Heavy', 'Moderate']:
            reasons.append("🚦 Traffic congestion = People stuck = More ad views")
        
        return reasons[:3]
    
    @staticmethod
    def _calculate_audience_match(factors: SuccessFactors, campaign: CampaignType) -> int:
        """Calculate how well the area audience matches the campaign's target demographics"""
        
        if not campaign or len(campaign.ideal_factors) == 0:
            return 50  # Default match if no campaign selected
        
        # Build factors dictionary from actual area data
        factors_dict = {
            'affluent_audience': factors.affluent_audience,
            'business_district': factors.business_district,
            'shopping_area': factors.shopping_area,
            'brand_conscious': factors.brand_conscious,
            'student_area': factors.student_area,
            'creative_area': factors.creative_area,
            'university_district': factors.university_district,
            'young_audience': factors.young_audience,
            'transport_hub': factors.transport_hub,
            'high_traffic': factors.high_traffic,
            'commuter_area': factors.commuter_area,
            'nightlife': factors.nightlife,
            'tourist_area': factors.tourist_area,
            'leisure_time': factors.leisure_time,
            'local_community': factors.local_community,
            'family_area': factors.family_area,
            'local_businesses': factors.local_businesses,
            'affluent_suburb': factors.affluent_suburb,
            'corporate_area': factors.corporate_area,
            'trendy_audience': factors.trendy_audience,
        }
        
        # Smart matching - some factors imply others
        matches = 0
        partial_matches = 0
        
        for ideal_factor in campaign.ideal_factors:
            # Direct match
            if factors_dict.get(ideal_factor, False):
                matches += 1
            # Smart partial matches (related factors)
            elif ideal_factor == 'brand_conscious':
                if factors.affluent_audience or factors.shopping_area or factors.creative_area:
                    partial_matches += 0.5
            elif ideal_factor == 'shopping_area':
                if factors.affluent_audience or factors.leisure_time:
                    partial_matches += 0.3
            elif ideal_factor == 'young_audience':
                if factors.student_area or factors.university_district or factors.nightlife:
                    partial_matches += 0.5
            elif ideal_factor == 'affluent_audience':
                if factors.business_district or factors.shopping_area or factors.affluent_suburb:
                    partial_matches += 0.5
            elif ideal_factor == 'creative_area':
                if factors.trendy_audience or factors.young_audience:
                    partial_matches += 0.3
        
        # Calculate score including partial matches
        total_matches = matches + partial_matches
        total_possible = len(campaign.ideal_factors)
        match_score = int((total_matches / total_possible) * 100)
        
        # Ensure reasonable range (30-100 instead of 20-100 for better differentiation)
        return max(30, min(100, match_score))
    
    @staticmethod
    def _generate_personalized_tips(campaign: CampaignType, area_data: AreaData, 
                                    weather_data: WeatherData, match_score: int) -> List[str]:
        """Generate personalized campaign tips based on brand type and context"""
        tips = []
        
        # Match-based tips
        if match_score >= 80:
            tips.append(f"🎯 **Perfect Audience Match ({match_score}%)**: This area is ideal for {campaign.name} campaigns")
        elif match_score >= 60:
            tips.append(f"✅ **Strong Audience Match ({match_score}%)**: Good fit for {campaign.name} - expect solid engagement")
        elif match_score >= 40:
            tips.append(f"⚠️ **Moderate Match ({match_score}%)**: Consider adjusting messaging for broader appeal")
        else:
            tips.append(f"❌ **Low Match ({match_score}%)**: This area may not align with your target demographics")
        
        # Demographics-specific tips
        demographics_str = ", ".join(campaign.target_demographics[:2])
        tips.append(f"👥 **Your Target**: {demographics_str} - tailor your message accordingly")
        
        # Weather-based creative tips
        condition = (weather_data.condition or '').lower()
        if "rain" in condition:
            tips.append("🌧️ **Weather Tip**: Use weather-responsive messaging like 'Rainy day deals' or comfort themes")
        elif "sunny" in condition or "clear" in condition:
            tips.append("☀️ **Weather Tip**: Leverage the good mood! Use bright, optimistic messaging")
        elif "cloud" in condition:
            tips.append("☁️ **Weather Tip**: Use cozy, indoor-focused messaging or contrast with vibrant colors")
        
        # Footfall timing tips
        if area_data.footfall_daily > 200000:
            tips.append("🚶 **High Traffic**: Consider rotating creative every few hours to avoid ad fatigue")
        
        # Context-specific tactical tips
        if area_data.success_factors.transport_hub:
            tips.append("🚉 **Transit Hub**: Use QR codes - people have time to scan while waiting")
        
        if area_data.success_factors.student_area:
            tips.append("🎓 **Student Area**: Mobile-first approach, social media integration, student discounts")
        
        if area_data.success_factors.affluent_audience:
            tips.append("💎 **Affluent Audience**: Premium positioning works - focus on quality and exclusivity")
        
        return tips[:5]  # Return top 5 most relevant tips
    
    @staticmethod
    def _generate_creative_recommendations(campaign: CampaignType, weather_data: WeatherData, 
                                          area_data: AreaData) -> List[str]:
        """Generate creative/design recommendations based on campaign type and context"""
        recommendations = []
        
        # Base creative style from campaign
        recommendations.append(f"🎨 **Creative Style**: {campaign.creative_style}")
        
        # Weather-responsive creative
        temp = weather_data.temperature
        condition = (weather_data.condition or '').lower()
        
        if temp > 25:
            recommendations.append("🌡️ **Heat-Responsive**: Use cooling colors (blues, whites), refreshment imagery")
        elif temp < 5:
            recommendations.append("🌡️ **Cold-Responsive**: Use warming colors (reds, oranges), comfort themes")
        
        if "rain" in condition:
            recommendations.append("☔ **Rain Creative**: Indoor activities, comfort products, or weather-proof features")
        elif "sunny" in condition:
            recommendations.append("☀️ **Sunny Creative**: Outdoor activities, vibrant energy, seasonal promotions")
        
        # Time-context recommendations
        if weather_data.visibility < 5:
            recommendations.append("👁️ **Low Visibility**: Use high-contrast, bold typography, fewer words")
        else:
            recommendations.append("👁️ **Clear Visibility**: Great conditions for detailed visuals and subtle branding")
        
        # Area-context recommendations
        if area_data.success_factors.business_district:
            recommendations.append("💼 **Business Area**: Professional tone, data-driven claims, LinkedIn-style copy")
        
        if area_data.success_factors.creative_area:
            recommendations.append("🎨 **Creative Area**: Take risks! Bold designs, unconventional layouts welcome here")
        
        if area_data.success_factors.student_area:
            recommendations.append("📱 **Student Area**: Memes, trends, social-first content, hashtag integration")
        
        if area_data.success_factors.family_area:
            recommendations.append("👨‍👩‍👧 **Family Area**: Family-friendly imagery, trust signals, community values")
        
        # Dynamic content suggestions
        if area_data.success_factors.transport_hub:
            recommendations.append("⏱️ **Dwell Time**: Include destination info or 'while you wait' value propositions")
        
        return recommendations[:6]  # Return top 6 recommendations
