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


def path_edge_demo(mask_n: bool, mask_s: bool, base_grass: Image.Image, seed: int) -> Image.Image:
    """Weg mit Grasrand oben/unten: Gras hängt in Büscheln über die Kante,
    darunter ein dunklerer Erdsaum (Tiefe statt harter Linie)."""
    rng = random.Random(seed)
    img = path_tile(seed)
    px = img.load()
    gpx = base_grass.load()
    for x in range(T):
        wob = int(round(1.2 * math.sin(x * 0.7 + seed) + 0.8 * math.sin(x * 1.9 + seed)))
        if not mask_n:
            edge = 5 + wob
            for y in range(0, edge):
                px[x, y] = gpx[x, y]
            px[x, edge] = color("moss", 3)
            px[x, edge + 1] = color("bark", 3)
            if rng.random() < 0.25:
                px[x, edge + 1] = color("moss", 3)
        if not mask_s:
            edge = T - 6 + wob
            px[x, edge - 1] = color("bark", 4)
            for y in range(edge, T):
                px[x, y] = gpx[x, y]
            px[x, edge] = color("moss", 5)
    return img


LEAVES = {
    "leaf": Material(color("moss", 0), color("moss", 2), color("moss", 3), color("moss", 5)),
    "leaf_mid": Material(color("moss", 0), color("moss", 3), color("moss", 4), color("moss", 5)),
    "leaf_hi": Material(color("moss", 0), color("moss", 4), color("moss", 5), color("moss", 6)),
    "leaf_spark": Material(color("moss", 0), color("moss", 6), color("moss", 6), color("moss", 7)),
    "trunk": Material(color("bark", 0), color("bark", 1), color("bark", 2), color("bark", 3)),
    "trunk_hi": Material(color("bark", 0), color("bark", 2), color("bark", 3), color("bark", 4)),
}


def tree() -> Image.Image:
    """Laubbaum 64x96 aus 13 Blattballen (hinten -> vorn), Stamm mit Wurzeln."""
    rng = random.Random(17)
    rig = Rig(64, 96)
    g = 0
    # Stamm mit Wurzelansatz und Rinde
    rig.capsule("trunk", g, 32, 93, 32, 58, 5.2, 3.6)
    rig.ellipse("trunk", g, 32, 92, 9, 2.8)
    rig.capsule("trunk", g, 27, 93, 23, 95, 2.0, 1.2)
    rig.capsule("trunk", g, 37, 93, 42, 95, 2.0, 1.2)
    rig.capsule("trunk_hi", g, 30, 90, 30, 64, 1.1, 0.8)      # Lichtkante links
    rig.capsule("trunk", g, 32, 66, 21, 54, 2.2, 1.4)          # Äste
    rig.capsule("trunk", g, 33, 63, 44, 52, 2.2, 1.4)
    # Blattballen: (cx, cy, r) von hinten nach vorn
    clumps = [
        (32, 22, 14), (19, 30, 11), (45, 30, 11), (26, 13, 10), (40, 14, 10),
        (13, 42, 10), (51, 42, 10), (22, 47, 11), (42, 47, 11), (32, 36, 13),
        (17, 25, 7), (47, 24, 7), (32, 52, 9),
    ]
    for i, (cx, cy, r) in enumerate(clumps):
        g = i + 1
        rig.ellipse("leaf", g, cx, cy, r, r * 0.88)
        rig.ellipse("leaf_mid", g, cx - r * 0.18, cy - r * 0.18, r * 0.72, r * 0.62)
        rig.ellipse("leaf_hi", g, cx - r * 0.38, cy - r * 0.42, r * 0.38, r * 0.3)
        # einzelne Lichtblätter
        for _ in range(2):
            a = rng.uniform(math.pi * 1.0, math.pi * 1.5)
            d = rng.uniform(0.35, 0.7) * r
            rig.pixels("leaf_spark", g, [(int(cx + math.cos(a) * d), int(cy + math.sin(a) * d))])
    return render(rig, LEAVES)


