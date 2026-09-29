"""Mooswiesen v2 – Qualitäts-Durchgang für Gras, Weg, Baum und Blumen.

Statt Rauschen werden kleine, handgezeichnete Motive ("Stempel") gezielt
gesetzt: Halmbüschel als V-Formen mit Lichtspitze, Kleeblätter, Kiesel mit
Glanzpunkt. Der Baum besteht aus einzelnen Blattballen, jeder mit eigener
Kontur, Lichtkappe oben links und Schattenseite, von hinten nach vorn
geschichtet – so entsteht die typische, "gezeichnete" Laubstruktur.
"""
from __future__ import annotations

import math
import random

from PIL import Image

from palette import color
from sl_common import TRANSPARENT
from sprites.rig import Material, Rig, render

T = 32

# Stempel: (dx, dy, Farbe) relativ zum Anker
TUFT_V = [(0, 0, ("moss", 3)), (1, 1, ("moss", 3)), (2, 0, ("moss", 3))]
TUFT_TALL = [(0, 1, ("moss", 3)), (1, 2, ("moss", 3)), (1, 1, ("moss", 3)), (2, 0, ("moss", 3)),
             (3, 1, ("moss", 3)), (1, 0, ("moss", 5)), (2, -1, ("moss", 6))]
TUFT_LIT = [(0, 0, ("moss", 5)), (1, 1, ("moss", 3)), (2, 0, ("moss", 5)), (1, 0, ("moss", 6))]
CLOVER = [(0, 0, ("moss", 5)), (1, 0, ("moss", 5)), (0, 1, ("moss", 5)), (1, 1, ("moss", 3)),
          (-1, 1, ("moss", 5)), (0, 2, ("moss", 3)), (0, -1, ("moss", 6))]
SPECK = [(0, 0, ("moss", 5))]
DARK_SPECK = [(0, 0, ("moss", 3))]


def _stamp(px, stamp: list, x: int, y: int) -> None:
    for dx, dy, (ramp, step) in stamp:
        px[(x + dx) % T, (y + dy) % T] = color(ramp, step)


def grass_tile(variant: int) -> Image.Image:
    """Sonnige Wiese: Grundton moss4, darin verteilte Büschel und Klee.
    Positionen per Seed, aber mit Mindestabstand (kein Klumpen, kein Rauschen)."""
    rng = random.Random(4200 + variant)
    img = Image.new("RGBA", (T, T), color("moss", 4))
    px = img.load()
    placed: list[tuple[int, int]] = []

    def free(x: int, y: int, d: int) -> bool:
        for px_, py_ in placed:
            ddx = min(abs(x - px_), T - abs(x - px_))
            ddy = min(abs(y - py_), T - abs(y - py_))
            if ddx < d and ddy < d:
                return False
        return True

    plan = [(TUFT_V, 7), (TUFT_LIT, 4), (DARK_SPECK, 6), (SPECK, 6)]
    if variant == 1:
        plan.append((TUFT_TALL, 2))
    if variant == 2:
        plan.append((CLOVER, 3))
    if variant == 3:
        plan.append((TUFT_TALL, 1))
        plan.append((CLOVER, 1))
    for stamp, count in plan:
        tries = 0
        while count > 0 and tries < 400:
            tries += 1
            x, y = rng.randrange(T), rng.randrange(T)
            if free(x, y, 5 if len(stamp) > 1 else 3):
                _stamp(px, stamp, x, y)
                placed.append((x, y))
                count -= 1
    return img


def path_tile(seed: int) -> Image.Image:
    """Sandiger Weg: Grundton bark5, feine dunklere Körnung, Kiesel mit Licht oben links."""
    rng = random.Random(seed)
    img = Image.new("RGBA", (T, T), color("bark", 5))
    px = img.load()
    for _ in range(26):
        x, y = rng.randrange(T), rng.randrange(T)
        px[x, y] = color("bark", 4)
    for _ in range(10):
        x, y = rng.randrange(T), rng.randrange(T)
        px[x, y] = color("bark", 6)
    for _ in range(4):
        x, y = rng.randrange(1, T - 2), rng.randrange(1, T - 2)
        big = rng.random() < 0.5
        cells = [(0, 0), (1, 0), (0, 1), (1, 1)] if big else [(0, 0), (1, 0)]
        for dx, dy in cells:
            px[x + dx, y + dy] = color("stone", 4)
        px[x, y] = color("stone", 5)
        for dx, dy in cells:
            if (dx, dy + 1) not in cells:
                px[x + dx, y + dy + 1] = color("bark", 3)  # Schlagschatten unten
    return img


LEAVES = {
    "leaf": Material(color("moss", 0), color("moss", 2), color("moss", 3), color("moss", 5)),
    "leaf_mid": Material(color("moss", 0), color("moss", 3), color("moss", 4), color("moss", 5)),
    "leaf_hi": Material(color("moss", 0), color("moss", 4), color("moss", 5), color("moss", 6)),
    "leaf_spark": Material(color("moss", 0), color("moss", 6), color("moss", 6), color("moss", 7)),
    "trunk": Material(color("bark", 0), color("bark", 1), color("bark", 2), color("bark", 3)),
    "trunk_hi": Material(color("bark", 0), color("bark", 2), color("bark", 3), color("bark", 4)),
}


