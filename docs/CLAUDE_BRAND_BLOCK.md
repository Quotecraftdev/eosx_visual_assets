# The brand block

**This file is the canonical text.** Every repo's `CLAUDE.md` carries a copy of the section
below, and `tools/check_brand_block.py` fails when a copy differs from this one.

Copies are allowed; divergence is not. On 05-10-2026 one bullet in this block was wrong and had
to be rewritten in thirteen files by hand, which is the failure this arrangement ends: there is
one source, and drift is detected rather than noticed.

Do not edit a repo's copy. Edit this file, bump the library, and run the checker.

---

## Brand — read this before writing any colour, font or asset

The group brand is one library. This repo does not define it and does not keep a copy of it.

**Source.** `eosx-visual-assets`, installed from its tag:
`eosx-visual-assets @ git+https://github.com/Quotecraftdev/eosx_visual_assets@v0.2.1`
The registry is `src/eosx_visual_assets/tokens/brand_tokens.json`, inside the package. Read it
through the package — `from eosx_visual_assets import tokens` — never by a path into another
folder on the machine.

**Rules.** `C:\Quotecraft\Knowledge Base\KB_GROUP.md` §7. The rules live there, not here, and are
deliberately not restated here. If a rule seems to be missing, read §7 before inventing one.

**Never:**

- **Type a hex, an `rgb()` or a font name into this repo.** If a value is needed and the token
  file does not carry it, stop and ask Chris. Inventing one is how 296 colours got into an estate
  that sanctions 22.
- **Copy a banner, favicon, lockup or token file into this repo.** 437 of the estate's 747 asset
  files are redundant copies, and the three apps that look most on-brand are the three now
  carrying forked assets. Copying buys today's consistency with next quarter's drift.
- **Invent a banner.** A banner may be built in HTML where the surface reflows — see
  `KB_GROUP.md` §7.4 — but every value in it comes from the registry: the app name, the
  punchline, the strapline, the domains, every colour. Never retyped, never edited per app.
- **Hand-draw a favicon or a lockup.** Those are generated only, by
  `python -m eosx_visual_assets.build`.
- **Put the section or page name in the banner.** The sidebar already says where the user is.
- **Use Montserrat.** It is not an Energy OSX face (Chris, 04-10-2026).

**Faces.** Manrope for headings, Inter for body, IBM Plex Mono for metric labels. The library
ships the TTFs. A render that silently falls back to a system font produces wrong metrics — never
report a screen render as evidence about a committed file without stating which fonts resolved.

**The HTML visual register is for people, not for code.**
`C:\Quotecraft\Energy OSX Ltd\Visual Assets\BRAND_VISUAL_REGISTER.html` is how Chris reviews the
system. Never read a value out of it: it is a rendering of the tokens, one step downstream of
them.
