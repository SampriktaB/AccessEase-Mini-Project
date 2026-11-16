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

    # -------------------------------------------------------------
    # 1. Left: Dedicated Category Icon Badge (Pure icon, Rounded & 100% Centered!)
    # -------------------------------------------------------------
    icon_canvas = tk.Canvas(
        card,
        width=58,
        height=58,
        bg=SURFACE_CARD,
        highlightthickness=0,
    )
    icon_canvas.pack(side="left", padx=(0, 14))
    draw_rounded_rect(
        icon_canvas,
        2, 2, 56, 56,
        radius=14,
        fill=cat_theme["bg"],
        outline=cat_theme["border"],
        width=1,
    )
    icon_canvas.create_text(29, 29, text=cat_theme["icon"], font=("Segoe UI Emoji", 24))

    # -------------------------------------------------------------
    # 2. Center: Name, Address, Contact, and Facility Chips
    # -------------------------------------------------------------
    center_frame = tk.Frame(card, bg=SURFACE_CARD)
    center_frame.pack(side="left", fill="both", expand=True)

    # Line 1: Venue Name
    title_row = tk.Frame(center_frame, bg=SURFACE_CARD)
    title_row.pack(anchor="w", fill="x")

    tk.Label(
        title_row,
        text=place["name"],
        font=FONT_CARD_TITLE,
        bg=SURFACE_CARD,
        fg=TEXT_MAIN,
    ).pack(side="left")

    # Line 2: Address & Contact
    info_row = tk.Frame(center_frame, bg=SURFACE_CARD)
    info_row.pack(anchor="w", fill="x", pady=(2, 5))

    region_str = f", {place['region']}" if place.get("region") and str(place.get("region")).strip() else ""
    addr_text = f"📍 {place['address']}{region_str}, {place['city']}"
    contact_text = f"📞 {place['contact']}"

    tk.Label(
        info_row,
        text=f"{addr_text}    {contact_text}",
        font=FONT_CARD_INFO,
        bg=SURFACE_CARD,
        fg=TEXT_MUTED,
    ).pack(side="left")

    # Line 3: Soft Lavender Facility Chips
    chips_row = tk.Frame(center_frame, bg=SURFACE_CARD)
    chips_row.pack(anchor="w", fill="x", pady=(2, 0))

    # Collect available facilities
    available_chips = []
    for col_key, chip_name in FACILITY_SHORT_NAMES.items():
        if str(place.get(col_key, "")).strip().capitalize() == "Available":
            available_chips.append(chip_name)

    # Show up to 5 chips
    for chip_text in available_chips[:5]:
        c_lbl = tk.Label(
            chips_row,
            text=chip_text,
            font=FONT_CHIP,
            bg=CHIP_BG,
            fg=CHIP_FG,
            padx=8,
            pady=2,
            relief="flat",
        )
        c_lbl.pack(side="left", padx=(0, 6))

    if not available_chips:
         c_lbl = tk.Label(
            chips_row,
            text="Accessibility verification in progress",
            font=FONT_CHIP,
            bg="#F3F0F9",
            fg="#7E7295",
            padx=8,
            pady=2,
        )
        c_lbl.pack(side="left") 

    # -------------------------------------------------------------
    # 3. Right: Distance Pill, Match Pill & Action Buttons
    # -------------------------------------------------------------
    right_frame = tk.Frame(card, bg=SURFACE_CARD)
    right_frame.pack(side="right", padx=(10, 0))

    # Proximity Distance Pill (Anchor-Based Landmark System)
    dist_val = place.get("distance_km")
    if dist_val is not None:
        try:
            d_float = float(dist_val)
            dist_canvas = tk.Canvas(right_frame, width=96, height=28, bg=SURFACE_CARD, highlightthickness=0)
            draw_rounded_rect(dist_canvas, 1, 1, 95, 27, radius=12, fill=DISTANCE_BG, outline=DISTANCE_BORDER, width=1)
            dist_canvas.create_text(48, 14, text=f"📍 {d_float:.2f} km", font=FONT_MATCH_BADGE, fill=DISTANCE_FG)
            dist_canvas.pack(side="left", padx=(0, 8))
        except (ValueError, TypeError):
            pass

    # Match Pill
    if match_pct >= 80:
        match_bg, match_fg = MATCH_HIGH_BG, MATCH_HIGH_FG
        icon_str = "✔"
    elif match_pct >= 50:
        match_bg, match_fg = MATCH_MED_BG, MATCH_MED_FG
        icon_str = "✨"
    else:
        match_bg, match_fg = MATCH_LOW_BG, MATCH_LOW_FG
        icon_str = "💡"

    match_border = MATCH_HIGH_FG if match_pct >= 80 else (MATCH_MED_FG if match_pct >= 50 else MATCH_LOW_FG)
    match_canvas = tk.Canvas(right_frame, width=108, height=28, bg=SURFACE_CARD, highlightthickness=0)
    draw_rounded_rect(match_canvas, 1, 1, 107, 27, radius=12, fill=match_bg, outline=match_border, width=1)
    match_canvas.create_text(54, 14, text=f"{icon_str} {match_pct}% Match", font=FONT_MATCH_BADGE, fill=match_fg)
    match_canvas.pack(side="left", padx=(0, 10))

    # Heart Bookmark Button
    bm_icon = "💖" if is_saved else "🤍"
    bm_bg = "#FCE7F3" if is_saved else "#F5F1FB"
    bm_fg = "#BE185D" if is_saved else "#6D28D9"

    btn_bm = tk.Button(
        right_frame,
        text=bm_icon,
        command=lambda: on_toggle_bookmark(place_id),
        font=("Segoe UI Emoji", 10),
        bg=bm_bg,
        fg=bm_fg,
        activebackground="#FCE7F3",
        relief="flat",
        bd=0,
        width=3,
        cursor="hand2",
    )
    btn_bm.pack(side="left", padx=(0, 6))

    # Arrow Details Button
    btn_details = tk.Button(
        right_frame,
        text="❯",
        command=lambda: on_open_details(place),
        font=("Segoe UI", 10, "bold"),
        bg="#F5F1FB",
        fg=PRIMARY_COLOR,
        activebackground=PRIMARY_LIGHT,
        relief="flat",
        bd=0,
        width=3,
        cursor="hand2",
    )
    btn_details.pack(side="left")


def show_audit_details_dialog(parent_window, place, active_features):
    """
    Opens a modern, accessible modal dialog displaying the full 8-facility audit.
    """
    dialog = tk.Toplevel(parent_window)
    dialog.title(f"Facility Audit - {place['name']}")
    dialog.geometry("640x580")
    dialog.configure(bg=BACKGROUND_PAGE)
    dialog.transient(parent_window)
    dialog.grab_set()
