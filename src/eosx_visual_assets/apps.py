# ==============================================================
# File: apps.py
# Version: v0.1.0 | Date: 2026-07-14
# Purpose: The app registry. Every Energy OSX app is one entry
#          here (name, icon glyph id, punch line). Adding a new
#          app = adding one entry, then running the build. No
#          hand-built banner or favicon should ever exist outside
#          this pipeline.
# ==============================================================

from __future__ import annotations

from dataclasses import dataclass

from eosx_visual_assets.tokens import TOKENS


@dataclass(frozen=True)
class App:
    slug: str          # "market"
    name: str          # "Market Intelligence"
    icon: str          # glyph id in icons.py
    punchline: str     # "POSITION. GAP. WIN."
    tagline_draft: bool  # True until Chris signs the punch line off


def _load_apps() -> dict[str, App]:
    apps: dict[str, App] = {}
    for slug, cfg in TOKENS["apps"].items():
        apps[slug] = App(
            slug=slug,
            name=cfg["name"],
            icon=cfg["icon"],
            punchline=cfg["punchline"],
            tagline_draft=cfg.get("tagline_draft", False),
        )
    return apps


APPS: dict[str, App] = _load_apps()

# Canonical display order (matches how the products are listed).
ORDER = ["signal", "pricing", "integrity", "market",
         "settlement", "bespoke", "pipeline", "dashboard"]


def ordered_apps() -> list[App]:
    """Apps in canonical display order, tolerant of registry additions."""
    seen = list(ORDER)
    for slug in APPS:
        if slug not in seen:
            seen.append(slug)
    return [APPS[s] for s in seen if s in APPS]


__all__ = ["App", "APPS", "ORDER", "ordered_apps"]
