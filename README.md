# eosx-visual-assets

The shared brand and visual-asset library for the Energy OSX platform. It holds the design tokens, logo lockups and reference sheets, and — most importantly — a **template system** that renders every app's banner and favicon from a single registry.

It exists so that Energy OSX apps *pull* finished, on-brand assets from one place instead of hand-building a banner or favicon mid-app-build. Add an app to the registry, run the build, consume the file.

## What's in here

```
src/eosx_visual_assets/tokens/
               brand_tokens.json — the single source of truth
               (colours, fonts, app registry). Inside the package so it
               ships with an install; raw-file consumers read it from
               that path on GitHub.
brand/         brand PDF, colour/logo/UI reference sheets, wallpaper
logos/         Energy OSX wordmark, icon, and product logo lockups (SVG + PNG)
banners/       generated app banners  (banner_<slug>.svg / .png)
favicons/      generated app favicons (favicon_<slug>.svg / _<size>.png)
docs/          index.html contact sheet + catalogue.md
src/           the generator package (template + icon library + build)
```

Generated assets in `banners/` and `favicons/` are committed so apps can grab a raw file without running Python.

## Add an app (the whole workflow)

1. Add one entry to `src/eosx_visual_assets/tokens/brand_tokens.json` under `apps`:

   ```json
   "risk": { "name": "Risk Intelligence", "icon": "market",
             "punchline": "SEE. SIZE. HEDGE.", "tagline_draft": true }
   ```

2. If it needs a new glyph, add it to `src/eosx_visual_assets/icons.py` (44×44 box).
3. Rebuild:

   ```bash
   pip install -e ".[render]"
   python -m eosx_visual_assets.build          # SVG + PNG
   python -m eosx_visual_assets.build --no-png  # SVG masters only (no cairosvg)
   ```

That regenerates every banner, favicon, the contact sheet and the catalogue.

## Design rules (locked)

The banner is the shipped house style: a dark navy panel with a left→teal gradient, the platform lockup and `The operating layer for energy intelligence` strapline on the left, and the app identity on the right. **The accent stays constant teal (`#35C5C5`) on every app** — apps are told apart by their glyph and three-word punch line, never by a different colour. See [docs/principles.md](docs/principles.md).

## Apps

Eight apps ship in `v0.1.0`: Signal, Pricing, Integrity, Market, Settlement, Bespoke, Pipeline, Dashboard. Market and Pricing punch lines are approved; the other six are drafts (`tagline_draft: true`) pending sign-off — see [docs/catalogue.md](docs/catalogue.md).

## Status

`v0.1.0`: tokens, app registry, banner + favicon templates, an 8-glyph icon library, and committed assets for all eight apps. Sibling to [`eosx-charts`](../eosx_charts), which owns the chart theming.

## Relationship to eosx-charts

`eosx-charts` themes charts; `eosx-visual-assets` owns brand identity (banners, favicons, logos, tokens). Both read the same locked palette and type stack so a chart, a banner and a favicon feel like one product.
