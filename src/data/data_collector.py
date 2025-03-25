import pandas as pd
import requests
from datetime import datetime, timedelta
import json
import numpy as np

class BeemDataCollector:
    def __init__(self, config):
        self.config = config
        self.weather_api_key = config.get('weather_api_key')
        self.traffic_api_key = config.get('traffic_api_key')
        
    def get_weather_forecast(self, location):
        """
        Fetch weather forecast data for a given location
        """
        # Check if we have an actual API key
        if self.weather_api_key and self.weather_api_key != 'demo_key':
            try:
                # WeatherAPI.com endpoint
                url = f"http://api.weatherapi.com/v1/current.json?key={self.weather_api_key}&q={location}&aqi=no"
                
                print(f"Fetching weather data from: {url}")
                response = requests.get(url, timeout=10)
                
                if response.status_code != 200:
                    print(f"Weather API error: {response.status_code} - {response.text}")
                    raise Exception(f"Weather API returned status code {response.status_code}")
                
                data = response.json()
                
                # Extract the relevant data
                if 'current' in data:
                    current = data['current']
                    print(f"Weather data received: Temp={current.get('temp_c', 0)}°C, Condition={current.get('condition', {}).get('text', 'unknown')}")
                    return {
                        'temperature': current.get('temp_c', 0),
                        'precipitation': current.get('precip_mm', 0),
                        'wind_speed': current.get('wind_kph', 0),
                        'condition': current.get('condition', {}).get('text', 'unknown'),
                        'forecast': []
                    }
                else:
                    print(f"Unexpected API response format: {data}")
            except Exception as e:
                print(f"Error fetching weather data: {e}")
                # Fallback to simulated data if API call fails
        
        # Simulated weather data for demo or fallback
        print("Using simulated weather data (API key missing or API call failed)")
        return {
            'temperature': 12.0,  # Default to current Manchester temperature
            'precipitation': max(0, np.random.normal(0, 1)),
            'wind_speed': max(0, np.random.normal(10, 5)),
            'condition': 'partly cloudy',
            'forecast': []
        }

    def get_traffic_data(self, zone):
        """
        Fetch real-time traffic data for a given zone
        """
        # Check if we have an actual API key
        if self.traffic_api_key and self.traffic_api_key != 'demo_key':
            try:
                # TomTom Traffic Flow API
                lat = zone['latitude']
                lon = zone['longitude']
                url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key={self.traffic_api_key}"
                
                response = requests.get(url)
                data = response.json()
                
                # Extract relevant traffic data
                if 'flowSegmentData' in data:
                    flow_data = data['flowSegmentData']
                    
                    return {
                        'flow_speed': flow_data.get('currentSpeed', 40),
                        'free_flow_speed': flow_data.get('freeFlowSpeed', 50),
                        'congestion_level': min(1.0, max(0.0, 1 - (flow_data.get('currentSpeed', 40) / max(1, flow_data.get('freeFlowSpeed', 50)))))
                    }
            except Exception as e:
                print(f"Error fetching traffic data: {e}")
                # Fallback to simulated data if API call fails
        
        # Simulated traffic data for demo or fallback
        return {
            'flow_speed': 40 + np.random.normal(0, 10),
            'free_flow_speed': 50,
            'congestion_level': np.random.uniform(0.4, 0.8)
        }

    def get_historical_engagement(self, start_date, end_date):
        """
        Fetch historical engagement data from database
        """
        dates = pd.date_range(start=start_date, end=end_date, freq='H')
        
        data = []
        for date in dates:
            hour = date.hour
            is_weekend = date.weekday() >= 5
            
            # Simulate different engagement patterns
            base_engagement = 0.4
            
            # Time-based adjustments
            if hour in [8, 9, 17, 18, 19]:  # Rush hours
                base_engagement *= 1.5
            elif hour in [12, 13, 14]:  # Lunch hours
                base_engagement *= 1.3
            elif hour < 6 or hour > 22:  # Late night/early morning
                base_engagement *= 0.3
                
            # Weekend adjustments
            if is_weekend:
                if hour in [11, 12, 13, 14, 15]:  # Weekend afternoon
                    base_engagement *= 1.4
                else:
                    base_engagement *= 0.8
                    
            data.append({
                'timestamp': date,
                'engagement_rate': base_engagement + np.random.normal(0, 0.1),
                'impressions': int(base_engagement * 1000 + np.random.normal(0, 100)),
                'zone_id': 'sample_zone',
                'temperature': 20 + np.random.normal(0, 5),
                'precipitation': max(0, np.random.normal(0, 1)),
                'wind_speed': max(0, np.random.normal(10, 5)),
                'pedestrian_density': base_engagement + np.random.normal(0, 0.1),
                'traffic_flow': base_engagement + np.random.normal(0, 0.1)
            })
            
        return pd.DataFrame(data)

    def get_pedestrian_density(self, zone, timestamp):
        """
        Estimate pedestrian density based on various data sources
        """
        hour = timestamp.hour
        is_weekend = timestamp.weekday() >= 5
        
        # Base density patterns
        if hour in [8, 9, 17, 18, 19]:  # Rush hours
            base_density = 0.8
        elif hour in [12, 13, 14]:  # Lunch hours
            base_density = 0.7
        elif hour < 6 or hour > 22:  # Late night/early morning
            base_density = 0.1
        else:
            base_density = 0.5
            
        # Weekend adjustments
        if is_weekend:
            if hour in [11, 12, 13, 14, 15]:  # Weekend afternoon
                base_density *= 1.2
            else:
                base_density *= 0.7
                
        # Add some randomness
        density = min(1.0, max(0.0, base_density + np.random.normal(0, 0.1)))
        
        return density

    def integrate_data(self, zone, timestamp):
        """
        Integrate all data sources for a given zone and time
        """
        weather_data = self.get_weather_forecast(f"{zone['latitude']},{zone['longitude']}")
        traffic_data = self.get_traffic_data(zone)
        pedestrian_density = self.get_pedestrian_density(zone, timestamp)
        
        return {
            'zone_id': zone['zone_id'],
            'timestamp': timestamp,
            'weather': weather_data,
            'traffic': traffic_data,
            'pedestrian_density': pedestrian_density,
            'latitude': zone['latitude'],
            'longitude': zone['longitude']
        }

    def prepare_training_data(self, start_date, end_date, zones):
        """
        Prepare historical training data for the model
        """
        historical_data = self.get_historical_engagement(start_date, end_date)
        
        # Enrich with additional features
        for zone in zones:
            zone_data = historical_data[historical_data['zone_id'] == zone['zone_id']].copy()
            
            # Add location features
            zone_data['latitude'] = zone['latitude']
            zone_data['longitude'] = zone['longitude']
            
        return historical_data 