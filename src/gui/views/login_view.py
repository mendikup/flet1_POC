import flet as ft
import globals


@ft.component
def LoginView(on_login_success):
    # Hooks - משתני המצב
    username, set_username = ft.use_state("")
    password, set_password = ft.use_state("")
    error, set_error = ft.use_state("")

    def handle_login(e):
        if username and password:
            on_login_success()
        else:
            set_error("נא להזין שם משתמש וסיסמה")

    return ft.Container(
        expand=True,
        # שימוש באובייקט Alignment מפורש למניעת שגיאות Serialization
        alignment=ft.Alignment(0, 0),

        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("התחברות", size=30, weight=ft.FontWeight.BOLD, color=globals.TEXT_COLOR),

                ft.TextField(
                    key="username_input",
                    label="שם משתמש",
                    value=username,  # <<< התיקון: קישור ל-State
                    rtl=True,
                    on_change=lambda e: set_username(e.control.value)
                ),

                ft.TextField(
                    key="password_input",
                    label="סיסמה",
                    value=password,  # <<< התיקון: קישור ל-State
                    password=True,
                    rtl=True,
                    on_change=lambda e: set_password(e.control.value)
                ),

                ft.Text(error, color=ft.Colors.RED, size=12, visible=bool(error)),

                # כפתור עם content כדי לעקוף בעיות תאימות
                ft.ElevatedButton(
                    key="login_btn",
                    content=ft.Text("הכנס", color=ft.Colors.BLACK),
                    on_click=handle_login,
                    style=ft.ButtonStyle(
                        bgcolor=globals.ACCENT_COLOR,
                    )
                )
            ]
        ),
        **globals.GLASS_STYLE
    )