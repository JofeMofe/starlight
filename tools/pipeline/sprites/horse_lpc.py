"""Pferd aus dem LPC-Set von bluecarrot16 (vendor/lpc_horses), auf die Palette umgefärbt.

Gangarten im Spiel: Schritt = LPC-Schritt, Trab = LPC-Schritt schneller getaktet,
Galopp = LPC-Galopp. Stehen = eigene Stehpose je Richtung; im Stand wird ab und zu
gegrast (Fressen-Zeilen).
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image

from sprites.klio_lpc import recolor

SHEET = Path(__file__).resolve().parent.parent / "vendor" / "lpc_horses" / "horse.png"
FRAME = 128
# LPC-Richtungsreihenfolge je Block: oben, links, unten, rechts
DIR = {"up": 0, "side": 1, "down": 2}
GALLOP, WALK, STAND, EAT = 0, 4, 8, 9


def _sheet() -> Image.Image:
    im = recolor(Image.open(SHEET), {})
    px = im.load()
    # Einzelne verirrte Pixel ohne Nachbarn entfernen
    for y in range(im.height):
        for x in range(im.width):
            if px[x, y][3] and not any(
                    0 <= x + dx < im.width and 0 <= y + dy < im.height and px[x + dx, y + dy][3]
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1))):
                px[x, y] = (0, 0, 0, 0)
    return im


_CACHE: list[Image.Image] = []


def frame(block: int, view: str, col: int) -> Image.Image:
    if not _CACHE:
        _CACHE.append(_sheet())
    im = _CACHE[0]
    if block == STAND:
        row, col = STAND, DIR[view]
    else:
        row = block + DIR[view]
    return im.crop((col * FRAME, row * FRAME, (col + 1) * FRAME, (row + 1) * FRAME))
