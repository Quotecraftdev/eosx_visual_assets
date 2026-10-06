# ==============================================================
# File: geometry.py
# Version: v0.1.0 | Date: 2026-10-06
# Purpose: The app banner's geometry, as data.
#
#          Until now the SVG renderer and the HTML renderer each
#          held their own numbers - headline 52 against 21, app
#          name 40 against 17, no shared constant between them and
#          no test comparing the two. They were two readings of the
#          same prose, which is why they drifted.
#
#          Every number now comes from
#          tokens/banner_geometry.json, read off the decided
#          drawing (energy_osx_banner_final_pricing_intelligence
#          .html, 12-07-2026; KB_GROUP.md 7.4). A renderer that
#          types a number is a renderer that has forked.
#
#          Colours here are NAMES, resolved against the registry
#          by colour(). Nothing in this file is a hex.
# ==============================================================

from __future__ import annotations

import json
from importlib.resources import files
from typing import Any

from eosx_visual_assets import tokens as T

__all__ = ["GEOMETRY", "colour", "scale_expr", "part"]

_RESOURCE = files("eosx_visual_assets").joinpath("tokens/banner_geometry.json")
GEOMETRY: dict[str, Any] = json.loads(_RESOURCE.read_text(encoding="utf-8"))

#: Colour names the geometry may use, resolved from the registry.
_COLOURS = {
    "white": T.WHITE,
    "accent_teal": T.ACCENT_TEAL,
    "muted_teal": T.MUTED_TEAL,
    "sublabel": T.SUBLABEL,
    "divider": T.DIVIDER,
    "deep_navy": T.DEEP_NAVY,
}


def colour(name: str) -> str:
    """Resolve a geometry colour name against the registry.

    The geometry names a colour; the registry owns its value. A name the
    registry has no value for is an error, not a default - that is how an
    invented colour would get in.
    """
    try:
        return _COLOURS[name]
    except KeyError:
        raise KeyError(
            "%r is not a registry colour. The banner may only use: %s"
            % (name, ", ".join(sorted(_COLOURS)))
        ) from None


def part(*path: str) -> dict[str, Any]:
    """A block of the geometry, e.g. part("platform", "headline")."""
    node: Any = GEOMETRY
    for key in path:
        node = node[key]
    return node


def scale_expr(value: float) -> str:
    """A CSS length, in the drawing's own units.

    The sizes are fixed on purpose. The drawing is the design at any width:
    the box reflows, the type does not. An earlier build multiplied every
    size by a scale derived from a 1440px reference - a number the drawing
    has not got - so the banner shrank in a narrow column rather than
    matching the standard.
    """
    if value == 0:
        return "0"
    return "%gpx" % value
