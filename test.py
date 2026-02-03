import flet as ft
from main import main as flet_main
import threading
import time
from playwright.sync_api import sync_playwright
import unittest


def run_flet_app():
    # הרצת האפליקציה במצב HTML - זה מה שמאפשר ל-Playwright לראות אלמנטים
    ft.app(target=flet_main, view=ft.AppView.WEB_BROWSER, port=8550, web_renderer=ft.WebRenderer.HTML)


class TestFletPlaywright(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # הפעלת האפליקציה ב-Thread נפרד כדי שהטסט יוכל לרוץ במקביל
        cls.thread = threading.Thread(target=run_flet_app, daemon=True)
        cls.thread.start()
        time.sleep(5)  # זמן המתנה לעליית השרת

    def test_navigation(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # headless=False כדי שתראה את הדפדפן עובד
            page = browser.new_page()
            page.goto("http://localhost:8550")

            # Playwright מוצא את הכפתור לפי הטקסט שלו (בזכות ה-HTML Renderer)
            btn_nav = page.get_by_role("button", name="להגדרות")
            btn_nav.wait_for(state="visible")
            btn_nav.click()

            # המתנה קצרה לשינוי הנתיב
            time.sleep(1)

            # בדיקה שהנתיב (URL) השתנה
            self.assertIn("/settings", page.url)
            print("✓ Playwright הצליח לנווט בהצלחה!")

            browser.close()


if __name__ == "__main__":
    unittest.main()