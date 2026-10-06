# ==============================================================
# File: test_streamlit_host.py
# Version: v1.0.0 | Date: 2026-10-06
# Purpose: Render the banner in a REAL Streamlit app and inspect
#          the DOM the browser ends up with.
#
#          This exists because the banner shipped broken twice.
#          Both times it had been checked by rendering the markup
#          standalone in a file, which proves nothing about a host:
#          Streamlit runs the string through a Markdown pipeline
#          and an HTML sanitiser before the browser ever sees it,
#          and the test page skipped both.
#
#          What this proves: every line of the banner reaches the
#          DOM, inside Streamlit, with its text and its class
#          intact, and the stylesheet arrives with it.
#
#          What it does not prove: the painted colour. Reading
#          computed styles needs a scripting channel into the page
#          that Streamlit's sanitiser closes. The colours are
#          covered by test_banner_html.py instead.
#
#          Skips, loudly, when streamlit or Chrome are missing.
# ==============================================================

from __future__ import annotations

import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

from eosx_visual_assets import tokens as T
from eosx_visual_assets.apps import APPS
from eosx_visual_assets.banner_html import headline_lines

APP_SOURCE = '''
import streamlit as st
from eosx_visual_assets.banner_html import app_banner_css, app_banner_html

st.set_page_config(page_title="banner host test", layout="centered")
st.markdown(
    " ".join(
        line.strip()
        for line in ("<style>%s</style>%s"
                     % (app_banner_css(), app_banner_html("pricing"))).splitlines()
    ),
    unsafe_allow_html=True,
)
'''

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "google-chrome",
    "chromium",
]


def _chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if os.path.sep in c:
            if Path(c).exists():
                return c
        elif shutil.which(c):
            return shutil.which(c)
    return None


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_for(port: int, timeout: float = 90.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket() as s:
            s.settimeout(1.0)
            if s.connect_ex(("127.0.0.1", port)) == 0:
                return True
        time.sleep(0.5)
    return False


@pytest.fixture(scope="module")
def streamlit_render(tmp_path_factory: pytest.TempPathFactory) -> tuple[str, Path]:
    pytest.importorskip("streamlit", reason="a real Streamlit is the point of this test")
    chrome = _chrome()
    if not chrome:
        pytest.skip("Chrome is needed to render the app")

    work = tmp_path_factory.mktemp("sthost")
    app = work / "app.py"
    app.write_text(APP_SOURCE, encoding="utf-8")
    # Mirror a real deployed app: a light base sets the page's own text colour,
    # which is what the banner's colours have to survive. Testing without it
    # would be testing a friendlier host than production.
    cfg = work / ".streamlit"
    cfg.mkdir(exist_ok=True)
    (cfg / "config.toml").write_text(
        chr(10).join(['[theme]', 'base = "light"',
                      'primaryColor = "%s"' % T.TEAL, '']),
        encoding="utf-8")
    port = _free_port()

    proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", str(app),
         "--server.headless=true", "--server.port=%d" % port,
         "--browser.gatherUsageStats=false", "--server.fileWatcherType=none"],
        cwd=work, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    try:
        if not _wait_for(port):
            proc.kill()
            tail = proc.stdout.read()[-400:] if proc.stdout else ""
            pytest.skip("Streamlit did not start: %s" % tail)
        # Streamlit delivers the page over a websocket after the shell loads.
        # --virtual-time-budget fast-forwards timers but not real network time,
        # so a single dump catches an empty shell. Re-dump until the content
        # arrives; this is the same trap that made the screenshots useless.
        dom = ""
        for attempt in range(12):
            dom = subprocess.run(
                [chrome, "--headless", "--disable-gpu", "--dump-dom",
                 "--virtual-time-budget=15000",
                 "--user-data-dir=%s" % (work / ("chrome%d" % attempt)),
                 "http://127.0.0.1:%d/" % port],
                capture_output=True, text=True, encoding="utf-8", timeout=180,
            ).stdout or ""
            if "eosx-banner" in dom:
                break
            time.sleep(2)
        else:
            out = ""
            if proc.poll() is not None and proc.stdout:
                out = proc.stdout.read()[-600:]
            pytest.fail(
                "the banner never reached the DOM after 12 attempts. "
                "Streamlit output: %s" % (out or "(still running, no error)")
            )
        shot = work / "banner.png"
        subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
             "--screenshot=%s" % shot, "--window-size=1200,900",
             "--virtual-time-budget=15000",
             "--user-data-dir=%s" % (work / "chromeshot"),
             "http://127.0.0.1:%d/" % port],
            capture_output=True, text=True, timeout=180,
        )
    finally:
        proc.kill()
    return dom, shot


