import flet as ft

@ft.component
def App():
    page = ft.context.page
    appbar_color, set_color = ft.use_state(ft.Colors.BLUE)
    route = page.route

    # פונקציות אסינכרוניות לניווט ושינוי מצב
    async def go_settings():
        await page.push_route("/settings")

    async def toggle_color():
        new_color = ft.Colors.RED if appbar_color == ft.Colors.BLUE else ft.Colors.BLUE
        set_color(new_color)

    home_view = ft.View(
        route="/",
        appbar=ft.AppBar(title=ft.Text("דף הבית"), bgcolor=appbar_color, key="home_appbar"),
        controls=[
            # שימוש ב-run_task מבטיח שהפעולה תרוץ ברקע בצורה תקינה
            ft.Button("שנה צבע",
                      on_click=lambda _: page.run_task(toggle_color),
                      key="btn_color"),
            ft.Button("להגדרות",
                      on_click=lambda _: page.run_task(go_settings),
                      key="btn_nav")
        ]
    )

    settings_view = ft.View(
        route="/settings",
        appbar=ft.AppBar(title=ft.Text("הגדרות"), key="settings_appbar"),
        controls=[
            ft.Button("חזור",
                      on_click=lambda _: page.run_task(page.push_route, "/"),
                      key="btn_back")
        ]
    )

    return [home_view] if route == "/" else [home_view, settings_view]

def main(page: ft.Page):
    page.render_views(App)

if __name__ == "__main__":
    ft.run(main)