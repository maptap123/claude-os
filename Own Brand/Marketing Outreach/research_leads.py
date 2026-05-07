#!/usr/bin/env python3
"""
Lead Research Script — Google Places API
=========================================
Finds local businesses by industry + location within a radius,
enriches each with phone/website/rating data, and outputs a
prioritized CSV for outreach.

One-time setup (free — $200/month credit from Google):
--------------------------------------------------------
1. Go to https://console.cloud.google.com
2. Create a new project (or pick an existing one)
3. Search "Places API (New)" in the top bar and click Enable
4. Go to APIs & Services > Credentials > Create Credentials > API Key
5. Copy the key. Then run this once in PowerShell:

   setx GOOGLE_PLACES_API_KEY "your-key-here"

   (Close and reopen your terminal after.)

Your key won't be charged — the first $200 of usage each month is free.
That covers roughly 5,000—10,000 detailed business lookups.

Usage:
------
  # Search electricians within 40 miles of Lawrenceburg, IN
  python research_leads.py --industry electrician --city "Lawrenceburg, IN" --radius 40

  # Search dentists, bigger radius
  python research_leads.py --industry dentist --city "Lawrenceburg, IN" --radius 50

  # Search with a custom keyword instead of a place type
  python research_leads.py --keyword "hvac contractor" --city "Lawrenceburg, IN" --radius 40

  # Custom output file
  python research_leads.py --industry plumber --city "Lawrenceburg, IN" -o plumber_leads.csv

  # Combine multiple CSVs into one master list
  python research_leads.py --merge electrician_leads.csv dentist_leads.csv plumber_leads.csv -o master_leads.csv

How it works:
-------------
Searches from multiple grid points across your target area so we
catch more than the 60-result-per-search limit. Deduplicates by
Google place ID. Enriches each result with full details (website,
phone, address) via a second API call.

Output columns:
---------------
  business_name, phone, website, has_website, address, city, state,
  rating, review_count, industry, place_id, google_maps_url

Priority tiers (populated in the priority column):
  TIER_1 — no website found (highest value lead)
  TIER_2 — has a website (still worth outreach for SEO)
  TIER_3 — has a site AND high rating count (less urgent)
"""

import os
import sys
import csv
import json
import time
import math
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY", "")

# Supported place types that map to our target industries
# Full list: https://developers.google.com/maps/documentation/places/web-service/supported_types
PLACE_TYPE_MAP = {
    "electrician":        "electrician",
    "plumber":            "plumber",
    "hvac":               None,  # use keyword search
    "roofer":             "roofing_contractor",
    "general contractor": "general_contractor",
    "painter":            "painter",
    "landscaper":         None,
    "dentist":            "dentist",
    "chiropractor":       None,
    "physiotherapist":    "physiotherapist",
    "optometrist":        None,
    "auto repair":        "car_repair",
    "towing":             None,
    "cleaning service":   None,
    "pest control":       None,
    "nail salon":         "beauty_salon",
    "hair salon":         "beauty_salon",
    "restaurant":         "restaurant",
    "florist":            "florist",
    "massage":            None,
}

# Output CSV columns
CSV_COLUMNS = [
    "business_name", "phone", "website", "has_website", "address",
    "city", "state", "rating", "review_count", "industry",
    "priority", "place_id", "google_maps_url",
]

# ---------------------------------------------------------------------------
# Geocoding (free — uses Google Geocoding API, same key)
# ---------------------------------------------------------------------------

