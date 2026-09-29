"""Bodenkacheln aus dem LPC-Geländeset von ElizaWy (vendor/eliza/Terrain), Originalfarben.

Die LPC-Vorlagen sind eckbasiert: Übergänge verlaufen durch die Kachelmitte, jede
Kachel wird durch die Geländeart ihrer vier Ecken bestimmt. Im Spiel liegt diese
Bodenebene deshalb um eine halbe Kachel versetzt über dem Kartenraster („Dual Grid“):
die vier Ecken einer sichtbaren Kachel sind die vier angrenzenden Kartenzellen.

Atlas (32er-Kacheln, 16 Spalten):
- Zeile 0: Gras/Weg, Index = Eckmaske (Bit gesetzt = Ecke ist Weg): TL=8, TR=4, BL=2, BR=1
- Zeile 1: Gras/Wasser, Index = Eckmaske (Bit gesetzt = Ecke ist Wasser)
- Zeile 2: Gras-Varianten, Zeile 3: Weg-Varianten, Zeile 4: Wasser-Varianten
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

TERRAIN = Path(__file__).resolve().parent.parent / "vendor" / "eliza" / "Terrain"
T = 32
H = 16
TL, TR, BL, BR = 8, 4, 2, 1

# Kacheln im Frühlingsblatt, je Eckmaske der OBEREN Art (Bit = obere Art an dieser Ecke)
# Gras über transparentem Grund: Außenblob (0..2, 0..2), Innenecken 2x2 bei (0, 6)
GRASS_OVER = {
    0b0001: (0, 0), 0b0010: (2, 0), 0b0100: (0, 2), 0b1000: (2, 2),
    0b0011: (1, 0), 0b1100: (1, 2), 0b0101: (0, 1), 0b1010: (2, 1),
    0b1110: (0, 6), 0b1101: (1, 6), 0b1011: (0, 7), 0b0111: (1, 7),
    0b1111: (1, 1),
}
# Wasser in Gras (Grund eingebacken): See-Blob (0..2, 10..12), Innenecken = Insel 2x2 bei (0, 13)
WATER_IN = {
    0b0001: (0, 10), 0b0010: (2, 10), 0b0100: (0, 12), 0b1000: (2, 12),
    0b0011: (1, 10), 0b1100: (1, 12), 0b0101: (0, 11), 0b1010: (2, 11),
    0b1110: (0, 13), 0b1101: (1, 13), 0b1011: (0, 14), 0b0111: (1, 14),
    0b1111: (1, 11),
}
PLAIN = {
    "grass": [(3, 1), (4, 1), (5, 1), (3, 2), (4, 2), (5, 2)],
    "dirt": [(3, 3), (4, 3), (5, 3), (3, 4), (4, 4), (5, 4)],
    "water": [(12, 16), (13, 16), (14, 16), (15, 16), (12, 17), (13, 17)],
}
VARIANTS = 6


def sheet(season: str = "spring") -> Image.Image:
    # Originalfarben: Umfärben auf die 64er-Palette würde die Texturen einebnen
    return Image.open(TERRAIN / f"terrain_{season}.png").convert("RGBA")


def _tile(sh: Image.Image, xy: tuple[int, int]) -> Image.Image:
    x, y = xy
    return sh.crop((x * T, y * T, (x + 1) * T, (y + 1) * T))


def plain(sh: Image.Image, kind: str, variant: int) -> Image.Image:
    return _tile(sh, PLAIN[kind][variant % len(PLAIN[kind])])


def _combo(sh: Image.Image, table: dict[int, tuple[int, int]], mask: int) -> Image.Image:
    """Kachel für eine Eckmaske; die zwei Diagonalfälle werden aus Vierteln zusammengesetzt."""
    if mask in table:
        return _tile(sh, table[mask])
    out = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    for bit, (qx, qy) in ((TL, (0, 0)), (TR, (H, 0)), (BL, (0, H)), (BR, (H, H))):
        src = _tile(sh, table[bit]) if mask & bit else None
        if src is None:
            continue
        out.paste(src.crop((qx, qy, qx + H, qy + H)), (qx, qy))
    return out


def atlas(season: str = "spring") -> Image.Image:
    sh = sheet(season)
    out = Image.new("RGBA", (16 * T, 5 * T), (0, 0, 0, 0))
    for m in range(16):
        # Zeile 0: Gras über Weg. Maske = Weg-Ecken -> Gras-Ecken = invertiert
        grass_bits = (~m) & 0b1111
        tile = plain(sh, "dirt", m).copy()
        if grass_bits:
            tile.alpha_composite(_combo(sh, GRASS_OVER, grass_bits))
        out.paste(tile, (m * T, 0))
        # Zeile 1: Wasser in Gras
        if m == 0:
            tile = plain(sh, "grass", 0)
        else:
            tile = plain(sh, "grass", 1).copy()
            tile.alpha_composite(_combo(sh, WATER_IN, m))
        out.paste(tile, (m * T, T))
    for i in range(VARIANTS):
        out.paste(plain(sh, "grass", i), (i * T, 2 * T))
        out.paste(plain(sh, "dirt", i), (i * T, 3 * T))
        out.paste(plain(sh, "water", i), (i * T, 4 * T))
    return out
