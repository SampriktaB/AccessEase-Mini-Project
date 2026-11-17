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

        # -------------------------------------------------------------
    # Main Layout (Sidebar + Scrollable Content Canvas)
    # -------------------------------------------------------------
    def _build_main_layout(self):
        # 1. Left Navigation Sidebar (Increased width for spacious layout)
        self.sidebar_frame = tk.Frame(self, bg=SIDEBAR_BG, width=SIDEBAR_WIDTH)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)
        self._build_sidebar(self.sidebar_frame)

        # 2. Right Scrollable Canvas Area
        scroll_outer = tk.Frame(self, bg=BACKGROUND_PAGE)
        scroll_outer.pack(side="left", fill="both", expand=True)

        self.main_canvas = tk.Canvas(scroll_outer, bg=BACKGROUND_PAGE, highlightthickness=0)
        self.main_scrollbar = ttk.Scrollbar(scroll_outer, orient="vertical", style="Violet.Vertical.TScrollbar", command=self.main_canvas.yview)
        self.main_content = tk.Frame(self.main_canvas, bg=BACKGROUND_PAGE)

        self.main_content.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")),
        )
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.main_content, anchor="nw")
        self.main_canvas.bind(
            "<Configure>",
            lambda e: self.main_canvas.itemconfig(self.canvas_window, width=e.width),
        )

        self.main_canvas.configure(yscrollcommand=self.main_scrollbar.set)
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.main_scrollbar.pack(side="right", fill="y")

        # Smooth mousewheel scrolling
        self.main_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Populate Sections
        self._build_hero_section(self.main_content)
        self._build_proximity_section(self.main_content)
        self._build_browse_category_section(self.main_content)
        self._build_places_section(self.main_content)

    def _on_mousewheel(self, event):
        if self.main_canvas.winfo_exists():
            self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # -------------------------------------------------------------
    # 1. Sidebar Architecture & Rounded Navigation Helpers
    # -------------------------------------------------------------
    @staticmethod
    def _round_image_corners(im: Image.Image, radius: int = 18, border_color=None, border_width: int = 1) -> Image.Image:
        """
        Applies smooth anti-aliased rounded corners to any PIL RGBA image.
        Uses 2x supersampling to ensure completely smooth, anti-aliased curved borders.
        """
        im = im.convert("RGBA")
        w, h = im.size

        scale = 2
        big_size = (w * scale, h * scale)
        mask = Image.new("L", big_size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle(
            [(0, 0), (big_size[0] - 1, big_size[1] - 1)],
            radius=radius * scale,
            fill=255,
        )
        mask = mask.resize((w, h), Image.Resampling.LANCZOS)

        result = im.copy()

        if border_color:
            border_overlay = Image.new("RGBA", big_size, (0, 0, 0, 0))
            b_draw = ImageDraw.Draw(border_overlay)
            b_draw.rounded_rectangle(
                [(1, 1), (big_size[0] - 2, big_size[1] - 2)],
                radius=radius * scale,
                outline=border_color,
                width=border_width * scale,
            )
            border_overlay = border_overlay.resize((w, h), Image.Resampling.LANCZOS)
            result = Image.alpha_composite(result, border_overlay)

        # Apply rounded corner alpha mask ensuring completely transparent corners
        orig_r, orig_g, orig_b, orig_a = result.split()
        final_a = ImageChops.multiply(orig_a, mask)
        result.putalpha(final_a)

        return result

    def _build_sidebar(self, parent):
        # Top Logo & Tagline (Centered in top of panel, enlarged, with smooth rounded corners)
        logo_path = os.path.join(ASSETS_DIR, "sidebar_logo_v2.png")
        if os.path.exists(logo_path):
            try:
                im = Image.open(logo_path).convert("RGBA")
                # Enlarged proportionally with comfortable bottom padding for tagline
                im = im.resize((216, 181), Image.Resampling.LANCZOS)
                # Apply smooth rounded corners to the logo box
                im = self._round_image_corners(im, radius=18, border_color="#6432B8", border_width=1)
                self.images_cache["sidebar_logo"] = ImageTk.PhotoImage(im)
                lbl_logo = tk.Label(parent, image=self.images_cache["sidebar_logo"], bg=SIDEBAR_BG, bd=0, highlightthickness=0)
                lbl_logo.pack(side="top", anchor="center", pady=(18, 8))
            except Exception:
                self._build_fallback_brand(parent)
        else:
            self._build_fallback_brand(parent)

        # Nav Menu Container (Rounded capsule buttons shifted downwards with generous spacing)
        self.nav_buttons = {}
        nav_items = [
            ("🏠 Home", "Home"),
            ("📍 Nearby Places", "Nearby Places"),
            ("🤍 Favorites", "Favorites"),
            ("🕒 History", "History"),
            ("⚙ Settings", "Settings"),
        ]

        menu_frame = tk.Frame(parent, bg=SIDEBAR_BG)
        menu_frame.pack(fill="x", padx=14, pady=(16, 0))

        for display_text, nav_key in nav_items:
            is_active = (nav_key == "Home")
            btn = RoundedNavButton(
                menu_frame,
                text=display_text,
                command=lambda k=nav_key: self._on_nav_clicked(k),
                is_active=is_active,
                width=232,
                height=44,
                radius=16,
            )
            btn.pack(fill="x", pady=3)
            self.nav_buttons[nav_key] = btn

        # Spacer pushing bottom art down
        tk.Frame(parent, bg=SIDEBAR_BG).pack(fill="both", expand=True)

        # Bottom Cursive Script Quote: "Accessible today... Inclusive tomorrow ♡" (Centered text with balanced top & bottom margins)
        quote_path = os.path.join(ASSETS_DIR, "sidebar_quote.png")
        if os.path.exists(quote_path):
            try:
                im = Image.open(quote_path).convert("RGBA")
                # Reduced height to 226x104 for balanced vertical centering above and below text
                im = im.resize((226, 104), Image.Resampling.LANCZOS)
                # Apply smooth rounded corners to the bottom quote box
                im = self._round_image_corners(im, radius=16, border_color="#6432B8", border_width=1)
                self.images_cache["sidebar_quote"] = ImageTk.PhotoImage(im)
                lbl_quote = tk.Label(parent, image=self.images_cache["sidebar_quote"], bg=SIDEBAR_BG, bd=0, highlightthickness=0)
                lbl_quote.pack(side="bottom", anchor="center", pady=(0, 18))
            except Exception:
                self._build_fallback_quote(parent)
        else:
            self._build_fallback_quote(parent)

    def _build_fallback_brand(self, parent):
        brand_canvas = tk.Canvas(parent, width=216, height=120, bg=SIDEBAR_BG, highlightthickness=0)
        brand_canvas.pack(side="top", anchor="center", pady=(18, 12))
        draw_rounded_rect(brand_canvas, 2, 2, 214, 118, radius=18, fill="#3A286B", outline="#6432B8", width=1)
        brand_canvas.create_text(108, 36, text=f"{APP_ICON}", font=("Segoe UI Emoji", 26), fill="#FFFFFF")
        brand_canvas.create_text(108, 74, text=APP_NAME, font=("Segoe UI", 16, "bold"), fill="#FFFFFF")
        brand_canvas.create_text(108, 98, text=APP_TAGLINE, font=("Segoe UI", 8), fill="#C8B8EE")

    def _build_fallback_quote(self, parent):
        quote_canvas = tk.Canvas(parent, width=226, height=90, bg=SIDEBAR_BG, highlightthickness=0)
        quote_canvas.pack(side="bottom", anchor="center", pady=(0, 18))
        draw_rounded_rect(quote_canvas, 2, 2, 224, 88, radius=18, fill="#3A286B", outline="#6432B8", width=1)
        quote_canvas.create_text(113, 34, text="Accessible today...", font=("Segoe Script", 11, "italic"), fill="#D8CBF8")
        quote_canvas.create_text(113, 62, text="Inclusive tomorrow ♡", font=("Segoe Script", 11, "italic"), fill="#D8CBF8")

    # -------------------------------------------------------------
    # 2. Hero Banner with Integrated Search (Rounded Box)
    # -------------------------------------------------------------
    def _build_hero_section(self, parent):
        self.hero_container = tk.Frame(parent, bg=BACKGROUND_PAGE, padx=20)
        self.hero_container.pack(fill="x", pady=(16, 8))

        self.hero_canvas = tk.Canvas(self.hero_container, bg=BACKGROUND_PAGE, highlightthickness=0, height=138)
        self.hero_canvas.pack(fill="x", expand=True)

        hero_card = tk.Frame(self.hero_canvas, bg=HERO_BG)
        self.hero_win = self.hero_canvas.create_window(18, 10, window=hero_card, anchor="nw")

        def _on_hero_resize(e):
            w = e.width
            self.hero_canvas.delete("hero_bg")
            draw_rounded_rect(self.hero_canvas, 2, 2, w - 4, 134, radius=20, fill=HERO_BG, outline="#C9BDF5", width=1, tags="hero_bg")
            self.hero_canvas.tag_lower("hero_bg")
            self.hero_canvas.itemconfig(self.hero_win, width=w - 36)

        self.hero_canvas.bind("<Configure>", _on_hero_resize)

        # Left Column: Heading + Subtitle + Integrated Search Pill
        left_box = tk.Frame(hero_card, bg=HERO_BG)
        left_box.pack(side="left", fill="both", expand=True, anchor="w")

        tk.Label(
            left_box,
            text="Find. Access. Belong.",
            font=FONT_HERO_TITLE,
            bg=HERO_BG,
            fg=HERO_TITLE_COLOR,
        ).pack(anchor="w")

        tk.Label(
            left_box,
            text="More Access, Less Stress!",
            font=FONT_HERO_SUB,
            bg=HERO_BG,
            fg=HERO_SUB_COLOR,
        ).pack(anchor="w", pady=(3, 10))

        # Integrated Wide Search Pill Box (Smooth rounded pill)
        search_pill_canvas = tk.Canvas(left_box, width=460, height=38, bg=HERO_BG, highlightthickness=0)
        search_pill_canvas.pack(anchor="w")
        draw_rounded_rect(search_pill_canvas, 1, 1, 459, 37, radius=18, fill="#FFFFFF", outline="#C8BCF2", width=1)

        search_pill = tk.Frame(search_pill_canvas, bg="#FFFFFF")
        # Explicit width=436, height=30 so search_pill spans the full inner pill length
        search_pill_canvas.create_window(12, 4, window=search_pill, anchor="nw", width=436, height=30)

        # Purple Search Action Button (Packed on far right end of the bar)
        btn_search = tk.Button(
            search_pill,
            text="  🔍  ",
            command=self.refresh_venue_list,
            font=("Segoe UI Emoji", 9, "bold"),
            bg=PRIMARY_COLOR,
            fg="#FFFFFF",
            activebackground=PRIMARY_HOVER,
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=8,
            pady=2,
        )
        btn_search.pack(side="right", padx=(2, 2))

        # Clear Search (✕)
        btn_clear = tk.Label(search_pill, text="✕", font=("Segoe UI", 9, "bold"), bg="#FFFFFF", fg="#A393BD", cursor="hand2")
        btn_clear.pack(side="right", padx=(2, 6))
        btn_clear.bind("<Button-1>", lambda e: self._clear_search())

        self.entry_search = tk.Entry(
            search_pill,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            bg="#FFFFFF",
            fg=TEXT_MAIN,
            relief="flat",
            bd=0,
        )
        self.entry_search.pack(side="left", fill="x", expand=True, padx=(4, 6))
        self.entry_search.bind("<KeyRelease>", lambda e: self.refresh_venue_list())

        # Right Column: Skyline & Wheelchair Outline Artwork
        art_path = os.path.join(ASSETS_DIR, "hero_art_v2.png")
        if os.path.exists(art_path):
            try:
                im = Image.open(art_path).convert("RGBA")
                orig_w, orig_h = im.size
                target_h = 118
                target_w = int((orig_w / orig_h) * target_h)
                im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
                self.images_cache["hero_art_v2"] = ImageTk.PhotoImage(im)
                lbl_art = tk.Label(hero_card, image=self.images_cache["hero_art_v2"], bg=HERO_BG)
                lbl_art.pack(side="right", padx=(14, 0))
            except Exception:
                pass

    def _clear_search(self):
        self.search_var.set("")
        self.refresh_venue_list()

        # -------------------------------------------------------------
    # 2b. Anchor Landmark Proximity Navigation Bar (Rounded Box + Pastel Blue)
    # -------------------------------------------------------------
    def _build_proximity_section(self, parent):
        self.proximity_container = tk.Frame(parent, bg=BACKGROUND_PAGE, padx=20)
        self.proximity_container.pack(fill="x", pady=(2, 6))

        self.prox_canvas = tk.Canvas(self.proximity_container, bg=BACKGROUND_PAGE, highlightthickness=0, height=52)
        self.prox_canvas.pack(fill="x", expand=True)

        bar = tk.Frame(self.prox_canvas, bg=SURFACE_CARD)
        self.prox_win = self.prox_canvas.create_window(16, 26, window=bar, anchor="w")

        def _on_prox_resize(e):
            w = e.width
            h = e.height
            self.prox_canvas.delete("prox_bg")
            draw_rounded_rect(self.prox_canvas, 2, 2, w - 4, h - 2, radius=16, fill=SURFACE_CARD, outline=BORDER_CARD, width=1, tags="prox_bg")
            self.prox_canvas.tag_lower("prox_bg")
            self.prox_canvas.coords(self.prox_win, 16, h // 2)
            self.prox_canvas.itemconfig(self.prox_win, width=w - 32)

        self.prox_canvas.bind("<Configure>", _on_prox_resize)

        # 1. Landmark Selector
        lm_box = tk.Frame(bar, bg=SURFACE_CARD)
        lm_box.pack(side="left", padx=(0, 14))

        tk.Label(
            lm_box,
            text="📍 Nearest Landmark:",
            font=("Segoe UI", 9, "bold"),
            bg=SURFACE_CARD,
            fg=PRIMARY_DARK,
        ).pack(side="left", padx=(0, 6))

        self.landmark_options = ["None (All Pune Venues)"]
        if not self.df_landmarks.empty:
            for _, row in self.df_landmarks.iterrows():
                area = f" ({row['landmark_area']})" if str(row.get("landmark_area", "")).strip() else ""
                desc = f" — {row['description']}" if str(row.get("description", "")).strip() else ""
                self.landmark_options.append(f"{row['name']}{area}{desc}")

        self.landmark_var = tk.StringVar(value=self.landmark_options[0])

        self.combo_landmark = ttk.Combobox(
            lm_box,
            textvariable=self.landmark_var,
            values=self.landmark_options,
            state="readonly",
            style="Pastel.TCombobox",
            width=36,
            font=("Segoe UI", 9),
        )
        self.combo_landmark.pack(side="left")
        self.combo_landmark.bind("<<ComboboxSelected>>", lambda e: self._on_proximity_changed())

        # Enable horizontal side-scroll in landmark dropdown
        enable_combobox_horizontal_scroll(self.combo_landmark)

        # 2. Radius Filter
        rad_box = tk.Frame(bar, bg=SURFACE_CARD)
        rad_box.pack(side="left", padx=(0, 14))

        tk.Label(
            rad_box,
            text="📏 Radius:",
            font=("Segoe UI", 9, "bold"),
            bg=SURFACE_CARD,
            fg=PRIMARY_DARK,
        ).pack(side="left", padx=(0, 6))

        self.radius_options = ["Any Distance", "Within 2 km", "Within 5 km", "Within 10 km"]
        self.radius_var = tk.StringVar(value=self.radius_options[0])

        self.combo_radius = ttk.Combobox(
            rad_box,
            textvariable=self.radius_var,
            values=self.radius_options,
            state="readonly",
            style="Pastel.TCombobox",
            width=13,
            font=("Segoe UI", 9),
        )
        self.combo_radius.pack(side="left")
        self.combo_radius.bind("<<ComboboxSelected>>", lambda e: self._on_proximity_changed())

        # 3. Sort Preference
        sort_box = tk.Frame(bar, bg=SURFACE_CARD)
        sort_box.pack(side="left", padx=(0, 10))

        tk.Label(
            sort_box,
            text="🔀 Sort:",
            font=("Segoe UI", 9, "bold"),
            bg=SURFACE_CARD,
            fg=PRIMARY_DARK,
        ).pack(side="left", padx=(0, 6))

        self.sort_options = ["Highest Match %", "Nearest Distance"]
        self.sort_var = tk.StringVar(value=self.sort_options[0])

        self.combo_sort = ttk.Combobox(
            sort_box,
            textvariable=self.sort_var,
            values=self.sort_options,
            state="readonly",
            style="Pastel.TCombobox",
            width=17,
            font=("Segoe UI", 9),
        )
        self.combo_sort.pack(side="left")
        self.combo_sort.bind("<<ComboboxSelected>>", lambda e: self._on_proximity_changed())

        # Reset Proximity Button
        btn_reset_prox = tk.Button(
            bar,
            text="Reset Proximity",
            command=self._reset_proximity,
            font=("Segoe UI", 8, "bold"),
            bg=DROPDOWN_BG,
            fg=DROPDOWN_TEXT,
            activebackground=DROPDOWN_BG_HOVER,
            relief="flat",
            bd=0,
            padx=10,
            pady=3,
            cursor="hand2",
        )
        btn_reset_prox.pack(side="right")

    def _on_proximity_changed(self):
        sel_idx = self.combo_landmark.current()
        if sel_idx > 0 and not self.df_landmarks.empty:
            row = self.df_landmarks.iloc[sel_idx - 1]
            self.selected_landmark = {
                "id": int(row["id"]),
                "name": str(row["name"]),
                "area": str(row["landmark_area"]),
                "latitude": float(row["latitude"]),
                "longitude": float(row["longitude"]),
            }
        else:
            self.selected_landmark = None

        rad_idx = self.combo_radius.current()
        radius_map = {0: None, 1: 2.0, 2: 5.0, 3: 10.0}
        self.selected_radius_km = radius_map.get(rad_idx, None)

        sort_idx = self.combo_sort.current()
        self.sort_mode = "distance" if sort_idx == 1 else "match"

        self.refresh_venue_list()

    def _reset_proximity(self):
        self.landmark_var.set(self.landmark_options[0])
        self.radius_var.set(self.radius_options[0])
        self.sort_var.set(self.sort_options[0])
        self.selected_landmark = None
        self.selected_radius_km = None
        self.sort_mode = "match"
        self.refresh_venue_list()

    # -------------------------------------------------------------
    # 3. "Browse by Category" Section
    # -------------------------------------------------------------
    def _build_browse_category_section(self, parent):
        self.cat_section = tk.Frame(parent, bg=BACKGROUND_PAGE, padx=20)
        self.cat_section.pack(fill="x", pady=(6, 10))

        # Header Row: "Browse by Category" + "View All →" + "⚙ Filters"
        header_row = tk.Frame(self.cat_section, bg=BACKGROUND_PAGE)
        header_row.pack(fill="x", pady=(0, 10))

        tk.Label(
            header_row,
            text="Browse by Category",
            font=FONT_SECTION_TITLE,
            bg=BACKGROUND_PAGE,
            fg=TEXT_MAIN,
        ).pack(side="left")

        actions_box = tk.Frame(header_row, bg=BACKGROUND_PAGE)
        actions_box.pack(side="right")

        # "View All →" Link
        btn_view_all = tk.Label(
            actions_box,
            text="View All →",
            font=("Segoe UI", 10, "bold"),
            bg=BACKGROUND_PAGE,
            fg=PRIMARY_COLOR,
            cursor="hand2",
        )
        btn_view_all.pack(side="left", padx=(0, 14))
        btn_view_all.bind("<Button-1>", lambda e: self._on_category_card_clicked("All Categories"))

        # "⚙ Filters" Button
        btn_filter = tk.Button(
            actions_box,
            text="⚙ Filters",
            font=("Segoe UI", 9, "bold"),
            bg="#FFFFFF",
            fg=PRIMARY_COLOR,
            activebackground="#EDE7FB",
            relief="flat",
            bd=0,
            padx=12,
            pady=4,
            cursor="hand2",
            command=self._open_filters_modal,
        )
        btn_filter.pack(side="left")

        # Category Cards Row (Rounded Cards)
        cards_row = tk.Frame(self.cat_section, bg=BACKGROUND_PAGE)
        cards_row.pack(fill="x")

        self.category_card_widgets = {}

        for icon_char, label_text, cat_key in CATEGORY_CARDS_DATA:
            cat_theme = CATEGORY_THEMES.get(cat_key, CATEGORY_THEMES["Public Buildings"])
            is_active = (cat_key == self.current_category)

            # Smooth rounded canvas card for each category box
            card_canvas = tk.Canvas(
                cards_row,
                width=134,
                height=104,
                bg=BACKGROUND_PAGE,
                highlightthickness=0,
                cursor="hand2",
            )
            card_canvas.pack(side="left", padx=(0, 10))

            outline_c = cat_theme["color"] if is_active else cat_theme["border"]
            outline_w = 3 if is_active else 1

            rect_id = draw_rounded_rect(
                card_canvas,
                2, 2, 132, 102,
                radius=16,
                fill=cat_theme["bg"],
                outline=outline_c,
                width=outline_w,
            )

            ic_id = card_canvas.create_text(
                67, 36,
                text=icon_char,
                font=("Segoe UI Emoji", 21),
                fill=cat_theme["color"],
            )

            lb_id = card_canvas.create_text(
                67, 74,
                text=label_text,
                font=("Segoe UI", 9, "bold"),
                fill=cat_theme["color"],
                justify="center",
            )

            for w_id in (rect_id, ic_id, lb_id):
                card_canvas.tag_bind(w_id, "<Button-1>", lambda e, ck=cat_key: self._on_category_card_clicked(ck))
            card_canvas.bind("<Button-1>", lambda e, ck=cat_key: self._on_category_card_clicked(ck))

            self.category_card_widgets[cat_key] = (card_canvas, rect_id, ic_id, lb_id, cat_theme)

    def _on_category_card_clicked(self, category_key):
        self.current_category = category_key

        # Update visual highlight on cards matching category colors
        for ck, (canvas, rect_id, ic_id, lb_id, theme) in self.category_card_widgets.items():
            active = (ck == category_key)
            canvas.itemconfig(
                rect_id,
                outline=theme["color"] if active else theme["border"],
                width=3 if active else 1,
            )

        self.refresh_venue_list()

        # -------------------------------------------------------------
    # 4. "Nearby Accessible Places" Section
    # -------------------------------------------------------------
    def _build_places_section(self, parent):
        self.places_section = tk.Frame(parent, bg=BACKGROUND_PAGE, padx=20)
        self.places_section.pack(fill="both", expand=True, pady=(6, 12))

        # Section Heading Frame
        self.heading_row = tk.Frame(self.places_section, bg=BACKGROUND_PAGE)
        self.heading_row.pack(fill="x", pady=(0, 8))

        self.lbl_places_heading = tk.Label(
            self.heading_row,
            text="Nearby Accessible Places",
            font=FONT_SECTION_TITLE,
            bg=BACKGROUND_PAGE,
            fg=TEXT_MAIN,
        )
        self.lbl_places_heading.pack(side="left")

        self.lbl_places_sub = tk.Label(
            self.heading_row,
            text="",
            font=("Segoe UI", 9, "italic"),
            bg=BACKGROUND_PAGE,
            fg=TEXT_MUTED,
        )
        self.lbl_places_sub.pack(side="left", padx=(10, 0))

        # Venue Cards Container
        self.cards_list_frame = tk.Frame(self.places_section, bg=BACKGROUND_PAGE)
        self.cards_list_frame.pack(fill="both", expand=True)

    # -------------------------------------------------------------
    # Navigation Controller Callbacks
    # -------------------------------------------------------------
    def _apply_nav_layout(self, nav_key):
        """Unpacks dynamic sections and repacks them in clean sequential order."""
        # Unpack all dynamic sections first
        self.hero_container.pack_forget()
        self.proximity_container.pack_forget()
        self.cat_section.pack_forget()
        self.places_section.pack_forget()

        # Repack in strict top-to-bottom order based on tab
        if nav_key == "Home":
            self.hero_container.pack(fill="x", pady=(16, 8))
            self.proximity_container.pack(fill="x", pady=(2, 6))
            self.cat_section.pack(fill="x", pady=(6, 10))
            self.places_section.pack(fill="both", expand=True, pady=(6, 12))
            self.lbl_places_heading.config(text="Nearby Accessible Places")
        elif nav_key == "Nearby Places":
            self.proximity_container.pack(fill="x", pady=(14, 6))
            self.cat_section.pack(fill="x", pady=(6, 10))
            self.places_section.pack(fill="both", expand=True, pady=(6, 12))
            self.lbl_places_heading.config(text="Nearby Accessible Places")
        elif nav_key == "Favorites":
            self.places_section.pack(fill="both", expand=True, pady=(16, 12))
            self.lbl_places_heading.config(text="💖 Your Saved Favorites")
        elif nav_key == "History":
            self.places_section.pack(fill="both", expand=True, pady=(16, 12))
            self.lbl_places_heading.config(text="🕒 Recently Inspected Venues")

        self.main_content.update_idletasks()
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        self.main_canvas.yview_moveto(0)

    def _on_nav_clicked(self, nav_key):
        self.current_nav = nav_key

        # Update button highlights
        for k, btn in self.nav_buttons.items():
            if k == nav_key:
                btn.config(bg=SIDEBAR_ACTIVE, fg=SIDEBAR_TEXT_ACTIVE)
            else:
                btn.config(bg=SIDEBAR_BG, fg=SIDEBAR_TEXT)

        if nav_key == "Settings":
            self._open_filters_modal()
            return

        self._apply_nav_layout(nav_key)

        if nav_key == "Home":
            self.current_category = "All Categories"
            self.search_var.set("")
            self._on_category_card_clicked("All Categories")
        elif nav_key == "Nearby Places":
            self.current_category = "All Categories"
            self.search_var.set("")
            # Automatically activate 1st anchor landmark (e.g. Karve Statue Chowk) and 5 km radius if none selected
            if not self.selected_landmark and not self.df_landmarks.empty:
                self.combo_landmark.current(1)
                self.combo_radius.current(2)  # Within 5 km
                self._on_proximity_changed()
            else:
                self.refresh_venue_list()
        elif nav_key == "Favorites":
            self.refresh_venue_list()
        elif nav_key == "History":
            self._render_history_view()

    def _toggle_bookmark(self, place_id):
        if place_id in self.saved_places:
            self.saved_places.remove(place_id)
        else:
            self.saved_places.add(place_id)

        # Update Favorites Nav label
        btn_fav = self.nav_buttons.get("Favorites")
        if btn_fav:
            count = len(self.saved_places)
            label = f"  🤍 Favorites ({count})" if count > 0 else "  🤍 Favorites"
            btn_fav.config(text=label)

        if self.current_nav == "History":
            self._render_history_view()
        else:
            self.refresh_venue_list()

    def _open_details(self, place):
        p_id = int(place["id"])
        if p_id not in self.history_places:
            self.history_places.insert(0, p_id)
            if len(self.history_places) > 15:
                self.history_places.pop()

        active_features = [name for name, var in self.feature_vars.items() if var.get()]
        show_audit_details_dialog(self, place, active_features)
