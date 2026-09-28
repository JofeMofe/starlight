"""Baut die Pixel-Schrift "Glimmer" aus tools/pipeline/fonts/glimmer.txt.

Ausgabe: assets/fonts/glimmer.png (weiße Glyphenmaske, wird zur Laufzeit
per font_color eingefärbt) + glimmer.fnt (AngelCode BMFont, Textformat),
das Godot direkt als FontFile importiert.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

from sl_common import ASSETS, ROOT, GeneratedAsset, save_png

GEN = "tools/pipeline/generators/gen_font_glimmer.py"
SOURCE = ROOT / "tools/pipeline/fonts/glimmer.txt"
FACE = "Glimmer"
CELL_HEIGHT = 11      # Zeilen pro Glyph (Akzente + Versalhöhe + Unterlänge)
LINE_HEIGHT = 12      # inkl. 1 px Zeilenabstand
BASELINE = 9          # Abstand Zellenoberkante -> Grundlinie
SPACE_ADVANCE = 4
ATLAS_WIDTH = 128
GLYPH_COLOR = (255, 255, 255, 255)


def parse_glyphs(path: Path) -> dict[int, list[str]]:
    glyphs: dict[int, list[str]] = {}
    current: int | None = None
    rows: list[str] = []

    def flush() -> None:
        if current is None:
            return
        if len(rows) == CELL_HEIGHT - 2:
            full = ["." * len(rows[0])] * 2 + rows
        elif len(rows) == CELL_HEIGHT:
            full = rows
        else:
            raise ValueError(f"Glyph U+{current:04X}: {len(rows)} Zeilen (erwartet 9 oder 11)")
        width = len(full[0])
        if any(len(r) != width for r in full):
            raise ValueError(f"Glyph U+{current:04X}: ungleich lange Zeilen")
        if current in glyphs:
            raise ValueError(f"Glyph U+{current:04X} doppelt definiert")
        glyphs[current] = full

    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("@ "):
            flush()
            token = line[2:]
            current = int(token[2:], 16) if token.startswith("U+") else ord(token)
            rows = []
        elif current is not None and line:
            rows.append(line)
    flush()
    return glyphs


def build() -> list[GeneratedAsset]:
    glyphs = parse_glyphs(SOURCE)
    # Einfaches Zeilen-Packing, 1 px Abstand gegen Textur-Bleeding
    placements: dict[int, tuple[int, int]] = {}
    x, y = 0, 0
    for code in sorted(glyphs):
        w = len(glyphs[code][0])
        if x + w > ATLAS_WIDTH:
            x, y = 0, y + CELL_HEIGHT + 1
        placements[code] = (x, y)
        x += w + 1
    height = y + CELL_HEIGHT
    height = 1 << (height - 1).bit_length()  # Zweierpotenz
    atlas = Image.new("RGBA", (ATLAS_WIDTH, height), (0, 0, 0, 0))
    px = atlas.load()
    for code, rows in glyphs.items():
        gx, gy = placements[code]
        for ry, row in enumerate(rows):
            for rx, ch in enumerate(row):
                if ch == "#":
                    px[gx + rx, gy + ry] = GLYPH_COLOR
    out_dir = ASSETS / "fonts"
    png_path = save_png(atlas, out_dir / "glimmer.png")

    lines = [
        f'info face="{FACE}" size={LINE_HEIGHT} bold=0 italic=0 charset="" unicode=1 '
        f'stretchH=100 smooth=0 aa=1 padding=0,0,0,0 spacing=1,1',
        f"common lineHeight={LINE_HEIGHT} base={BASELINE} scaleW={ATLAS_WIDTH} "
        f"scaleH={height} pages=1 packed=0",
        'page id=0 file="glimmer.png"',
        f"chars count={len(glyphs) + 1}",
        f"char id=32 x=0 y=0 width=0 height=0 xoffset=0 yoffset=0 xadvance={SPACE_ADVANCE} page=0 chnl=15",
    ]
    for code in sorted(glyphs):
        gx, gy = placements[code]
        w = len(glyphs[code][0])
        lines.append(
            f"char id={code} x={gx} y={gy} width={w} height={CELL_HEIGHT} "
            f"xoffset=0 yoffset=0 xadvance={w + 1} page=0 chnl=15")
    fnt_path = out_dir / "glimmer.fnt"
    fnt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return [
        GeneratedAsset(png_path, "font", GEN, f"Pixel-Schrift Glimmer, {len(glyphs)} Glyphen"),
        GeneratedAsset(fnt_path, "font", GEN, "BMFont-Beschreibung zu glimmer.png"),
    ]


def render_text(text: str, scale: int = 4) -> Image.Image:
    """Vorschau-Hilfe für die visuelle Kontrolle (nicht Teil des Builds)."""
    glyphs = parse_glyphs(SOURCE)
    width = sum(SPACE_ADVANCE if c == " " else len(glyphs[ord(c)][0]) + 1 for c in text)
    img = Image.new("RGBA", (width + 2, LINE_HEIGHT + 2), (43, 33, 64, 255))
    px = img.load()
    x = 1
    for c in text:
        if c == " ":
            x += SPACE_ADVANCE
            continue
        rows = glyphs[ord(c)]
        for ry, row in enumerate(rows):
            for rx, ch in enumerate(row):
                if ch == "#":
                    px[x + rx, 1 + ry] = (244, 236, 223, 255)
        x += len(rows[0]) + 1
    return img.resize((img.width * scale, img.height * scale), Image.Resampling.NEAREST)
