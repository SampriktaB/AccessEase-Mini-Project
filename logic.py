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

