# ==============================================================
# File: lockup.py
# Version: v0.1.0 | Date: 2026-09-06
# Purpose: The Energy OSX product-lockup template — the small dark
#          card that signs a product's name above its video, on a
#          slide, or anywhere the product speaks for itself.
#
#          This is NOT the banner. The banner (banner.py) carries
#          the platform lockup, the strapline and the three
#          domains — it introduces Energy OSX. The lockup carries
#          the wave mark, the wordmark and one product name, and
#          nothing else. On a product page the platform is already
#          named in the nav, so the video slot takes the lockup.
#
#          Geometry lifted from the two lockups already shipped
#          (Pricing, Professional) so generated lockups sit beside
#          them without a visible seam. Closes W34.
# ==============================================================

from __future__ import annotations

from eosx_visual_assets import tokens as T
from eosx_visual_assets.apps import App
from eosx_visual_assets.text import text_width

# ── Canvas ────────────────────────────────────────────────
W, H, RX = 689, 219, 16
CARD_INSET = 1.0
CARD_STROKE_W = 1.5

# ── Wave mark ─────────────────────────────────────────────
ARC = "M166.7 149.3 A72 72 0 1 1 166.7 60.7"
ARC_SW = 8.5
WAVE_SW = 7.5
WAVES = (
    "M58 77 C80 62,102 62,122 77 C143 92,165 92,186 77 C202 65,218 65,232 73",
    "M58 105 C80 90,102 90,122 105 C143 120,165 120,186 105 C202 93,218 93,232 101",
    "M58 133 C80 118,102 118,122 133 C143 148,165 148,186 133 C202 121,218 121,232 129",
)

# ── Type ──────────────────────────────────────────────────
TEXT_X = 252
WORD_SIZE, WORD_LS, WORD_BASELINE = 58, -0.5, 112
LABEL_X, LABEL_SIZE, LABEL_LS, LABEL_BASELINE = 255, 14.5, 3.2, 144
LABEL_RIGHT_EDGE = W - 40          # the label must not run to the card edge
LABEL_LS_MIN = 1.2                 # tighten tracking before shrinking type
LABEL_SIZE_MIN = 11.5


def _fit_label(label: str) -> tuple[float, float]:
    """Return (size, letter_spacing) that keeps `label` inside the card.

    Tracking gives first — the wide-set label is the look, but a name
    that runs off the card is not. Only when tracking is spent does the
    type size come down.
    """
    size, ls = LABEL_SIZE, LABEL_LS
    room = LABEL_RIGHT_EDGE - LABEL_X
    while True:
        if text_width(label, T.FONT_BODY, size, ls) <= room:
            return size, ls
        if ls > LABEL_LS_MIN:
            ls = round(ls - 0.1, 2)
            continue
        if size > LABEL_SIZE_MIN:
            size = round(size - 0.5, 2)
            continue
        return size, ls


def build_lockup_svg(app: App) -> str:
    """Return a standalone SVG string for `app`'s product lockup."""
    label = app.name.upper()
    label_size, label_ls = _fit_label(label)

    accent = T.LOCKUP_WAVE_ACCENT
    wave_colours = (accent, T.LOCKUP_WAVE_AQUA, T.LOCKUP_WAVE_SLATE)
    waves = "\n    ".join(
        f'<path d="{d}" stroke="{c}" stroke-width="{WAVE_SW}"/>'
        for d, c in zip(WAVES, wave_colours)
    )

    hd = T.FONT_STACK_HEADING
    bd = T.FONT_STACK_BODY
    card_w = W - CARD_INSET * 2
    card_h = H - CARD_INSET * 2

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" \
width="100%" role="img" aria-label="Energy OSX — {app.name} logo">
  <title>Energy OSX — {app.name} logo</title>
  <desc>Dark navy lockup: a white open arc with three flowing waves in teal, \
aqua and slate, the Energy OS wordmark with a teal X, and the label \
{app.name}.</desc>

  <rect x="{CARD_INSET}" y="{CARD_INSET}" width="{card_w:g}" height="{card_h:g}" \
rx="{RX}" fill="{T.LOCKUP_CARD_FILL}" stroke="{T.LOCKUP_CARD_STROKE}" \
stroke-width="{CARD_STROKE_W}"/>

  <g fill="none" stroke-linecap="round">
    <path d="{ARC}" stroke="{T.WHITE}" stroke-width="{ARC_SW}"/>
    {waves}
  </g>

  <text x="{TEXT_X}" y="{WORD_BASELINE}" font-family='{hd}' font-size="{WORD_SIZE}" \
font-weight="800" letter-spacing="{WORD_LS}"><tspan fill="{T.WHITE}">Energy OS</tspan>\
<tspan fill="{accent}">X</tspan></text>

  <text x="{LABEL_X}" y="{LABEL_BASELINE}" font-family='{bd}' font-size="{label_size:g}" \
font-weight="600" letter-spacing="{label_ls:g}" fill="{T.LOCKUP_LABEL}">{label}</text>
</svg>
'''


__all__ = ["build_lockup_svg", "W", "H"]
