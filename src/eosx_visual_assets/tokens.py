# ==============================================================
# File: tokens.py
# Version: v0.1.0 | Date: 2026-07-14
# Purpose: Single source of truth for Energy OSX visual-asset
#          tokens. Loads tokens/brand_tokens.json and exposes it
#          as typed constants. Nothing in this package defines a
#          colour or font anywhere else.
# ==============================================================

from __future__ import annotations

import json
from pathlib import Path

# tokens/brand_tokens.json lives at the repo root, two levels up
# from src/eosx_visual_assets/.
_REPO_ROOT = Path(__file__).resolve().parents[2]
TOKENS_PATH = _REPO_ROOT / "tokens" / "brand_tokens.json"

with TOKENS_PATH.open(encoding="utf-8") as _f:
    TOKENS: dict = json.load(_f)

# ── Core brand palette ────────────────────────────────────
DEEP_NAVY = TOKENS["colours"]["deep_navy"]
NAVY = TOKENS["colours"]["navy"]
TEAL = TOKENS["colours"]["teal"]
AQUA = TOKENS["colours"]["aqua"]
MIST = TOKENS["colours"]["mist"]
ICE = TOKENS["colours"]["ice"]
WHITE = TOKENS["colours"]["white"]
SLATE = TOKENS["colours"]["slate"]
BORDER = TOKENS["colours"]["border"]

# ── On-dark surface tokens (banners, favicons, sidebar) ───
# The accent is held constant teal on dark; apps differ by
# icon + punch line, never by colour. This mirrors the shipped
# production banner and the market mockup.
GRADIENT = TOKENS["on_dark"]["gradient"]
GRADIENT_STOPS = TOKENS["on_dark"]["gradient_stops"]
ACCENT_TEAL = TOKENS["on_dark"]["accent_teal"]   # #35C5C5
MUTED_TEAL = TOKENS["on_dark"]["muted_teal"]     # #7FBFC8
SUBLABEL = TOKENS["on_dark"]["sublabel"]         # #8FA6BC
DIVIDER = TOKENS["on_dark"]["divider"]

# ── Product lockup (the small dark card, not the banner) ──
LOCKUP_CARD_FILL = TOKENS["lockup"]["card_fill"]      # #0C2340
LOCKUP_CARD_STROKE = TOKENS["lockup"]["card_stroke"]  # #16324f
LOCKUP_WAVE_ACCENT = TOKENS["lockup"]["wave_accent"]  # #00A7A7
LOCKUP_WAVE_AQUA = TOKENS["lockup"]["wave_aqua"]      # #4EC7D9
LOCKUP_WAVE_SLATE = TOKENS["lockup"]["wave_slate"]    # #64748B
LOCKUP_LABEL = TOKENS["lockup"]["label"]              # #8FA3B8

# ── Typography ────────────────────────────────────────────
FONT_HEADING = TOKENS["fonts"]["heading"]  # Manrope
FONT_BODY = TOKENS["fonts"]["body"]        # Inter
FONT_MONO = TOKENS["fonts"]["mono"]        # IBM Plex Mono

# Fallback stacks kept identical to eosx-charts for consistency.
FONT_STACK_HEADING = f'"{FONT_HEADING}", "DejaVu Sans", sans-serif'
FONT_STACK_BODY = f'"{FONT_BODY}", "DejaVu Sans", sans-serif'

# ── Brand strings ─────────────────────────────────────────
BRAND = TOKENS["brand"]
WORDMARK = TOKENS["wordmark"]
TAGLINE = TOKENS["tagline"]
DOMAINS = TOKENS["domains"]  # ["Operational", "Commercial", "Financial"]

__all__ = [
    "TOKENS", "TOKENS_PATH",
    "DEEP_NAVY", "NAVY", "TEAL", "AQUA", "MIST", "ICE", "WHITE", "SLATE", "BORDER",
    "GRADIENT", "GRADIENT_STOPS", "ACCENT_TEAL", "MUTED_TEAL", "SUBLABEL", "DIVIDER",
    "LOCKUP_CARD_FILL", "LOCKUP_CARD_STROKE", "LOCKUP_WAVE_ACCENT",
    "LOCKUP_WAVE_AQUA", "LOCKUP_WAVE_SLATE", "LOCKUP_LABEL",
    "FONT_HEADING", "FONT_BODY", "FONT_MONO",
    "FONT_STACK_HEADING", "FONT_STACK_BODY",
    "BRAND", "WORDMARK", "TAGLINE", "DOMAINS",
]