def geocode(city_name: str) -> tuple[float, float] | None:
    """Convert a city name to lat/lng."""
    params = urllib.parse.urlencode({"address": city_name, "key": API_KEY})
    url = f"https://maps.googleapis.com/maps/api/geocode/json?{params}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        if data.get("status") == "OK":
            loc = data["results"][0]["geometry"]["location"]
            return loc["lat"], loc["lng"]
    except Exception as e:
        print(f"  Geocoding failed for '{city_name}': {e}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Grid point generation
# ---------------------------------------------------------------------------

def generate_search_grid(center_lat: float, center_lng: float,
                         radius_miles: float, spacing_miles: float = 12.0):
    """
    Generate a grid of lat/lng points covering the target area.
    Returns unique points spaced by ~spacing_miles within the radius.
    """
    points = []
    lat_per_mile = 1.0 / 69.0
    step = spacing_miles * lat_per_mile
    radius_lat = radius_miles * lat_per_mile
    # longitude degrees per mile varies by latitude
    lng_per_mile = 1.0 / (69.0 * math.cos(math.radians(center_lat)))

    lat = center_lat - radius_lat
    while lat <= center_lat + radius_lat:
        lng = center_lng - (radius_miles * lng_per_mile)
        while lng <= center_lng + (radius_miles * lng_per_mile):
            # Only include points within the radius circle
            dist_lat = (lat - center_lat) / lat_per_mile
            dist_lng = (lng - center_lng) / lng_per_mile
            if math.sqrt(dist_lat**2 + dist_lng**2) <= radius_miles:
                points.append((round(lat, 6), round(lng, 6)))
            lng += step
        lat += step

    # Sort by distance from center so the best results come first
    points.sort(key=lambda p: (p[0] - center_lat)**2 + (p[1] - center_lng)**2)
    return points


# ---------------------------------------------------------------------------
# Place search
# ---------------------------------------------------------------------------

def search_places(lat: float, lng: float, radius_meters: int,
                  place_type: str | None = None,
                  keyword: str | None = None,
                  page_token: str | None = None) -> dict | None:
    """Call Google Places Nearby Search. Returns parsed JSON or None."""

    if page_token:
        params = urllib.parse.urlencode({
            "pagetoken": page_token,
            "key": API_KEY,
        })
    else:
        params = {
            "location": f"{lat},{lng}",
            "radius": str(radius_meters),
            "key": API_KEY,
        }
        if place_type:
            params["type"] = place_type
        if keyword:
            params["keyword"] = keyword
        params = urllib.parse.urlencode(params)

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?{params}"

    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  Search error at {lat},{lng}: {e}", file=sys.stderr)
        return None


def search_all_pages(lat: float, lng: float, radius_meters: int,
                     place_type: str | None = None,
                     keyword: str | None = None) -> list[dict]:
    """Search and paginate through all available results (up to 60)."""
    results = []
    page_token = None
    pages = 0

    while pages < 3:  # Nearby Search maxes out at 3 pages (60 results)
        if pages == 0:
            data = search_places(lat, lng, radius_meters, place_type, keyword)
        else:
            time.sleep(2)  # page tokens need a moment to activate
            data = search_places(lat, lng, radius_meters, place_type, keyword,
                                 page_token=page_token)

        if data is None:
            break

        status = data.get("status", "")
        if status not in ("OK", "ZERO_RESULTS"):
            if status != "INVALID_REQUEST":
                print(f"  API status: {status}", file=sys.stderr)
            break

        results.extend(data.get("results", []))
        page_token = data.get("next_page_token")
        if not page_token:
            break
        pages += 1

    return results


# ---------------------------------------------------------------------------
# Place details (website, phone, address components)
# ---------------------------------------------------------------------------

def get_place_details(place_id: str) -> dict | None:
    """Fetch full details for a single place."""
    fields = "website,formatted_phone_number,formatted_address,address_components,rating,user_ratings_total,name,place_id,url"
    params = urllib.parse.urlencode({
        "place_id": place_id,
        "fields": fields,
        "key": API_KEY,
    })
    url = f"https://maps.googleapis.com/maps/api/place/details/json?{params}"

    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        if data.get("status") == "OK":
            return data.get("result", {})
    except Exception as e:
        print(f"  Details error for {place_id}: {e}", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Address parsing
# ---------------------------------------------------------------------------

def extract_city_state(components: list[dict]) -> tuple[str, str]:
    """Extract city and state from address_components."""
    city = state = ""
    for comp in components:
        if "locality" in comp.get("types", []):
            city = comp.get("long_name", "")
        elif "administrative_area_level_1" in comp.get("types", []):
            state = comp.get("short_name", "")
    return city, state


# ---------------------------------------------------------------------------
# Enrichment
# ---------------------------------------------------------------------------

def enrich_places(places: list[dict], industry: str) -> list[dict]:
    """
    Take raw place search results, fetch details for each,
    and return structured rows ready for CSV.
    """
    rows = []
    seen = set()

    for i, place in enumerate(places):
        place_id = place.get("place_id", "")
        if not place_id or place_id in seen:
            continue
        seen.add(place_id)

        # Basic info from search result
        name = place.get("name", "")
        rating = place.get("rating", 0.0)
        review_count = place.get("user_ratings_total", 0)

        # Fetch full details
        details = get_place_details(place_id)
        if details is None:
            print(f"  [{i+1}/{len(places)}] {name} — FAILED (no details)")
            continue

        phone = details.get("formatted_phone_number", "") or ""
        website = details.get("website", "") or ""
        address = details.get("formatted_address", "") or ""
        gmaps_url = details.get("url", "") or ""
        components = details.get("address_components", [])
        city, state = extract_city_state(components)

        has_website = "yes" if website else "no"

        # Priority tiering
        if not website:
            priority = "TIER_1"
        elif review_count < 20 or rating < 3.5:
            priority = "TIER_2"
        else:
            priority = "TIER_3"

        rows.append({
            "business_name": name,
            "phone": phone,
            "website": website,
            "has_website": has_website,
            "address": address,
            "city": city,
            "state": state,
            "rating": rating,
            "review_count": review_count,
            "industry": industry,
            "priority": priority,
            "place_id": place_id,
            "google_maps_url": gmaps_url,
        })

        status = "NO SITE (TIER 1)" if not website else f"has site ({priority})"
        print(f"  [{i+1}/{len(places)}] {name} — {status}")

        # Respect rate limits — free tier is generous but play nice
        time.sleep(0.15)

    return rows


# ---------------------------------------------------------------------------
# CSV I/O
# ---------------------------------------------------------------------------

def write_csv(rows: list[dict], filepath: str):
    """Write rows to CSV, creating or overwriting the file."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in rows:
            # Ensure all values are strings for CSV
            clean = {k: str(v) for k, v in row.items()}
            writer.writerow(clean)


def read_csv(filepath: str) -> list[dict]:
    """Read a CSV back into a list of dicts."""
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def merge_csvs(filepaths: list[str], output_path: str):
    """Combine multiple CSVs into one, deduplicating by place_id."""
    seen = set()
    all_rows = []
    for fp in filepaths:
        if not Path(fp).exists():
            print(f"  Skipping missing file: {fp}", file=sys.stderr)
            continue
        for row in read_csv(fp):
            pid = row.get("place_id", "")
            if pid and pid not in seen:
                seen.add(pid)
                all_rows.append(row)

    write_csv(all_rows, output_path)
    tier1 = sum(1 for r in all_rows if r.get("priority") == "TIER_1")
    tier2 = sum(1 for r in all_rows if r.get("priority") == "TIER_2")
    tier3 = sum(1 for r in all_rows if r.get("priority") == "TIER_3")
    print(f"  Merged {len(all_rows)} unique leads → {output_path}")
    print(f"    TIER_1 (no website): {tier1}")
    print(f"    TIER_2 (weak presence): {tier2}")
    print(f"    TIER_3 (has site): {tier3}")


# ---------------------------------------------------------------------------
# Main run
# ---------------------------------------------------------------------------

def run_search(industry: str, keyword: str | None, city: str,
               radius_miles: float, output_path: str):
    """Full pipeline: geocode → grid → search → enrich → write."""

    print(f"\n{'='*60}")
    print(f"Lead Research: {keyword or industry} near {city} ({radius_miles}mi radius)")
    print(f"{'='*60}\n")

    # 1. Geocode
    print(f"[1/4] Geocoding '{city}'...")
    coords = geocode(city)
    if coords is None:
        print("ERROR: Could not geocode the city. Check spelling and try again.", file=sys.stderr)
        sys.exit(1)
    center_lat, center_lng = coords
    print(f"       Coordinates: {center_lat}, {center_lng}")

    # 2. Generate search grid
    print(f"[2/4] Generating search grid...")
    grid_points = generate_search_grid(center_lat, center_lng, radius_miles)
    print(f"       {len(grid_points)} grid points across {radius_miles}-mile radius")

    # Determine place type and keyword
    place_type = None
    if industry:
        place_type = PLACE_TYPE_MAP.get(industry)
        if place_type is None:
            # Industry not in the supported type list; use keyword instead
            keyword = keyword or industry.replace("_", " ")
            print(f"       '{industry}' not a direct place type — using keyword search")

    radius_meters = int(radius_miles * 1609.34)
    # Cap at 50000m (API max)
    search_radius = min(radius_meters, 50000)

    # 3. Search all grid points
    print(f"[3/4] Searching...")
    all_raw = []
    for i, (lat, lng) in enumerate(grid_points):
        print(f"       Grid point {i+1}/{len(grid_points)} ({lat}, {lng})...")
        results = search_all_pages(lat, lng, search_radius, place_type, keyword)
        print(f"         → {len(results)} results")
        all_raw.extend(results)
        time.sleep(0.5)  # Be polite between grid points

    # Deduplicate raw results
    seen = set()
    unique_raw = []
    for p in all_raw:
        pid = p.get("place_id", "")
        if pid and pid not in seen:
            seen.add(pid)
            unique_raw.append(p)

    print(f"\n       Total unique leads found: {len(unique_raw)}")

    # 4. Enrich with details
    print(f"[4/4] Fetching details for {len(unique_raw)} businesses...\n")
    rows = enrich_places(unique_raw, industry or keyword or "")

    # Write output
    write_csv(rows, output_path)
    tier1 = sum(1 for r in rows if r["priority"] == "TIER_1")
    tier2 = sum(1 for r in rows if r["priority"] == "TIER_2")
    tier3 = sum(1 for r in rows if r["priority"] == "TIER_3")

    print(f"\n{'='*60}")
    print(f"DONE — {len(rows)} leads saved to {output_path}")
    print(f"  TIER_1 (no website — call first): {tier1}")
    print(f"  TIER_2 (has site, weak presence):  {tier2}")
    print(f"  TIER_3 (has site, decent presence): {tier3}")
    print(f"{'='*60}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Research local business leads via Google Places API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python research_leads.py --industry electrician --city "Lawrenceburg, IN" --radius 40
  python research_leads.py --keyword "hvac contractor" --city "Cincinnati, OH" --radius 30
  python research_leads.py --industry dentist --city "Lawrenceburg, IN"
  python research_leads.py --merge *.csv -o master_leads.csv
        """.strip(),
    )

    parser.add_argument("--industry", "-i",
                        help="Business type (e.g. electrician, plumber, dentist)")
    parser.add_argument("--keyword", "-k",
                        help="Custom search keyword (e.g. 'hvac contractor')")
    parser.add_argument("--city", "-c",
                        help="Target city + state (e.g. 'Lawrenceburg, IN')")
    parser.add_argument("--radius", "-r", type=float, default=40,
                        help="Search radius in miles (default: 40)")
    parser.add_argument("--output", "-o",
                        help="Output CSV path (default: <industry>_leads.csv)")

    parser.add_argument("--merge", nargs="+",
                        help="Merge multiple CSV files into one, deduplicating")
    parser.add_argument("--list-types", action="store_true",
                        help="Show supported industry types and exit")

    args = parser.parse_args()

    # --list-types
    if args.list_types:
        print("Supported --industry values (maps to Google place type):")
        for name, ptype in sorted(PLACE_TYPE_MAP.items()):
            marker = "yes" if ptype else "(keyword search)"
            print(f"  {name:25s} {marker}")
        print("\nUse --keyword for anything not listed above.")
        return

    # --merge mode
    if args.merge:
        output = args.output or "master_leads.csv"
        merge_csvs(args.merge, output)
        return

    # --search mode
    if not API_KEY:
        print("ERROR: GOOGLE_PLACES_API_KEY environment variable not set.\n", file=sys.stderr)
        print("1. Go to https://console.cloud.google.com", file=sys.stderr)
        print('2. Enable "Places API (New)"', file=sys.stderr)
        print("3. Create an API key under Credentials", file=sys.stderr)
        print("4. Run: setx GOOGLE_PLACES_API_KEY \"your-key-here\"", file=sys.stderr)
        print("5. Reopen your terminal and re-run.\n", file=sys.stderr)
        sys.exit(1)

    if not args.city:
        print("ERROR: --city is required for search (e.g. --city \"Lawrenceburg, IN\")\n", file=sys.stderr)
        sys.exit(1)

    if not args.industry and not args.keyword:
        print("ERROR: Must provide --industry or --keyword\n", file=sys.stderr)
        sys.exit(1)

    output = args.output or f"{args.industry or args.keyword.replace(' ', '_')}_leads.csv"
    run_search(
        industry=args.industry or "",
        keyword=args.keyword,
        city=args.city,
        radius_miles=args.radius,
        output_path=output,
    )


if __name__ == "__main__":
    main()
