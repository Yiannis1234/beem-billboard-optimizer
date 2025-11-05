"""FastAPI application exposing BritMetrics prediction endpoints for the React front-end."""

from __future__ import annotations

import logging
import re
from dataclasses import asdict
from datetime import datetime
from typing import Dict, List, Optional
from collections import deque

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.api_services import (
    EventbriteService,
    GooglePlacesService,
    TrafficAPIService,
    WeatherAPIService,
)
from backend.business_logic import AdSuccessCalculator
from backend.models import (
    AdSuccessResult,
    AreaData,
    AreaDatabase,
    CampaignDatabase,
    EventsData,
    PlacesData,
    TrafficData,
    WeatherData,
)

logger = logging.getLogger("britmetrics.api")
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="BritMetrics API", version="1.0.0")

# Allow local development by default; adjust origins in production as needed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


_slug_pattern = re.compile(r"[^a-z0-9]+")


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = value.replace("&", "and")
    value = _slug_pattern.sub("-", value)
    return value.strip("-")


class PredictRequest(BaseModel):
    cityId: str
    areaId: str
    campaignId: Optional[str] = None


_weather_service = WeatherAPIService()
_traffic_service = TrafficAPIService()
_places_service = GooglePlacesService()
_events_service = EventbriteService()


class Registry:
    """Caches lookup tables for cities, areas, and campaigns."""

    def __init__(self) -> None:
        self.campaigns_payload: List[Dict] = []
        self.campaign_id_to_key: Dict[str, Optional[str]] = {}

        self.cities_payload: List[Dict] = []
        self.city_id_to_name: Dict[str, str] = {}
        self.city_id_to_areas: Dict[str, Dict[str, str]] = {}

        self._build_campaigns()
        self._build_cities()

    def _build_campaigns(self) -> None:
        # Generic option so the UI can run without choosing a specific campaign
        self.campaigns_payload.append(
            {
                "id": "generic",
                "name": "None (Generic Analysis)",
                "summary": "Use this for a quick pulse check before client onboarding.",
                "highlights": [
                    "Baseline forecast without demographic filters",
                    "Great for testing city + area combinations",
                    "Add a campaign to unlock tailored tactics",
                ],
                "idealFactors": [],
                "targetDemographics": [],
            }
        )
        self.campaign_id_to_key["generic"] = None

        for campaign_name, campaign in CampaignDatabase.CAMPAIGNS.items():
            campaign_id = slugify(campaign_name)
            self.campaign_id_to_key[campaign_id] = campaign_name
            highlights = [
                f"Target: {', '.join(campaign.target_demographics[:2])}",
                f"Ideal factors: {', '.join(campaign.ideal_factors[:3])}",
                f"Creative style: {campaign.creative_style}",
            ]
            self.campaigns_payload.append(
                {
                    "id": campaign_id,
                    "name": campaign.name,
                    "summary": campaign.creative_style,
                    "targetDemographics": campaign.target_demographics,
                    "idealFactors": campaign.ideal_factors,
                    "highlights": highlights,
                }
            )

    def _build_cities(self) -> None:
        for city_name in AreaDatabase.get_all_cities():
            city_id = slugify(city_name)
            self.city_id_to_name[city_id] = city_name
            areas_payload: List[Dict] = []
            area_slug_lookup: Dict[str, str] = {}

            for area_name, area in AreaDatabase.get_areas(city_name).items():
                area_id = slugify(area_name)
                area_slug_lookup[area_id] = area_name
                areas_payload.append(
                    {
                        "id": area_id,
                        "name": area_name,
                        "description": area.description,
                        "footfallDaily": area.footfall_daily,
                        "population": area.population,
                        "center": {
                            "lat": area.center.lat,
                            "lon": area.center.lon,
                        },
                        "meta": f"Footfall: {area.footfall_daily:,}/day · Population: {area.population:,}",
                    }
                )

            self.cities_payload.append({"id": city_id, "name": city_name, "areas": areas_payload})
            self.city_id_to_areas[city_id] = area_slug_lookup

    def resolve_city(self, city_id: str) -> str:
        try:
            return self.city_id_to_name[city_id]
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=f"Unknown city id '{city_id}'") from exc

    def resolve_area(self, city_id: str, area_id: str) -> str:
        areas = self.city_id_to_areas.get(city_id)
        if not areas:
            raise HTTPException(status_code=404, detail=f"City '{city_id}' has no area mapping")
        try:
            return areas[area_id]
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=f"Unknown area id '{area_id}' for city '{city_id}'") from exc

    def resolve_campaign(self, campaign_id: Optional[str]):
        if not campaign_id:
            return None
        if campaign_id not in self.campaign_id_to_key:
            raise HTTPException(status_code=404, detail=f"Unknown campaign id '{campaign_id}'")
        campaign_name = self.campaign_id_to_key[campaign_id]
        if campaign_name is None:
            return None
        return CampaignDatabase.CAMPAIGNS[campaign_name]


