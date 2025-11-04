#!/usr/bin/env python3
"""
Test script to verify audience match calculation is working correctly
"""

from backend.models import AreaDatabase, CampaignDatabase
from backend.business_logic import AdSuccessCalculator
from backend.api_services import WeatherAPIService, TrafficAPIService

def test_audience_match():
    """Test audience match calculation with various combinations"""
    print("=" * 80)
    print("AUDIENCE MATCH CALCULATION TEST")
    print("=" * 80)
    print()
    
    # Test 1: Perfect match
    print("TEST 1: Perfect Match Scenario")
    print("-" * 80)
    area = AreaDatabase.get_area('Manchester', 'Albert Square')
    campaign = CampaignDatabase.CAMPAIGNS['Luxury Fashion Brand']
    match = AdSuccessCalculator._calculate_audience_match(area.success_factors, campaign)
    print(f"Area: Albert Square")
    print(f"Campaign: {campaign.name}")
    print(f"Ideal Factors: {campaign.ideal_factors}")
    print(f"Area Factors: affluent_audience={area.success_factors.affluent_audience}, "
          f"business_district={area.success_factors.business_district}, "
          f"shopping_area={area.success_factors.shopping_area}, "
          f"brand_conscious={area.success_factors.brand_conscious}")
    print(f"✅ Match Score: {match}%")
    print(f"Expected: 100% (all factors match)")
    assert match == 100, f"Expected 100%, got {match}%"
    print("✅ PASSED")
    print()
    
    # Test 2: Good match with partial
    print("TEST 2: Good Match with Partial Scoring")
    print("-" * 80)
    area = AreaDatabase.get_area('Manchester', 'Oxford Road')
    campaign = CampaignDatabase.CAMPAIGNS['Tech Startup']
    match = AdSuccessCalculator._calculate_audience_match(area.success_factors, campaign)
    print(f"Area: Oxford Road")
    print(f"Campaign: {campaign.name}")
    print(f"Ideal Factors: {campaign.ideal_factors}")
    print(f"Area Factors: student_area={area.success_factors.student_area}, "
          f"creative_area={area.success_factors.creative_area}, "
          f"university_district={area.success_factors.university_district}, "
          f"young_audience={area.success_factors.young_audience}")
    print(f"✅ Match Score: {match}%")
    print(f"Expected: 75-100% (3 direct matches, 1 missing)")
    assert 75 <= match <= 100, f"Expected 75-100%, got {match}%"
    print("✅ PASSED")
    print()
    
    # Test 3: Poor match
    print("TEST 3: Poor Match Scenario")
    print("-" * 80)
    area = AreaDatabase.get_area('Manchester', 'Chorlton')
    campaign = CampaignDatabase.CAMPAIGNS['Tech Startup']
    match = AdSuccessCalculator._calculate_audience_match(area.success_factors, campaign)
    print(f"Area: Chorlton")
    print(f"Campaign: {campaign.name}")
    print(f"Ideal Factors: {campaign.ideal_factors}")
    print(f"Area Factors: student_area={area.success_factors.student_area}, "
          f"creative_area={area.success_factors.creative_area}, "
          f"university_district={area.success_factors.university_district}, "
          f"young_audience={area.success_factors.young_audience}")
    print(f"✅ Match Score: {match}%")
    print(f"Expected: <50% (no direct matches)")
    assert match < 50, f"Expected <50%, got {match}%"
    print("✅ PASSED")
    print()
    
    # Test 4: Test all campaigns with all areas
    print("TEST 4: Comprehensive Test - All Campaigns vs All Areas")
    print("-" * 80)
    areas = {**AreaDatabase.MANCHESTER_AREAS, **AreaDatabase.LONDON_AREAS}
    
    for campaign_name, campaign in CampaignDatabase.CAMPAIGNS.items():
        print(f"\n📊 Campaign: {campaign_name}")
        print(f"   Target: {', '.join(campaign.target_demographics[:2])}")
        print(f"   Ideal Factors: {campaign.ideal_factors}")
        
        matches = []
        for area_name, area_data in list(areas.items())[:5]:  # Test first 5 areas
            match = AdSuccessCalculator._calculate_audience_match(area_data.success_factors, campaign)
            matches.append((area_name, match))
        
        # Sort by match score
        matches.sort(key=lambda x: x[1], reverse=True)
        
        print("   Top Matches:")
        for area_name, match in matches:
            print(f"     • {area_name}: {match}%")
        
        # Verify we have variation in scores
        scores = [m[1] for m in matches]
        if max(scores) - min(scores) < 10:
            print(f"   ⚠️ WARNING: Low variation in scores (min={min(scores)}, max={max(scores)})")
        else:
            print(f"   ✅ Good variation in scores (min={min(scores)}, max={max(scores)})")
    
    print()
    print("=" * 80)
    print("ALL TESTS COMPLETED")
    print("=" * 80)

def test_full_prediction_flow():
    """Test the full prediction flow with APIs"""
    print("\n" + "=" * 80)
    print("FULL PREDICTION FLOW TEST (with APIs)")
    print("=" * 80)
    print()
    
    weather_service = WeatherAPIService()
    traffic_service = TrafficAPIService()
    
    # Test API connectivity
    print("Testing API Services...")
    area = AreaDatabase.get_area('Manchester', 'Albert Square')
    
    weather_data = weather_service.get_weather_data(area.center.lat, area.center.lon)
    print(f"✅ Weather API: {weather_data.api_status}")
    print(f"   Temperature: {weather_data.temperature}°C, Condition: {weather_data.condition}")
    
    traffic_data = traffic_service.get_traffic_data(area.center.lat, area.center.lon)
    print(f"✅ Traffic API: {traffic_data.api_status}")
    print(f"   Congestion: {traffic_data.congestion_level}")
    
    # Test full calculation
    campaign = CampaignDatabase.CAMPAIGNS['Luxury Fashion Brand']
    result = AdSuccessCalculator.calculate_ad_success_score(
        "Albert Square", area, weather_data, traffic_data, campaign=campaign
    )
    
    print()
    print("Full Prediction Result:")
    print(f"✅ Success Score: {result.success_score}/100")
    print(f"✅ Audience Match: {result.audience_match_score}%")
    print(f"✅ Impressions/Hour: {result.impressions_per_hour}")
    print(f"✅ Target Audience Size: {result.target_audience_size}")
    
    assert result.audience_match_score > 0, "Audience match should be > 0 when campaign is provided"
    print()
    print("✅ FULL PREDICTION TEST PASSED")

if __name__ == "__main__":
    try:
        test_audience_match()
        test_full_prediction_flow()
        print("\n🎉 ALL TESTS PASSED! Audience match is working correctly.")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

