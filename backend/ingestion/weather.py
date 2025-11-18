"""
Weather and Air Quality data integration
"""
import httpx
from datetime import datetime
from typing import Dict, Any, Optional
import logging
from api.config import settings

logger = logging.getLogger(__name__)


class WeatherClient:
    """Client for fetching weather data from OpenWeatherMap"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/3.0"

    async def get_current_weather(
        self,
        lat: float,
        lon: float
    ) -> Dict[str, Any]:
        """Get current weather data"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/weather",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key,
                        "units": "metric"
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch weather data: {e}")
            return {}

    async def get_air_quality(
        self,
        lat: float,
        lon: float
    ) -> Dict[str, Any]:
        """Get air quality data"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/air_pollution",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch air quality data: {e}")
            return {}

    async def get_uv_index(
        self,
        lat: float,
        lon: float
    ) -> Dict[str, Any]:
        """Get UV index data"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/uvi",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "appid": self.api_key
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch UV index: {e}")
            return {}


class AirQualityClient:
    """Client for fetching air quality data from AirNow"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.AIRNOW_API_KEY
        self.base_url = "https://www.airnowapi.org/aq"

    async def get_current_aqi(
        self,
        lat: float,
        lon: float
    ) -> Dict[str, Any]:
        """Get current AQI data"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/observation/latLong/current/",
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "format": "application/json",
                        "API_KEY": self.api_key
                    }
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch AQI data: {e}")
            return {}


def normalize_weather_data(
    weather_data: Dict[str, Any],
    aqi_data: Dict[str, Any],
    uv_data: Dict[str, Any]
) -> list[Dict[str, Any]]:
    """
    Normalize weather and environmental data into standard metric format

    Args:
        weather_data: Raw weather data from API
        aqi_data: Raw AQI data from API
        uv_data: Raw UV index data from API

    Returns:
        List of normalized metrics ready for database insertion
    """
    normalized_metrics = []
    timestamp = datetime.now()

    # TODO: Implement data normalization
    # Extract temperature, humidity, pressure, AQI, UV index, etc.

    return normalized_metrics
