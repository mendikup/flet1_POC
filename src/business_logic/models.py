"""
Data models for weather information.
"""
from dataclasses import dataclass
from typing import List


@dataclass
class HourlyForecast:
    """Hourly weather forecast data."""
    time: str
    icon: str
    temp: int


@dataclass
class DailyForecast:
    """Daily weather forecast data."""
    day: str
    humidity: int
    high: int
    low: int


@dataclass
class WeatherData:
    """Complete weather data for a city."""
    city_name: str
    current_temp: int
    condition: str
    aqi: int
    uv_index: int
    humidity: int
    hourly: List[HourlyForecast]
    daily: List[DailyForecast]