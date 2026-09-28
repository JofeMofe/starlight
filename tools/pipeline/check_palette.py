"""Prüft jedes PNG in assets/ gegen die Master-Palette.

Fehler, wenn
- eine deckende Farbe nicht in der Palette liegt,
- Alpha nicht binär ist (0 oder 255), d. h. Anti-Aliasing gegen Transparenz,
- reines Schwarz/Weiß vorkommt (über die Palette ohnehin ausgeschlossen).

Ausnahmen (Normal Maps, Lichttexturen, Masken, UI-Transparenzen) stehen als
Glob-Muster in `palette_whitelist.txt`.
"""
from __future__ import annotations

import fnmatch
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from sl_common import ASSETS, ROOT, palette_set, rel

WHITELIST_FILE = Path(__file__).with_name("palette_whitelist.txt")


def load_whitelist() -> list[str]:
    patterns: list[str] = []
    for line in WHITELIST_FILE.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            patterns.append(line)
    return patterns


def is_whitelisted(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, p) for p in patterns)


def check_image(path: Path, allowed: set[tuple[int, int, int]]) -> list[str]:
    errors: list[str] = []
    arr = np.asarray(Image.open(path).convert("RGBA"))
    alpha = arr[..., 3]
    partial = np.count_nonzero((alpha > 0) & (alpha < 255))
    if partial:
        errors.append(f"{partial} halbtransparente Pixel (Alpha muss 0 oder 255 sein)")
    opaque = arr[alpha == 255][:, :3]
    if opaque.size:
        uniq = {tuple(int(v) for v in c) for c in np.unique(opaque, axis=0)}
        bad = sorted(uniq - allowed)
        if bad:
            sample = ", ".join("#%02x%02x%02x" % c for c in bad[:6])
            errors.append(f"{len(bad)} Farben außerhalb der Palette (z. B. {sample})")
    return errors


def main() -> int:
    allowed = palette_set()
    patterns = load_whitelist()
    failures = 0
    checked = 0
    for path in sorted(ASSETS.rglob("*.png")):
        rpath = rel(path)
        if is_whitelisted(rpath, patterns):
            continue
        checked += 1
        for err in check_image(path, allowed):
            print(f"FEHLER {rpath}: {err}")
            failures += 1
    print(f"check_palette: {checked} PNGs geprüft, {failures} Fehler")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "tools" / "pipeline"))
    sys.exit(main())
