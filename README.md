📦 Daraz Scraper

This project lets you scrape product data from Daraz.pk reliably using Selenium + Requests.
It first extracts fresh cookies & headers (including _m_h5_tk tokens) with Selenium, saves them to a JSON file, and then uses those credentials in the scraper to fetch product data.

📂 Project Structure
DarazScraper/
│
├── launcher.py                 # Main entrypoint (runs setup + scraper)
├── json.py (or cookies_setup.py)  # Gets fresh cookies & headers via Selenium
├── scraper.py                  # Actual scraper (reads cookies/headers JSON)
├── daraz_cookies_headers.json  # Auto-generated cookies + headers
│
├── chromedriver-win64/         # ChromeDriver folder
│   └── chromedriver.exe
│
└── venv/ (optional)            # Python virtual environment

🔧 Requirements

Google Chrome (latest version)
👉 Download Chrome

ChromeDriver (matching your Chrome version)
👉 Chrome for Testing Downloads

Place the chromedriver.exe inside chromedriver-win64/.

Python 3.9+ (installed & added to PATH)

Dependencies (install once in your project folder):

pip install selenium webdriver-manager requests openpyxl

🚀 How It Works

json.py

Launches Chrome (non-headless).

Opens Daraz.pk search page.

Extracts cookies + headers (_m_h5_tk, _m_h5_tk_enc, User-Agent, etc.).

Saves them into daraz_cookies_headers.json.

scraper.py

Reads cookies & headers from JSON.

Makes requests to Daraz’s API.

Saves results into Excel.

launcher.py

Automatically runs json.py first.

Then runs scraper.py.

One file to rule them all ✨

▶️ Usage
Step 1 — Clone / Copy Project

Place all files in one folder (e.g., D:\DarazScraper).

Step 2 — Run Launcher
python launcher.py


OR just double-click launcher.py if .py is associated with Python.

First, it will open Chrome, fetch cookies, and save them.

Then, it will start scraping products and saving them to Excel.

📝 Notes

If Daraz updates their tokens or blocks scraping, simply delete daraz_cookies_headers.json and rerun launcher.py to refresh cookies.

Keep Chrome + ChromeDriver versions matched.

You can adjust search queries inside scraper.py.
