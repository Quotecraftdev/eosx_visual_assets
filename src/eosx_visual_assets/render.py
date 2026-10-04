# ==============================================================
# File: render.py
# Version: v0.1.0 | Date: 2026-07-14
# Purpose: Rasterise brand SVGs to PNG with the bundled brand fonts.
#          Isolated here so the rest of the package has no hard
#          dependency on cairosvg (SVG masters build without it).
# ==============================================================

from __future__ import annotations

from pathlib import Path


def png_from_svg(svg: str, out_path: Path, *, width: int | None = None) -> None:
    """Rasterise an SVG string to a PNG file at `out_path`.

    `width` sets the output pixel width; height follows the viewBox
    aspect ratio. Requires cairosvg (an optional dependency).
    """
    import cairosvg  # imported lazily so SVG-only builds don't need it

    out_path.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(
        bytestring=svg.encode("utf-8"),
        write_to=str(out_path),
        output_width=width,
    )


__all__ = ["png_from_svg"]
