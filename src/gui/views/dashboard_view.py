import flet as ft
import globals

CITIES = ["Tel Aviv", "Jerusalem", "Haifa", "Eilat"]


@ft.component
def DashboardView(on_city_select):
    def render_city_card(city):
        return ft.Container(
            key=f"city_card_{city.lower().replace(' ', '_')}",
            height=150,
            width=150,
            # --- התיקון הגדול ---
            # במקום image_src, משתמשים ב-image עם DecorationImage
            image=ft.DecorationImage(
                src=globals.get_city_image(city),
                fit="cover",  # שימוש במחרוזת למניעת שגיאות Import
            ),
            # --------------------
            border_radius=15,
            padding=10,
            on_click=lambda _: on_city_select(city),
            # שימוש ב-Alignment מפורש (מונע קריסות)
            alignment=ft.Alignment(0, 1),
            content=ft.Container(
                bgcolor=ft.Colors.with_opacity(0.6, ft.Colors.BLACK),
                padding=5,
                border_radius=5,
                content=ft.Text(
                    city,
                    color=globals.TEXT_COLOR,
                    weight=ft.FontWeight.BOLD,
                    text_align="center"
                )
            )
        )

    return ft.Column(
        expand=True,
        controls=[
            ft.Container(
                padding=20,
                content=ft.Text(
                    "בחר עיר",
                    size=24,
                    color=globals.TEXT_COLOR,
                    text_align="right"
                )
            ),
            ft.Row(
                wrap=True,
                alignment="center",
                controls=[render_city_card(city) for city in CITIES]
            )
        ]
    )