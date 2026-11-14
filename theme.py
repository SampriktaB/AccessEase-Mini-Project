"""
AccessEase - Modern Purple & Pastel Lilac Design System (Mockup v2)
Author: Samprikta
Description:
    Matches the modern, sleek mockup design v2:
    - Deep Royal Purple Sidebar (#482490)
    - Soothing Pastel Lilac Canvas (#F5F3FE)
    - Hero Banner with Integrated Search (#D6CFFB)
    - "Browse by Category" Cards Grid
    - "Nearby Accessible Places" List with centered category icon badges
"""

# -----------------------------------------------------------------------------
# Branding & App Identity
# -----------------------------------------------------------------------------
APP_NAME            = "AccessEase"
APP_ICON            = "♿"
APP_SUBTITLE        = "Accessibility Assistant"
APP_TAGLINE         = "Connect • Access • Include"

# -----------------------------------------------------------------------------
# Color Palette (Matching Mockup Aesthetics)
# -----------------------------------------------------------------------------
# Sidebar Colors
SIDEBAR_WIDTH       = 260         # Increased width for spacious left side panel
SIDEBAR_BG          = "#482490"   # Deep Royal Purple Sidebar
SIDEBAR_HOVER       = "#582BAF"   # Hover state for nav items
SIDEBAR_ACTIVE      = "#6432B8"   # Active nav pill (soft glowing capsule)
SIDEBAR_TEXT        = "#D8CBF8"   # Soft lavender navigation text
SIDEBAR_TEXT_ACTIVE = "#FFFFFF"   # Bright white text for active tab
SIDEBAR_DIVIDER     = "#5A2EAC"   # Subtle separator

# Main Surface & Canvas
BACKGROUND_PAGE     = "#F5F3FE"   # Calming pastel lilac background
SURFACE_CARD        = "#FFFFFF"   # Clean white card surface
BORDER_CARD         = "#E5DCF8"   # Subtle card border
BORDER_SUBTLE       = "#D8C9F3"   # General subtle border

# Hero Banner
HERO_BG             = "#D6CFFB"   # Soft lavender hero container
HERO_TITLE_COLOR    = "#220D4A"   # Bold deep purple ("Find. Access. Belong.")
HERO_SUB_COLOR      = "#4A3575"   # Muted purple subtitle ("More Access, Less Stress!")

# Brand Accents & Interactive Elements
PRIMARY_COLOR       = "#5E29A8"   # Rich Purple (Search button & Active category)
PRIMARY_DARK        = "#482490"   # Deep Purple Header/Accent
PRIMARY_LIGHT       = "#EDE7FB"   # Soft Lilac Chip Background
PRIMARY_HOVER       = "#4F1E94"   # Hover state for buttons

# Typography Colors
TEXT_MAIN           = "#1E1038"   # Deep purple-black for venue names
TEXT_MUTED          = "#5C4F73"   # Muted slate for address and contact
TEXT_SECONDARY      = "#796A93"   # Secondary meta information

# Facility Chips & Status Badges
CHIP_BG             = "#EDE7FB"   # Soft lavender chip background
CHIP_FG             = "#5B21B6"   # Deep purple chip text
MATCH_HIGH_BG       = "#D1FAE5"   # Mint green pill for high matches
MATCH_HIGH_FG       = "#065F46"   # Forest green text
MATCH_MED_BG        = "#FEF3C7"   # Warm amber pill
MATCH_MED_FG        = "#92400E"   # Deep amber text
MATCH_LOW_BG        = "#FCE7F3"   # Soft rose pill
MATCH_LOW_FG        = "#9D174D"   # Berry red text
DISTANCE_BG         = "#EDE7FB"   # Soft purple for landmark distance pill
DISTANCE_FG         = "#5B21B6"   # Deep purple distance text
DISTANCE_BORDER     = "#D8CBF8"   # Distance pill border

# Pastel Violet / Lavender Dropdown Theme
DROPDOWN_BG         = "#EDE7FB"   # Soft pastel lilac / lavender
DROPDOWN_BG_HOVER   = "#DDD6FE"   # Active / hover soft violet
DROPDOWN_BORDER     = "#C4B5FD"   # Pastel violet outline
DROPDOWN_ARROW      = "#5B21B6"   # Deep purple chevron
DROPDOWN_TEXT       = "#482490"   # Deep royal violet text
DROPDOWN_POPUP_BG   = "#FAF8FF"   # Clean light lavender-white for dropdown list

# Category Ribbon & Icon Colors
CATEGORY_THEMES = {
    "Hospitals": {
        "icon": "🏥",
        "label": "Hospitals",
        "color": "#0284C7",
        "bg": "#E0F2FE",
        "border": "#BAE6FD",
    },
    "Colleges": {
        "icon": "🎓",
        "label": "Colleges",
        "color": "#1E40AF",
        "bg": "#DBEAFE",
        "border": "#BFDBFE",
    },
    "Parks": {
        "icon": "🌳",
        "label": "Parks &\nGardens",
        "color": "#15803D",
        "bg": "#DCFCE7",
        "border": "#BBF7D0",
    },
    "Malls": {
        "icon": "🛍",
        "label": "Retail &\nShopping",
        "color": "#BE185D",
        "bg": "#FCE7F3",
        "border": "#FBCFE8",
    },
    "Railway/Metro Stations": {
        "icon": "🚇",
        "label": "Metro\nStations",
        "color": "#9A3412",
        "bg": "#FFEDD5",
        "border": "#FDBA74",
    },
    "Public Buildings": {
        "icon": "🏛",
        "label": "Public\nPlaces",
        "color": "#A16207",
        "bg": "#FEF9C3",
        "border": "#FDE047",
    },
}