def flowers() -> Image.Image:
    """Blumeninsel 32x32: Glockenblumen, Gänseblümchen, Mohn, mit Stielen und Blättern."""
    img = Image.new("RGBA", (T, T), TRANSPARENT)
    px = img.load()
    rng = random.Random(9)
    kinds = [
        ([("fae", 3), ("fae", 4)], ("fae", 1)),     # Glockenblume
        ([("dusk", 6), ("dusk", 6)], ("ember", 3)),  # Gänseblümchen
        ([("rose", 3), ("rose", 4)], ("rose", 0)),   # Mohn
        ([("ember", 4), ("ember", 5)], ("ember", 2)),  # Butterblume
    ]
    spots = [(7, 12), (15, 9), (23, 13), (11, 20), (20, 21), (26, 24), (5, 25)]
    for i, (x, y) in enumerate(spots):
        petals, center = kinds[i % len(kinds)]
        for dy in range(1, 5):
            px[x, y + dy] = color("moss", 3 if dy > 1 else 2)
        px[x + 1, y + 3] = color("moss", 5)
        px[x - 1, y + 4] = color("moss", 4)
        for dx, dy in ((-1, 0), (1, 0), (0, -1)):
            px[x + dx, y + dy] = color(*petals[0])
        px[x, y + 1] = color(*petals[1]) if rng.random() < 0.5 else color(*petals[0])
        px[x - 1, y - 1] = color(*petals[1])
        px[x, y] = color(*center)
    return img


def _leaf_texture(img: Image.Image, seed: int) -> Image.Image:
    """Legt Blattstruktur auf die Laubflächen: kleine gebogene Blattformen
    in der nächstdunkleren Stufe (Schattenseite) bzw. Lichtflecken (oben)."""
    rng = random.Random(seed)
    px = img.load()
    w, h = img.size
    ramp = [color("moss", i) for i in range(8)]
    idx = {c: i for i, c in enumerate(ramp)}
    leaf_shapes = [[(0, 0), (1, 1), (2, 1)], [(0, 1), (1, 0), (2, 0)], [(0, 0), (1, 0), (1, 1)]]
    for y in range(1, h - 2, 3):
        for x in range(1 + (y // 3) % 2 * 2, w - 3, 4):
            jx, jy = x + rng.randint(-1, 1), y + rng.randint(-1, 1)
            if not (0 <= jx < w - 3 and 0 <= jy < h - 2):
                continue
            base = px[jx, jy]
            if base not in idx or idx[base] < 2 or idx[base] > 6:
                continue
            level = idx[base]
            shape = rng.choice(leaf_shapes)
            # im Licht eher helle Tupfer, im Schatten dunkle Blattkanten
            delta = -1 if level <= 3 or rng.random() < 0.55 else 1
            new = ramp[max(1, min(7, level + delta))]
            for dx, dy in shape:
                if px[jx + dx, jy + dy] == base:
                    px[jx + dx, jy + dy] = new
    return img


def tree_textured() -> Image.Image:
    return _leaf_texture(tree().copy(), 23)


def tall_grass(seed: int) -> Image.Image:
    """16x16 hohes Grasbüschel: 9 gebogene Halme, hinten dunkel, vorn hell,
    Spitzen mit Licht – gut sichtbar gegen die Wiese."""
    rng = random.Random(seed)
    img = Image.new("RGBA", (16, 16), TRANSPARENT)
    px = img.load()
    blades = sorted([(rng.uniform(2, 13), rng.uniform(7, 14), rng.uniform(-3.5, 3.5)) for _ in range(9)],
                    key=lambda b: b[1])
    for i, (bx, height, lean) in enumerate(blades):
        shade = 2 if i < 3 else (3 if i < 6 else 5)
        for s_ in range(int(height)):
            t = s_ / height
            x = int(round(bx + lean * t * t))
            y = 15 - s_
            if 0 <= x < 16 and 0 <= y < 16:
                tip = s_ >= height - 2
                px[x, y] = color("moss", min(7, shade + (2 if tip else 0)))
                if s_ < 3 and 0 <= x + 1 < 16 and i >= 6:
                    px[x + 1, y] = color("moss", 3)
    return img


def pebble_cluster(seed: int) -> Image.Image:
    rng = random.Random(seed)
    img = Image.new("RGBA", (16, 16), TRANSPARENT)
    px = img.load()
    for _ in range(3):
        x, y = rng.randint(2, 11), rng.randint(6, 12)
        w = rng.choice([2, 3])
        for dx in range(w):
            px[x + dx, y] = color("stone", 4)
            px[x + dx, y + 1] = color("stone", 3)
            px[x + dx, y + 2] = color("moss", 3)
        px[x, y] = color("stone", 5)
    return img
