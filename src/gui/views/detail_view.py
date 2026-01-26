import flet as ft
import globals


@ft.component
def DetailView(weather_data, on_back):
    weather = weather_data
    selected_tab, set_selected_tab = ft.use_state(0)

    # --- פונקציות עזר לתוכן ---

    def build_hourly():
        return ft.Container(
            height=160,
            padding=ft.padding.only(top=10, bottom=10),
            # מגדיר שהתוכן בפנים הוא RTL (מימין לשמאל)
            rtl=True,
            content=ft.Row(
                scroll="auto",
                spacing=15,
                # --- התיקון לקפיצה ---
                # במקום לנסות למרכז (מה שגורם לקפיצה כשיש גלילה),
                # אנחנו מצמידים להתחלה (ימין ב-RTL)
                alignment=ft.MainAxisAlignment.START,
                # ---------------------
                controls=[
                    ft.Container(
                        width=80,
                        height=120,
                        border_radius=15,
                        bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                        border=ft.border.all(1, ft.Colors.with_opacity(0.2, ft.Colors.WHITE)),
                        content=ft.Column(
                            spacing=5,
                            # יישור התוכן בתוך הכרטיסייה עצמה
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(h.time, size=14, weight=ft.FontWeight.W_500),
                                ft.Icon(h.icon, color=globals.ACCENT_COLOR, size=32),
                                ft.Text(f"{h.temp}°", size=18, weight=ft.FontWeight.BOLD)
                            ]
                        )
                    ) for h in weather.hourly
                ]
            )
        )

    def build_daily():
        return ft.Column(
            scroll="auto",
            controls=[
                ft.Container(
                    padding=15,
                    margin=ft.margin.only(bottom=10),
                    border_radius=10,
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
                    content=ft.Row(
                        alignment="spaceBetween",
                        rtl=True,  # וודא שהשורה מוצגת מימין לשמאל
                        controls=[
                            ft.Text(day.day, width=70, weight=ft.FontWeight.BOLD),
                            ft.Row([
                                ft.Icon(ft.Icons.WATER_DROP, size=16, color=globals.ACCENT_COLOR),
                                ft.Text(f"{day.humidity}%")
                            ], width=70),
                            ft.Text(f"{day.high}° / {day.low}°", width=90, text_align="right")  # ב-RTL זה יהיה בשמאל
                        ]
                    )
                ) for day in weather.daily
            ]
        )

    def _detail_card(title, value, icon, is_progress):
        content_controls = [
            ft.Icon(icon, color=globals.ACCENT_COLOR, size=28),
            ft.Text(title, size=14, color=ft.Colors.WHITE70),
            ft.Text(str(value), size=22, weight=ft.FontWeight.BOLD)
        ]

        if is_progress:
            try:
                progress_val = int(value) / 300
            except:
                progress_val = 0.5
            content_controls.append(
                ft.ProgressBar(value=progress_val, color=globals.ACCENT_COLOR, width=60, height=6)
            )

        return ft.Container(
            width=110,
            height=140,
            bgcolor=globals.GLASS_STYLE["bgcolor"],
            border_radius=globals.GLASS_STYLE["border_radius"],
            border=globals.GLASS_STYLE["border"],
            padding=globals.GLASS_STYLE["padding"],
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
                controls=content_controls
            )
        )

    def build_details():
        return ft.Row(
            alignment="spaceEvenly",
            rtl=True,
            controls=[
                _detail_card("AQI", weather.aqi, ft.Icons.AIR, True),
                _detail_card("UV Index", weather.uv_index, ft.Icons.WB_SUNNY, False),
                _detail_card("לחות", f"{weather.humidity}%", ft.Icons.WATER_DROP, False)
            ]
        )

    # --- כפתור טאב ---
    def TabButton(text, index):
        is_selected = selected_tab == index
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            border_radius=20,
            bgcolor=globals.ACCENT_COLOR if is_selected else ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
            on_click=lambda _: set_selected_tab(index),
            animate=ft.Animation(300, "easeOut"),
            content=ft.Text(
                text,
                color=ft.Colors.BLACK if is_selected else ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD if is_selected else ft.FontWeight.NORMAL
            )
        )

    def get_tab_content():
        if selected_tab == 0:
            return build_hourly()
        elif selected_tab == 1:
            return build_daily()
        elif selected_tab == 2:
            return build_details()
        return ft.Text("Error")

    # --- Render ---
    return ft.Container(
        expand=True,
        image=ft.DecorationImage(
            src=globals.get_city_image(weather.city_name),
            fit="cover",
            opacity=1.0
        ),
        content=ft.Stack(
            controls=[
                # גרדיאנט
                ft.Container(
                    gradient=ft.LinearGradient(
                        begin=ft.Alignment(0, -1),
                        end=ft.Alignment(0, 1),
                        colors=[
                            ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                            ft.Colors.with_opacity(0.85, ft.Colors.BLACK)
                        ],
                    ),
                    expand=True
                ),

                ft.Column(
                    expand=True,
                    rtl=True,  # וודא שכל העמוד הראשי ב-RTL
                    controls=[
                        # Header
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    on_click=lambda _: on_back(),
                                    icon_color=ft.Colors.WHITE,
                                    icon_size=30
                                )
                            ]
                        ),

                        # City Info
                        ft.Container(
                            padding=20,
                            content=ft.Column([
                                ft.Text(weather.city_name, size=40, weight=ft.FontWeight.BOLD),
                                ft.Text(f"{weather.current_temp}°", size=70, weight=ft.FontWeight.BOLD),
                                ft.Text(weather.condition, size=24, color=globals.ACCENT_COLOR,
                                        weight=ft.FontWeight.W_500)
                            ])
                        ),

                        # Tabs Switcher
                        ft.Container(
                            padding=ft.padding.symmetric(horizontal=20),
                            margin=ft.margin.only(bottom=10),
                            content=ft.Row(
                                alignment="center",
                                spacing=10,
                                rtl=True,
                                controls=[
                                    TabButton("שעתי", 0),
                                    TabButton("יומי", 1),
                                    TabButton("פרטים", 2),
                                ]
                            )
                        ),

                        # Content
                        ft.Container(
                            expand=True,
                            padding=20,
                            # --- זה החלק שאחראי על האנימציה היפה! ---
                            content=ft.AnimatedSwitcher(
                                content=ft.Container(
                                    key=f"tab_{selected_tab}",  # המפתח משתנה -> טריגר לאנימציה
                                    content=get_tab_content()
                                ),
                                transition=ft.AnimatedSwitcherTransition.FADE,  # סוג המעבר (עמעום)
                                duration=200,  # משך האנימציה (300 מילישניות)
                            )
                        )
                    ]
                )
            ]
        )
    )