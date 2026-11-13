"""
AccessEase - Modern UI Components Module
Author: Leisha (Component & Dialog Specialist)
Description:
    Renders clean, modern venue cards matching the design mockup:
    - Pure category icon badges with 100% mathematical horizontal & vertical centering.
    - Zero pictures on cards, focusing on clear, accessible category iconography.
    - Verified facility chips in soft lavender.
    - Match score badges, bookmark toggle, and detailed audit modal.
"""

import os
import tkinter as tk
from tkinter import ttk

from theme import (
    BACKGROUND_PAGE,
    SURFACE_CARD,
    BORDER_CARD,
    BORDER_SUBTLE,
    PRIMARY_COLOR,
    PRIMARY_DARK,
    PRIMARY_LIGHT,
    PRIMARY_HOVER,
    TEXT_MAIN,
    TEXT_MUTED,
    CHIP_BG,
    CHIP_FG,
    MATCH_HIGH_BG,
    MATCH_HIGH_FG,
    MATCH_MED_BG,
    MATCH_MED_FG,
    MATCH_LOW_BG,
    MATCH_LOW_FG,
    DISTANCE_BG,
    DISTANCE_FG,
    DISTANCE_BORDER,
    CATEGORY_THEMES,
    FONT_CARD_TITLE,
    FONT_CARD_INFO,
    FONT_CHIP,
    FONT_MATCH_BADGE,
    FONT_BUTTON,
    draw_rounded_rect,
)
from logic import ACCESSIBILITY_FEATURES, get_status_badge

# Friendly chip label mappings
FACILITY_SHORT_NAMES = {
    "wheelchair_ramps": "Wheelchair Ramps",
    "step_free_entrances": "Step-free Entrance",
    "lifts": "Lifts",
    "accessible_toilets": "Accessible Toilets",
    "accessible_parking": "Accessible Parking",
    "tactile_pathways": "Tactile Pathways",
    "audio_assistance": "Audio Assistance",
    "large_text_signage": "Large-text Signage",
}


