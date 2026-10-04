# ==============================================================
# File: banner.py
# Version: v0.1.0 | Date: 2026-07-14
# Purpose: The Energy OSX app-banner template. One function turns a
#          registry App into a standalone, house-style SVG banner:
#          platform lockup + three-domain strapline on the left,
#          app identity (glyph + name + punch line) on the right.
#          Matches the shipped production banner and market mockup.
# ==============================================================

from __future__ import annotations

from eosx_visual_assets import tokens as T
from eosx_visual_assets.apps import App
from eosx_visual_assets.icons import ICON_BOX, glyph
from eosx_visual_assets.text import text_width

# ── Canvas ────────────────────────────────────────────────
W, H, RX = 1440, 300, 20
PAD_L = 64
R_EDGE = W - 64          # right content edge
DIVIDER_X = 792

# ── Left column type ──────────────────────────────────────
EYEBROW_SIZE, EYEBROW_LS, EYEBROW_Y = 20, 2.6, 74
HEAD_SIZE = 52
HEAD_Y1, HEAD_Y2 = 142, 200
SUB_SIZE, SUB_LS, SUB_Y = 21, 0.4, 250

# ── Right column type ─────────────────────────────────────
NAME_SIZE = 40
NAME_BASELINE = 146
ICON_SIZE = 46
ICON_CY = 132
ICON_GAP = 18
PUNCH_SIZE, PUNCH_LS, PUNCH_BASELINE = 19, 3.0, 184


def _fit_name_size(name: str) -> int:
    """Shrink the app name until its group clears the divider."""
    size = NAME_SIZE
    while size > 26:
        name_w = text_width(name, T.FONT_HEADING, size)
        group_left = R_EDGE - (ICON_SIZE + ICON_GAP + name_w)
        if group_left >= DIVIDER_X + 16:
            return size
        size -= 1
    return size


def build_banner_svg(app: App) -> str:
    """Return a standalone SVG string for `app`'s banner."""
    name_size = _fit_name_size(app.name)
    name_w = text_width(app.name, T.FONT_HEADING, name_size)
    group_left = R_EDGE - (ICON_SIZE + ICON_GAP + name_w)
    icon_x = group_left
    icon_top = ICON_CY - ICON_SIZE / 2
    name_x = group_left + ICON_SIZE + ICON_GAP
    scale = ICON_SIZE / ICON_BOX

    grad_stops = "".join(
        f'<stop offset="{o:.2%}" stop-color="{c}"/>'
        for c, o in zip(T.GRADIENT, T.GRADIENT_STOPS)
    )

    glyph_markup = glyph(app.icon, stroke=T.ACCENT_TEAL, fill=T.ACCENT_TEAL, sw=2.6)

    hd = T.FONT_STACK_HEADING
    bd = T.FONT_STACK_BODY

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" \
width="100%" role="img" aria-label="Energy OSX — {app.name} banner">
  <title>Energy OSX — {app.name}</title>
  <desc>Dark navy banner: the Energy OSX platform lockup with the strapline \
"The operating layer for energy intelligence" and the domains \
{" / ".join(T.DOMAINS)} on the left; the {app.name} identity with its glyph and \
the line "{app.punchline}" on the right.</desc>
  <defs>
    <linearGradient id="eosxG" x1="0" y1="0" x2="1" y2="0">{grad_stops}</linearGradient>
  </defs>

  <rect x="0" y="0" width="{W}" height="{H}" rx="{RX}" fill="url(#eosxG)"/>

  <!-- Left: platform lockup + strapline -->
  <text x="{PAD_L}" y="{EYEBROW_Y}" font-family='{bd}' font-size="{EYEBROW_SIZE}" \
font-weight="600" letter-spacing="{EYEBROW_LS}" fill="{T.MUTED_TEAL}">ENERGY OSX</text>

  <text x="{PAD_L}" y="{HEAD_Y1}" font-family='{hd}' font-size="{HEAD_SIZE}" \
font-weight="600" fill="{T.WHITE}">The operating layer</text>
  <text x="{PAD_L}" y="{HEAD_Y2}" font-family='{hd}' font-size="{HEAD_SIZE}" \
font-weight="600"><tspan fill="{T.WHITE}">for </tspan><tspan \
fill="{T.ACCENT_TEAL}">energy intelligence</tspan></text>

  <text x="{PAD_L}" y="{SUB_Y}" font-family='{bd}' font-size="{SUB_SIZE}" \
letter-spacing="{SUB_LS}" fill="{T.SUBLABEL}">{" · ".join(T.DOMAINS)}</text>

  <!-- Divider -->
  <line x1="{DIVIDER_X}" y1="64" x2="{DIVIDER_X}" y2="236" \
stroke="{T.DIVIDER}" stroke-width="1.5"/>

  <!-- Right: app identity -->
  <g transform="translate({icon_x:.1f} {icon_top:.1f}) scale({scale:.4f})">{glyph_markup}</g>
  <text x="{name_x:.1f}" y="{NAME_BASELINE}" font-family='{hd}' \
font-size="{name_size}" font-weight="600" fill="{T.WHITE}">{app.name}</text>
  <text x="{R_EDGE}" y="{PUNCH_BASELINE}" text-anchor="end" font-family='{bd}' \
font-size="{PUNCH_SIZE}" font-weight="600" letter-spacing="{PUNCH_LS}" \
fill="{T.MUTED_TEAL}">{app.punchline}</text>
</svg>
'''


__all__ = ["build_banner_svg", "W", "H"]
