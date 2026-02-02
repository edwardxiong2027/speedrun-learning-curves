#!/usr/bin/env python3
"""
Speedrun Data Collection Script
Author: Edward Xiong
Diamond Bar High School, 11th Grade
JEI Research Project: The Mathematics of Speedrunning

This script collects world record progression data from speedrun.com API
for analysis of learning curves and record-breaking patterns.
"""

import requests
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Optional
import csv

# API Configuration
BASE_URL = "https://www.speedrun.com/api/v1"
RATE_LIMIT_DELAY = 0.7  # Stay under 100 requests/minute

# Popular games with large speedrunning communities
GAMES_TO_ANALYZE = [
    "Super Mario 64",
    "The Legend of Zelda: Ocarina of Time",
    "Minecraft: Java Edition",
    "Celeste",
    "Portal",
    "Super Mario Bros.",
    "Dark Souls",
    "Hollow Knight",
    "Hades",
    "Cuphead",
    "Super Metroid",
    "GoldenEye 007",
    "Half-Life",
    "Doom (1993)",
    "Sekiro: Shadows Die Twice"
]


def api_request(endpoint: str, params: Optional[Dict] = None) -> Dict:
    """Make a rate-limited request to the speedrun.com API."""
    url = f"{BASE_URL}/{endpoint}"
    time.sleep(RATE_LIMIT_DELAY)

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return {"data": []}


def search_game(game_name: str) -> Optional[Dict]:
    """Search for a game by name and return the best match."""
    data = api_request("games", {"name": game_name, "max": 1})
    games = data.get("data", [])
    return games[0] if games else None


def get_game_categories(game_id: str) -> List[Dict]:
    """Get all speedrun categories for a game."""
    data = api_request(f"games/{game_id}/categories")
    return data.get("data", [])


def get_category_records(game_id: str, category_id: str) -> List[Dict]:
    """Get the leaderboard (current records) for a category."""
    data = api_request(
        f"leaderboards/{game_id}/category/{category_id}",
        {"top": 100}  # Get top 100 runs
    )
    return data.get("data", {}).get("runs", [])


def get_all_verified_runs(game_id: str, category_id: str) -> List[Dict]:
    """Get all verified runs for a category (paginated)."""
    all_runs = []
    offset = 0
    max_runs = 200  # Per page

    while True:
        data = api_request(
            "runs",
            {
                "game": game_id,
                "category": category_id,
                "status": "verified",
                "orderby": "date",
                "direction": "asc",
                "max": max_runs,
                "offset": offset
            }
        )

        runs = data.get("data", [])
        if not runs:
            break

        all_runs.extend(runs)
        offset += max_runs

        # Check for pagination
        pagination = data.get("pagination", {})
        if offset >= pagination.get("size", 0):
            break

        print(f"  Collected {len(all_runs)} runs...")

        # Safety limit
        if len(all_runs) >= 5000:
            print("  Reached 5000 run limit")
            break

    return all_runs


def extract_world_record_progression(runs: List[Dict]) -> List[Dict]:
    """
    Extract the world record progression from a list of runs.
    Returns a list of runs that were world records at the time of submission.
    """
    if not runs:
        return []

    # Sort by date
    dated_runs = [r for r in runs if r.get("date")]
    dated_runs.sort(key=lambda x: x["date"])

    progression = []
    current_wr = float('inf')

    for run in dated_runs:
        # Get primary time in seconds
        times = run.get("times", {})
        primary_time = times.get("primary_t")

        if primary_time is None:
            continue

        # Check if this is a new world record
        if primary_time < current_wr:
            current_wr = primary_time
            progression.append({
                "date": run["date"],
                "time_seconds": primary_time,
                "run_id": run["id"],
                "weblink": run.get("weblink", "")
            })

    return progression


def calculate_wr_statistics(progression: List[Dict]) -> Dict:
    """Calculate statistics about the world record progression."""
    if len(progression) < 2:
        return {}

    # Convert dates to timestamps
    for record in progression:
        record["timestamp"] = datetime.strptime(record["date"], "%Y-%m-%d").timestamp()

    # Calculate improvements
    improvements = []
    for i in range(1, len(progression)):
        prev = progression[i-1]
        curr = progression[i]

        time_improvement = prev["time_seconds"] - curr["time_seconds"]
        percent_improvement = (time_improvement / prev["time_seconds"]) * 100
        days_between = (curr["timestamp"] - prev["timestamp"]) / 86400

        improvements.append({
            "from_date": prev["date"],
            "to_date": curr["date"],
            "time_saved_seconds": time_improvement,
            "percent_improvement": percent_improvement,
            "days_between_records": days_between
        })

    # Calculate summary statistics
    total_improvement = progression[0]["time_seconds"] - progression[-1]["time_seconds"]
    total_days = (progression[-1]["timestamp"] - progression[0]["timestamp"]) / 86400

    return {
        "first_record_date": progression[0]["date"],
        "first_record_time": progression[0]["time_seconds"],
        "current_record_date": progression[-1]["date"],
        "current_record_time": progression[-1]["time_seconds"],
        "total_improvement_seconds": total_improvement,
        "total_improvement_percent": (total_improvement / progression[0]["time_seconds"]) * 100,
        "total_days": total_days,
        "number_of_records": len(progression),
        "avg_days_between_records": total_days / (len(progression) - 1) if len(progression) > 1 else 0,
        "improvements": improvements
    }


