import flet as ft

# Theme Constants
GLASS_COLOR = ft.Colors.with_opacity(0.15, ft.Colors.WHITE)
GLASS_BLUR = 20
TEXT_COLOR = ft.Colors.WHITE
ACCENT_COLOR = ft.Colors.CYAN_ACCENT

GLASS_STYLE = {
    "bgcolor": GLASS_COLOR,
    "blur": ft.Blur(GLASS_BLUR, GLASS_BLUR),
    "border_radius": 15,
    "border": ft.border.all(1, ft.Colors.with_opacity(0.3, ft.Colors.WHITE)),
    "padding": 10,
}

# תמונות ישירות מ-CDN (קישורים יציבים)
CITY_IMAGES_MAP = {"Tel Aviv": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Tel_Aviv_Beach.jpg",
    "Jerusalem": "https://upload.wikimedia.org/wikipedia/commons/d/d4/Jerusalem_Dome_of_the_rock_BW_14.JPG",
    "Haifa": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Haifa_Gardens.jpg",
    "Eilat": "https://upload.wikimedia.org/wikipedia/commons/5/5b/Eilat_coast.jpg"
}

# רקע שמיים כללי
WEATHER_BACKGROUND = "https://images.unsplash.com/photo-1534088568595-a066f410bcda?ixlib=rb-4.0.3&q=85&fm=jpg&crop=entropy&cs=srgb&w=1200"

def get_city_image(city_name: str) -> str:
    return CITY_IMAGES_MAP.get(city_name, WEATHER_BACKGROUND)