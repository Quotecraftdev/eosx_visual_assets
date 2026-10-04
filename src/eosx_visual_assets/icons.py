# ==============================================================
# File: icons.py
# Version: v0.1.0 | Date: 2026-07-14
# Purpose: The Energy OSX app-glyph library. One line-drawn glyph
#          per app, all authored in a 44x44 box (centre 22,22) so
#          they drop into banners and favicons at any scale. Glyphs
#          are stroke-based teal line art to match the house mark.
# ==============================================================

from __future__ import annotations

ICON_BOX = 44  # every glyph is authored in a 44x44 coordinate box


def _wrap(paths: str, stroke: str, fill: str, sw: float) -> str:
    """Wrap raw glyph geometry in a styled group.

    `paths` uses the sentinel {S} for stroked-only elements and {F}
    for filled elements so a single template drives both.
    """
    body = paths.format(
        S=f'fill="none" stroke="{stroke}" stroke-width="{sw}" '
          f'stroke-linecap="round" stroke-linejoin="round"',
        F=f'fill="{fill}" stroke="none"',
    )
    return f'<g>{body}</g>'


# ── Glyph geometry (44x44 box) ────────────────────────────
# Each is a format string exposing {S} (stroke style) / {F} (fill).

_GLYPHS: dict[str, str] = {
    # Signal — broadcast / radar: origin dot with two rising arcs.
    "signal": (
        '<circle cx="13" cy="31" r="2.8" {F}/>'
        '<path d="M13 24 A9 9 0 0 1 20 31" {S}/>'
        '<path d="M13 16 A17 17 0 0 1 28 31" {S}/>'
        '<path d="M13 8 A25 25 0 0 1 36 31" {S}/>'
    ),
    # Pricing — price tag with hole, tip to the lower-left.
    "pricing": (
        '<path d="M21 8 H34 a2 2 0 0 1 2 2 V23 a2 2 0 0 1 -0.6 1.4 '
        'L23 36 a2 2 0 0 1 -2.8 0 L8.6 24.4 a2 2 0 0 1 0 -2.8 '
        'L19.6 8.6 A2 2 0 0 1 21 8 Z" {S}/>'
        '<circle cx="28" cy="16" r="2.4" {S}/>'
    ),
    # Integrity — shield with a check: audited & trusted.
    "integrity": (
        '<path d="M22 7 L35 12 V22 C35 30 29 35 22 38 '
        'C15 35 9 30 9 22 V12 Z" {S}/>'
        '<path d="M16.5 22 L20.5 26 L28 17" {S}/>'
    ),
    # Market — bullseye / target: position and gap.
    "market": (
        '<circle cx="22" cy="22" r="15" {S}/>'
        '<circle cx="22" cy="22" r="8.5" {S}/>'
        '<circle cx="22" cy="22" r="3" {F}/>'
    ),
    # Settlement — balance scales: bought vs billed.
    "settlement": (
        '<circle cx="22" cy="9" r="2" {F}/>'
        '<line x1="10" y1="14" x2="34" y2="14" {S}/>'
        '<line x1="22" y1="11" x2="22" y2="31" {S}/>'
        '<line x1="15" y1="33" x2="29" y2="33" {S}/>'
        '<path d="M4 18 a6 4 0 0 0 12 0" {S}/>'
        '<path d="M28 18 a6 4 0 0 0 12 0" {S}/>'
        '<line x1="10" y1="14" x2="10" y2="17" {S}/>'
        '<line x1="34" y1="14" x2="34" y2="17" {S}/>'
    ),
    # Bespoke — sliders / configurable build.
    "bespoke": (
        '<line x1="9" y1="13" x2="35" y2="13" {S}/>'
        '<line x1="9" y1="22" x2="35" y2="22" {S}/>'
        '<line x1="9" y1="31" x2="35" y2="31" {S}/>'
        '<circle cx="28" cy="13" r="3.4" {F}/>'
        '<circle cx="16" cy="22" r="3.4" {F}/>'
        '<circle cx="30" cy="31" r="3.4" {F}/>'
    ),
    # Pipeline — funnel: track, flow, convert.
    "pipeline": (
        '<path d="M8 11 H36 L25 24 V33 H19 V24 Z" {S}/>'
    ),
    # Dashboard — 2x2 tile grid, top-left tile filled as accent.
    "dashboard": (
        '<rect x="9" y="9" width="11" height="11" rx="2.4" {F}/>'
        '<rect x="24" y="9" width="11" height="11" rx="2.4" {S}/>'
        '<rect x="9" y="24" width="11" height="11" rx="2.4" {S}/>'
        '<rect x="24" y="24" width="11" height="11" rx="2.4" {S}/>'
    ),
    # Professional — a written record: page with a turned corner and rules.
    #   Codify, standardise, automate — the service writes the process down.
    "professional": (
        '<path d="M13 7 H27 L33 13 V37 H13 Z" {S}/>'
        '<path d="M27 7 V13 H33" {S}/>'
        '<path d="M18 21 H28" {S}/>'
        '<path d="M18 27 H28" {S}/>'
        '<path d="M18 33 H24" {S}/>'
    ),
    # Custom — modular blocks: three in place, one being set down.
    #   The parts already work; yours is another arrangement of them.
    "custom": (
        '<rect x="8" y="23" width="13" height="13" rx="2.5" {S}/>'
        '<rect x="23" y="23" width="13" height="13" rx="2.5" {S}/>'
        '<rect x="8" y="8" width="13" height="13" rx="2.5" {S}/>'
        '<rect x="23" y="8" width="13" height="13" rx="2.5" {F}/>'
    ),
    # Learning — two stacked pages with a marker: one source, four
    #   resources built from it.
    "learning": (
        '<rect x="14" y="6" width="22" height="28" rx="2.6" {S}/>'
        '<rect x="8" y="12" width="22" height="28" rx="2.6" {S}/>'
        '<circle cx="19" cy="26" r="3" {F}/>'
    ),
}


def available() -> list[str]:
    return sorted(_GLYPHS)


def glyph(icon_id: str, stroke: str, fill: str, sw: float = 2.6) -> str:
    """Return SVG markup for `icon_id`, drawn in the 44x44 box.

    Wrap the result in a transform group to place/scale it.
    """
    if icon_id not in _GLYPHS:
        raise KeyError(f"unknown glyph {icon_id!r}; have {available()}")
    return _wrap(_GLYPHS[icon_id], stroke, fill, sw)


__all__ = ["ICON_BOX", "available", "glyph"]