@pytest.mark.slow
def test_the_banner_markup_survives_streamlits_sanitiser(streamlit_render) -> None:
    streamlit_dom = streamlit_render[0]
    for cls in ("eosx-banner", "eosx-banner__inner", "eosx-banner__platform",
                "eosx-banner__eyebrow", "eosx-banner__headline",
                "eosx-banner__domains", "eosx-banner__app",
                "eosx-banner__appname", "eosx-banner__punchline"):
        assert cls in streamlit_dom, "Streamlit stripped %s from the banner" % cls


@pytest.mark.slow
def test_every_line_of_text_reaches_the_dom(streamlit_render) -> None:
    """The failure that shipped: only the accent phrase rendered."""
    streamlit_dom = streamlit_render[0]
    head, joiner, accent = headline_lines()
    expected = [T.WORDMARK, head, accent, APPS["pricing"].name, APPS["pricing"].punchline]
    expected += list(T.DOMAINS)
    missing = [t for t in expected if t not in streamlit_dom]
    assert not missing, "these never reached the DOM inside Streamlit: %s" % missing


@pytest.mark.slow
def test_the_stylesheet_arrives_with_it(streamlit_render) -> None:
    streamlit_dom = streamlit_render[0]
    assert "container-type: inline-size" in streamlit_dom, "the <style> block was stripped"
    assert "eosx-banner__headline" in streamlit_dom, "the banner rules never reached the page"


@pytest.mark.slow
def test_the_text_is_actually_painted_not_merely_present(streamlit_render) -> None:
    """The symptom that reached a user: present in the DOM, invisible on screen.

    Chris, 06-10-2026: "left is missing the logo & theres just two orphaned
    words." The markup was all there; most of it was being painted in a colour
    that vanished against the bar. A DOM check cannot see that. This samples
    the pixels.
    """
    from PIL import Image

    _, shot = streamlit_render
    if not shot.exists():
        pytest.skip("no screenshot was produced")
    im = Image.open(shot).convert("RGB")
    w, h = im.size
    px = im.load()

    def near(a, b, tol=26):
        return all(abs(a[i] - b[i]) <= tol for i in range(3))

    def hex_rgb(v):
        v = v.lstrip("#")
        return tuple(int(v[i:i + 2], 16) for i in (0, 2, 4))

    band = [(x, y) for y in range(0, h) for x in range(0, w)
            if near(px[x, y], hex_rgb(T.DEEP_NAVY), 40)]
    assert band, "the banner itself was never painted"
    top, bottom = min(y for _, y in band), max(y for _, y in band)
    left_half = range(0, w // 2)

    found = {}
    for label, want in (("headline (white)", T.WHITE),
                        ("eyebrow (muted teal)", T.MUTED_TEAL),
                        ("accent (teal)", T.ACCENT_TEAL)):
        target = hex_rgb(want)
        found[label] = any(
            near(px[x, y], target) for y in range(top, bottom + 1) for x in left_half
        )
    missing = [k for k, v in found.items() if not v]
    assert not missing, (
        "painted nowhere in the banner's left zone: %s - the text is present "
        "but not visible, which is exactly the fault that reached a user" % missing
    )
