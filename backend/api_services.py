"""
API services for external data sources.
Handles weather and traffic data retrieval.
"""

import requests
from datetime import datetime
from typing import Dict, Any, Optional, List
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional
from .models import WeatherData, TrafficData, PlacesData, EventsData, EventData


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
                    is_day=current.get('is_day', 1),
                    api_status='Live Data'
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
            is_day=1,
            api_status='Fallback (API unavailable)'
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


class GooglePlacesService:
    """Service for retrieving footfall and place data from Google Places API"""
    
    def __init__(self, api_key: Optional[str] = None):
        # Use provided key, or try environment variable, or use the verified key
        self.api_key = api_key or os.getenv('GOOGLE_PLACES_API_KEY', 'AIzaSyDOR3SP5wXTznBEscqYcrJHlMom8bR18lw')
        self.base_url = "https://maps.googleapis.com/maps/api/place"
    
    def search_place(self, query: str, location: Optional[tuple] = None) -> Optional[Dict]:
        """Search for a place by name and optional location"""
        try:
            url = f"{self.base_url}/textsearch/json"
            params = {
                "query": query,
                "key": self.api_key
            }
            if location:
                params["location"] = f"{location[0]},{location[1]}"
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK' and data.get('results'):
                    return data['results'][0]  # Return first result
            return None
        except Exception as e:
            print(f"Error searching place: {e}")
            return None
    
    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """Get detailed place information"""
        try:
            url = f"{self.base_url}/details/json"
            params = {
                "place_id": place_id,
                "fields": "name,rating,user_ratings_total,formatted_address,types,place_id",
                "key": self.api_key
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'OK':
                    return data.get('result')
            return None
        except Exception as e:
            print(f"Error fetching place details: {e}")
            return None
    
    def get_places_data(self, place_name: str, lat: float, lon: float) -> PlacesData:
        """Get comprehensive place data including footfall indicators"""
        try:
            # First, search for the place
            search_result = self.search_place(place_name, (lat, lon))
            if not search_result:
                return self._get_fallback_places_data(place_name)
            
            place_id = search_result.get('place_id')
            if not place_id:
                return self._get_fallback_places_data(place_name)
            
            # Get detailed information
            details = self.get_place_details(place_id)
            if not details:
                # Use search result if details fail
                return PlacesData(
                    place_id=place_id,
                    place_name=search_result.get('name', place_name),
                    rating=search_result.get('rating', 0.0),
                    user_ratings_total=search_result.get('user_ratings_total', 0),
                    formatted_address=search_result.get('formatted_address', ''),
                    types=search_result.get('types', []),
                    popularity_score=self._calculate_popularity_score(search_result),
                    api_status='Live Data (Search)'
                )
            
            # Use detailed data
            return PlacesData(
                place_id=place_id,
                place_name=details.get('name', place_name),
                rating=details.get('rating', 0.0),
                user_ratings_total=details.get('user_ratings_total', 0),
                formatted_address=details.get('formatted_address', ''),
                types=details.get('types', []),
                popularity_score=self._calculate_popularity_score(details),
                api_status='Live Data'
            )
        except Exception as e:
            print(f"Error getting places data: {e}")
            return self._get_fallback_places_data(place_name)
    
    def _calculate_popularity_score(self, place_data: Dict) -> float:
        """Calculate a popularity score (0-100) based on rating and review count"""
        rating = place_data.get('rating', 0.0)
        review_count = place_data.get('user_ratings_total', 0)
        
        # Base score from rating (0-5 scale -> 0-50 points)
        rating_score = (rating / 5.0) * 50
        
        # Review count score (log scale, max 50 points)
        # 1000+ reviews = 50 points, 100 reviews = 30 points, 10 reviews = 15 points
        if review_count >= 1000:
            review_score = 50
        elif review_count >= 100:
            review_score = 30 + ((review_count - 100) / 900) * 20
        elif review_count >= 10:
            review_score = 15 + ((review_count - 10) / 90) * 15
        else:
            review_score = (review_count / 10) * 15
        
        return min(100, rating_score + review_score)
    
    def _get_fallback_places_data(self, place_name: str) -> PlacesData:
        """Provide fallback place data when API is unavailable"""
        return PlacesData(
            place_id="",
            place_name=place_name,
            rating=0.0,
            user_ratings_total=0,
            formatted_address="",
            types=[],
            popularity_score=0.0,
            api_status='Fallback (API unavailable)'
        )


class EventbriteService:
    """Service for retrieving event data from Eventbrite API"""
    
    def __init__(self, api_token: Optional[str] = None):
        # Use provided token, or try environment variable, or use the verified token
        self.api_token = api_token or os.getenv('EVENTBRITE_API_TOKEN', 'I7CHBQ2D7JKF5RFZ63MO')
        self.base_url = "https://www.eventbriteapi.com/v3"
        self.headers = {
            'Authorization': f'Bearer {self.api_token}'
        }
    
    def get_events_near_location(self, location_name: str, lat: float, lon: float, radius_km: int = 10) -> EventsData:
        """Get events near a location"""
        try:
            # Try multiple methods to get events
            events_list = []
            
            # Method 1: Try to get events from user's organizations
            user_orgs = self._get_user_organizations()
            if user_orgs:
                for org_id in user_orgs:
                    org_events = self._get_organization_events(org_id, location_name)
                    events_list.extend(org_events)
            
            # Method 2: Try public search (if available)
            # Note: Eventbrite's public search API may require different access
            # This is a fallback that can be enhanced later
            
            # Remove duplicates
            unique_events = {}
            for event in events_list:
                if event.event_id not in unique_events:
                    unique_events[event.event_id] = event
            
            events_list = list(unique_events.values())
            
            # Filter upcoming events
            from datetime import datetime
            upcoming = [e for e in events_list if e.status == 'live']
            
            if events_list:
                return EventsData(
                    location_name=location_name,
                    events=events_list,
                    total_events=len(events_list),
                    upcoming_events=len(upcoming),
                    api_status='Live Data'
                )
            else:
                return self._get_fallback_events_data(location_name)
                
        except Exception as e:
            print(f"Error getting events: {e}")
            return self._get_fallback_events_data(location_name)
    
    def _get_user_organizations(self) -> List[str]:
        """Get list of organization IDs for the user"""
        try:
            url = f"{self.base_url}/users/me/organizations/"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                orgs = data.get('organizations', [])
                return [org['id'] for org in orgs]
            return []
        except Exception:
            return []
    
    def _get_organization_events(self, org_id: str, location_filter: str = None) -> List[EventData]:
        """Get events from a specific organization"""
        try:
            url = f"{self.base_url}/organizations/{org_id}/events/"
            params = {'status': 'live', 'expand': 'venue'}
            
            # Add location filter if specified
            if location_filter:
                params['location.address'] = location_filter
            
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                return [self._parse_event(event) for event in events]
            return []
        except Exception:
            return []
    
    def _parse_event(self, event_data: Dict) -> EventData:
        """Parse Eventbrite event data into EventData model"""
        try:
            name = event_data.get('name', {})
            venue = event_data.get('venue', {})
            start = event_data.get('start', {})
            end = event_data.get('end', {})
            
            return EventData(
                event_id=event_data.get('id', ''),
                event_name=name.get('text', 'Unknown Event') if isinstance(name, dict) else str(name),
                start_date=start.get('local', '') if isinstance(start, dict) else '',
                end_date=end.get('local', '') if isinstance(end, dict) else '',
                venue_name=venue.get('name', '') if isinstance(venue, dict) else '',
                venue_address=venue.get('address', {}).get('localized_area_display', '') if isinstance(venue, dict) else '',
                event_url=event_data.get('url', ''),
                category=event_data.get('category_id', ''),
                status=event_data.get('status', ''),
                api_status='Live Data'
            )
        except Exception:
            return EventData(
                event_id='',
                event_name='Unknown',
                api_status='Parse Error'
            )
    
    def _get_fallback_events_data(self, location_name: str) -> EventsData:
        """Provide fallback events data when API is unavailable"""
        return EventsData(
            location_name=location_name,
            events=[],
            total_events=0,
            upcoming_events=0,
            api_status='No events found or API unavailable'
        )
