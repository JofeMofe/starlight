"""Prüft, dass jede Datei in assets/ einen Eintrag in docs/ASSET_MANIFEST.csv hat.

Zusätzlich: Manifest-Einträge ohne Datei, verbotene Lizenzen und fehlende
Lizenztexte für Fremd-Assets (docs/licenses/).
"""
from __future__ import annotations

import sys

from sl_common import ASSETS, ROOT, read_manifest, rel

# Godot-Nebendateien gehören nicht ins Manifest.
IGNORED_SUFFIXES = {".import", ".uid"}
ALLOWED_LICENSES = {"MIT", "CC0", "CC0-1.0", "CC-BY-4.0", "OFL-1.1", "Public Domain", "OGA-BY-3.0",
                    "Sunnyside-World-V1"}
FORBIDDEN_MARKERS = ("NC", "ND", "PROPRIETARY", "UNKNOWN")


def main() -> int:
    rows = read_manifest()
    by_path = {r["pfad"]: r for r in rows}
    failures = 0

    files = [p for p in ASSETS.rglob("*") if p.is_file() and p.suffix not in IGNORED_SUFFIXES]
    for path in sorted(files):
        rpath = rel(path)
        if rpath not in by_path:
            print(f"FEHLER {rpath}: kein Eintrag in ASSET_MANIFEST.csv")
            failures += 1

    for rpath, row in sorted(by_path.items()):
        if not (ROOT / rpath).exists():
            print(f"FEHLER {rpath}: im Manifest, aber Datei fehlt")
            failures += 1
        lic = row.get("lizenz", "").strip()
        if lic not in ALLOWED_LICENSES or any(m in lic.upper() for m in FORBIDDEN_MARKERS):
            print(f"FEHLER {rpath}: Lizenz '{lic}' nicht erlaubt")
            failures += 1
        lic_url = row.get("lizenz_url", "").strip()
        if not lic_url:
            print(f"FEHLER {rpath}: lizenz_url fehlt")
            failures += 1
        elif not lic_url.startswith("http") and not (ROOT / lic_url).exists():
            print(f"FEHLER {rpath}: Lizenztext '{lic_url}' fehlt im Repo")
            failures += 1

    print(f"check_licenses: {len(files)} Dateien, {len(rows)} Manifest-Einträge, {failures} Fehler")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
