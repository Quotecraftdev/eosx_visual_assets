# ==============================================================
# File: text.py
# Version: v0.1.0 | Date: 2026-07-14
# Purpose: Pixel-accurate text measurement using the bundled brand
#          TTFs, so the SVG generator can right-align names and
#          place icons precisely rather than guessing widths.
# ==============================================================

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

_FONT_DIR = Path(__file__).resolve().parent / "assets" / "fonts"
_FONT_FILES = {
    "Manrope": "Manrope.ttf",
    "Inter": "Inter.ttf",
    "IBM Plex Mono": "IBMPlexMono-Medium.ttf",
}


@lru_cache(maxsize=64)
def _font(family: str, size: int) -> ImageFont.FreeTypeFont:
    fname = _FONT_FILES.get(family, "Inter.ttf")
    return ImageFont.truetype(str(_FONT_DIR / fname), size)


def text_width(text: str, family: str, size: float, letter_spacing: float = 0.0) -> float:
    """Advance width of `text` in SVG user units.

    letter_spacing is added between glyphs (SVG `letter-spacing`
    semantics: it does not add trailing space after the last glyph).
    """
    font = _font(family, int(round(size)))
    width = font.getlength(text)
    if letter_spacing and len(text) > 1:
        width += letter_spacing * (len(text) - 1)
    return float(width)


__all__ = ["text_width"]
