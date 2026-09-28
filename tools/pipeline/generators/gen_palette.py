"""Schreibt die Master-Palette als .hex, Swatch-PNG und 64x1-Lookup-Streifen."""
from __future__ import annotations

from PIL import Image

from palette import RAMPS, palette_hex, palette_rgb
from sl_common import ASSETS, GeneratedAsset, save_png

GEN = "tools/pipeline/generators/gen_palette.py"
CELL = 8


def build() -> list[GeneratedAsset]:
    out_dir = ASSETS / "palette"
    out_dir.mkdir(parents=True, exist_ok=True)

    hex_path = out_dir / "starlight.hex"
    hex_path.write_text("\n".join(palette_hex()) + "\n", encoding="utf-8")

    # Swatch: eine Zeile pro Rampe, damit die Rampenlogik sichtbar ist.
    longest = max(len(r) for r in RAMPS.values())
    swatch = Image.new("RGBA", (longest * CELL, len(RAMPS) * CELL), (0, 0, 0, 0))
    for row, ramp in enumerate(RAMPS.values()):
        for col, h in enumerate(ramp):
            rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
            swatch.paste((*rgb, 255), (col * CELL, row * CELL, (col + 1) * CELL, (row + 1) * CELL))
    swatch_path = save_png(swatch, out_dir / "starlight_swatch.png")

    strip = Image.new("RGBA", (64, 1))
    strip.putdata([(*c, 255) for c in palette_rgb()])
    strip_path = save_png(strip, out_dir / "starlight_strip.png")

    return [
        GeneratedAsset(hex_path, "palette", GEN, "Master-Palette, 64 Farben"),
        GeneratedAsset(swatch_path, "palette", GEN, "Swatch, eine Zeile pro Rampe"),
        GeneratedAsset(strip_path, "palette", GEN, "64x1-Lookup für Shader"),
    ]
