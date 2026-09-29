"""Welt-Objekte aus dem LPC-Geländeset von ElizaWy (vendor/eliza/Terrain), Originalfarben.

Jedes Objekt ist ein Ausschnitt (Pixelrechteck) aus einem Vorlagenblatt. Der
Feenring wird aus kleinen Pilzen der Vorlage zu einem Kreis gelegt.
"""
from __future__ import annotations

import math

from PIL import Image

from sprites.lpc_terrain import TERRAIN

# Name -> (Blatt, Ausschnitt x0, y0, x1, y1)
CROPS: dict[str, tuple[str, tuple[int, int, int, int]]] = {
    "tree": ("trees_spring.png", (129, 16, 223, 109)),
    "tree_blossom": ("trees_spring.png", (129, 144, 223, 237)),
    "bush": ("plants_spring.png", (0, 0, 32, 32)),
    "flowers": ("flowers.png", (4, 70, 27, 90)),
    "tall_grass": ("plants_spring.png", (263, 23, 285, 51)),
    "rock": ("Rocks, Grasslands.png", (129, 71, 158, 95)),
    "pebbles": ("Rocks, Grasslands.png", (163, 77, 190, 91)),
}
MUSHROOM = ("mushrooms.png", (13, 144, 20, 153))


def crop(name: str) -> Image.Image:
    """Ausschnitt auf ein 32er-Raster aufgefüllt: waagrecht mittig, unten bündig
    (Fußpunkt = Unterkante, zentrierte Sprites landen auf ganzen Pixeln)."""
    sheet, box = CROPS[name]
    img = Image.open(TERRAIN / sheet).convert("RGBA").crop(box)
    w, h = -(-img.width // 32) * 32, -(-img.height // 32) * 32
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.alpha_composite(img, ((w - img.width) // 2, h - img.height))
    return _hard_alpha(out)


def _hard_alpha(img: Image.Image) -> Image.Image:
    """Binäres Alpha (Styleguide): weiche Kantenpixel werden voll deckend oder entfallen."""
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if 0 < a < 255:
                px[x, y] = (r, g, b, 255) if a >= 128 else (0, 0, 0, 0)
    return img


def fairy_ring(w: int = 64, h: int = 32, count: int = 11) -> Image.Image:
    sheet, box = MUSHROOM
    m = Image.open(TERRAIN / sheet).convert("RGBA").crop(box)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    spots = []
    for i in range(count):
        a = 2 * math.pi * i / count + 0.3
        x = round(w / 2 + math.cos(a) * (w / 2 - 6) - m.width / 2)
        y = round(h / 2 + math.sin(a) * (h / 2 - 7) - m.height / 2)
        spots.append((y, x))
    for y, x in sorted(spots):          # von hinten nach vorn zeichnen
        img = m if (x + y) % 3 else m.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        out.alpha_composite(img, (x, y))
    return _hard_alpha(out)
