import requests
import json
import csv
import os
import time
from datetime import datetime, timedelta
from aiAnalyser import evaluateListing
from telegram import sendMessage
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_facebook_day_ids(days=30, reference_day_id=20198, reference_date=datetime(2025, 4, 19)):
    today = datetime.today()
    delta_days = (today - reference_date).days
    today_id = reference_day_id + delta_days
    return ";".join(str(today_id - i) for i in range(days))

ctime_days_param = get_facebook_day_ids()
CSV_FILE = "bikeDeals.csv"

cookies = {
    "sb": "1HyEZuoCMTs76RX-MAIZKWK8",
    "dpr": "1.25",
    "datr": "tTUGaJHGSDSMYjhsm7av_IGl",
    "locale": "en_GB",
    "oo": "v1",
    "c_user": "100067986370644",
    "xs": "30%3AhCdhIjX-N5ewSA%3A2%3A1745959832%3A-1%3A-1%3A%3AAcV0RDYZvVFVhOhGMnOzRfC7wrvdmmrLrookDZO4Mw",
    "fr": "0BYIcy3wXhEX9am23.AWfVf9b-qSMyNaImB2kiwUd8N3LxDrWfIFyuYVuTwvQbGbEbT5c.BoETuX..AAA.0.0.BoETuX.AWfZBG6xTyjs4-zye01Pp15LvtM",
    "presence": 'C{"t3":[],"utc3":1745959841825,"v":1}',
    "wd": "618x730"
}


headers = {
    "authority": "www.facebook.com",
    "accept": "*/*",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://www.facebook.com",
    "referer": "https://www.facebook.com/marketplace/106058999434808/search?sortBy=creation_time_descend&query=bike&exact=false",
    "user-agent": "Mozilla/5.0...",
    "x-asbd-id": "359341",
    "x-fb-friendly-name": "CometMarketplaceSearchContentContainerQuery",
    "x-fb-lsd": "-D93_l-SrtZX_03XzvGGYy"
}

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
            "commerce_search_and_rp_ctime_days": ctime_days_param,
            "filter_location_latitude": 51.7359,
            "filter_location_longitude": 0.4693,
            "filter_location": {
                "latitude": 51.7359,
                "longitude": 0.4693,
                "radius_km": 10
            },
            "filter_price_lower_bound": 0,
            "filter_price_upper_bound": 214748364700,
            "filter_radius_km": 10,
            "commerce_search_sort_by": "CREATION_TIME_DESCEND"
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
    "av": "100067986370644", #userID
    "fb_dtsg": "NAcN18rlk2rz-Xlrkeio_IALkst7a1U7AKBOtjAUeBdZ-ldhPs44CmA:30:1745959832", #this changes every day ish
    "doc_id": "9277343979049234", #this doesnt change
    "variables": json.dumps(variables),
    "server_timestamps": "true"
}

first_scan = True

while True:
    existing_ids = set()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_ids.add(row["ID"])

    response = requests.post("https://www.facebook.com/api/graphql/", headers=headers, cookies=cookies, data=data)

    try:
        results = response.json()
        listings = results["data"]["marketplace_search"]["feed_units"]["edges"][:4]
        new_rows = []

        print("[🔍] New listings:")
        for item in listings:
            node = item["node"]
            story_key = node.get("story_key", "")
            listing = node.get("listing", {})

            title = listing.get("marketplace_listing_title", "N/A")
            price = listing.get("listing_price", {}).get("formatted_amount", "N/A")
            location = listing.get("location", {}).get("reverse_geocode", {}).get("city", "Unknown")
            image_url = listing.get("primary_listing_photo", {}).get("image", {}).get("uri", "N/A")
            post_url = f"https://www.facebook.com/marketplace/item/{story_key}" if story_key else "N/A"

            print(f" - {title}")

            if first_scan or story_key not in existing_ids:
                new_rows.append({
                    "ID": story_key,
                    "Title": title,
                    "Price": price,
                    "Location": location,
                    "Image URL": image_url,
                    "Post URL": post_url
                })

                if not first_scan:
                    result = evaluateListing(title, price, location, image_url, post_url)
                    print(result)
                    if "[YES]" in result:
                        sendMessage(post_url)

        if new_rows:
            file_exists = os.path.exists(CSV_FILE)
            with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["ID", "Title", "Price", "Location", "Image URL", "Post URL"])
                if not file_exists:
                    writer.writeheader()
                writer.writerows(new_rows)

            print(f"[✅] Added {len(new_rows)} new listings to {CSV_FILE}")

    except Exception as e:
        print("[❌] Failed to parse response:", e)
        print(response.text)

    first_scan = False
    print("[⏳] Scan completed. Waiting for next cycle...\n")
    time.sleep(20)  # Every 5 minutes