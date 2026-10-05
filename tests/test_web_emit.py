# ==============================================================
# File: test_web_emit.py
# Version: v1.0.0 | Date: 2026-10-05
# Purpose: Prove the React rendering and the Python rendering are
#          the same banner, not two banners that resemble each
#          other.
#
#          Two layers. The cheap checks always run and need no
#          toolchain. The equality check bundles the generated
#          component with esbuild, renders it with react-dom/server
#          and compares the DOM to app_banner_html() node by node -
#          it needs node and npm, and skips rather than lies when
#          they are not there.
# ==============================================================

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path

import pytest

from eosx_visual_assets import tokens as T
from eosx_visual_assets.apps import APPS
from eosx_visual_assets.banner_html import app_banner_html
from eosx_visual_assets.web import banner_tsx, emit_web, tokens_ts

ALL_SLUGS = sorted(APPS)


# ---------------------------------------------------------------- cheap checks


def test_emit_writes_the_three_files(tmp_path: Path) -> None:
    written = emit_web(tmp_path / "web")
    assert sorted(p.name for p in written) == ["Banner.tsx", "banner.css", "tokens.ts"]
    for p in written:
        assert p.read_text(encoding="utf-8").strip()


def test_tokens_ts_carries_every_app_exactly_as_the_registry_has_it() -> None:
    ts = tokens_ts()
    for slug in ALL_SLUGS:
        app = APPS[slug]
        assert '"%s": {' % slug in ts.replace("\n", " ").replace("  ", " ") or f'"{slug}"' in ts
        assert app.name in ts
        assert app.punchline in ts
    assert "export type AppSlug" in ts
    for slug in ALL_SLUGS:
        assert '"%s"' % slug in ts


def test_the_component_holds_no_values_of_its_own() -> None:
    """Every value must come from tokens.ts, or this is a second copy."""
    tsx = banner_tsx()
    assert not re.search(r"#[0-9a-fA-F]{6}", tsx), "a colour is typed into the component"
    for slug in ALL_SLUGS:
        assert APPS[slug].punchline not in tsx, "a punchline is typed into the component"
        assert APPS[slug].name not in tsx, "an app name is typed into the component"
    assert T.TAGLINE not in tsx, "the strapline is typed into the component"


def test_the_component_refuses_an_app_outside_the_registry() -> None:
    assert "is not in the registry" in banner_tsx()


def test_class_names_match_the_python_markup_in_the_same_order() -> None:
    """A structural check that needs no toolchain, so it always runs."""
    py = re.findall(r'class="([^"]+)"', app_banner_html("market"))
    ts = re.findall(r'className="([^"]+)"', banner_tsx())
    assert py == ts, "the component's elements differ from the Python markup"


# ------------------------------------------------- the real equality check


class _Canon(HTMLParser):
    """Normalise markup to a comparable node stream."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[tuple] = []

    def handle_starttag(self, tag, attrs):
        self.out.append(
            (tag, tuple(sorted((k, re.sub(r"\s+", " ", v or "").strip()) for k, v in attrs)))
        )

    handle_startendtag = handle_starttag

    def handle_endtag(self, tag):
        self.out.append(("/" + tag, ()))

    def handle_data(self, data):
        text = re.sub(r"\s+", " ", data).strip()
        if text:
            self.out.append(("#text", text))


def _canon(markup: str) -> list[tuple]:
    p = _Canon()
    p.feed(markup)
    return p.out


RENDER_HARNESS = """\
import { renderToStaticMarkup } from "react-dom/server";
import { Banner } from "./Banner";
import { apps, type AppSlug } from "./tokens";
const out: Record<string, string> = {};
for (const slug of Object.keys(apps) as AppSlug[]) {
  out[slug] = renderToStaticMarkup(<Banner app={slug} />);
}
process.stdout.write(JSON.stringify(out));
"""


@pytest.mark.slow
def test_react_renders_the_same_dom_as_python(tmp_path: Path) -> None:
    if not shutil.which("node") or not shutil.which("npm"):
        pytest.skip("node and npm are needed to render the component")

    work = tmp_path / "reactcheck"
    work.mkdir()
    emit_web(work)
    (work / "package.json").write_text('{"name":"c","private":true,"type":"module"}', "utf-8")
    (work / "render.tsx").write_text(RENDER_HARNESS, "utf-8")

    install = subprocess.run(
        ["npm", "install", "--silent", "react@19", "react-dom@19", "esbuild"],
        cwd=work, capture_output=True, text=True,
        shell=(os.name == "nt"),
    )
    if install.returncode != 0:
        pytest.skip("npm install failed (offline?): %s" % install.stderr[-200:])

    esbuild = work / "node_modules" / ".bin" / (
        "esbuild.cmd" if os.name == "nt" else "esbuild")
    build = subprocess.run(
        [str(esbuild), "render.tsx", "--bundle", "--platform=node", "--format=cjs",
         "--jsx=automatic", "--outfile=render.cjs", "--log-level=error"],
        cwd=work, capture_output=True, text=True,
    )
    assert build.returncode == 0, "the generated TSX did not compile:\n" + build.stderr

    # node writes UTF-8; without encoding= this decodes as cp1252 on Windows and
    # turns the domain separator into a question mark - a false mismatch.
    run = subprocess.run(["node", "render.cjs"], cwd=work, capture_output=True,
                         text=True, encoding="utf-8")
    assert run.returncode == 0, "the component did not render:\n" + run.stderr
    rendered = json.loads(run.stdout)

    assert sorted(rendered) == ALL_SLUGS, "React rendered a different set of apps"
    for slug in ALL_SLUGS:
        assert _canon(app_banner_html(slug)) == _canon(rendered[slug]), (
            "React and Python render different DOM for %s" % slug
        )
