# CLAUDE.md — eosx_visual_assets

The brand library. This file points; it does not restate. Everything it points at is the
source, and a second copy of any of it is the failure this repository exists to end.

## The one source of truth

`src/eosx_visual_assets/tokens/brand_tokens.json` holds the group's colour, type and app
registry. It lives **inside the package**, so it ships with an install; a raw-file consumer
reads it from that path on GitHub. **Nothing in this repo, and nothing in any consuming app,
defines a colour or a font anywhere else.** If you are about to type a hex value or a font
name, stop and read the registry instead.

## The rules are not here

The brand rules live in **`C:\Quotecraft\Knowledge Base\KB_GROUP.md` §7**. This repository is
the *implementation* of those rules. **They are not duplicated here, deliberately.** If a rule
seems to be missing from this repo, read §7 — do not write a second copy of it. The palette,
the type scale and the product punchlines are in the tokens file and in §7; they do not belong
in this document.

## Generated, never drawn

Banners, favicons and lockups are produced from the registry by `eosx-assets-build`. **Never
hand-draw one**, here or in a consuming app. `docs/principles.md` already states this and is
the longer argument for it.

## Fonts, and what a render proves

The committed PNGs are rendered with the TTFs in `src/eosx_visual_assets/assets/fonts/`. A
render that falls back to a system font produces wrong metrics and clipped output. **Never
report a screen render as evidence about a committed file without stating which fonts
resolved.**

`Manrope.ttf` and `Inter.ttf` are variable fonts. Manrope's weight axis runs 200–800 and
**defaults to 200**, so a renderer that does not set a weight draws ExtraLight where the brand
expects 600 or 800. `src/eosx_visual_assets/assets/fonts/LICENSES.md` has the detail, and the
licence of every bundled face.

## Known, as at 0.2.1

- **The eleven banner PNGs are clipped.** They were rasterised without Manrope resolving. The
  SVGs beside them are correct. Covered by its own work order — do not regenerate them here.
- **`v0.2.0` is published and cannot be imported.** The registry sat outside `src/`, so it was
  never packaged, and `tokens.py` found it by walking up from `__file__` — which resolves in a
  checkout and not in an install. Fixed in `0.2.1` by moving the registry into the package and
  reading it with `importlib.resources`. The tag is left in place as the honest record.
- **Do not add a fallback that tries one path then another.** Two lookups are how this reached
  a release: the tests passed from the source tree, where the broken path worked.
