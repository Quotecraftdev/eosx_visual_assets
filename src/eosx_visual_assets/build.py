# ==============================================================
# File: build.py
# Version: v0.2.0 | Date: 2026-09-06
# Purpose: Build every app's banner and favicon from the registry
#          into banners/, lockups/ and favicons/, plus a docs/index.html
#          contact sheet and docs/catalogue.md. This is the whole
#          pipeline: registry in, versioned assets out.
#
# Usage:  python -m eosx_visual_assets.build [--no-png]
# ==============================================================

from __future__ import annotations

import argparse
from pathlib import Path

from eosx_visual_assets import __version__
from eosx_visual_assets.apps import App, ordered_apps
from eosx_visual_assets.banner import build_banner_svg
from eosx_visual_assets.favicon import FAVICON_PNG_SIZES, build_favicon_svg
from eosx_visual_assets.lockup import build_lockup_svg

REPO_ROOT = Path(__file__).resolve().parents[2]
BANNERS = REPO_ROOT / "banners"
LOCKUPS = REPO_ROOT / "lockups"
FAVICONS = REPO_ROOT / "favicons"
DOCS = REPO_ROOT / "docs"

BANNER_PNG_WIDTH = 2880  # 2x the 1440 viewBox — crisp for slides/social
LOCKUP_PNG_WIDTH = 1378  # 2x the 689 viewBox


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_all(make_png: bool = True) -> list[App]:
    apps = ordered_apps()
    png = None
    if make_png:
        try:
            from eosx_visual_assets.render import png_from_svg as png
        except Exception as exc:  # pragma: no cover
            print(f"  ! PNG export unavailable ({exc}); writing SVG only")
            png = None

    for app in apps:
        banner_svg = build_banner_svg(app)
        _write(BANNERS / f"banner_{app.slug}.svg", banner_svg)

        lockup_svg = build_lockup_svg(app)
        _write(LOCKUPS / f"lockup_{app.slug}.svg", lockup_svg)

        fav_svg = build_favicon_svg(app)
        _write(FAVICONS / f"favicon_{app.slug}.svg", fav_svg)

        if png:
            png(banner_svg, BANNERS / f"banner_{app.slug}.png", width=BANNER_PNG_WIDTH)
            png(lockup_svg, LOCKUPS / f"lockup_{app.slug}.png", width=LOCKUP_PNG_WIDTH)
            for s in FAVICON_PNG_SIZES:
                png(fav_svg, FAVICONS / f"favicon_{app.slug}_{s}.png", width=s)

        flag = "  (draft punch line)" if app.tagline_draft else ""
        print(f"  + {app.slug:<11} {app.name}{flag}")

    _write(DOCS / "index.html", _contact_sheet(apps))
    _write(DOCS / "catalogue.md", _catalogue(apps))
    print(f"\nBuilt {len(apps)} apps -> banners/  lockups/  favicons/  docs/index.html")
    return apps


_FONT_HREF = (
    "https://fonts.googleapis.com/css2"
    "?family=Inter:wght@400;500;600&family=Manrope:wght@600;800&display=swap"
)

# Plain (non-f) string: real braces, no escaping, no f-string edge cases.
_CONTACT_CSS = """
  :root{ --navy:#031A3A; --teal:#35C5C5; --muted:#7FBFC8; }
  *{ box-sizing:border-box }
  body{ margin:0; background:#0A1622; color:#E7EEF4; padding:40px;
        font-family:Inter,system-ui,sans-serif; }
  header{ max-width:1200px; margin:0 auto 28px }
  header h1{ font-family:Manrope,sans-serif; font-weight:800; margin:0 0 6px; font-size:26px }
  header p{ margin:0; color:var(--muted); font-size:14px }
  main{ max-width:1200px; margin:0 auto; display:flex; flex-direction:column; gap:26px }
  .card{ background:#0E1B29; border:1px solid #1B2A3A; border-radius:14px; padding:18px }
  .head{ display:flex; align-items:center; gap:14px; margin-bottom:14px }
  .fav{ width:46px; height:46px; border-radius:11px }
  .head h2{ font-family:Manrope,sans-serif; font-weight:600; font-size:18px; margin:0 }
  .slug{ font-family:'IBM Plex Mono',monospace; font-size:11px;
         color:var(--muted); margin-left:10px }
  .punch{ margin:2px 0 0; font-size:12px; letter-spacing:.14em; color:var(--muted) }
  .banner{ width:100%; display:block; border-radius:10px }
"""


