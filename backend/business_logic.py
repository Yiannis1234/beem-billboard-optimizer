"""
Business logic for ad success prediction.
Contains the core prediction algorithms and calculations.
"""

from typing import List, Tuple
from .models import AreaData, WeatherData, TrafficData, AdSuccessResult, SuccessFactors


class AdSuccessCalculator:
    """Core business logic for ad success prediction"""
    
    @staticmethod
    def calculate_ad_success_score(area_name: str, area_data: AreaData, 
                                 weather_data: WeatherData, traffic_data: TrafficData) -> AdSuccessResult:
        """Calculate realistic ad success score (0-100) with visible weather effects"""
        
        # Base score from footfall
        base_score = min(60, (area_data.footfall_daily / 10000))  # Max 60 from footfall
        
        # Factor boost from area characteristics
        factor_boost = AdSuccessCalculator._calculate_factor_boost(area_data.success_factors)
        
        # Weather adjustments
        weather_score_delta, impression_pct_delta, weather_notes = AdSuccessCalculator._weather_adjustments(weather_data)
        
        # Traffic boost
        traffic_boost = AdSuccessCalculator._calculate_traffic_boost(traffic_data)
        
        # Calculate final score
        raw_score = base_score + factor_boost + weather_score_delta + traffic_boost
        success_score = int(min(95, max(0, raw_score)))
        
        # Calculate impressions
        base_impressions_per_hour = int((area_data.footfall_daily / 24) * 0.15)
        adjusted_impressions_per_hour = int(base_impressions_per_hour * (1 + (impression_pct_delta / 100.0)))
        
        return AdSuccessResult(
            area_name=area_name,
            success_score=success_score,
            impressions_per_hour=max(0, adjusted_impressions_per_hour),
            success_level=AdSuccessCalculator.get_success_level(success_score),
            key_reasons=AdSuccessCalculator.get_success_reasons(area_data.success_factors, weather_data, traffic_data, weather_notes),
            description=area_data.description,
            weather_notes=weather_notes,
            weather_score_delta=weather_score_delta,
            impression_pct_delta=impression_pct_delta,
            base_impressions_per_hour=base_impressions_per_hour
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
