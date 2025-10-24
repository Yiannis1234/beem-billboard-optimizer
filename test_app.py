#!/usr/bin/env python3
"""
Test script for the Ad Success Predictor application.
Tests the organized backend and frontend structure.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_backend_imports():
    """Test backend module imports"""
    try:
        from backend.models import AreaDatabase, AreaData, WeatherData, TrafficData
        from backend.api_services import WeatherAPIService, TrafficAPIService
        from backend.business_logic import AdSuccessCalculator
        print("✅ Backend imports successful")
        return True
    except ImportError as e:
        print(f"❌ Backend import error: {e}")
        return False

def test_frontend_imports():
    """Test frontend module imports"""
    try:
        from frontend.styles import UNIVERSAL_CSS
        print("✅ Frontend styles imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Frontend import error: {e}")
        return False

def test_area_database():
    """Test area database functionality"""
    try:
        from backend.models import AreaDatabase
        
        # Test getting areas
        manchester_areas = AreaDatabase.get_areas("Manchester")
        london_areas = AreaDatabase.get_areas("London")
        
        print(f"✅ Manchester areas: {len(manchester_areas)}")
        print(f"✅ London areas: {len(london_areas)}")
        
        # Test getting specific area
        albert_square = AreaDatabase.get_area("Manchester", "Albert Square")
        if albert_square:
            print(f"✅ Albert Square data: {albert_square.description}")
        
        return True
    except Exception as e:
        print(f"❌ Area database error: {e}")
        return False

def test_api_services():
    """Test API services"""
    try:
        from backend.api_services import WeatherAPIService, TrafficAPIService
        
        weather_service = WeatherAPIService()
        traffic_service = TrafficAPIService()
        
        # Test with Manchester coordinates
        weather_data = weather_service.get_weather_data(53.4794, -2.2453)
        traffic_data = traffic_service.get_traffic_data(53.4794, -2.2453)
        
        print(f"✅ Weather data: {weather_data.condition}, {weather_data.temperature}°C")
        print(f"✅ Traffic data: {traffic_data.congestion_level}, {traffic_data.current_speed} km/h")
        
        return True
    except Exception as e:
        print(f"❌ API services error: {e}")
        return False

def test_business_logic():
    """Test business logic"""
    try:
        from backend.models import AreaDatabase
        from backend.api_services import WeatherAPIService, TrafficAPIService
        from backend.business_logic import AdSuccessCalculator
        
        # Get test data
        area_data = AreaDatabase.get_area("Manchester", "Albert Square")
        weather_service = WeatherAPIService()
        traffic_service = TrafficAPIService()
        
        weather_data = weather_service.get_weather_data(area_data.center.lat, area_data.center.lon)
        traffic_data = traffic_service.get_traffic_data(area_data.center.lat, area_data.center.lon)
        
        # Calculate success
        result = AdSuccessCalculator.calculate_ad_success_score(
            "Albert Square", area_data, weather_data, traffic_data
        )
        
        print(f"✅ Success calculation: {result.success_score}/100 ({result.success_level})")
        print(f"✅ Impressions/hour: {result.impressions_per_hour:,}")
        
        return True
    except Exception as e:
        print(f"❌ Business logic error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Ad Success Predictor Application")
    print("=" * 50)
    
    tests = [
        ("Backend Imports", test_backend_imports),
        ("Frontend Imports", test_frontend_imports),
        ("Area Database", test_area_database),
        ("API Services", test_api_services),
        ("Business Logic", test_business_logic),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
