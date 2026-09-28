"""Prüft Maße und Raster aller PNGs in assets/ gegen `size_rules.json`.

Jede Regel gilt für ein Glob-Muster (erste passende Regel gewinnt) und
verlangt, dass Breite/Höhe Vielfache eines Rasters sind. Spritesheets mit
einer JSON-Nachbardatei (von atlas.py) werden zusätzlich auf ihre
Framegröße geprüft.
"""
from __future__ import annotations

import fnmatch
import json
import sys
from pathlib import Path

from PIL import Image

from sl_common import ASSETS, rel

RULES_FILE = Path(__file__).with_name("size_rules.json")


def find_rule(path: str, rules: list[dict]) -> dict | None:
    for rule in rules:
        if fnmatch.fnmatch(path, rule["glob"]):
            return rule
    return None


def main() -> int:
    rules: list[dict] = json.loads(RULES_FILE.read_text(encoding="utf-8"))["rules"]
    failures = 0
    checked = 0
    for path in sorted(ASSETS.rglob("*.png")):
        rpath = rel(path)
        rule = find_rule(rpath, rules)
        if rule is None:
            print(f"FEHLER {rpath}: keine Größenregel in size_rules.json")
            failures += 1
            continue
        if rule.get("skip"):
            continue
        checked += 1
        w, h = Image.open(path).size
        gx, gy = rule.get("grid", [1, 1])
        if w % gx or h % gy:
            print(f"FEHLER {rpath}: {w}x{h} ist kein Vielfaches von {gx}x{gy} ({rule['name']})")
            failures += 1
        if "max" in rule and (w > rule["max"][0] or h > rule["max"][1]):
            print(f"FEHLER {rpath}: {w}x{h} größer als erlaubt {rule['max']} ({rule['name']})")
            failures += 1
        meta = path.with_suffix(".json")
        if meta.exists():
            frame = json.loads(meta.read_text(encoding="utf-8")).get("frame_size")
            if frame and (w % frame[0] or h % frame[1]):
                print(f"FEHLER {rpath}: Sheet {w}x{h} passt nicht zu Framegröße {frame}")
                failures += 1
    print(f"check_sizes: {checked} PNGs geprüft, {failures} Fehler")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
