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


def enable_combobox_horizontal_scroll(combobox):
    """Enables horizontal side scrollbar and pastel styling on the dropdown popdown listbox."""
    try:
        popdown = combobox.tk.eval(f"ttk::combobox::PopdownWindow {combobox}")
        f = f"{popdown}.f"
        combobox.tk.eval(f"""
            if {{![winfo exists {f}.hsb]}} {{
                ttk::scrollbar {f}.hsb -orient horizontal -style Blue.Horizontal.TScrollbar -command [list {f}.l xview]
                {f}.l configure -xscrollcommand [list {f}.hsb set] -background {DROPDOWN_POPUP_BG} -foreground #1E1038 -selectbackground {DROPDOWN_BG_HOVER} -selectforeground {DROPDOWN_TEXT}
                grid {f}.hsb -row 1 -column 0 -sticky ew
            }}
            catch {{{f}.sb configure -style Blue.Vertical.TScrollbar}}
            if {{![winfo exists {f}.corner]}} {{
                frame {f}.corner -background {DROPDOWN_BG} -bd 0 -highlightthickness 0
                grid {f}.corner -row 1 -column 1 -sticky nsew
            }} else {{
                {f}.corner configure -background {DROPDOWN_BG}
            }}
            catch {{{f} configure -style ComboboxPopdownFrame}}
        """)
    except Exception:
        pass


class RoundedNavButton(tk.Canvas):
    """
    A modern rounded capsule navigation button for the sidebar.
    Renders smooth rounded pill shapes with active and hover states.
    """
    def __init__(self, parent, text, command, is_active=False, width=232, height=44, radius=16):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=SIDEBAR_BG,
            highlightthickness=0,
            cursor="hand2",
        )
        self.command = command
        self.is_active = is_active
        self.radius = radius
        self.w = width
        self.h = height
        self._text_str = text
        self._hovered = False

        self._render()

        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _render(self):
        self.delete("all")
        bg_fill = SIDEBAR_ACTIVE if self.is_active else (SIDEBAR_HOVER if self._hovered else SIDEBAR_BG)
        fg_color = SIDEBAR_TEXT_ACTIVE if self.is_active else SIDEBAR_TEXT

        self.rect_id = draw_rounded_rect(
            self,
            2, 2, self.w - 2, self.h - 2,
            radius=self.radius,
            fill=bg_fill,
            outline="#7946D6" if self.is_active else "",
            width=1 if self.is_active else 0,
            tags="bg_pill",
        )
        self.text_id = self.create_text(
            20, self.h // 2,
            text=f"  {self._text_str.strip()}",
            font=FONT_NAV_ITEM,
            fill=fg_color,
            anchor="w",
            tags="text_label",
        )
        self.tag_bind(self.rect_id, "<Button-1>", lambda e: self.command())
        self.tag_bind(self.text_id, "<Button-1>", lambda e: self.command())

    def _on_enter(self, e):
        if not self.is_active:
            self._hovered = True
            self.itemconfig(self.rect_id, fill=SIDEBAR_HOVER)

    def _on_leave(self, e):
        if not self.is_active:
            self._hovered = False
            self.itemconfig(self.rect_id, fill=SIDEBAR_BG)

    def set_active(self, active: bool):
        self.is_active = active
        self._hovered = False
        self._render()

    def set_text(self, text: str):
        self._text_str = text
        self.itemconfig(self.text_id, text=f"  {text.strip()}")

    def config(self, **kwargs):
        if "text" in kwargs:
            self.set_text(kwargs["text"])
        if "bg" in kwargs:
            active = (kwargs["bg"] == SIDEBAR_ACTIVE)
            self.set_active(active)
        if "fg" in kwargs and not self.is_active:
            self.itemconfig(self.text_id, fill=kwargs["fg"])

    def cget(self, key):
        if key == "text":
            return self._text_str
        return super().cget(key)

    def __getitem__(self, key):
        return self.cget(key)


