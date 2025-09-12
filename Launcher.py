import subprocess
import sys
import time
import json
import os

COOKIES_FILE = "daraz_cookies_headers.json"

def run_program(file_name):
    try:
        print(f"🚀 Running {file_name}...")
        result = subprocess.run([sys.executable, file_name], check=True)
        if result.returncode == 0:
            print(f"✅ {file_name} finished successfully!\n")
            return True
        else:
            print(f"⚠️ {file_name} exited with code {result.returncode}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {file_name}: {e}")
        return False

def validate_json(file_path):
    if not os.path.exists(file_path):
        print(f"❌ JSON file not found: {file_path}")
        return False
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Check if essential keys exist
        if "cookies" in data and "headers" in data:
            print(f"✅ Cookies and headers JSON is valid.")
            return True
        else:
            print(f"❌ JSON file missing 'cookies' or 'headers' keys.")
            return False
    except Exception as e:
        print(f"❌ Failed to read JSON file: {e}")
        return False

if __name__ == "__main__":
    print("==== Daraz Scraper Launcher ====\n")

    # Step 1: Run Json.py
    if not run_program("Json.py"):
        print("❌ Json.py failed. Cannot continue scraping.")
        sys.exit(1)

    # Step 2: Validate the JSON
    if not validate_json(COOKIES_FILE):
        print("❌ Invalid cookies JSON. Aborting scraping.")
        sys.exit(1)

    # Step 3: Small pause
    print("\n⏳ Preparing to start Scrapper.py...\n")
    time.sleep(2)

    # Step 4: Run Scrapper.py
    if not run_program("Scrapper.py"):
        print("❌ Scrapper.py failed.")
        sys.exit(1)

    print("🎉 All tasks completed successfully!")
