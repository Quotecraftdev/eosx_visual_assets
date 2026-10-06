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


def test_the_type_scale_is_one_multiplier() -> None:
    """Proportion is the requirement, so every size must share one variable.

    If a size is ever hardcoded in px, two apps at different widths stop
    looking like one system - which is the fault this module exists to end.
    """
    css = app_banner_css()
    sizes = re.findall(r"font-size:\s*([^;]+);", css)
    assert sizes, "no font sizes in the stylesheet"
    for s in sizes:
        assert "var(--eosx-b)" in s, "font-size does not scale with the banner: %r" % s


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
