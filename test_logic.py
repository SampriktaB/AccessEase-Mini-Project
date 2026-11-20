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
        ]
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

    def test_filter_by_category(self):
        """Filtering by category should isolate matching records."""
        filtered = filter_places(self.df, category="Hospitals")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered.iloc[0]["name"], "Alpha General Hospital")

    def test_filter_by_search_query(self):
        """Search query matches name, address, city, or notes."""
        filtered = filter_places(self.df, search_query="braille")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered.iloc[0]["id"], 100)

    def test_filter_by_saved_places(self):
        """Only saved IDs should appear when only_saved is True."""
        filtered = filter_places(self.df, saved_ids=[99, 101], only_saved=True)
        self.assertEqual(len(filtered), 2)
        self.assertSetEqual(set(filtered["id"]), {99, 101})

    def test_status_badge(self):
        """Check badge formatting for accessibility."""
        self.assertIn("Available", get_status_badge("Available"))
        self.assertIn("Unavailable", get_status_badge("Unavailable"))
        self.assertIn("Unknown", get_status_badge("Unknown"))
        self.assertIn("Unknown", get_status_badge(""))

    def test_load_places_csv(self):
        """Check reading places.csv loads valid records with required columns."""
        df = load_places_data()
        self.assertFalse(df.empty, "places.csv should not be empty")
        for col in ACCESSIBILITY_FEATURES.values():
            self.assertIn(col, df.columns)
            # Ensure no NaNs exist in accessibility columns
            self.assertFalse(df[col].isna().any(), f"Column {col} has NaN values")

    def test_haversine_distance_accuracy(self):
        """Check great-circle distance calculation using Haversine formula."""
        # Karve Statue Chowk: 18.5018, 73.8166
        # MIT-WPU Kothrud: 18.5180, 73.8150
        dist = haversine_distance(18.5018, 73.8166, 18.5180, 73.8150)
        self.assertIsNotNone(dist)
        self.assertAlmostEqual(dist, 1.81, places=1)

    def test_haversine_distance_same_point(self):
        """Distance between identical coordinates must be exactly 0.0 km."""
        dist = haversine_distance(18.5018, 73.8166, 18.5018, 73.8166)
        self.assertEqual(dist, 0.0)

    def test_haversine_distance_invalid_coordinates(self):
        """Invalid or missing coordinates return None without raising exceptions."""
        self.assertIsNone(haversine_distance(None, 73.8166, 18.5180, 73.8150))
        self.assertIsNone(haversine_distance("invalid", "coords", 18.5180, 73.8150))

    def test_load_landmarks_csv(self):
        """Check reading landmarks.csv loads 20 reference starting points."""
        df_lm = load_landmarks_dataset()
        self.assertEqual(len(df_lm), 20, "landmarks.csv must contain exactly 20 reference landmarks")
        for col in ["id", "name", "landmark_area", "latitude", "longitude"]:
            self.assertIn(col, df_lm.columns)
            self.assertFalse(df_lm[col].isna().any(), f"Landmark column {col} has missing values")

    def test_filter_places_with_proximity_and_radius(self):
        """Check proximity calculation and radius filtering in filter_places."""
        df_places = load_places_data()
        # Filter within 2 km of Karve Statue Chowk (18.5018, 73.8166)
        filtered_2km = filter_places(
            df=df_places,
            landmark_lat=18.5018,
            landmark_lon=73.8166,
            max_distance_km=2.0,
            sort_by="distance",
        )
        self.assertFalse(filtered_2km.empty)
        # All returned places must have distance <= 2.0 km
        self.assertTrue((filtered_2km["distance_km"] <= 2.0).all())
        # Results must be sorted nearest first
        distances = list(filtered_2km["distance_km"])
        self.assertEqual(distances, sorted(distances))


if __name__ == "__main__":
    unittest.main()
