# ==============================================================
# File: favicon.py
# Version: v0.1.0 | Date: 2026-07-14
# Purpose: The Energy OSX app-favicon template. The app glyph,
#          centred on a deep-navy rounded square, in constant teal.
#          One master SVG per app; PNG sizes are rasterised in
#          build.py. Keeps favicons on-brand and consistent instead
#          of hand-drawn per app.
# ==============================================================

from __future__ import annotations

from eosx_visual_assets import tokens as T
from eosx_visual_assets.apps import App
from eosx_visual_assets.icons import ICON_BOX, glyph

SIZE = 512
RX = 112               # iOS-style ~22% corner radius
GLYPH_TARGET = 268     # glyph box edge within the square
FAVICON_PNG_SIZES = [16, 32, 48, 64, 180, 192, 512]


def build_favicon_svg(app: App) -> str:
    scale = GLYPH_TARGET / ICON_BOX
    offset = (SIZE - GLYPH_TARGET) / 2
    glyph_markup = glyph(app.icon, stroke=T.ACCENT_TEAL, fill=T.ACCENT_TEAL, sw=2.4)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" \
width="{SIZE}" height="{SIZE}" role="img" aria-label="Energy OSX {app.name} icon">
  <title>Energy OSX — {app.name} icon</title>
  <defs>
    <linearGradient id="fg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{T.DEEP_NAVY}"/>
      <stop offset="100%" stop-color="#06304A"/>
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="{SIZE}" height="{SIZE}" rx="{RX}" fill="url(#fg)"/>
  <g transform="translate({offset:.1f} {offset:.1f}) scale({scale:.4f})">{glyph_markup}</g>
</svg>
'''


__all__ = ["build_favicon_svg", "SIZE", "FAVICON_PNG_SIZES"]
