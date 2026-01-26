"""
Weather service for fetching weather data.
"""
import flet as ft
from .models import WeatherData, HourlyForecast, DailyForecast


class WeatherService:
    """Service class for fetching weather data."""

    @staticmethod
    def get_weather(city: str) -> WeatherData:
        """
        Fetch weather data for a given city.

        Args:
            city: Name of the city

        Returns:
            WeatherData object with complete weather information
        """
        # Mock hourly forecast data
        hourly_data = [
            HourlyForecast("12:00", ft.Icons.WB_SUNNY, 28),
            HourlyForecast("13:00", ft.Icons.WB_SUNNY, 29),
            HourlyForecast("14:00", ft.Icons.CLOUD, 30),
            HourlyForecast("15:00", ft.Icons.CLOUD, 29),
            HourlyForecast("16:00", ft.Icons.CLOUD_QUEUE, 28),
            HourlyForecast("17:00", ft.Icons.WB_CLOUDY, 27),
            HourlyForecast("18:00", ft.Icons.NIGHTS_STAY, 25),
            HourlyForecast("19:00", ft.Icons.NIGHTS_STAY, 24),
        ]

        # Mock daily forecast data
        daily_data = [
            DailyForecast("ראשון", 65, 32, 22),
            DailyForecast("שני", 70, 30, 21),
            DailyForecast("שלישי", 75, 28, 20),
            DailyForecast("רביעי", 68, 29, 21),
            DailyForecast("חמישי", 72, 31, 22),
        ]

        # Mock weather data based on city
        conditions = {
            "תל אביב": "שמשי",
            "ירושלים": "מעונן חלקית",
            "חיפה": "שמשי",
            "אילת": "שמש וחם"
        }

        temps = {
            "תל אביב": 28,
            "ירושלים": 25,
            "חיפה": 27,
            "אילת": 35
        }

        aqis = {
            "תל אביב": 45,
            "ירושלים": 38,
            "חיפה": 42,
            "אילת": 30
        }

        return WeatherData(
            city_name=city,
            current_temp=temps.get(city, 26),
            condition=conditions.get(city, "שמשי"),
            aqi=aqis.get(city, 40),
            uv_index=7,
            humidity=65,
            hourly=hourly_data,
            daily=daily_data
        )