"""
AccessEase - Modern Accessibility Assistant Desktop Application (Design v2)
Author: Samprikta (Team Leader & Lead Architect)
Description:
    Implements the updated modern design layout:
    - Deep Royal Purple Sidebar (#482490) with branded logo, glowing active nav pill,
      and bottom cursive quote art ("Accessible today... Inclusive tomorrow ♡").
    - Integrated Hero Banner with "Find. Access. Belong.", subtitle, skyline artwork,
      and integrated wide search pill with purple search button.
    - "Browse by Category" interactive cards grid (Metro Stations, Retail & Shopping,
      Colleges, Public Places, Hospitals) + "View All →" reset and "⚙ Filters".
    - "Nearby Accessible Places" list preserving the clean, centered category icon badges!
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageChops

# Project Modules
from theme import (
    APP_NAME,
    APP_ICON,
    APP_SUBTITLE,
    APP_TAGLINE,
    SIDEBAR_WIDTH,
    SIDEBAR_BG,
    SIDEBAR_HOVER,
    SIDEBAR_ACTIVE,
    SIDEBAR_TEXT,
    SIDEBAR_TEXT_ACTIVE,
    BACKGROUND_PAGE,
    SURFACE_CARD,
    BORDER_CARD,
    BORDER_SUBTLE,
    HERO_BG,
    HERO_TITLE_COLOR,
    HERO_SUB_COLOR,
    PRIMARY_COLOR,
    PRIMARY_DARK,
    PRIMARY_LIGHT,
    PRIMARY_HOVER,
    TEXT_MAIN,
    TEXT_MUTED,
    CHIP_BG,
    CHIP_FG,
    DROPDOWN_BG,
    DROPDOWN_BG_HOVER,
    DROPDOWN_BORDER,
    DROPDOWN_ARROW,
    DROPDOWN_TEXT,
    DROPDOWN_POPUP_BG,
    CATEGORY_THEMES,
    FONT_FAMILY,
    FONT_HERO_TITLE,
    FONT_HERO_SUB,
    FONT_NAV_ITEM,
    FONT_SECTION_TITLE,
    FONT_CARD_TITLE,
    FONT_CARD_INFO,
    FONT_BUTTON,
    draw_rounded_rect,
)
from data_manager import load_places_dataset, load_landmarks_dataset
from logic import (
    ACCESSIBILITY_FEATURES,
    PROFILES,
    CATEGORIES,
    filter_places,
    haversine_distance,
)
from ui_components import render_venue_card, show_audit_details_dialog

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Category definitions for the "Browse by Category" cards (Hospitals, Metro Stations, Retail & Shopping, Parks & Gardens, Public Places, Colleges)
CATEGORY_CARDS_DATA = [
    ("🏥", "Hospitals", "Hospitals"),
    ("🚇", "Metro\nStations", "Railway/Metro Stations"),
    ("🛍", "Retail &\nShopping", "Malls"),
    ("🌳", "Parks &\nGardens", "Parks"),
    ("🏛", "Public\nPlaces", "Public Buildings"),
    ("🎓", "Colleges", "Colleges"),
]



