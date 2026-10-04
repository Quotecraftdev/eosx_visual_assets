"""Banner + favicon template checks (SVG-level, no rasteriser needed)."""

from __future__ import annotations

import xml.dom.minidom as minidom

import pytest

from eosx_visual_assets.apps import ordered_apps
from eosx_visual_assets.banner import build_banner_svg
from eosx_visual_assets.favicon import build_favicon_svg


@pytest.fixture(params=ordered_apps(), ids=lambda a: a.slug)
def app(request):
    return request.param


def _parse(svg: str):
    # Raises if the SVG is not well-formed XML.
    return minidom.parseString(svg)


def test_banner_is_well_formed_xml(app):
    _parse(build_banner_svg(app))


def test_favicon_is_well_formed_xml(app):
    _parse(build_favicon_svg(app))


def test_banner_contains_identity(app):
    svg = build_banner_svg(app)
    assert app.name in svg
    assert app.punchline in svg
    assert "The operating layer" in svg
    assert "energy intelligence" in svg


def test_banner_uses_constant_accent(app):
    # The teal accent must appear; no per-app colour drift.
    from eosx_visual_assets import tokens as T
    assert T.ACCENT_TEAL in build_banner_svg(app)


def test_favicon_names_the_app(app):
    assert app.name in build_favicon_svg(app)