class AccessEaseDesktopApp(tk.Tk):
    """Modern Desktop Application Controller matching mockup v2."""

    def __init__(self):
        super().__init__()

        # Window Setup
        self.title(f"{APP_NAME} - {APP_SUBTITLE}")
        self.geometry("1240x840")
        self.minsize(1100, 720)
        self.configure(bg=BACKGROUND_PAGE)

        # Center Window
        self._center_window(1240, 840)

        # Application State
        self.df_places = load_places_dataset()
        self.df_landmarks = load_landmarks_dataset()
        self.saved_places = set()
        self.history_places = []
        self.feature_vars = {feat: tk.BooleanVar(value=False) for feat in ACCESSIBILITY_FEATURES.keys()}
        self.active_profile = "Wheelchair User"
        self.current_category = "All Categories"
        self.current_nav = "Home"
        self.search_var = tk.StringVar(value="")

        # Anchor-Based Landmark Proximity State
        self.selected_landmark = None
        self.selected_radius_km = None
        self.sort_mode = "match"

        # Image references to avoid garbage collection
        self.images_cache = {}

        # Set default profile (Wheelchair User)
        self._apply_profile_preset("Wheelchair User")

        # Build UI Architecture
        self._setup_ttk_styles()
        self._build_main_layout()

        # Initial Render
        self.refresh_venue_list()

    def _center_window(self, width, height):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = max(0, int((screen_w - width) / 2))
        y = max(0, int((screen_h - height) / 2))
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _setup_ttk_styles(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=BACKGROUND_PAGE)
        style.configure("Card.TFrame", background=SURFACE_CARD)
        style.configure("ComboboxPopdownFrame", background=DROPDOWN_BG)

        # Pastel Violet / Lavender Dropdown Theme
        style.configure(
            "Pastel.TCombobox",
            fieldbackground=DROPDOWN_BG,
            background=DROPDOWN_BG_HOVER,
            foreground=DROPDOWN_TEXT,
            arrowcolor=DROPDOWN_ARROW,
            bordercolor=DROPDOWN_BORDER,
            lightcolor=DROPDOWN_BG,
            darkcolor=DROPDOWN_BORDER,
            selectbackground=DROPDOWN_BG_HOVER,
            selectforeground=DROPDOWN_TEXT,
            padding=5,
        )
        style.map(
            "Pastel.TCombobox",
            fieldbackground=[
                ("readonly", DROPDOWN_BG),
                ("hover", DROPDOWN_BG_HOVER),
                ("focus", DROPDOWN_BG),
            ],
            background=[
                ("readonly", DROPDOWN_BG_HOVER),
                ("hover", DROPDOWN_BORDER),
                ("active", DROPDOWN_BORDER),
            ],
            selectbackground=[("readonly", DROPDOWN_BG)],
            selectforeground=[("readonly", DROPDOWN_TEXT)],
        )

        # Dark Violet Main Scrollbar Theme (Right Sidebar)
        style.configure(
            "Violet.Vertical.TScrollbar",
            background="#482490",       # Dark violet thumb
            troughcolor=BACKGROUND_PAGE, # Seamless soft lilac trough
            bordercolor="#E5DCF8",
            arrowcolor="#482490",
            lightcolor="#5E29A8",
            darkcolor="#3A1C78",
            relief="flat",
            borderwidth=0,
            arrowsize=13,
        )
        style.map(
            "Violet.Vertical.TScrollbar",
            background=[("pressed", "#3A1C78"), ("active", "#5E29A8")],
            arrowcolor=[("pressed", "#3A1C78"), ("active", "#5E29A8")],
        )

        # Dark Violet Scrollbar Theme (Landmark Dropdown)
        style.configure(
            "Blue.Horizontal.TScrollbar",
            background="#482490",       # Dark violet thumb
            troughcolor=DROPDOWN_BG,    # Soft pastel lilac trough (#EDE7FB)
            bordercolor="#DDD6FE",
            arrowcolor="#482490",
            lightcolor="#5E29A8",
            darkcolor="#3A1C78",
            relief="flat",
            borderwidth=0,
            arrowsize=11,
        )
        style.map(
            "Blue.Horizontal.TScrollbar",
            background=[("pressed", "#3A1C78"), ("active", "#5E29A8")],
            arrowcolor=[("pressed", "#3A1C78"), ("active", "#5E29A8")],
        )

        style.configure(
            "Blue.Vertical.TScrollbar",
            background="#482490",       # Dark violet thumb
            troughcolor=DROPDOWN_BG,    # Soft pastel lilac trough (#EDE7FB)
            bordercolor="#DDD6FE",
            arrowcolor="#482490",
            lightcolor="#5E29A8",
            darkcolor="#3A1C78",
            relief="flat",
            borderwidth=0,
            arrowsize=11,
        )
        style.map(
            "Blue.Vertical.TScrollbar",
            background=[("pressed", "#3A1C78"), ("active", "#5E29A8")],
            arrowcolor=[("pressed", "#3A1C78"), ("active", "#5E29A8")],
        )

        
