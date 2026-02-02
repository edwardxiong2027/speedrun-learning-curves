#!/usr/bin/env python3
"""Quick data collection for initial analysis."""

import requests
import json
import time
import os
import sys
from datetime import datetime

BASE_URL = "https://www.speedrun.com/api/v1"
RATE_LIMIT_DELAY = 0.7

# Start with popular games with lots of history
GAMES = [
    "Super Mario 64",
    "Minecraft: Java Edition",
    "Portal",
    "Celeste",
    "Super Mario Bros."
]

def api_request(endpoint, params=None):
    url = f"{BASE_URL}/{endpoint}"
    time.sleep(RATE_LIMIT_DELAY)
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"API Error: {e}", flush=True)
        return {"data": []}

def search_game(name):
    data = api_request("games", {"name": name, "max": 1})
    games = data.get("data", [])
    return games[0] if games else None

def get_categories(game_id):
    data = api_request(f"games/{game_id}/categories")
    return data.get("data", [])

def get_runs(game_id, category_id, max_runs=1000):
    all_runs = []
    offset = 0

    while len(all_runs) < max_runs:
        data = api_request("runs", {
            "game": game_id,
            "category": category_id,
            "status": "verified",
            "orderby": "date",
            "direction": "asc",
            "max": 200,
            "offset": offset
        })

        runs = data.get("data", [])
        if not runs:
            break

        all_runs.extend(runs)
        offset += 200
        print(f"    {len(all_runs)} runs collected...", flush=True)

    return all_runs

def extract_wr_progression(runs):
    if not runs:
        return []

    dated_runs = [r for r in runs if r.get("date")]
    dated_runs.sort(key=lambda x: x["date"])

    progression = []
    current_wr = float('inf')

    for run in dated_runs:
        times = run.get("times", {})
        primary_time = times.get("primary_t")

        if primary_time is None:
            continue

        if primary_time < current_wr:
            current_wr = primary_time
            progression.append({
                "date": run["date"],
                "time_seconds": primary_time,
                "run_id": run["id"]
            })

    return progression

def main():
    print("=" * 60, flush=True)
    print("QUICK SPEEDRUN DATA COLLECTION", flush=True)
    print("=" * 60, flush=True)

    all_data = []

    for game_name in GAMES:
        print(f"\n{'='*50}", flush=True)
        print(f"Game: {game_name}", flush=True)
        print("="*50, flush=True)

        game = search_game(game_name)
        if not game:
            print(f"  Not found", flush=True)
            continue

        game_id = game["id"]
        game_info = {
            "name": game["names"]["international"],
            "id": game_id,
            "categories": []
        }
        print(f"  Found: {game_info['name']}", flush=True)

        categories = get_categories(game_id)
        main_cats = [c for c in categories if c.get("type") == "per-game"][:3]

        for cat in main_cats:
            cat_name = cat["name"]
            cat_id = cat["id"]
            print(f"\n  Category: {cat_name}", flush=True)

            runs = get_runs(game_id, cat_id, max_runs=500)
            print(f"    Total runs: {len(runs)}", flush=True)

            if len(runs) < 10:
                continue

            progression = extract_wr_progression(runs)
            print(f"    WR progression: {len(progression)} records", flush=True)

            if len(progression) >= 5:
                first_time = progression[0]["time_seconds"]
                current_time = progression[-1]["time_seconds"]
                improvement = (1 - current_time/first_time) * 100
                print(f"    Improvement: {improvement:.1f}%", flush=True)

                game_info["categories"].append({
                    "name": cat_name,
                    "id": cat_id,
                    "total_runs": len(runs),
                    "wr_progression": progression,
                    "statistics": {
                        "first_record_date": progression[0]["date"],
                        "first_record_time": first_time,
                        "current_record_date": progression[-1]["date"],
                        "current_record_time": current_time,
                        "total_improvement_percent": improvement,
                        "number_of_records": len(progression)
                    }
                })

        if game_info["categories"]:
            all_data.append(game_info)

    # Save data
    output_path = os.path.join(os.path.dirname(__file__), "speedrun_data.json")
    with open(output_path, "w") as f:
        json.dump(all_data, f, indent=2)
    print(f"\n\nData saved to: {output_path}", flush=True)

    print("\n" + "="*60, flush=True)
    print("COLLECTION COMPLETE", flush=True)
    print("="*60, flush=True)
    print(f"Games: {len(all_data)}", flush=True)
    total_cats = sum(len(g["categories"]) for g in all_data)
    print(f"Categories: {total_cats}", flush=True)
    total_records = sum(len(c["wr_progression"]) for g in all_data for c in g["categories"])
    print(f"World records: {total_records}", flush=True)

if __name__ == "__main__":
    main()
