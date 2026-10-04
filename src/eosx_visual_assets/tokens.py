# ==============================================================
# File: tokens.py
# Version: v0.2.1 | Date: 2026-10-04
# Purpose: Single source of truth for Energy OSX visual-asset
#          tokens. Loads the registry and exposes it as typed
#          constants. Nothing in this package defines a colour
#          or font anywhere else.
#
#          The registry lives INSIDE the package, at
#          eosx_visual_assets/tokens/brand_tokens.json, and is
#          read with importlib.resources. It used to sit at the
#          repo root and be found by walking up from __file__,
#          which worked in a checkout and failed on every
#          installed copy - 0.2.0 shipped unimportable because
#          of it. One location, one lookup, no fallback.
# ==============================================================

from __future__ import annotations

import json
from importlib.resources import as_file, files
from pathlib import Path

_TOKENS_RESOURCE = files("eosx_visual_assets").joinpath("tokens/brand_tokens.json")
TOKENS: dict = json.loads(_TOKENS_RESOURCE.read_text(encoding="utf-8"))

# TOKENS_PATH is exported and callers may expect a real path. From a normal
# install or a checkout the resource IS a file on disk, so give them that.
# Only a zipimported package has no path, and then it is None rather than a
# path that does not exist.
try:
    with as_file(_TOKENS_RESOURCE) as _p:
        TOKENS_PATH: Path | None = Path(_p)
except (FileNotFoundError, TypeError):  # pragma: no cover - zipimport only
    TOKENS_PATH = None

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
