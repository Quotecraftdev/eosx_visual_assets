# Changelog

All notable changes to `eosx-visual-assets` are documented here. The format
follows Keep a Changelog; versions track the design tokens and template API.

## [0.2.0] — 2026-10-04

**Reconstructed from the working tree, not from history.** The library was a plain folder
with no `.git` until this release, so there is nothing to read back: this entry records the
difference between what 0.1.0 documented and what the tree actually contains on the day it
became a repository. Individual changes are not dated, because the dates are not recoverable.

### Added
- `lockup.py` and the `lockups/` output directory — the product lockup, a small dark card
  carrying the wave mark, the wordmark and one product name. It is deliberately not the
  banner: the banner introduces the platform, the lockup signs a single product where the
  platform is already named.
- Three apps in the registry, taking it from eight to eleven: **custom**, **learning** and
  **professional**. Each has a glyph in `icons.py`, an entry in `tokens/brand_tokens.json`
  and generated output.
- `icons.py` now holds eleven glyphs, one per registered app, against the eight the 0.1.0
  entry describes.
- `src/eosx_visual_assets/assets/fonts/LICENSES.md` — the bundled faces had no licence file
  while the repository's own `LICENSE` is MIT, which does not cover them. All four are SIL
  Open Font License 1.1, read from each file's own `name` table rather than assumed.

### Changed
- Punchline approvals have moved. 0.1.0 recorded two approved and six draft; the registry now
  has **five approved** — learning, market, pipeline, pricing, signal — and six still marked
  `tagline_draft: true`: bespoke, custom, dashboard, integrity, professional, settlement.
- `pyproject.toml`: `version` 0.1.0 → 0.2.0, and `[project.urls] Repository` filled in. It had
  carried the literal placeholder `{{REPO_URL}}`, which would have shipped as-is.

### Removed
- Four internal documents that were sitting in the folder and would have been published by
  making this repository public — three sales briefs and one page brief, none of which belong
  in a shared asset library. All four were redundant copies of files held elsewhere, verified
  byte-identical or superseded before they were moved. They were moved out of the folder
  rather than gitignored: an ignore rule is one `git add -f` away from publishing what it
  hides, so content that must not ship should not be in the tree at all.

### Notes
- The eleven banner PNGs are clipped. They were rasterised without Manrope resolving, and the
  SVGs beside them are correct. Tracked by its own work order; nothing here regenerates them.
- `Manrope.ttf` and `Inter.ttf` are **variable** fonts. Manrope's weight axis defaults to 200,
  so a renderer that does not set a weight draws ExtraLight where the brand expects 600 or
  800 — see `assets/fonts/LICENSES.md`.

## [0.1.0] — 2026-07-14

### Added
- `tokens/brand_tokens.json` — single source of truth: core palette, on-dark
  surface tokens, fonts, per-module accents, and the app registry.
- Generator package `eosx_visual_assets`: `tokens`, `apps` (registry),
  `icons` (8-glyph library), `text` (font-accurate measurement), `banner`,
  `favicon`, `render`, and `build`.
- Banner template matching the shipped production banner and market mockup:
  navy left→teal gradient, platform lockup + strapline left, app identity right,
  constant teal accent.
- Favicon template: app glyph on a deep-navy rounded square, SVG + PNG at
  16/32/48/64/180/192/512.
- Committed assets for eight apps — Signal, Pricing, Integrity, Market,
  Settlement, Bespoke, Pipeline, Dashboard.
- `docs/index.html` contact sheet and `docs/catalogue.md`.
- Seeded `brand/` and `logos/` from the Energy OSX visual-assets library.

### Notes
- Market and Pricing punch lines are approved; the other six are drafts
  (`tagline_draft: true`) pending sign-off.
