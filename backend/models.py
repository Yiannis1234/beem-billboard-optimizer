"""
Data models for the Ad Success Predictor application.
Contains area definitions and data structures.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class Coordinates:
    """Geographic coordinates"""
    lat: float
    lon: float


@dataclass
class SuccessFactors:
    """Success factors for an area"""
    high_traffic: bool = False
    business_district: bool = False
    transport_hub: bool = False
    affluent_audience: bool = False
    student_area: bool = False
    shopping_area: bool = False
    creative_area: bool = False
    tourist_area: bool = False
    nightlife: bool = False
    family_area: bool = False
    local_businesses: bool = False
    local_community: bool = False
    corporate_area: bool = False
    commuter_area: bool = False
    university_district: bool = False
    young_audience: bool = False
    trendy_audience: bool = False
    brand_conscious: bool = False
    leisure_time: bool = False
    affluent_suburb: bool = False


@dataclass
class AreaData:
    """Complete area data structure"""
    center: Coordinates
    population: int
    footfall_daily: int
    success_factors: SuccessFactors
    description: str


@dataclass
class WeatherData:
    """Weather data structure"""
    temperature: float
    condition: str
    visibility: float
    wind_kph: float
    humidity: int
    uv: int = 0
    precip_mm: float = 0.0
    is_day: int = 1
    api_status: str = "Unknown"


@dataclass
class TrafficData:
    """Traffic data structure"""
    current_speed: float
    free_flow_speed: float
    congestion_level: str
    congestion_color: str
    speed_ratio: float
    confidence: int
    delay_minutes: float
    traffic_density: float
    api_status: str
    last_updated: str


@dataclass
class PlacesData:
    """Google Places API data structure"""
    place_id: str
    place_name: str
    rating: float = 0.0
    user_ratings_total: int = 0
    formatted_address: str = ""
    types: List[str] = None
    popularity_score: float = 0.0  # Relative popularity (0-100)
    api_status: str = "Unknown"
    
    def __post_init__(self):
        if self.types is None:
            self.types = []


@dataclass
class EventData:
    """Eventbrite event data structure"""
    event_id: str
    event_name: str
    start_date: str = ""
    end_date: str = ""
    venue_name: str = ""
    venue_address: str = ""
    event_url: str = ""
    category: str = ""
    status: str = ""
    api_status: str = "Unknown"
    
    def __post_init__(self):
        pass


@dataclass
class EventsData:
    """Collection of events data for a location"""
    location_name: str
    events: List[EventData] = None
    total_events: int = 0
    upcoming_events: int = 0
    api_status: str = "Unknown"
    
    def __post_init__(self):
        if self.events is None:
            self.events = []


@dataclass
class CampaignType:
    """Campaign type and targeting information"""
    name: str
    target_demographics: List[str]
    ideal_factors: List[str]
    creative_style: str
    
    
@dataclass
class AdSuccessResult:
    """Ad success prediction result"""
    area_name: str
    success_score: int
    impressions_per_hour: int
    success_level: str
    key_reasons: List[str]
    description: str
    weather_notes: List[str]
    weather_score_delta: int
    impression_pct_delta: float
    base_impressions_per_hour: int
    # New personalization fields
    audience_match_score: int = 0
    personalized_tips: List[str] = None
    creative_recommendations: List[str] = None
    target_audience_size: int = 0


class AreaDatabase:
    """Database of areas with their characteristics"""
    
    MANCHESTER_AREAS = {
        "Albert Square": AreaData(
            center=Coordinates(lat=53.4794, lon=-2.2453),
            population=25000,
            footfall_daily=120000,
            success_factors=SuccessFactors(
                high_traffic=True,
                business_district=True,
                transport_hub=True,
                affluent_audience=True,
                shopping_area=True,
                brand_conscious=True
            ),
            description="Historic square with Town Hall - high foot traffic and prestige"
        ),
        "Piccadilly": AreaData(
            center=Coordinates(lat=53.4808, lon=-2.2308),
            population=10000,
            footfall_daily=400000,
            success_factors=SuccessFactors(
                high_traffic=True,
                transport_hub=True,
                commuter_area=True
            ),
            description="Main transport hub - people wait here, perfect for ads"
        ),
        "Oxford Road": AreaData(
            center=Coordinates(lat=53.4708, lon=-2.2358),
            population=25000,
            footfall_daily=300000,
            success_factors=SuccessFactors(
                high_traffic=True,
                student_area=True,
                university_district=True,
                young_audience=True
            ),
            description="University area - young, engaged audience"
        ),
        "Northern Quarter": AreaData(
            center=Coordinates(lat=53.4858, lon=-2.2358),
            population=8000,
            footfall_daily=120000,
            success_factors=SuccessFactors(
                creative_area=True,
                trendy_audience=True,
                nightlife=True,
                young_audience=True,
                brand_conscious=True
            ),
            description="Creative district - trendy, brand-conscious audience"
        ),
        "Deansgate": AreaData(
            center=Coordinates(lat=53.4758, lon=-2.2508),
            population=7000,
            footfall_daily=180000,
            success_factors=SuccessFactors(
                high_traffic=True,
                shopping_area=True,
                affluent_audience=True,
                leisure_time=True,
                brand_conscious=True
            ),
            description="Shopping district - people with money and time to spend"
        ),
        "Spinningfields": AreaData(
            center=Coordinates(lat=53.4788, lon=-2.2508),
            population=5000,
            footfall_daily=200000,
            success_factors=SuccessFactors(
                high_traffic=True,
                business_district=True,
                affluent_audience=True,
                corporate_area=True,
                brand_conscious=True
            ),
            description="Financial district - high-earning professionals"
        ),
        "Chorlton": AreaData(
            center=Coordinates(lat=53.4508, lon=-2.2708),
            population=18000,
            footfall_daily=90000,
            success_factors=SuccessFactors(
                affluent_suburb=True,
                family_area=True,
                local_businesses=True
            ),
            description="Trendy suburb - affluent families and professionals"
        ),
        "Didsbury": AreaData(
            center=Coordinates(lat=53.4208, lon=-2.2308),
            population=22000,
            footfall_daily=75000,
            success_factors=SuccessFactors(
                affluent_suburb=True,
                family_area=True,
                local_community=True
            ),
            description="Affluent suburb - wealthy families and professionals"
        ),
        "Stockport": AreaData(
            center=Coordinates(lat=53.4106, lon=-2.1575),
            population=35000,
            footfall_daily=45000,
            success_factors=SuccessFactors(
                high_traffic=True,
                shopping_area=True,
                transport_hub=True
            ),
            description="Historic market town - good shopping and transport links"
        ),
        "Bolton": AreaData(
            center=Coordinates(lat=53.5767, lon=-2.4282),
            population=40000,
            footfall_daily=55000,
            success_factors=SuccessFactors(
                high_traffic=True,
                shopping_area=True,
                business_district=True
            ),
            description="Large town with shopping center and business district"
        ),
        "Bury": AreaData(
            center=Coordinates(lat=53.5928, lon=-2.2981),
            population=28000,
            footfall_daily=38000,
            success_factors=SuccessFactors(
                high_traffic=True,
                shopping_area=True,
                transport_hub=True
            ),
            description="Market town with good shopping and transport connections"
        ),
        "Rochdale": AreaData(
            center=Coordinates(lat=53.6097, lon=-2.1561),
            population=32000,
            footfall_daily=42000,
            success_factors=SuccessFactors(
                high_traffic=True,
                shopping_area=True,
                business_district=True
            ),
            description="Historic town with shopping center and business activity"
        ),
        "Oldham": AreaData(
            center=Coordinates(lat=53.5409, lon=-2.1114),
            population=30000,
            footfall_daily=40000,
            success_factors=SuccessFactors(
                high_traffic=True,
                shopping_area=True,
                transport_hub=True
            ),
            description="Town center with shopping and transport hub"
        )
    }

    LONDON_AREAS = {
        "Oxford Circus": AreaData(
            center=Coordinates(lat=51.5154, lon=-0.1410),
            population=20000,
            footfall_daily=450000,
            success_factors=SuccessFactors(
                high_traffic=True,
                shopping_area=True,
                affluent_audience=True
            ),
            description="Iconic West End shopping junction with extremely high footfall"
        ),
        "Piccadilly Circus": AreaData(
            center=Coordinates(lat=51.5098, lon=-0.1340),
            population=15000,
            footfall_daily=400000,
            success_factors=SuccessFactors(
                high_traffic=True,
                shopping_area=True,
                tourist_area=True
            ),
            description="Tourist hotspot with giant screens and constant pedestrian flow"
        ),
        "Liverpool Street": AreaData(
            center=Coordinates(lat=51.5178, lon=-0.0824),
            population=18000,
            footfall_daily=380000,
            success_factors=SuccessFactors(
                high_traffic=True,
                transport_hub=True,
                business_district=True
            ),
            description="Major commuter hub in the City with strong professional audience"
        ),
        "Canary Wharf": AreaData(
            center=Coordinates(lat=51.5054, lon=-0.0235),
            population=12000,
            footfall_daily=300000,
            success_factors=SuccessFactors(
                business_district=True,
                affluent_audience=True,
                high_traffic=True
            ),
            description="Financial district with affluent professionals and premium brands"
        ),
        "Shoreditch": AreaData(
            center=Coordinates(lat=51.5260, lon=-0.0803),
            population=10000,
            footfall_daily=180000,
            success_factors=SuccessFactors(
                creative_area=True,
                nightlife=True,
                high_traffic=True
            ),
            description="Trendy creative area with young, brand-conscious audience"
        ),
        "South Bank": AreaData(
            center=Coordinates(lat=51.5066, lon=-0.1163),
            population=8000,
            footfall_daily=220000,
            success_factors=SuccessFactors(
                tourist_area=True,
                shopping_area=True,
                high_traffic=True
            ),
            description="Riverside cultural district with heavy tourist footfall"
        ),
        "King's Cross": AreaData(
            center=Coordinates(lat=51.5308, lon=-0.1238),
            population=11000,
            footfall_daily=320000,
            success_factors=SuccessFactors(
                transport_hub=True,
                business_district=True,
                high_traffic=True
            ),
            description="Major rail hub with offices and retail – long dwell times"
        ),
        "Camden Town": AreaData(
            center=Coordinates(lat=51.5416, lon=-0.1420),
            population=9000,
            footfall_daily=160000,
            success_factors=SuccessFactors(
                creative_area=True,
                shopping_area=True,
                nightlife=True
            ),
            description="Market and music area – strong youth and tourist traffic"
        )
    }

    @classmethod
    def get_areas(cls, city: str) -> Dict[str, AreaData]:
        """Get areas for a specific city"""
        if city.lower() == "manchester":
            return cls.MANCHESTER_AREAS
        elif city.lower() == "london":
            return cls.LONDON_AREAS
        else:
            raise ValueError(f"Unknown city: {city}")

    @classmethod
    def get_area(cls, city: str, area_name: str) -> Optional[AreaData]:
        """Get specific area data"""
        areas = cls.get_areas(city)
        return areas.get(area_name)

    @classmethod
    def get_all_cities(cls) -> List[str]:
        """Get list of all available cities"""
        return ["Manchester", "London"]


class CampaignDatabase:
    """Database of campaign types for personalized targeting"""
    
    CAMPAIGNS = {
        "Luxury Fashion Brand": CampaignType(
            name="Luxury Fashion Brand",
            target_demographics=["affluent", "business professionals", "trend-conscious"],
            ideal_factors=["affluent_audience", "business_district", "shopping_area", "brand_conscious"],
            creative_style="Elegant, minimalist, aspirational imagery"
        ),
        "Tech Startup": CampaignType(
            name="Tech Startup",
            target_demographics=["young professionals", "students", "early adopters"],
            ideal_factors=["student_area", "creative_area", "university_district", "young_audience"],
            creative_style="Bold, innovative, QR codes and AR integration"
        ),
        "Fast Food / Quick Service": CampaignType(
            name="Fast Food / Quick Service",
            target_demographics=["commuters", "students", "busy professionals"],
            ideal_factors=["transport_hub", "high_traffic", "student_area", "commuter_area"],
            creative_style="Vibrant colors, time-limited offers, appetite appeal"
        ),
        "Financial Services": CampaignType(
            name="Financial Services",
            target_demographics=["professionals", "high earners", "homeowners"],
            ideal_factors=["business_district", "affluent_audience", "corporate_area", "affluent_suburb"],
            creative_style="Trust-building, data-driven, professional tone"
        ),
        "Entertainment / Events": CampaignType(
            name="Entertainment / Events",
            target_demographics=["young adults", "families", "tourists"],
            ideal_factors=["nightlife", "creative_area", "tourist_area", "leisure_time"],
            creative_style="Dynamic, colorful, FOMO-driven messaging"
        ),
        "Education / Training": CampaignType(
            name="Education / Training",
            target_demographics=["students", "young professionals", "career changers"],
            ideal_factors=["student_area", "university_district", "transport_hub", "young_audience"],
            creative_style="Aspirational, future-focused, clear CTAs"
        ),
        "Local Business / Services": CampaignType(
            name="Local Business / Services",
            target_demographics=["local residents", "families", "community members"],
            ideal_factors=["local_community", "family_area", "local_businesses", "affluent_suburb"],
            creative_style="Community-focused, friendly, trustworthy"
        ),
        "Health & Fitness": CampaignType(
            name="Health & Fitness",
            target_demographics=["health-conscious", "young professionals", "affluent"],
            ideal_factors=["affluent_audience", "young_audience", "business_district", "affluent_suburb"],
            creative_style="Motivational, transformation-focused, lifestyle imagery"
        ),
        "Eco-Friendly / Sustainable": CampaignType(
            name="Eco-Friendly / Sustainable",
            target_demographics=["millennials", "families", "affluent conscious consumers"],
            ideal_factors=["creative_area", "family_area", "trendy_audience", "affluent_suburb"],
            creative_style="Natural colors, transparent messaging, impact-focused"
        ),
        "Nightlife / Hospitality": CampaignType(
            name="Nightlife / Hospitality",
            target_demographics=["young adults", "tourists", "social groups"],
            ideal_factors=["nightlife", "creative_area", "tourist_area", "trendy_audience"],
            creative_style="Energetic, social proof, time-sensitive promotions"
        )
    }
