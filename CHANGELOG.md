# Changelog

All notable changes to `eosx-visual-assets` are documented here. The format
follows Keep a Changelog; versions track the design tokens and template API.

## [0.3.0] — 2026-10-05

### Added
- `banner_html.py` — the app banner as HTML and CSS, generated from the registry.
  `banner.py` emits a fixed 1440×300 SVG, which is right on a web page and wrong in an app: a
  fixed viewBox scales uniformly, so narrowing the column shrinks the type with it. This emits
  the same banner as markup that reflows, with every size driven by **one multiplier** so the
  proportions hold at any width. Below 560px the app zone moves under the platform zone rather
  than the type shrinking past legibility.
- `tests/test_banner_html.py` — the guarantee, not a description of one. It asserts the left
  platform zone is **byte-identical across all eleven apps**, that each right zone is exactly the
  registry's name and punchline, that no section or page name appears, that every colour in the
  stylesheet is a token, and that no font-size is hardcoded. Each check was confirmed to fail
  against a deliberately tampered stylesheet before being trusted.

### Why
Seven apps were hand-writing their own header against a spec that exists in three places, two of
which had already diverged. A document cannot make eleven apps agree; a shared artefact and a
failing test can. KB_GROUP.md §7.4 named this as the end state — this is it.

An app now renders `app_banner_html(slug)` and includes `app_banner_css()` once. No geometry, no
colour and no punchline remains in app code, so there is nothing left to drift.

## [0.2.1] — 2026-10-04

**0.2.0 was published, installable, and impossible to import.** `pip install` succeeded and
`import eosx_visual_assets` then raised `FileNotFoundError`. The registry lived at the repo
root, outside `src/`, so `packages.find` never collected it and `package-data` named only the
fonts; `tokens.py` reached it by walking up from `__file__`, which is the repo root in a
checkout and `Lib/` in an install. The load runs at import, so nothing in the package was
usable — not partly, at all. **The `v0.2.0` tag is left in place deliberately.** Nothing
consumes it, and the record is worth more than a tidy tag list.

### Fixed
- The registry moved to `src/eosx_visual_assets/tokens/brand_tokens.json` — inside the package,
  one location, no copy left at the root. `tokens.py` reads it with `importlib.resources`
  instead of path arithmetic, and `package-data` ships it beside the fonts. **No fallback was
  added**: trying the root first and the package second is how this survived to a release,
  because the tests pass from the source tree where the broken path works.
- `TOKENS_PATH` stays exported and stays a real `Path` that exists, for both a checkout and a
  normal install. It is `None` only under zipimport, where no filesystem path exists — rather
  than a path that is merely wrong.

### Added
- `tests/test_installed_package.py` — builds the package, installs it into a throwaway
  virtualenv, and asserts from a directory that is not the repo, with `PYTHONPATH` stripped,
  that the package imports, that the registry holds eleven apps, that `TOKENS_PATH` exists and
  that the console script was created. Verified against the 0.2.0 tree: three of its four
  checks fail there. **Sixty tests passed over a release that could not be imported, because
  every one of them ran from the source tree.**
- `.github/workflows/ci.yml` — the first CI in the group. Lint, test, build the wheel, assert
  the registry is inside it, then install and import it from outside the repo. **Written but
  not yet pushed:** the GitHub token in use lacks the `workflow` scope, so the remote refuses
  any commit that creates `.github/workflows/`. It is on disk, untracked, awaiting
  `gh auth refresh -h github.com -s workflow`.

### Changed
- `README.md`, `CLAUDE.md`, `docs/catalogue.md` and the catalogue line `build.py` generates all
  named the old root path and now name the real one. `docs/catalogue.md` was edited directly,
  not regenerated — regenerating it would re-rasterise the banner PNGs, which is another work
  order's job.
- `build.py` keeps its `REPO_ROOT` for *writing* generated output into a checkout, which is
  legitimate. It never used that route to find the registry.

## [0.2.0] — 2026-10-04 — BROKEN, do not use

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