def _safe_dataclass_dict(data):
    if data is None:
        return None
    return asdict(data)


def _serialize_weather(weather: Optional[WeatherData]):
    if weather is None:
        return None
    return {
        "condition": weather.condition,
        "temperatureC": weather.temperature,
        "visibilityKm": weather.visibility,
        "windKph": weather.wind_kph,
        "precipMm": weather.precip_mm,
        "humidity": weather.humidity,
        "uvIndex": weather.uv,
        "isDay": weather.is_day,
        "apiStatus": weather.api_status,
    }


def _serialize_traffic(traffic: Optional[TrafficData]):
    if traffic is None:
        return None
    return {
        "currentSpeed": traffic.current_speed,
        "freeFlowSpeed": traffic.free_flow_speed,
        "congestionLevel": traffic.congestion_level,
        "congestionColor": traffic.congestion_color,
        "speedRatio": traffic.speed_ratio,
        "confidence": traffic.confidence,
        "delayMinutes": traffic.delay_minutes,
        "trafficDensity": traffic.traffic_density,
        "apiStatus": traffic.api_status,
        "lastUpdated": traffic.last_updated,
    }


def _serialize_places(places: Optional[PlacesData]):
    if places is None:
        return None
    return {
        "placeId": places.place_id,
        "placeName": places.place_name,
        "rating": places.rating,
        "userRatingsTotal": places.user_ratings_total,
        "formattedAddress": places.formatted_address,
        "types": places.types,
        "popularityScore": places.popularity_score,
        "apiStatus": places.api_status,
    }


def _serialize_events(events_data: Optional[EventsData]):
    if events_data is None:
        return []
    results = []
    for event in events_data.events:
        results.append(
            {
                "id": event.event_id,
                "name": event.event_name,
                "start": event.start_date,
                "end": event.end_date,
                "venue": event.venue_name or event.venue_address,
                "url": event.event_url,
                "status": event.status,
            }
        )
    return results


def _serialize_result(
    result: AdSuccessResult,
    weather: Optional[WeatherData],
    traffic: Optional[TrafficData],
    places: Optional[PlacesData],
    events: Optional[EventsData],
    area: AreaData,
) -> Dict:
    return {
        "successScore": result.success_score,
        "successLevel": result.success_level,
        "audienceMatch": result.audience_match_score if result.audience_match_score is not None else None,
        "impressionsPerHour": result.impressions_per_hour,
        "targetAudienceSize": result.target_audience_size,
        "baseImpressionsPerHour": result.base_impressions_per_hour,
        "keyReasons": result.key_reasons,
        "personalizedTips": result.personalized_tips or [],
        "creativeRecommendations": result.creative_recommendations or [],
        "weather": _serialize_weather(weather),
        "traffic": _serialize_traffic(traffic),
        "places": _serialize_places(places),
        "events": _serialize_events(events),
        "refreshedAt": datetime.utcnow().isoformat() + "Z",
        "area": {
            "name": result.area_name,
            "population": area.population,
            "footfallDaily": area.footfall_daily,
        },
    }


_registry = Registry()

# Store recent analyses for analytics (in-memory, last 100 analyses)
_recent_analyses: deque = deque(maxlen=100)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}


@app.get("/api/campaigns")
def list_campaigns():
    return {
        "campaigns": _registry.campaigns_payload,
        "defaultCampaignId": _registry.campaigns_payload[0]["id"] if _registry.campaigns_payload else None,
    }


@app.get("/api/cities")
def list_cities():
    return {
        "cities": _registry.cities_payload,
        "defaultCityId": _registry.cities_payload[0]["id"] if _registry.cities_payload else None,
    }


