"""Ein Befehl für alle generierten Assets: `python tools/pipeline/build_assets.py`

1. Führt alle Generatoren in `generators/gen_*.py` aus (je eine `build()`-Funktion)
2. Aktualisiert die generierten Zeilen in docs/ASSET_MANIFEST.csv
   (Fremd-Assets bleiben unangetastet)
3. Führt check_palette, check_sizes und check_licenses aus

Mit `--check-only` werden nur die Prüfungen ausgeführt.
Exit-Code != 0, sobald ein Schritt fehlschlägt.
"""
from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import check_licenses  # noqa: E402
import check_palette  # noqa: E402
import check_sizes  # noqa: E402
from sl_common import GeneratedAsset, read_manifest, write_manifest  # noqa: E402


def run_generators() -> list[GeneratedAsset]:
    produced: list[GeneratedAsset] = []
    for gen_file in sorted((HERE / "generators").glob("gen_*.py")):
        module = importlib.import_module(f"generators.{gen_file.stem}")
        assets = module.build()
        print(f"  {gen_file.stem}: {len(assets)} Asset(s)")
        produced.extend(assets)
    return produced


def update_manifest(produced: list[GeneratedAsset]) -> None:
    rows = [r for r in read_manifest() if not r["quelle_url"].startswith("tools/pipeline/")]
    rows.extend(a.manifest_row() for a in produced)
    write_manifest(rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()
    if not args.check_only:
        print("Generiere Assets …")
        update_manifest(run_generators())
    print("Prüfe Assets …")
    results = [check_palette.main(), check_sizes.main(), check_licenses.main()]
    ok = not any(results)
    print("build_assets: OK" if ok else "build_assets: FEHLGESCHLAGEN")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