def collect_game_data(game_name: str) -> Optional[Dict]:
    """Collect all speedrun data for a game."""
    print(f"\n{'='*60}")
    print(f"Collecting data for: {game_name}")
    print('='*60)

    # Find the game
    game = search_game(game_name)
    if not game:
        print(f"  Game not found: {game_name}")
        return None

    game_id = game["id"]
    game_info = {
        "name": game["names"]["international"],
        "id": game_id,
        "abbreviation": game.get("abbreviation", ""),
        "released": game.get("released", ""),
        "weblink": game.get("weblink", ""),
        "categories": []
    }

    print(f"  Found: {game_info['name']} (ID: {game_id})")

    # Get categories
    categories = get_game_categories(game_id)
    print(f"  Found {len(categories)} categories")

    # Focus on main categories (full game runs)
    main_categories = [c for c in categories if c.get("type") == "per-game"]

    for category in main_categories[:5]:  # Limit to top 5 categories
        cat_name = category["name"]
        cat_id = category["id"]
        print(f"\n  Category: {cat_name}")

        # Get all runs for this category
        runs = get_all_verified_runs(game_id, cat_id)
        print(f"    Total verified runs: {len(runs)}")

        if not runs:
            continue

        # Extract world record progression
        wr_progression = extract_world_record_progression(runs)
        print(f"    World records in progression: {len(wr_progression)}")

        if len(wr_progression) < 3:
            print("    Skipping (insufficient data)")
            continue

        # Calculate statistics
        stats = calculate_wr_statistics(wr_progression)

        game_info["categories"].append({
            "name": cat_name,
            "id": cat_id,
            "total_runs": len(runs),
            "wr_progression": wr_progression,
            "statistics": stats
        })

        if stats:
            print(f"    First WR: {stats['first_record_time']:.2f}s ({stats['first_record_date']})")
            print(f"    Current WR: {stats['current_record_time']:.2f}s ({stats['current_record_date']})")
            print(f"    Total improvement: {stats['total_improvement_percent']:.1f}%")

    return game_info


def save_data(data: List[Dict], filename: str):
    """Save collected data to JSON file."""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\nData saved to: {filepath}")


def save_progression_csv(all_data: List[Dict], filename: str):
    """Save world record progression data to CSV for analysis."""
    filepath = os.path.join(os.path.dirname(__file__), filename)

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'game', 'category', 'record_number', 'date',
            'time_seconds', 'days_since_first', 'percent_of_first'
        ])

        for game in all_data:
            game_name = game['name']

            for category in game.get('categories', []):
                cat_name = category['name']
                progression = category.get('wr_progression', [])

                if not progression:
                    continue

                first_time = progression[0]['time_seconds']
                first_date = datetime.strptime(progression[0]['date'], "%Y-%m-%d")

                for i, record in enumerate(progression):
                    record_date = datetime.strptime(record['date'], "%Y-%m-%d")
                    days_since_first = (record_date - first_date).days
                    percent_of_first = (record['time_seconds'] / first_time) * 100

                    writer.writerow([
                        game_name,
                        cat_name,
                        i + 1,
                        record['date'],
                        record['time_seconds'],
                        days_since_first,
                        percent_of_first
                    ])

    print(f"CSV saved to: {filepath}")


def main():
    """Main data collection function."""
    print("="*60)
    print("SPEEDRUN DATA COLLECTION")
    print("JEI Research Project - Edward Xiong")
    print("="*60)

    all_game_data = []

    for game_name in GAMES_TO_ANALYZE:
        game_data = collect_game_data(game_name)
        if game_data and game_data.get('categories'):
            all_game_data.append(game_data)

    # Save raw data
    save_data(all_game_data, "speedrun_data.json")

    # Save CSV for analysis
    save_progression_csv(all_game_data, "wr_progression.csv")

    # Summary
    print("\n" + "="*60)
    print("COLLECTION SUMMARY")
    print("="*60)
    print(f"Games collected: {len(all_game_data)}")

    total_categories = sum(len(g.get('categories', [])) for g in all_game_data)
    print(f"Categories with data: {total_categories}")

    total_records = sum(
        len(c.get('wr_progression', []))
        for g in all_game_data
        for c in g.get('categories', [])
    )
    print(f"Total world records tracked: {total_records}")


if __name__ == "__main__":
    main()
