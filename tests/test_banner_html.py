# ==============================================================
# File: test_banner_html.py
# Version: v1.0.0 | Date: 2026-10-05
# Purpose: The guarantee. A spec cannot make eleven apps render the
#          same header - only a shared artefact plus a test that
#          fails when one drifts.
#
#          These assert the two things KB_GROUP.md section 7.4
#          actually requires: the left platform zone is byte-
#          identical on every app, and every value in the right
#          zone comes from the registry rather than from the app.
# ==============================================================

from __future__ import annotations

import re

import pytest

from eosx_visual_assets import tokens as T
from eosx_visual_assets.apps import APPS
from eosx_visual_assets.banner_html import app_banner_css, app_banner_html
from eosx_visual_assets.geometry import GEOMETRY

ALL_SLUGS = sorted(APPS)


def _platform_zone(markup: str) -> str:
    m = re.search(r'__platform">(.*?)</div>', markup, re.S)
    assert m, "no platform zone in the markup"
    return m.group(1)


def test_every_app_renders() -> None:
    assert len(ALL_SLUGS) >= 11, "the registry shrank: %s" % ALL_SLUGS
    for slug in ALL_SLUGS:
        assert app_banner_html(slug).strip().startswith("<div")


def test_left_platform_zone_is_byte_identical_across_every_app() -> None:
    """The whole point. One zone, eleven apps, no exceptions."""
    zones = {slug: _platform_zone(app_banner_html(slug)) for slug in ALL_SLUGS}
    distinct = set(zones.values())
    assert len(distinct) == 1, (
        "the platform zone differs between apps: %s"
        % {s: z[:60] for s, z in zones.items()}
    )


@pytest.mark.parametrize("slug", ALL_SLUGS)
def test_right_zone_is_exactly_what_the_registry_says(slug: str) -> None:
    app = APPS[slug]
    markup = app_banner_html(slug)
    name = re.search(r"<span>(.*?)</span>", markup, re.S).group(1)
    punch = re.search(r'__punchline">(.*?)</p>', markup, re.S).group(1)
    assert name == app.name, "app name is not the registry's"
    assert punch == app.punchline, "punchline is not the registry's"


@pytest.mark.parametrize("slug", ALL_SLUGS)
def test_strapline_and_domains_come_from_the_registry(slug: str) -> None:
    markup = app_banner_html(slug)
    assert T.WORDMARK in markup
    for domain in T.DOMAINS:
        assert domain in markup
    # the strapline is rendered over two lines, so check both halves
    head, _, tail = T.TAGLINE.partition(" for ")
    assert head in markup and tail in markup


@pytest.mark.parametrize("slug", ALL_SLUGS)
def test_no_section_or_page_name_in_the_banner(slug: str) -> None:
    """Section 7.4: the sidebar already says where the user is."""
    markup = app_banner_html(slug).lower()
    for banned in ("dashboard</h", "section", "page ", "overview</", "home</"):
        assert banned not in markup, "the banner names a section or page: %r" % banned


def test_every_colour_in_the_css_is_a_token() -> None:
    """No typed colour survives in the stylesheet."""
    css = app_banner_css()
    sanctioned = {c.lower() for c in (
        list(T.GRADIENT) + [T.ACCENT_TEAL, T.MUTED_TEAL, T.SUBLABEL, T.WHITE,
                            T.DEEP_NAVY, T.NAVY, T.TEAL, T.AQUA, T.MIST, T.ICE,
                            T.SLATE, T.BORDER])}
    found = {h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}", css)}
    assert found <= sanctioned, "unsanctioned colour in the banner CSS: %s" % (found - sanctioned)


def test_every_font_size_is_a_size_the_geometry_holds() -> None:
    """The drawing's sizes are the design at any width.

    This replaces a check that every size scaled by one multiplier. The
    multiplier was derived from a 1440px reference, which the drawing has not
    got, and it made the banner shrink in a narrow column instead of matching
    the standard.
    """
    sizes = {float(s["size"]) for group in ("platform", "app")
             for s in GEOMETRY[group].values() if isinstance(s, dict) and "size" in s}
    found = {float(m) for m in re.findall(r"font-size:\s*(\d+(?:\.\d+)?)px", app_banner_css())}
    assert found, "no font sizes in the stylesheet"
    assert found <= sizes, "font sizes not in the geometry: %s" % sorted(found - sizes)


def test_unknown_app_is_refused_rather_than_rendered() -> None:
    with pytest.raises(KeyError) as e:
        app_banner_html("not-an-app")
    assert "registry" in str(e.value)


def test_css_is_identical_regardless_of_which_app_asked_for_it() -> None:
    assert app_banner_css() == app_banner_css()
    scoped = app_banner_css(scope=".x-banner")
    assert scoped.count(".x-banner") == app_banner_css().count(".eosx-banner")


def test_every_child_rule_is_scoped_exactly_twice() -> None:
    """Specificity, locked down - both ways of getting it wrong have happened.

    One scope (`.eosx-banner__headline`) loses to a host's own text rule -
    Streamlit colours `[data-testid="stMarkdownContainer"] p`, which outranks
    a single class, and the whole platform zone went invisible on a dark bar
    in a live app. Three scopes needs three nested ancestors and matches
    nothing, which killed the accent word in the same hour.
    """
    css = app_banner_css()
    selectors = [s.strip() for s in re.findall(r"^\s*(\.[^{]*)\{", css, re.M)]
    assert selectors, "no selectors in the stylesheet"
    for sel in selectors:
        n = sel.count(".eosx-banner")
        if "__" in sel:
            assert n == 2, "child rule must carry the scope twice, found %d: %s" % (n, sel)
        else:
            assert n == 1, "root rule must carry the scope once, found %d: %s" % (n, sel)


def _geometry_numbers() -> set[float]:
    """Every number the geometry file holds, at any depth."""
    out: set[float] = set()

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if not k.startswith("_"):
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
        elif isinstance(node, (int, float)) and not isinstance(node, bool):
            out.add(float(node))
    walk(GEOMETRY)
    return out


def test_no_number_in_the_css_was_typed_by_the_renderer() -> None:
    """The whole point of the geometry file.

    Before it, the SVG renderer said headline 52 and the HTML renderer said 21,
    with no shared constant and nothing comparing them. Any number here that is
    not in the geometry file is a renderer inventing one again.
    """
    allowed = _geometry_numbers() | {0.0, 1.0, 100.0, 90.0, 50.0, 55.0, 2.0}
    css = app_banner_css()
    numbers = {float(n) for n in re.findall(r"(?<![\w-])(\d+(?:\.\d+)?)(?=px|em|%|)", css)}
    stray = sorted(n for n in numbers if n not in allowed)
    assert not stray, (
        "numbers in the stylesheet that the geometry file does not hold: %s" % stray
    )


def test_the_renderer_reads_the_geometry_rather_than_copying_it() -> None:
    """Change the data, and the stylesheet must change with it."""
    import copy

    from eosx_visual_assets import banner_html, geometry

    original = copy.deepcopy(geometry.GEOMETRY)
    try:
        geometry.GEOMETRY["banner"]["radius"] = 999
        assert "999" in banner_html.app_banner_css(), (
            "the stylesheet ignored a changed geometry value - it is holding its own copy"
        )
    finally:
        geometry.GEOMETRY.clear()
        geometry.GEOMETRY.update(original)
    assert "999" not in app_banner_css()
