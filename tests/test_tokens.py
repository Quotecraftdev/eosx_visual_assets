"""Token + registry integrity checks."""

from __future__ import annotations

import re

from eosx_visual_assets import tokens as T
from eosx_visual_assets.apps import APPS, ordered_apps
from eosx_visual_assets.icons import available

HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def test_core_palette_is_hex():
    for name in ("DEEP_NAVY", "NAVY", "TEAL", "AQUA", "WHITE", "SLATE"):
        assert HEX.match(getattr(T, name)), name


def test_on_dark_accents_present():
    assert HEX.match(T.ACCENT_TEAL)
    assert HEX.match(T.MUTED_TEAL)
    assert len(T.GRADIENT) == len(T.GRADIENT_STOPS) == 3


def test_registry_non_empty_and_ordered():
    apps = ordered_apps()
    assert len(apps) == len(APPS) >= 8
    slugs = [a.slug for a in apps]
    assert len(slugs) == len(set(slugs)), "duplicate slugs"


def test_every_app_uses_a_known_glyph():
    known = set(available())
    for app in APPS.values():
        assert app.icon in known, f"{app.slug} references unknown glyph {app.icon!r}"


def test_punchlines_present():
    for app in APPS.values():
        assert app.punchline.strip(), f"{app.slug} has an empty punch line"
