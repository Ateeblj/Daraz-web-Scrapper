import requests
import pandas as pd
import json
import time

# ==============================
# Load cookies and headers from JSON
# ==============================
with open("daraz_cookies_headers.json", "r") as f:
    data = json.load(f)
cookies = data.get("cookies", {})
headers = data.get("headers", {})

# ==============================
# Product search
# ==============================
search_query = input("🔍 Enter the product you want to search for: ").strip()

# Base AJAX URL
base_url = "https://www.daraz.pk/catalog/?ajax=true&page={page}&q={query}"

# Settings
products = []
seen_first_product = None
max_pages = 200
save_every = 5
retries = 3

page = 1
while page <= max_pages:
    print(f"🔹 Scraping page {page}...")

    for attempt in range(retries):
        try:
            url = base_url.format(page=page, query=search_query.replace(" ", "%20"))
            response = requests.get(url, headers=headers, cookies=cookies, timeout=15)
            data = response.json()
            break
        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    else:
        print(f"❌ Skipping page {page} after {retries} failed attempts.")
        page += 1
        continue

    items = data.get("mods", {}).get("listItems", [])
    if not items:
        print("✅ No more products found. Stopping.")
        break

    # Stop on duplicate first product (looped pages)
    if seen_first_product == items[0].get("itemId"):
        print("⚠️ Duplicate page detected. Stopping.")
        break
    seen_first_product = items[0].get("itemId")

    # Collect all product details
    for item in items:
        raw_url = item.get("productUrl") or item.get("itemUrl")
        if raw_url:
            if raw_url.startswith("//"):
                product_url = "https:" + raw_url
            elif raw_url.startswith("/"):
                product_url = "https://www.daraz.pk" + raw_url
            else:
                product_url = raw_url
        else:
            product_url = None

        products.append({
            "Name": item.get("name"),
            "Brand": item.get("brandName"),
            "Price": item.get("price"),
            "Original Price": item.get("originalPrice"),
            "Discount": item.get("discount"),
            "Rating": item.get("ratingScore"),
            "Total Reviews": item.get("review"),
            "Seller": item.get("sellerName"),
            "Product URL": product_url,
            "Image": item.get("image"),
            "Product ID": item.get("itemId"),
            "Shop ID": item.get("sellerId"),
            "Stock Status": item.get("stock"),
            "Shipping Info": item.get("shipping"),
            "Badge Info": item.get("badge"),
            "Promotion": item.get("promotion"),
        })

    # ✅ Save progress every N pages
    if page % save_every == 0:
        filename = f"daraz_{search_query.replace(' ', '_')}.xlsx"
        pd.DataFrame(products).to_excel(filename, index=False)
        print(f"💾 Progress saved at page {page} ({len(products)} products)")

    page += 1
    time.sleep(1)  # polite delay

# Final save
filename = f"daraz_{search_query.replace(' ', '_')}.xlsx"
pd.DataFrame(products).to_excel(filename, index=False)
print(f"✅ Finished! Scraped {len(products)} products for '{search_query}'.")