@app.post("/api/predict")
def predict_success(payload: PredictRequest):
    city_name = _registry.resolve_city(payload.cityId)
    area_name = _registry.resolve_area(payload.cityId, payload.areaId)
    campaign = _registry.resolve_campaign(payload.campaignId)

    area_data = AreaDatabase.get_area(city_name, area_name)
    if area_data is None:
        raise HTTPException(status_code=404, detail=f"Area '{area_name}' not found for city '{city_name}'")

    weather_data: Optional[WeatherData] = None
    traffic_data: Optional[TrafficData] = None
    places_data: Optional[PlacesData] = None
    events_data: Optional[EventsData] = None

    try:
        weather_data = _weather_service.get_weather_data(area_data.center.lat, area_data.center.lon)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Weather API failed: %s", exc)

    try:
        traffic_data = _traffic_service.get_traffic_data(area_data.center.lat, area_data.center.lon)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Traffic API failed: %s", exc)

    try:
        places_data = _places_service.get_places_data(area_name, area_data.center.lat, area_data.center.lon)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Places API failed: %s", exc)

    # Eventbrite removed - not relevant for most users
    events_data = None

    result = AdSuccessCalculator.calculate_ad_success_score(
        area_name,
        area_data,
        weather_data or WeatherData(temperature=0, condition="Unknown", visibility=0, wind_kph=0, humidity=0),
        traffic_data or TrafficData(
            current_speed=0,
            free_flow_speed=0,
            congestion_level="Unknown",
            congestion_color="#cccccc",
            speed_ratio=0,
            confidence=0,
            delay_minutes=0,
            traffic_density=0,
            api_status="Unavailable",
            last_updated=datetime.utcnow().isoformat() + "Z",
        ),
        campaign=campaign,
        places_data=places_data,
    )

    serialized = _serialize_result(result, weather_data, traffic_data, places_data, events_data, area_data)
    
    # Store analysis for analytics
    _recent_analyses.append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "cityId": payload.cityId,
        "cityName": city_name,
        "areaId": payload.areaId,
        "areaName": area_name,
        "campaignId": payload.campaignId,
        "campaignName": campaign.name if campaign else "Generic",
        "successScore": result.success_score,
        "audienceMatch": result.audience_match_score if result.audience_match_score is not None else None,
        "impressionsPerHour": result.impressions_per_hour,
        "targetAudienceSize": result.target_audience_size,
        "footfallDaily": area_data.footfall_daily,
    })
    
    return serialized


@app.get("/api/analytics")
def get_analytics():
    """Return aggregated analytics from recent analyses."""
    if not _recent_analyses:
        return {
            "totalAnalyses": 0,
            "averageSuccessScore": 0,
            "totalImpressions": 0,
            "locationPerformance": [],
            "campaignPerformance": [],
            "recentAnalyses": [],
        }
    
    analyses = list(_recent_analyses)
    
    # Calculate aggregates
    total_analyses = len(analyses)
    avg_success_score = sum(a["successScore"] for a in analyses) / total_analyses if total_analyses > 0 else 0
    total_impressions = sum(a["impressionsPerHour"] for a in analyses)
    
    # Location performance (group by city + area)
    location_perf = {}
    for analysis in analyses:
        key = f"{analysis['cityName']} - {analysis['areaName']}"
        if key not in location_perf:
            location_perf[key] = {
                "location": key,
                "cityName": analysis["cityName"],
                "areaName": analysis["areaName"],
                "footfall": analysis["footfallDaily"],
                "successScore": analysis["successScore"],
                "audienceMatch": analysis["audienceMatch"],
                "count": 0,
            }
        location_perf[key]["count"] += 1
        # Average scores
        location_perf[key]["successScore"] = (location_perf[key]["successScore"] + analysis["successScore"]) / 2
        if analysis["audienceMatch"]:
            if location_perf[key]["audienceMatch"] is None:
                location_perf[key]["audienceMatch"] = analysis["audienceMatch"]
            else:
                location_perf[key]["audienceMatch"] = (location_perf[key]["audienceMatch"] + analysis["audienceMatch"]) / 2
    
    # Campaign performance
    campaign_perf = {}
    for analysis in analyses:
        campaign_name = analysis["campaignName"]
        if campaign_name not in campaign_perf:
            campaign_perf[campaign_name] = {
                "campaign": campaign_name,
                "successScore": analysis["successScore"],
                "audienceMatch": analysis["audienceMatch"],
                "count": 0,
            }
        campaign_perf[campaign_name]["count"] += 1
        campaign_perf[campaign_name]["successScore"] = (campaign_perf[campaign_name]["successScore"] + analysis["successScore"]) / 2
        if analysis["audienceMatch"]:
            if campaign_perf[campaign_name]["audienceMatch"] is None:
                campaign_perf[campaign_name]["audienceMatch"] = analysis["audienceMatch"]
            else:
                campaign_perf[campaign_name]["audienceMatch"] = (campaign_perf[campaign_name]["audienceMatch"] + analysis["audienceMatch"]) / 2
    
    return {
        "totalAnalyses": total_analyses,
        "averageSuccessScore": round(avg_success_score, 1),
        "totalImpressions": int(total_impressions),
        "locationPerformance": list(location_perf.values()),
        "campaignPerformance": list(campaign_perf.values()),
        "recentAnalyses": analyses[-10:],  # Last 10 analyses
    }


@app.get("/")
def root():
    return {
        "message": "BritMetrics API is running.",
        "campaignsEndpoint": "/api/campaigns",
        "citiesEndpoint": "/api/cities",
        "predictionEndpoint": "/api/predict",
        "analyticsEndpoint": "/api/analytics",
    }
