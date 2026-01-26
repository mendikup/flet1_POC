import flet as ft
import globals
from src.gui.views.login_view import LoginView
from src.gui.views.dashboard_view import DashboardView
from src.gui.views.detail_view import DetailView
from business_logic.weather_service import WeatherService


@ft.component
def AppRoot():
    current_route, set_route = ft.use_state("/login")
    weather_data, set_weather_data = ft.use_state(None)

    def nav_to_dashboard():
        set_route("/dashboard")

    def handle_city_select(city_name):
        data = WeatherService.get_weather(city_name)
        set_weather_data(data)
        set_route(f"/weather/{city_name}")

    def nav_back():
        set_route("/dashboard")

    def get_screen():
        if current_route == "/login":
            return LoginView(on_login_success=nav_to_dashboard)
        elif current_route == "/dashboard":
            return DashboardView(on_city_select=handle_city_select)
        elif current_route.startswith("/weather") and weather_data:
            return DetailView(weather_data=weather_data, on_back=nav_back)
        else:
            return ft.Text("404")

    # --- Container הראשי ---
    return ft.Container(
        expand=True,
        # תיקון המסך החצוי: יישור למרכז
        alignment=ft.Alignment(0, 0),

        # רקע כללי של מזג אוויר
        image=ft.Image(
            src=globals.WEATHER_BACKGROUND,
            fit="cover",
            opacity=0.5
        ),
        bgcolor=ft.Colors.BLACK,

        content=get_screen()
    )


def main(page: ft.Page):
    page.title = "Weather App Pro"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0

    # הגדרת פונט
    page.fonts = {
        "Roboto": "https://github.com/google/fonts/raw/main/apache/roboto/Roboto-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="Roboto")

    page.render(AppRoot)


if __name__ == "__main__":
    ft.run(main)