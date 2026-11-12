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


