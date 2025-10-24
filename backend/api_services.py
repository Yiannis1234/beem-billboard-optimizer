"""
API services for external data sources.
Handles weather and traffic data retrieval.
"""

import requests
from datetime import datetime
from typing import Dict, Any
from .models import WeatherData, TrafficData


class WeatherAPIService:
    """Service for retrieving weather data from WeatherAPI.com"""
    
    def __init__(self, api_key: str = "f70bd534000447b2a14202431252303"):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1"
    
    def get_weather_data(self, lat: float, lon: float) -> WeatherData:
        """Get real weather data from WeatherAPI.com with fallback"""
        try:
            url = f"{self.base_url}/forecast.json?key={self.api_key}&q={lat},{lon}&days=1&aqi=no&alerts=no"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                current = data.get('current', {})
                condition = current.get('condition', {}) or {}
                
                return WeatherData(
                    temperature=current.get('temp_c', 12),
                    condition=condition.get('text', 'Partly Cloudy'),
                    visibility=current.get('vis_km', 10),
                    wind_kph=current.get('wind_kph', 8),
                    humidity=current.get('humidity', 70),
                    uv=current.get('uv', 2),
                    precip_mm=current.get('precip_mm', 0.0),
                    is_day=current.get('is_day', 1)
                )
            else:
                return self._get_fallback_weather_data()
                
        except Exception:
            return self._get_fallback_weather_data()
    
    def _get_fallback_weather_data(self) -> WeatherData:
        """Provide fallback weather data when API is unavailable"""
        return WeatherData(
            temperature=12,
            condition='Partly Cloudy',
            visibility=10,
            wind_kph=8,
            humidity=70,
            uv=2,
            precip_mm=0.0,
            is_day=1
        )


class TrafficAPIService:
    """Service for retrieving traffic data from TomTom API"""
    
    def __init__(self, api_key: str = "sljp3YAvFa7J3EalnGslYfnSCZg6VQUg"):
        self.api_key = api_key
        self.base_url = "https://api.tomtom.com/traffic/services/4"
    
    def get_traffic_data(self, lat: float, lon: float) -> TrafficData:
        """Get comprehensive traffic data from TomTom API with enhanced fallback"""
        try:
            url = f"{self.base_url}/flowSegmentData/absolute/10/json?point={lat},{lon}&key={self.api_key}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if we have valid flow data
                if 'flowSegmentData' in data and data['flowSegmentData']:
                    flow_data = data['flowSegmentData']
                    current_speed = flow_data.get('currentSpeed', 0)
                    free_flow_speed = flow_data.get('freeFlowSpeed', 50)
                    confidence = flow_data.get('confidence', 0)
                    
                    # Calculate congestion level with more granular levels
                    speed_ratio = current_speed / free_flow_speed if free_flow_speed > 0 else 0
                    
                    if speed_ratio >= 0.9:
                        congestion_level = 'Free Flow'
                        congestion_color = '🟢'
                    elif speed_ratio >= 0.7:
                        congestion_level = 'Light'
                        congestion_color = '🟡'
                    elif speed_ratio >= 0.5:
                        congestion_level = 'Moderate'
                        congestion_color = '🟠'
                    elif speed_ratio >= 0.3:
                        congestion_level = 'Heavy'
                        congestion_color = '🔴'
                    else:
                        congestion_level = 'Very Heavy'
                        congestion_color = '🛑'
                    
                    # Calculate additional metrics
                    delay_minutes = max(0, (free_flow_speed - current_speed) / 60 * 10)  # Rough delay estimate
                    traffic_density = min(100, (1 - speed_ratio) * 100)  # Density percentage
                    
                    return TrafficData(
                        current_speed=round(current_speed, 1),
                        free_flow_speed=round(free_flow_speed, 1),
                        congestion_level=congestion_level,
                        congestion_color=congestion_color,
                        speed_ratio=round(speed_ratio, 2),
                        confidence=confidence,
                        delay_minutes=round(delay_minutes, 1),
                        traffic_density=round(traffic_density, 1),
                        api_status='Live Data',
                        last_updated=datetime.now().strftime('%H:%M')
                    )
                else:
                    # No flow data available
                    return self._get_fallback_traffic_data("No traffic data available")
            else:
                # API error
                return self._get_fallback_traffic_data(f"API Error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            return self._get_fallback_traffic_data("Request timeout")
        except requests.exceptions.RequestException as e:
            return self._get_fallback_traffic_data(f"Network error: {str(e)[:50]}")
        except Exception as e:
            return self._get_fallback_traffic_data(f"Unexpected error: {str(e)[:50]}")
    
    def _get_fallback_traffic_data(self, reason: str) -> TrafficData:
        """Provide fallback traffic data when API is unavailable"""
        return TrafficData(
            current_speed=28.0,
            free_flow_speed=50.0,
            congestion_level='Light',
            congestion_color='🟡',
            speed_ratio=0.56,
            confidence=0,
            delay_minutes=3.7,
            traffic_density=44.0,
            api_status=f'Fallback ({reason})',
            last_updated=datetime.now().strftime('%H:%M')
        )
