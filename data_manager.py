"""
AccessEase - Data Management Module
Author: Prachi (Data Specialist)
Description:
    Handles reading, validating, and managing venue data from CSV.
    Supports both:
    1. 20 Reference Anchor Landmarks (landmarks.csv)
    2. 50 Destination Venues (locations.csv / places.csv)
    Ensures missing values are normalized to 'Unknown' and coordinates
    are converted to numerical floats for offline distance calculations.
"""

import os
import pandas as pd

# The 8 mandatory accessibility criteria columns
REQUIRED_ACCESSIBILITY_COLUMNS = [
    "wheelchair_ramps",
    "step_free_entrances",
    "lifts",
    "accessible_toilets",
    "accessible_parking",
    "tactile_pathways",
    "audio_assistance",
    "large_text_signage",
]

# Standard metadata columns for each venue
METADATA_COLUMNS = [
    "id",
    "name",
    "category",
    "region",
    "city",
    "address",
    "contact",
    "verified_date",
    "notes",
    "latitude",
    "longitude",
]

# Landmark metadata columns
LANDMARK_COLUMNS = [
    "id",
    "name",
    "landmark_area",
    "latitude",
    "longitude",
    "description",
]

# Directory and File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LOCATIONS_PATH = os.path.join(BASE_DIR, "locations.csv")
DEFAULT_PLACES_PATH = os.path.join(BASE_DIR, "places.csv")
DEFAULT_LANDMARKS_PATH = os.path.join(BASE_DIR, "landmarks.csv")


def load_landmarks_dataset(csv_path=None):
    """
    Loads the 20 Reference Anchor Landmarks dataset.
    
    Landmarks are physical starting points (major chowks, flyovers, bridges, squares)
    used for offline Haversine proximity calculations.
    """
    if csv_path is None:
        csv_path = DEFAULT_LANDMARKS_PATH
    elif not os.path.isabs(csv_path):
        resolved_path = os.path.join(BASE_DIR, csv_path)
        if os.path.exists(resolved_path):
            csv_path = resolved_path

    if not os.path.exists(csv_path):
        return pd.DataFrame(columns=LANDMARK_COLUMNS)

    df = pd.read_csv(csv_path)

    # Standardize types
    if "id" in df.columns:
        df["id"] = pd.to_numeric(df["id"], errors="coerce").fillna(0).astype(int)
    if "latitude" in df.columns:
        df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    if "longitude" in df.columns:
        df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    return df
