# 🗺️ Google Places API - Quick Setup Guide

## WHERE TO FIND IT

### 1. Official Documentation (You're Already There!)
**URL:** https://developers.google.com/maps/documentation/places/web-service

**Direct Links:**
- **Main Documentation:** https://developers.google.com/maps/documentation/places/web-service
- **Get Started Button:** Click the blue "Get Started" button on the page
- **API Overview:** https://developers.google.com/maps/documentation/places/web-service/overview

---

## STEP-BY-STEP SETUP

### Step 1: Go to Google Cloud Console
1. Visit: **https://console.cloud.google.com/**
2. Sign in with your Google account
3. Create a new project or select an existing one

### Step 2: Enable Places API
1. Go to: **https://console.cloud.google.com/apis/library**
2. Search for: **"Places API"**
3. Click on **"Places API"** (not "Places API (New)" - that's the newer version)
4. Click **"Enable"** button

### Step 3: Get Your API Key
1. Go to: **https://console.cloud.google.com/apis/credentials**
2. Click **"Create Credentials"** → **"API Key"**
3. Copy your API key (you'll need this!)
4. **IMPORTANT:** Click on the API key to restrict it:
   - **Application restrictions:** IP addresses (for server) or HTTP referrers (for web)
   - **API restrictions:** Select "Restrict key" → Choose "Places API"

### Step 4: Enable Billing (Required!)
1. Go to: **https://console.cloud.google.com/billing**
2. Link a billing account (credit card required)
3. **Good News:** You get $200 free credit/month!
4. After $200, it's $0.017 per request

---

## KEY ENDPOINTS FOR YOUR USE CASE

### 1. Place Details (Get Popular Times)
**Endpoint:** `https://maps.googleapis.com/maps/api/place/details/json`

**What you need:**
- `place_id` - The ID of the place
- `fields` - Request specific data like `popularTimes`, `currentPopularity`, etc.

**Example Request:**
```python
import requests

API_KEY = "YOUR_API_KEY"
PLACE_ID = "ChIJN1t_tDeuEmsRUsoyG83frY4"  # Example: A location in Manchester

url = f"https://maps.googleapis.com/maps/api/place/details/json"
params = {
    "place_id": PLACE_ID,
    "fields": "popularTimes,currentPopularity,rating,user_ratings_total",
    "key": API_KEY
}

response = requests.get(url, params=params)
data = response.json()
```

### 2. Text Search (Find Places by Name)
**Endpoint:** `https://maps.googleapis.com/maps/api/place/textsearch/json`

**Example:**
```python
url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
params = {
    "query": "Piccadilly Gardens Manchester",
    "key": API_KEY
}
response = requests.get(url, params=params)
```

### 3. Nearby Search (Find Places Near Coordinates)
**Endpoint:** `https://maps.googleapis.com/maps/api/place/nearbysearch/json`

**Example:**
```python
url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
params = {
    "location": "53.4808,-2.2308",  # lat,lng
    "radius": 500,  # meters
    "type": "point_of_interest",
    "key": API_KEY
}
response = requests.get(url, params=params)
```

---

## IMPORTANT: Popular Times Data

**⚠️ Note:** The "popular times" data (hourly footfall) is available but:
- It's part of the Place Details response
- Some places may not have this data
- It shows relative popularity, not exact numbers
- Data is based on historical user visits

**How to access it:**
```python
# In the Place Details response, look for:
popular_times = data['result'].get('popularTimes', [])
# Returns array of day objects with hourly data
```

---

## QUICK START CODE

### Add to `backend/api_services.py`:

```python
class GooglePlacesService:
    """Service for retrieving footfall data from Google Places API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"
    
    def get_place_details(self, place_id: str):
        """Get detailed place information including popular times"""
        try:
            url = f"{self.base_url}/details/json"
            params = {
                "place_id": place_id,
                "fields": "popularTimes,currentPopularity,rating,user_ratings_total,name,formatted_address",
                "key": self.api_key
            }
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK':
                    return data['result']
            return None
        except Exception as e:
            print(f"Error fetching place details: {e}")
            return None
    
    def search_place(self, query: str, location: tuple = None):
        """Search for a place by name"""
        try:
            url = f"{self.base_url}/textsearch/json"
            params = {
                "query": query,
                "key": self.api_key
            }
            if location:
                params["location"] = f"{location[0]},{location[1]}"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK' and data.get('results'):
                    return data['results'][0]  # Return first result
            return None
        except Exception as e:
            print(f"Error searching place: {e}")
            return None
    
    def get_footfall_data(self, place_name: str, lat: float, lon: float):
        """Get footfall/popular times data for a location"""
        # First, search for the place
        place_result = self.search_place(place_name, (lat, lon))
        if not place_result:
            return None
        
        place_id = place_result.get('place_id')
        if not place_id:
            return None
        
        # Then get detailed info including popular times
        details = self.get_place_details(place_id)
        return details
```

---

## COST ESTIMATION

### Free Tier:
- **$200 free credit per month**
- After that: $0.017 per request

### Your Usage Estimate:
- **Place Details:** ~$0.017 per location
- **Text Search:** ~$0.032 per search
- **For 100 locations/day:** ~$1.70/day = ~$50/month
- **Within free tier:** You can do ~11,000 requests/month for FREE!

---

## SECURITY BEST PRACTICES

1. **Never commit API key to Git**
   - Add to `.env` file
   - Add `.env` to `.gitignore`

2. **Restrict API Key:**
   - IP restrictions (for server)
   - API restrictions (only Places API)

3. **Environment Variables:**
   ```bash
   # .env file
   GOOGLE_PLACES_API_KEY=your_api_key_here
   ```

4. **Load in Python:**
   ```python
   from dotenv import load_dotenv
   import os
   
   load_dotenv()
   api_key = os.getenv('GOOGLE_PLACES_API_KEY')
   ```

---

## DIRECT LINKS SUMMARY

1. **Documentation:** https://developers.google.com/maps/documentation/places/web-service
2. **Cloud Console:** https://console.cloud.google.com/
3. **API Library:** https://console.cloud.google.com/apis/library
4. **Credentials:** https://console.cloud.google.com/apis/credentials
5. **Billing:** https://console.cloud.google.com/billing
6. **Pricing:** https://developers.google.com/maps/billing-and-pricing/pricing

---

## NEXT STEPS

1. ✅ Go to Google Cloud Console
2. ✅ Enable Places API
3. ✅ Get API Key
4. ✅ Add to `.env` file
5. ✅ Implement `GooglePlacesService` in `backend/api_services.py`
6. ✅ Test with a known location
7. ✅ Integrate into `AdSuccessCalculator`

**Need help?** Contact: vamvak@outlook.com

