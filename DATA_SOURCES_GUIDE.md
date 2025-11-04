# 📡 Data Sources Guide for Marketing Agencies

## Overview
This guide explains where to get data for enhancing BritMetrics analytics capabilities for marketing agencies and event promotion companies.

## Currently Integrated Data Sources

### 1. WeatherAPI.com ✅
- **Status**: Active
- **What it provides**: Real-time weather conditions, temperature, visibility, wind, precipitation
- **Use case**: Weather-responsive creative recommendations, impact on footfall
- **Cost**: Free tier available, paid from $3.50/month
- **API Docs**: https://www.weatherapi.com/docs/

### 2. TomTom Traffic API ✅
- **Status**: Active  
- **What it provides**: Real-time traffic flow, congestion levels, speed data
- **Use case**: Traffic-based audience sizing, commute time analysis
- **Cost**: Free tier: 2,500 requests/day
- **API Docs**: https://developer.tomtom.com/traffic-api

## Recommended Data Sources to Add

### 3. Google Places API (High Priority)
- **What it provides**: 
  - Popular times data (hourly footfall patterns)
  - Place popularity scores
  - Visit frequency metrics
  - User reviews and ratings
- **Use case**: Accurate footfall predictions, peak time analysis
- **Cost**: $0.017 per request, $200 free credit/month
- **API Docs**: https://developers.google.com/places/web-service
- **Setup**: Get API key from Google Cloud Console

### 4. UK Census Data / ONS (Office for National Statistics)
- **What it provides**:
  - Population demographics by postcode
  - Age distribution
  - Income levels
  - Household composition
  - Employment statistics
- **Use case**: Demographic accuracy, audience targeting validation
- **Cost**: FREE - Open Government Data
- **API Docs**: https://www.ons.gov.uk/developer
- **How to access**: 
  - ONS API: https://www.ons.gov.uk/developer
  - Nomis API: https://www.nomisweb.co.uk/api/v01/

### 5. Foursquare Places API
- **What it provides**:
  - Footfall patterns
  - Visit frequency
  - Demographic insights
  - Popular times
- **Use case**: Alternative to Google Places, more detailed analytics
- **Cost**: Contact for pricing (enterprise plans)
- **API Docs**: https://developer.foursquare.com/

### 6. Twitter API v2
- **What it provides**:
  - Location-based tweets
  - Sentiment analysis
  - Trending topics by location
  - Engagement metrics
- **Use case**: Social sentiment, brand mentions, event promotion insights
- **Cost**: Free tier limited, paid plans available
- **API Docs**: https://developer.twitter.com/en/docs/twitter-api
- **Note**: Requires Twitter Developer account approval

### 7. Eventbrite API
- **What it provides**:
  - Upcoming events by location
  - Event attendance data
  - Event categories
  - Venue information
- **Use case**: Event promotion targeting, competitor analysis
- **Cost**: Free for basic access
- **API Docs**: https://www.eventbrite.com/platform/api/

### 8. Facebook Events API
- **What it provides**:
  - Public events by location
  - Event attendance estimates
  - Event categories
- **Use case**: Event promotion, audience overlap analysis
- **Cost**: Free (requires Facebook Developer account)
- **API Docs**: https://developers.facebook.com/docs/graph-api/reference/event

### 9. Google Analytics API
- **What it provides**:
  - Campaign performance metrics
  - Conversion tracking
  - Audience insights
  - Traffic sources
- **Use case**: Campaign ROI tracking, performance comparison
- **Cost**: Free (requires Google Analytics account)
- **API Docs**: https://developers.google.com/analytics/devguides/reporting/core/v4

### 10. Mapbox / Google Maps Platform
- **What it provides**:
  - Geocoding (address to coordinates)
  - Distance calculations
  - Route optimization
  - Location insights
- **Use case**: Location intelligence, distance-based targeting
- **Cost**: 
  - Mapbox: 100K free requests/month
  - Google: $0.005 per request, $200 free credit/month
- **API Docs**: 
  - Mapbox: https://docs.mapbox.com/api/
  - Google: https://developers.google.com/maps/documentation

## How to Integrate New Data Sources

### Step 1: Get API Access
1. Sign up with the provider
2. Create an API key/credentials
3. Store securely in `.env` file or environment variables

### Step 2: Create Service Class
Add to `backend/api_services.py`:

```python
class NewDataService:
    """Service for retrieving data from New Provider"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.provider.com/v1"
    
    def get_data(self, lat: float, lon: float):
        """Get data for a location"""
        try:
            url = f"{self.base_url}/endpoint?key={self.api_key}&lat={lat}&lon={lon}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return self._parse_data(data)
            else:
                return self._get_fallback_data()
        except Exception:
            return self._get_fallback_data()
    
    def _parse_data(self, data):
        """Parse API response"""
        # Parse and return structured data
        pass
    
    def _get_fallback_data(self):
        """Fallback when API unavailable"""
        # Return default/sample data
        pass
```

### Step 3: Add Data Model
Add to `backend/models.py`:

```python
@dataclass
class NewDataType:
    """New data structure"""
    field1: str
    field2: int
    # ... other fields
```

### Step 4: Integrate into Business Logic
Update `backend/business_logic.py` to use the new data:

```python
def calculate_ad_success_score(..., new_data: NewDataType):
    # Use new_data in calculations
    pass
```

### Step 5: Add to Analytics Dashboard
Update `pages/2_📊_Analytics_Dashboard.py` to display the new data with visualizations.

## Priority Recommendations

### For Marketing Agencies:
1. **Google Places API** - Essential for accurate footfall data
2. **UK Census Data** - Free demographic validation
3. **Twitter API** - Social sentiment analysis
4. **Eventbrite API** - Event promotion targeting

### For Event Promotion Companies:
1. **Eventbrite API** - Event discovery and competition analysis
2. **Facebook Events API** - Event promotion insights
3. **Google Places API** - Venue popularity and footfall
4. **Twitter API** - Event buzz and sentiment

## Cost Estimation

### Free Tier Start:
- WeatherAPI: Free tier available
- TomTom: 2,500 requests/day free
- UK Census: Completely free
- Mapbox: 100K requests/month free

### Paid Tier (for scale):
- Google Places: $200 free credit/month, then $0.017/request
- Twitter API: Contact for pricing
- Foursquare: Enterprise pricing
- Eventbrite: Free for basic access

### Monthly Cost Estimate (Small Agency):
- Google Places API: $50-100/month
- Twitter API: $100-200/month
- Total: ~$150-300/month for comprehensive data

## Security Best Practices

1. **Never commit API keys** to Git
2. **Use environment variables** for all keys
3. **Add `.env` to `.gitignore`**
4. **Rotate keys regularly**
5. **Use API key restrictions** (IP whitelisting, rate limits)

## Example `.env` File

```bash
# Existing
WEATHER_API_KEY=your_weather_api_key
TRAFFIC_API_KEY=your_tomtom_key

# New additions
GOOGLE_PLACES_API_KEY=your_google_key
TWITTER_BEARER_TOKEN=your_twitter_token
EVENTBRITE_API_KEY=your_eventbrite_key
```

## Support

For integration help or custom data source requirements, contact: vamvak@outlook.com