def _card(a: App) -> str:
    draft = " (draft)" if a.tagline_draft else ""
    return (
        '    <section class="card">\n'
        '      <div class="head">\n'
        f'        <img class="fav" src="../favicons/favicon_{a.slug}.svg" alt="{a.name} icon"/>\n'
        "        <div>\n"
        f'          <h2>{a.name}<span class="slug">{a.slug}</span></h2>\n'
        f'          <p class="punch">{a.punchline}{draft}</p>\n'
        "        </div>\n"
        "      </div>\n"
        f'      <img class="banner" src="../banners/banner_{a.slug}.svg" alt="{a.name} banner"/>\n'
        "    </section>"
    )


def _contact_sheet(apps: list[App]) -> str:
    rows = "\n".join(_card(a) for a in apps)
    subtitle = (
        f"Banner + favicon library v{__version__} - {len(apps)} apps - "
        "accent held constant teal, apps differ by glyph and punch line"
    )
    head = (
        "<!doctype html>\n"
        '<html lang="en"><head><meta charset="utf-8"/>\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>\n'
        "<title>Energy OSX - Visual Assets contact sheet</title>\n"
        '<link rel="preconnect" href="https://fonts.googleapis.com"/>\n'
        f'<link rel="stylesheet" href="{_FONT_HREF}"/>\n'
        "<style>" + _CONTACT_CSS + "</style></head>\n"
    )
    body = (
        "<body>\n"
        "  <header>\n"
        "    <h1>Energy OSX - Visual Assets</h1>\n"
        f"    <p>{subtitle}</p>\n"
        "  </header>\n"
        f"  <main>\n{rows}\n  </main>\n"
        "</body></html>\n"
    )
    return head + body


def _catalogue(apps: list[App]) -> str:
    lines = [
        "# App asset catalogue",
        "",
        f"Generated by `python -m eosx_visual_assets.build` - v{__version__}.",
        "",
        "Every app below is one entry in "
        "`src/eosx_visual_assets/tokens/brand_tokens.json`, rendered",
        "to a banner and a favicon by the same template. Add an app there, rerun",
        "the build; never hand-build a banner.",
        "",
        "| App | Slug | Glyph | Punch line | Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for a in apps:
        status = "draft" if a.tagline_draft else "approved"
        lines.append(f"| {a.name} | `{a.slug}` | `{a.icon}` | {a.punchline} | {status} |")
    lines += [
        "",
        "## Files per app",
        "",
        "- `banners/banner_<slug>.svg` - master (scales cleanly, use in web/app)",
        "- `banners/banner_<slug>.png` - 2880px raster for slides/social",
        "- `lockups/lockup_<slug>.svg` - product lockup (the small dark card:",
        "  wave mark, wordmark, product name — no strapline, no domains)",
        "- `lockups/lockup_<slug>.png` - 1378px raster",
        "- `favicons/favicon_<slug>.svg` - master icon",
        "- `favicons/favicon_<slug>_<size>.png` - 16/32/48/64/180/192/512",
        "",
        "See `docs/index.html` for the visual contact sheet.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Build Energy OSX visual assets.")
    ap.add_argument("--no-png", action="store_true", help="write SVG masters only")
    ap.add_argument("--web", action="store_true",
                    help="also emit dist/web: tokens.ts, Banner.tsx and banner.css "
                         "for the React apps")
    args = ap.parse_args()
    print(f"eosx-visual-assets build v{__version__}")
    build_all(make_png=not args.no_png)
    if args.web:
        from eosx_visual_assets.web import emit_web
        for path in emit_web(REPO_ROOT / "dist" / "web"):
            print(f"  web   {path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
