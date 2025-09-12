import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def save_cookies_and_headers():
    # Normal Chrome (non-headless, so Daraz thinks it's real)
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Step 1: Go to homepage
        driver.get("https://www.daraz.pk/")
        time.sleep(5)  # let homepage load

        # Step 2: Go to dummy search page (forces token refresh)
        driver.get("https://www.daraz.pk/catalog/?q=test")
        time.sleep(10)  # wait long enough for API calls to fire

        # Step 3: Extract cookies
        cookies = {c['name']: c['value'] for c in driver.get_cookies()}

        # Step 4: Extract headers (at least User-Agent and referer)
        user_agent = driver.execute_script("return navigator.userAgent;")
        headers = {
            "user-agent": user_agent,
            "referer": "https://www.daraz.pk/catalog/?q=test",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9"
        }

        # Step 5: Save to file
        with open("daraz_cookies_headers.json", "w", encoding="utf-8") as f:
            json.dump({"cookies": cookies, "headers": headers}, f, indent=4)

        print("✅ Cookies + headers saved to daraz_cookies_headers.json")

    finally:
        driver.quit()


if __name__ == "__main__":
    save_cookies_and_headers()
