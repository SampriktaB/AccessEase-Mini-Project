"""
AccessEase - Core Logic & Algorithms Module
Author: Shruti (Algorithm & Logic Specialist)
Description:
    Contains pure Python mathematical and filtering algorithms:
    1. Match percentage scoring formula.
    2. Multi-parameter searching (category, keywords, bookmarks).
    3. Accessibility persona profiles.
    4. Ethical tri-state badge indicators.
"""

import math
import pandas as pd
from data_manager import load_places_dataset, load_landmarks_dataset

# Mapping of UI checklist labels to CSV column names
ACCESSIBILITY_FEATURES = {
    "Wheelchair Ramps": "wheelchair_ramps",
    "Step-free Entrances": "step_free_entrances",
    "Lifts": "lifts",
    "Accessible Toilets": "accessible_toilets",
    "Accessible Parking": "accessible_parking",
    "Tactile Pathways": "tactile_pathways",
    "Audio Assistance": "audio_assistance",
    "Large-text Signage": "large_text_signage",
}

# Persona presets
PROFILES = {
    "Wheelchair User": [
        "Wheelchair Ramps",
        "Step-free Entrances",
        "Lifts",
        "Accessible Toilets",
        "Accessible Parking",
    ],
    "Visually Impaired": [
        "Tactile Pathways",
        "Audio Assistance",
        "Large-text Signage",
        "Lifts",
    ],
    "Mobility Difficulties": [
        "Step-free Entrances",
        "Lifts",
        "Accessible Parking",
        "Wheelchair Ramps",
    ],
    "Custom / Manual": [],
}

# The 6 primary public venue categories
CATEGORIES = [
    "All Categories",
    "Hospitals",
    "Colleges",
    "Parks",
    "Malls",
    "Railway/Metro Stations",
    "Public Buildings",
]


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates great-circle distance between two geographic coordinates in kilometers.
    Requires no external map APIs or internet connection (100% offline).
    """
    try:
        lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
    except (TypeError, ValueError):
        return None

    R = 6371.0  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return round(R * c, 2)


def calculate_place_match(place_row, selected_feature_columns):
    """
    Core Algorithm: Computes match percentage against user requirements.
    
    Formula:
        Match Percentage = round((Confirmed Available Count / Total Selected Requirements) * 100)
    
    Tri-State Rule:
        - 'Available' -> Counts as matched (+1 numerator)
        - 'Unavailable' -> Counts as unmet (0 numerator)
        - 'Unknown' -> Unverified (0 numerator, NEVER treated as absent)
    """
    total_selected = len(selected_feature_columns)

    if total_selected == 0:
        return {
            "match_percent": 100,
            "available_count": 0,
            "unavailable_count": 0,
            "unknown_count": 0,
            "total_selected": 0,
        }

    available_count = 0
    unavailable_count = 0
    unknown_count = 0

    for col in selected_feature_columns:
        val = str(place_row.get(col, "Unknown")).strip().capitalize()
        if val == "Available":
            available_count += 1
        elif val == "Unavailable":
            unavailable_count += 1
        else:
            unknown_count += 1

    match_percent = int(round((available_count / total_selected) * 100))

    return {
        "match_percent": match_percent,
        "available_count": available_count,
        "unavailable_count": unavailable_count,
        "unknown_count": unknown_count,
        "total_selected": total_selected,
    }


def filter_places(
    df,
    category="All Categories",
    search_query="",
    selected_feature_labels=None,
    saved_ids=None,
    only_saved=False,
    landmark_lat=None,
    landmark_lon=None,
    max_distance_km=None,
    sort_by="match",
):
    """
    Filters places by Category, Search Keyword, Saved status, and Proximity Radius,
    calculates match percentage, straight-line distance (Haversine formula),
    and sorts records accordingly.
    """
    if df.empty:
        return df

    filtered_df = df.copy()

    # 1. Filter by Saved Bookmarks
    if only_saved:
        saved_set = set(saved_ids or [])
        filtered_df = filtered_df[filtered_df["id"].isin(saved_set)]

    # 2. Filter by Category
    if category and category != "All Categories":
        filtered_df = filtered_df[filtered_df["category"] == category]

    # 3. Filter by Keyword (Name, City, Address, Region, or Auditor Notes)
    if search_query:
        query = search_query.strip().lower()
        search_match = (
            filtered_df["name"].str.lower().str.contains(query, na=False)
            | filtered_df["city"].str.lower().str.contains(query, na=False)
            | filtered_df["address"].str.lower().str.contains(query, na=False)
            | filtered_df["notes"].str.lower().str.contains(query, na=False)
        )
        if "region" in filtered_df.columns:
            search_match = search_match | filtered_df["region"].str.lower().str.contains(query, na=False)
        filtered_df = filtered_df[search_match]

    # 4. Map user-facing labels to column names
    selected_labels = selected_feature_labels or []
    selected_cols = [
        ACCESSIBILITY_FEATURES[lbl]
        for lbl in selected_labels
        if lbl in ACCESSIBILITY_FEATURES
    ]

    # 5. Compute match score for each row
    if not filtered_df.empty:
        match_results = filtered_df.apply(
            lambda row: calculate_place_match(row, selected_cols),
            axis=1,
            result_type="expand",
        )
        filtered_df["match_percent"] = match_results["match_percent"]
        filtered_df["available_count"] = match_results["available_count"]
        filtered_df["unavailable_count"] = match_results["unavailable_count"]
        filtered_df["unknown_count"] = match_results["unknown_count"]
        filtered_df["total_selected"] = match_results["total_selected"]

        # 6. Proximity & Distance Calculation (Anchor-Based Landmark System)
        has_coords = (landmark_lat is not None) and (landmark_lon is not None)
        if has_coords:
            filtered_df["distance_km"] = filtered_df.apply(
                lambda row: haversine_distance(
                    landmark_lat,
                    landmark_lon,
                    row.get("latitude"),
                    row.get("longitude"),
                ),
                axis=1,
            )

            # Apply distance radius filter if specified
            if max_distance_km is not None and max_distance_km > 0:
                filtered_df = filtered_df[
                    filtered_df["distance_km"].notna()
                    & (filtered_df["distance_km"] <= float(max_distance_km))
                ]

            # Sorting: by distance or by match percentage
            if sort_by == "distance":
                filtered_df = filtered_df.sort_values(
                    by=["distance_km", "match_percent", "name"],
                    ascending=[True, False, True],
                    na_position="last",
                )
            else:
                filtered_df = filtered_df.sort_values(
                    by=["match_percent", "distance_km", "name"],
                    ascending=[False, True, True],
                    na_position="last",
                )
        else:
            filtered_df["distance_km"] = None
            filtered_df = filtered_df.sort_values(
                by=["match_percent", "name"], ascending=[False, True]
            )
    else:
        for col in [
            "match_percent",
            "available_count",
            "unavailable_count",
            "unknown_count",
            "total_selected",
            "distance_km",
        ]:
            filtered_df[col] = []

    return filtered_df


def get_status_badge(status):
    """Returns an accessible visual indicator for a facility status."""
    clean_status = str(status).strip().capitalize()
    if clean_status == "Available":
        return "🟢 Available"
    elif clean_status == "Unavailable":
        return "🔴 Unavailable"
    else:
        return "⚪ Unknown / Unverified"


# Alias for backward compatibility
load_places_data = load_places_dataset
