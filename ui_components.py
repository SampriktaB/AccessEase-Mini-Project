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


def render_venue_card(parent_frame, place, selected_features, is_saved, on_toggle_bookmark, on_open_details):
    """
    Renders a sleek horizontal venue card matching the mockup design:
    [ Centered Icon Badge ]  [ Place Info + Facility Chips ]  [ Match Pill + Actions ]
    """
    place_id = int(place["id"])
    match_pct = int(place.get("match_percent", 100))
    category = place.get("category", "Public Buildings")
    cat_theme = CATEGORY_THEMES.get(category, CATEGORY_THEMES["Public Buildings"])

    # Outer container with padding
    card_container = tk.Frame(parent_frame, bg=BACKGROUND_PAGE)
    card_container.pack(fill="x", padx=16, pady=5)

    card_canvas = tk.Canvas(card_container, bg=BACKGROUND_PAGE, highlightthickness=0, height=86)
    card_canvas.pack(fill="x", expand=True)

    # Main Card Box with smooth rounded corners
    card = tk.Frame(card_canvas, bg=SURFACE_CARD)
    card_win = card_canvas.create_window(12, 8, window=card, anchor="nw")

    def _on_card_configure(event):
        w = event.width
        card_canvas.delete("card_bg")
        draw_rounded_rect(
            card_canvas,
            2, 2, w - 4, 82,
            radius=16,
            fill=SURFACE_CARD,
            outline=BORDER_CARD,
            width=1,
            tags="card_bg",
        )
        card_canvas.tag_lower("card_bg")
        card_canvas.itemconfig(card_win, width=w - 24)

    card_canvas.bind("<Configure>", _on_card_configure)