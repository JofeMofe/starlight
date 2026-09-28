"""Gemeinsame Helfer der Starlight-Asset-Pipeline."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from palette import palette_rgb

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"
MANIFEST = ROOT / "docs" / "ASSET_MANIFEST.csv"
MANIFEST_HEADER = [
    "pfad", "typ", "quelle_url", "autor", "lizenz", "lizenz_url",
    "abruf_datum", "modifiziert", "notiz",
]
GENERATED_AUTHOR = "Starlight-Projekt (prozedural generiert)"

RGBA = tuple[int, int, int, int]
TRANSPARENT: RGBA = (0, 0, 0, 0)


@dataclass
class GeneratedAsset:
    """Ein von einem Generator erzeugtes Asset (für das Manifest)."""
    path: Path
    typ: str
    generator: str
    note: str = ""

    def manifest_row(self) -> dict[str, str]:
        return {
            "pfad": rel(self.path),
            "typ": self.typ,
            "quelle_url": self.generator,
            "autor": GENERATED_AUTHOR,
            "lizenz": "MIT",
            "lizenz_url": "LICENSE",
            "abruf_datum": "-",
            "modifiziert": "nein",
            "notiz": self.note,
        }


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def save_png(img: Image.Image, path: Path) -> Path:
    """Speichert verlustfrei und deterministisch (keine Zeitstempel-Metadaten)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="PNG", optimize=True)
    return path


def pixelmap(rows: list[str], legend: dict[str, RGBA]) -> Image.Image:
    """Rendert eine ASCII-Pixelkarte. '.' und ' ' sind transparent.

    Alle Zeilen müssen gleich lang sein, damit Tippfehler in handgesetzten
    Sprites sofort auffallen statt ein verschobenes Bild zu erzeugen.
    """
    width = len(rows[0])
    for i, row in enumerate(rows):
        if len(row) != width:
            raise ValueError(f"Zeile {i} hat Länge {len(row)}, erwartet {width}: {row!r}")
    img = Image.new("RGBA", (width, len(rows)), TRANSPARENT)
    px = img.load()
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in ".  ":
                continue
            if ch not in legend:
                raise KeyError(f"Zeichen {ch!r} (x={x}, y={y}) fehlt in der Legende")
            px[x, y] = legend[ch]
    return img


def palette_set() -> set[tuple[int, int, int]]:
    return set(palette_rgb())


def read_manifest() -> list[dict[str, str]]:
    if not MANIFEST.exists():
        return []
    with MANIFEST.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def write_manifest(rows: list[dict[str, str]]) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    rows = sorted(rows, key=lambda r: r["pfad"])
    with MANIFEST.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=MANIFEST_HEADER, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
