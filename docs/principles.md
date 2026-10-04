# Visual-asset principles

`eosx-visual-assets` exists because Energy OSX is one platform made of many apps, and a user moving between them should never feel like they've left. These are the rules the banner and favicon templates enforce.

**One accent, held constant.** The teal accent (`#35C5C5` on dark) is the same on every app's banner and favicon. This is deliberate: the platform is the constant, the app is the variable. If each app had its own banner colour, the set would read as eight products from eight teams rather than one platform with eight surfaces. Per-module hues (`product_accents` in the tokens) survive only for light-surface UI chips and cards, never for the banner accent.

**Apps differ by glyph and punch line, not colour.** Recognition comes from the app's line-drawn glyph and its three-word punch line (`POSITION. GAP. WIN.`), both of which carry meaning, rather than from a colour the user has to learn. Glyphs are authored in one 44×44 box so the same mark serves the banner and the favicon at every size.

**The strapline never changes.** `The operating layer for energy intelligence`, with `energy intelligence` in accent teal, and the `Operational · Commercial · Financial` domain line, appear identically on every banner. They are the platform's signature; only the right-hand identity block varies.

**Templates, not hand-builds.** No banner or favicon should be drawn by hand in an app repo. Every asset is a pure function of one registry entry, so a new app is one line of JSON and a rebuild — and a brand change (a colour, the strapline, the gradient) propagates to all assets at once instead of being chased across repos.

**SVG is the master; PNG is a convenience.** The SVG carries the real typography and scales without loss — it is what apps should embed. PNGs are rasterised at fixed sizes for slides, social and favicon manifests where a raster is required.

**Restraint over decoration.** The dark navy gradient, a single hairline divider, and quiet muted-teal labels do the work. No drop shadows on the panel, no gradients inside the glyphs, no second accent. When in doubt, remove an element — the banner still reads.
