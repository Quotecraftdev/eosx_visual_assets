# ==============================================================
# File: check_brand_block.py
# Version: v1.0.0 | Date: 2026-10-05
# Purpose: Fail when any repo's copy of the brand block has
#          drifted from the canonical text in this library.
#
#          The block is deliberately copied into every repo's
#          CLAUDE.md, because a repo's own file is the only one
#          that travels to a clone, a teammate or CI. Copies are
#          fine. Copies nobody checks are not: on 05-10-2026 one
#          bullet was wrong in thirteen files at once and was
#          found by eye, not by a test.
#
#          Canonical text: docs/CLAUDE_BRAND_BLOCK.md
#
# Usage:   python tools/check_brand_block.py [root ...]
#          Exit 0 = every copy matches. 1 = a copy drifted.
#          2 = could not run.
# ==============================================================

from __future__ import annotations

import io
import os
import re
import sys
from pathlib import Path

HEADING = "## Brand \u2014 read this before writing any colour, font or asset"
CANONICAL = Path(__file__).resolve().parents[1] / "docs" / "CLAUDE_BRAND_BLOCK.md"
SKIP_DIRS = {".git", "node_modules", "venv", ".venv", "site-packages", "__pycache__",
             "dist", "build", ".pytest_cache", ".ruff_cache"}


def extract(text: str) -> str | None:
    """The block, from its heading to the next ## heading or the end."""
    i = text.find(HEADING)
    if i < 0:
        return None
    rest = text[i + len(HEADING):]
    m = re.search(r"\n## ", rest)
    block = HEADING + (rest[: m.start()] if m else rest)
    return block.replace("\r\n", "\n").rstrip() + "\n"


def canonical_block() -> str:
    block = extract(io.open(CANONICAL, encoding="utf-8").read())
    if block is None:
        raise SystemExit("2: the canonical file holds no block: %s" % CANONICAL)
    return block


def find_claude_files(root: Path) -> list[Path]:
    out = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        out.extend(Path(dp) / f for f in fn if f.lower() == "claude.md")
    return sorted(out)


def main(argv: list[str]) -> int:
    roots = [Path(a) for a in argv[1:]] or [Path(r"C:\Github")]
    want = canonical_block()
    checked = drifted = missing = 0

    for root in roots:
        if not root.exists():
            print("  ?  %s does not exist" % root)
            continue
        for path in find_claude_files(root):
            if path.resolve() == CANONICAL.resolve():
                continue
            got = extract(io.open(path, encoding="utf-8", errors="replace").read())
            if got is None:
                missing += 1
                print("  -  no block        %s" % path)
                continue
            checked += 1
            if got != want:
                drifted += 1
                print("  X  DRIFTED        %s" % path)
                for line in _first_difference(want, got):
                    print("        %s" % line)

    print("\n  %d copies checked, %d drifted, %d files with no block"
          % (checked, drifted, missing))
    if drifted:
        print("  Fix the copy, not the canonical text, unless the rule itself changed.")
        return 1
    print("  Every copy matches docs/CLAUDE_BRAND_BLOCK.md")
    return 0


def _first_difference(want: str, got: str) -> list[str]:
    w, g = want.split("\n"), got.split("\n")
    for i in range(max(len(w), len(g))):
        a = w[i] if i < len(w) else "(end of file)"
        b = g[i] if i < len(g) else "(end of file)"
        if a != b:
            return ["line %d" % (i + 1), "canonical: %s" % a[:88], "found    : %s" % b[:88]]
    return []


if __name__ == "__main__":
    sys.exit(main(sys.argv))
