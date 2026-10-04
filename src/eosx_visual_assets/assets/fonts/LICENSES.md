# Font licences

The repository's own `LICENSE` is MIT and covers the code. **It does not cover these font
files.** Each face carries its own licence, recorded below.

Every entry was read from the font file itself — the `name` table, records 0 (copyright),
13 (licence description) and 14 (licence URL) — on 04-10-2026, not inferred from the family
name or from a web page about the project.

| File | Family | Version | Licence (as stated inside the file) | Copyright |
|---|---|---|---|---|
| `Manrope.ttf` | Manrope | 4.504 | SIL Open Font License 1.1 | Copyright 2019 The Manrope Project Authors (https://github.com/sharanda/manrope) |
| `Inter.ttf` | Inter | 4.001 (`git-66647c0bb`) | SIL Open Font License 1.1 | Copyright 2016 The Inter Project Authors (https://github.com/rsms/inter) |
| `IBMPlexMono-Regular.ttf` | IBM Plex Mono | 2.3 | SIL Open Font License 1.1 | Copyright 2017 IBM Corp. All rights reserved. |
| `IBMPlexMono-Medium.ttf` | IBM Plex Mono Medium | 2.3 | SIL Open Font License 1.1 | Copyright 2017 IBM Corp. All rights reserved. |

All four declare **SIL Open Font License, Version 1.1**. The licence text each file points to:

- Manrope, IBM Plex Mono (both weights): `http://scripts.sil.org/OFL`
- Inter: `https://openfontlicense.org`

## What OFL 1.1 permits, and the one condition that applies here

The OFL allows these files to be bundled in this repository, redistributed with it, and
embedded in the images this package generates, including commercially. The conditions that
bear on this repo:

- **The licence must travel with the fonts.** This file, plus the copyright lines above, is
  how that is satisfied. Do not remove it, and do not move the fonts out of this directory
  without bringing it along.
- **The fonts must not be sold on their own.** They are not; they are a dependency of a
  generator.
- **A modified version must not use the reserved font name.** Nothing here modifies them.

## Two things to know about the files themselves

**`Manrope.ttf` and `Inter.ttf` are variable fonts, not static instances.**

| File | Axes | Default instance |
|---|---|---|
| `Manrope.ttf` | `wght` 200–800 | **200** — which is why the file reports its family as *"Manrope ExtraLight"* |
| `Inter.ttf` | `opsz` 14–32, `wght` 100–900 | 400 at `opsz` 14 |

The brand uses Manrope at 600 and 800. **A renderer that loads this file without setting the
weight axis draws it at 200**, which is a different typeface by eye and has different metrics.
If a render looks thin, or wider or narrower than expected, that is the first thing to check.
The name *"Manrope ExtraLight"* in a font dialog is not evidence that the wrong file is
bundled; it is the default instance of the right one.

The two IBM Plex Mono files are ordinary static fonts.
