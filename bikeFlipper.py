import requests
import json
import csv
import os
import time
from openai import OpenAI
client = OpenAI(api_key="sk-proj-e0uiUn0xUEIT2bMAwJZMT3BlbkFJJ342ylsoOlPmV7ph8N0Z")
pastMessages = [
    {"role":"system","content": "You are an experienced bike reseller, you will process images and information and tell me whether it is worth buying. The format that you'll answer with is: QUICK BUY - if you think that the bike is a complete steal, BUY - if you think the bike is worth reselling, NO - if you think the bike is not worth reselling "}
]

CSV_FILE = "bikeDeals.csv"

# --- COOKIES (keep fresh) ---
cookies = {
    "datr": "wXyEZscZtifXudZgwbkJ8C_t",
    "sb": "1HyEZuoCMTs76RX-MAIZKWK8",
    "dpr": "1.25",
    "c_user": "61574687576060",
    "oo": "v1",
    "fr": "10idTSgY9hh51sb1I.AWcdG6AYyuMeP5JLG0VtUarNRSGxDZUgCDiGaU0oYgW-8YJcd-M.Bn9j61..AAA.0.0.Bn9j61.AWf0WQoFqEaZIjehEz7X5ngKUy0",
    "ar_debug": "1",
    "xs": "31:DYx8lSwyIs_JCg:2:1742755659:-1:-1::AcUF45uIxG9f4lwXE0fsCUmWLczJq_9CJZyZjhYMnA4",
    "wd": "1536x730",
    "presence": 'C{"t3":[],"utc3":1744210718131,"v":1}',
}

# --- HEADERS ---
headers = {
    "authority": "www.facebook.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.facebook.com",
    "referer": "https://www.facebook.com/marketplace/106058999434808/search?sortBy=creation_time_descend&query=bike&exact=false",
    "sec-ch-prefers-color-scheme": "dark",
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "sec-ch-ua-full-version-list": '"Chromium";v="122.0.6261.129", "Not(A:Brand";v="24.0.0.0", "Google Chrome";v="122.0.6261.129"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua-platform-version": '"15.0.0"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "x-asbd-id": "359341",
    "x-fb-friendly-name": "CometMarketplaceSearchContentContainerQuery",
    "x-fb-lsd": "XbfZ_DLBBQPi4uemJdJKKw"
}

# --- VARIABLES ---
variables = {
    "buyLocation": {
        "latitude": 51.7359,
        "longitude": 0.4693
    },
    "contextual_data": None,
    "count": 24,
    "cursor": None,
    "params": {
        "bqf": {
            "callsite": "COMMERCE_MKTPLACE_WWW",
            "query": "bike"
        },
        "browse_request_params": {
            "commerce_enable_local_pickup": True,
            "commerce_enable_shipping": True,
            "commerce_search_and_rp_available": True,
            "commerce_search_and_rp_category_id": [],
            "commerce_search_and_rp_condition": None,
            "commerce_search_and_rp_ctime_days": "20187;20186",
            "filter_location_latitude": 51.7359,
            "filter_location_longitude": 0.4693,
            "filter_price_lower_bound": 0,
            "filter_price_upper_bound": 214748364700,
            "filter_radius_km": 10,
            "commerce_search_sort_by": "creation_time_descend"
        },
        "custom_request_params": {
            "browse_context": None,
            "contextual_filters": [],
            "referral_code": None,
            "saved_search_strid": None,
            "search_vertical": "C2C",
            "seo_url": None,
            "surface": "SEARCH",
            "virtual_contextual_filters": []
        }
    },
    "savedSearchID": None,
    "savedSearchQuery": "bike",
    "scale": 1,
    "shouldIncludePopularSearches": False,
    "topicPageParams": {
        "location_id": "106058999434808",
        "url": None
    }
}


data = {
    "av": "61574687576060",
    "fb_dtsg": "NAcMoujs1XiDY9ms5xl0b_3lzADZ04nm1uqT2OPYlhvne8-s2xwTA-A:31:1742755659",
    "doc_id": "9277343979049234",
    "variables": json.dumps(variables),
    "server_timestamps": "true"
}
while True:
    # --- Load existing story_keys (used to avoid duplicates) ---
    existing_ids = set()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_ids.add(row["ID"])

    # --- Fetch new listings ---
    response = requests.post("https://www.facebook.com/api/graphql/", headers=headers, cookies=cookies, data=data)

    try:
        results = response.json()
        listings = results["data"]["marketplace_search"]["feed_units"]["edges"]

        new_rows = []
        for item in listings:
            node = item["node"]
            story_key = node.get("story_key", "")
            listing = node.get("listing", {})

            if story_key in existing_ids:
                continue  # Already stored, skip

            title = listing.get("marketplace_listing_title", "N/A")
            price = listing.get("listing_price", {}).get("formatted_amount", "N/A")
            location = listing.get("location", {}).get("reverse_geocode", {}).get("city", "Unknown")
            image_url = listing.get("primary_listing_photo", {}).get("image", {}).get("uri", "N/A")
            post_url = f"https://www.facebook.com/marketplace/item/{story_key}" if story_key else "N/A"

            # Print to terminal
            print(f"🆕 New Listing: {title}")
            print(f"💷 {price} | 📍 {location}")
            print(f"🔗 {post_url}")
            print(f"🖼️  {image_url}\n{'-'*60}")

            new_rows.append({
                "ID": story_key,
                "Title": title,
                "Price": price,
                "Location": location,
                "Image URL": image_url,
                "Post URL": post_url
            })

        if new_rows:
            file_exists = os.path.exists(CSV_FILE)
            with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["ID", "Title", "Price", "Location", "Image URL", "Post URL"])
                if not file_exists:
                    writer.writeheader()
                writer.writerows(new_rows)

            print(f"[✅] Added {len(new_rows)} new listings to {CSV_FILE}")
        else:
            print("[ℹ️] No new listings found.")

    except Exception as e:
        print("[❌] Failed to parse response:", e)
        print(response.text)
    print("scan completed")
    time.sleep(60) # every minute