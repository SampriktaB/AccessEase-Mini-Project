"""
Unit Tests for AccessEase Core Logic
Running this file directly using:
    python test_logic.py
"""

import unittest
import pandas as pd
from data_manager import load_landmarks_dataset, load_places_dataset
from logic import (
    ACCESSIBILITY_FEATURES,
    PROFILES,
    CATEGORIES,
    load_places_data,
    calculate_place_match,
    filter_places,
    get_status_badge,
    haversine_distance,
)


class TestAccessEaseLogic(unittest.TestCase):

    def setUp(self):
        """Set up sample place records for testing."""
        self.sample_place = {
            "id": 99,
            "name": "Test Science Center",
            "category": "Colleges",
            "city": "Testville",
            "address": "123 Innovation Road",
            "notes": "Wheelchair ramp at rear entrance only.",
            "wheelchair_ramps": "Available",
            "step_free_entrances": "Available",
            "lifts": "Unavailable",
            "accessible_toilets": "Unknown",
            "accessible_parking": "Available",
            "tactile_pathways": "Unavailable",
            "audio_assistance": "Unknown",
            "large_text_signage": "Available",
        }

        self.df = pd.DataFrame([
            self.sample_place,
            {
                "id": 100,
                "name": "Alpha General Hospital",
                "category": "Hospitals",
                "city": "Metro City",
                "address": "500 Cure Street",
                "notes": "Full braille and ramp facilities.",
                "wheelchair_ramps": "Available",
                "step_free_entrances": "Available",
                "lifts": "Available",
                "accessible_toilets": "Available",
                "accessible_parking": "Available",
                "tactile_pathways": "Available",
                "audio_assistance": "Available",
                "large_text_signage": "Available",
            },
            {
                "id": 101,
                "name": "Old Heritage Market",
                "category": "Malls",
                "city": "Old Town",
                "address": "1 Ancient Square",
                "notes": "Historic cobblestones, no ramps.",
                "wheelchair_ramps": "Unavailable",
                "step_free_entrances": "Unavailable",
                "lifts": "Unavailable",
                "accessible_toilets": "Unavailable",
                "accessible_parking": "Unavailable",
                "tactile_pathways": "Unavailable",
                "audio_assistance": "Unavailable",
                "large_text_signage": "Unavailable",
            },
        ])

    def test_calculate_place_match_zero_selected(self):
        """When no requirements are selected, match score should default to 100%."""
        result = calculate_place_match(self.sample_place, [])
        self.assertEqual(result["match_percent"], 100)
        self.assertEqual(result["total_selected"], 0)

    def test_calculate_place_match_mixed(self):
        """
        Selected 4 features:
        - wheelchair_ramps: Available (1)
        - lifts: Unavailable (1)
        - accessible_toilets: Unknown (1)
        - accessible_parking: Available (1)
        Available = 2, Total = 4 -> Match = 50%
        """
        selected_cols = [
            "wheelchair_ramps",
            "lifts",
            "accessible_toilets",
            "accessible_parking",

        result = calculate_place_match(self.sample_place, selected_cols)
        self.assertEqual(result["total_selected"], 4)
        self.assertEqual(result["available_count"], 2)
        self.assertEqual(result["unavailable_count"], 1)
        self.assertEqual(result["unknown_count"], 1)
        self.assertEqual(result["match_percent"], 50)

    def test_missing_data_not_treated_as_unavailable(self):
        """Unknown or missing data must be classified as 'Unknown', not 'Unavailable'."""
        place_with_missing = {
            "wheelchair_ramps": "Available",
            "lifts": "",  # missing / blank
        }
        result = calculate_place_match(place_with_missing, ["wheelchair_ramps", "lifts"])
        self.assertEqual(result["available_count"], 1)
        self.assertEqual(result["unavailable_count"], 0)
        self.assertEqual(result["unknown_count"], 1)
        self.assertEqual(result["match_percent"], 50)
