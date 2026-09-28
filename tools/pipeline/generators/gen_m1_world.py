"""M1-Welt-Platzhalter in Palette: Wiesen-Tiles (Gras, Weg, Wasser mit
eigenen Kanten-Varianten), Zaun (16 Verbindungsvarianten), Objekte (Baum,
Busch, Stein, Blumen, Feenring), Effekte (Funkeln, Herz, Staub, Blitz) und
Schatten. Alles reproduzierbar mit festem Seed.

Kanten-Varianten: Index = Bitmaske der gleichartigen Nachbarn
N=1, O=2, S=4, W=8 (so wählt der MapBuilder im Spiel die passende Kachel).
"""
from __future__ import annotations

import math
import random

from PIL import Image

from palette import color
from sl_common import ASSETS, TRANSPARENT, GeneratedAsset, save_png
from sprites import meadow_v2 as M2
from sprites.rig import Material, Rig, render

GEN = "tools/pipeline/generators/gen_m1_world.py"
T = 32
N, E, S, W = 1, 2, 4, 8


def _grass(seed: int, kind: int) -> Image.Image:
    rng = random.Random(seed)
    img = Image.new("RGBA", (T, T), color("moss", 3))
    px = img.load()
    for _ in range(10):
        cx, cy = rng.randrange(T), rng.randrange(T)
        c = color("moss", 2) if rng.random() < 0.4 else color("moss", 4)
        for dx, dy in ((0, 0), (1, 0), (0, 1)):
            px[(cx + dx) % T, (cy + dy) % T] = c
    for _ in range(4 if kind == 1 else 2):
        cx, cy = rng.randrange(2, T - 2), rng.randrange(3, T)
        for dx in (-1, 0, 1):
            px[(cx + dx) % T, (cy - 1) % T] = color("moss", 2)
            px[(cx + dx) % T, (cy - 2 - (dx == 0)) % T] = color("moss", 5)
    if kind == 2:  # Wiesenblumen
        for _ in range(4):
            cx, cy = rng.randrange(1, T - 1), rng.randrange(1, T - 1)
            petal = rng.choice([color("rose", 6), color("dusk", 6), color("ember", 4), color("fae", 4)])
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                px[cx + dx, cy + dy] = petal
            px[cx, cy] = color("ember", 3)
    if kind == 3:  # Klee
        for _ in range(5):
            cx, cy = rng.randrange(1, T - 2), rng.randrange(1, T - 2)
            for dx, dy in ((0, 0), (1, 0), (0, 1), (1, 1)):
                px[cx + dx, cy + dy] = color("moss", 5)
            px[cx, cy] = color("moss", 6)
    return img


def _edge_tile(mask: int, seed: int, inner: tuple, inner_dark: tuple, inner_light: tuple,
               rim: tuple, rim_dark: tuple, speckle: float, base_grass: Image.Image) -> Image.Image:
    """Innenfläche (Weg/Wasser) mit weichem, unregelmäßigem Rand zu Gras,
    wo der Nachbar nicht gleichartig ist."""
    rng = random.Random(seed * 31 + mask)
    img = base_grass.copy()
    px = img.load()
    inset = 4

    def inside(x: int, y: int) -> float:
        # Abstand zum Rand der Fläche (negativ = außerhalb)
        d = 99.0
        wob = lambda v: 1.0 * math.sin(v * 0.9 + seed) + 0.6 * math.sin(v * 2.3 + seed * 2)
        if not mask & N:
            d = min(d, y - inset - wob(x))
        if not mask & S:
            d = min(d, (T - 1 - y) - inset - wob(x + 7))
        if not mask & W:
            d = min(d, x - inset - wob(y + 3))
        if not mask & E:
            d = min(d, (T - 1 - x) - inset - wob(y + 11))
        return d

    for y in range(T):
        for x in range(T):
            d = inside(x, y)
            if d < 0:
                continue
            if d < 1.0:
                px[x, y] = rim_dark
            elif d < 2.0:
                px[x, y] = rim
            else:
                r = rng.random()
                px[x, y] = inner_dark if r < speckle else (inner_light if r > 1 - speckle * 0.6 else inner)
    return img


def _edge_textured(mask: int, seed: int, inner: Image.Image, fringe: tuple, shade: tuple,
                   base_grass: Image.Image, inset: int = 4) -> Image.Image:
    """Wie _edge_tile, aber die Innenfläche ist eine Textur (Weg/Wasser v2).
    Am offenen Rand hängt ein Saum (fringe) über, innen eine Schattenlinie."""
    img = base_grass.copy()
    px = img.load()
    ipx = inner.load()

    def inside(x: int, y: int) -> float:
        d = 99.0
        wob = lambda v: 1.0 * math.sin(v * 0.9 + seed) + 0.6 * math.sin(v * 2.3 + seed * 2)
        if not mask & N:
            d = min(d, y - inset - wob(x))
        if not mask & S:
            d = min(d, (T - 1 - y) - inset - wob(x + 7))
        if not mask & W:
            d = min(d, x - inset - wob(y + 3))
        if not mask & E:
            d = min(d, (T - 1 - x) - inset - wob(y + 11))
        return d

    for y in range(T):
        for x in range(T):
            d = inside(x, y)
            if d < 0:
                continue
            if d < 1.0:
                px[x, y] = fringe
            elif d < 2.0:
                px[x, y] = shade
            else:
                px[x, y] = ipx[x, y]
    return img


def _water_inner(seed: int) -> Image.Image:
    rng = random.Random(seed)
    img = Image.new("RGBA", (T, T), color("sky", 3))
    px = img.load()
    for _ in range(40):
        x, y = rng.randrange(T), rng.randrange(T)
        px[x, y] = color("sky", 2)
    for _ in range(3):
        x, y = rng.randrange(T - 3), rng.randrange(T)
        for dx in range(3):
            px[x + dx, y] = color("sky", 4)
        px[x + 1, y] = color("sky", 5)
    return img


def _fence(mask: int) -> Image.Image:
    img = Image.new("RGBA", (T, T), TRANSPARENT)
    px = img.load()
    wood_o, wood_s, wood_b, wood_l = color("bark", 1), color("bark", 2), color("bark", 3), color("bark", 4)

    def rect(x0: int, y0: int, x1: int, y1: int, fill: tuple) -> None:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                px[x, y] = fill

    # Querlatten (horizontal) zu O/W-Nachbarn
    for ry in (14, 21):
        x0 = 0 if mask & W else 13
        x1 = T - 1 if mask & E else 18
        if x0 < x1:
            rect(x0, ry - 1, x1, ry + 1, wood_o)
            rect(x0, ry, x1, ry, wood_b)
            rect(x0, ry - 1 + 1, x1, ry - 1 + 1, wood_b)
            for x in range(x0, x1 + 1):
                px[x, ry - 1] = wood_l if 0 < x < T - 1 else wood_o
    # Längslatte (vertikal) zu N/S-Nachbarn: schmal, damit man von oben "durchsieht"
    if mask & (N | S):
        y0 = 0 if mask & N else 12
        y1 = T - 1 if mask & S else 24
        rect(14, y0, 17, y1, wood_o)
        rect(15, y0, 16, y1, wood_b)
        for y in range(y0, y1 + 1):
            px[15, y] = wood_l
    # Pfosten
    rect(12, 9, 19, 27, wood_o)
    rect(13, 10, 18, 26, wood_b)
    rect(13, 10, 14, 26, wood_l)
    rect(17, 10, 18, 26, wood_s)
    rect(13, 10, 18, 10, wood_l)
    return img


LEAF = {
    "leaf": Material(color("moss", 0), color("moss", 2), color("moss", 3), color("moss", 5)),
    "leaf_hi": Material(color("moss", 0), color("moss", 3), color("moss", 4), color("moss", 6)),
    "trunk": Material(color("bark", 0), color("bark", 1), color("bark", 2), color("bark", 3)),
    "berry": Material(color("rose", 0), color("rose", 2), color("rose", 3), color("rose", 5)),
    "stone": Material(color("dusk", 1), color("stone", 1), color("stone", 2), color("stone", 4)),
    "moss": Material(color("moss", 1), color("moss", 3), color("moss", 4), color("moss", 5)),
    "cap": Material(color("rose", 0), color("rose", 1), color("rose", 2), color("rose", 4)),
    "stem": Material(color("stone", 3), color("stone", 4), color("dusk", 6), color("dusk", 6)),
    "dot": Material(color("dusk", 6), color("dusk", 6), color("dusk", 6), color("dusk", 6)),
}


def tree() -> Image.Image:
    rng = random.Random(7)
    rig = Rig(64, 96)
    rig.capsule("trunk", 1, 32, 94, 32, 60, 5.5, 4.0)
    rig.capsule("trunk", 1, 32, 70, 22, 56, 2.5, 1.5)
    rig.capsule("trunk", 1, 33, 66, 43, 54, 2.5, 1.5)
    rig.ellipse("trunk", 1, 32, 93, 8, 2.5)                   # Wurzelansatz
    for cx, cy, rx, ry in ((32, 36, 26, 24), (18, 48, 12, 11), (46, 48, 13, 11), (32, 20, 18, 15),
                           (20, 28, 11, 10), (44, 28, 12, 11), (32, 54, 16, 9)):
        rig.ellipse("leaf", 2, cx, cy, rx, ry)
    for _ in range(9):
        cx, cy = rng.uniform(14, 46), rng.uniform(12, 44)
        rig.ellipse("leaf_hi", 2, cx - 3, cy - 2, rng.uniform(3, 5), rng.uniform(2, 3.5))
    return render(rig, LEAF)


def bush() -> Image.Image:
    rng = random.Random(11)
    rig = Rig(32, 32)
    for cx, cy, rx, ry in ((16, 20, 13, 10), (10, 16, 7, 7), (22, 15, 8, 7), (16, 12, 7, 6)):
        rig.ellipse("leaf", 1, cx, cy, rx, ry)
    for _ in range(5):
        rig.ellipse("leaf_hi", 1, rng.uniform(8, 22), rng.uniform(9, 20), 2.5, 1.8)
    for _ in range(4):
        x, y = rng.randint(7, 24), rng.randint(12, 25)
        rig.pixels("berry", 2, [(x, y)])
    return render(rig, LEAF)


def rock() -> Image.Image:
    rig = Rig(32, 32)
    rig.ellipse("stone", 1, 16, 21, 12, 8)
    rig.ellipse("stone", 1, 13, 17, 7, 6)
    rig.ellipse("moss", 2, 10, 14, 4, 2)
    return render(rig, LEAF)


def fairy_ring() -> Image.Image:
    """Pilzkreis (64x32): Ort für den Größenwechsel im frühen Spiel."""
    rig = Rig(64, 32)
    rng = random.Random(5)
    shrooms = []
    for i in range(11):
        a = i / 11 * 2 * math.pi + 0.2
        x = 32 + math.cos(a) * 25 + rng.uniform(-1, 1)
        y = 16 + math.sin(a) * 10 + rng.uniform(-0.5, 0.5)
        shrooms.append((y, x, rng.uniform(0.8, 1.2)))
    for y, x, s in sorted(shrooms):  # hintere zuerst
        rig.capsule("stem", 1, x, y + 1, x, y + 4 * s, 1.0, 1.1)
        rig.ellipse("cap", 2, x, y, 3.2 * s, 2.2 * s)
        rig.pixels("dot", 3, [(int(x) - 1, int(y) - 1), (int(x) + 1, int(y))])
    return render(rig, LEAF)


def flowers() -> Image.Image:
    img = Image.new("RGBA", (T, T), TRANSPARENT)
    px = img.load()
    rng = random.Random(3)
    for _ in range(6):
        x, y = rng.randint(4, 27), rng.randint(8, 27)
        for dy in range(1, 4):
            px[x, y + dy] = color("moss", 2)
        petal = rng.choice([color("rose", 6), color("fae", 4), color("ember", 4), color("dusk", 6)])
        for dx, dy in ((1, 0), (-1, 0), (0, -1), (0, 1)):
            px[x + dx, y + dy] = petal
        px[x, y] = color("ember", 3)
    return img


def shadow(w: int, h: int) -> Image.Image:
    """Einfarbige Schattenellipse; die Transparenz kommt im Spiel per Modulate."""
    img = Image.new("RGBA", (w, h), TRANSPARENT)
    px = img.load()
    for y in range(h):
        for x in range(w):
            if ((x + 0.5 - w / 2) / (w / 2)) ** 2 + ((y + 0.5 - h / 2) / (h / 2)) ** 2 <= 1.0:
                px[x, y] = color("dusk", 0)
    return img


def fx_sheet() -> Image.Image:
    """8x8-Effekte in einer Reihe: Funken klein, Funken groß, Herz, Staub, Punkt, Note."""
    img = Image.new("RGBA", (8 * 6, 8), TRANSPARENT)
    px = img.load()
    cream, gold, gold_d = color("dusk", 6), color("ember", 5), color("ember", 3)
    # 0: kleiner Funke
    for x, y, c in ((3, 3, cream), (3, 2, gold), (3, 4, gold), (2, 3, gold), (4, 3, gold)):
        px[x, y] = c
    # 1: großer Funke
    ox = 8
    for d in range(1, 4):
        c = gold if d < 3 else gold_d
        for x, y in ((3, 3 - d), (3, 3 + d), (3 - d, 3), (3 + d, 3)):
            px[ox + x, y] = c
    px[ox + 3, 3] = cream
    # 2: Herz
    ox = 16
    heart = ["........", ".##.##..", "#hh#rr#.", "#hrrrr#.", ".#rrr#..", "..#r#...", "...#....", "........"]
    for y, row in enumerate(heart):
        for x, ch in enumerate(row):
            if ch == "#":
                px[ox + x, y] = color("rose", 1)
            elif ch == "r":
                px[ox + x, y] = color("rose", 3)
            elif ch == "h":
                px[ox + x, y] = color("rose", 5)
    # 3: Staubwölkchen
    ox = 24
    dust = ["........", "..##....", ".#ll#...", "#llll##.", "#lllll#.", ".######.", "........", "........"]
    for y, row in enumerate(dust):
        for x, ch in enumerate(row):
            if ch == "#":
                px[ox + x, y] = color("bark", 5)
            elif ch == "l":
                px[ox + x, y] = color("bark", 7)
    # 4: Lichtpunkt (2x2)
    for x, y in ((3, 3), (4, 3), (3, 4), (4, 4)):
        px[32 + x, y] = cream
    # 5: Feenstaub (zart violett)
    for x, y, c in ((3, 3, color("fae", 4)), (3, 2, color("fae", 3)), (2, 3, color("fae", 3)),
                    (4, 3, color("fae", 3)), (3, 4, color("fae", 3))):
        px[40 + x, y] = c
    return img


def flash() -> Image.Image:
    """32x32 Lichtblitz der Verwandlung (Sternform, cremig mit Goldrand)."""
    img = Image.new("RGBA", (T, T), TRANSPARENT)
    px = img.load()
    c = 15.5
    for y in range(T):
        for x in range(T):
            dx, dy = abs(x - c), abs(y - c)
            v = dx ** 0.5 + dy ** 0.5
            d = (dx * dx + dy * dy) ** 0.5
            if v <= 2.3 or d <= 3.5:
                px[x, y] = color("dusk", 6)
            elif v <= 3.1 or d <= 5:
                px[x, y] = color("ember", 5)
            elif v <= 3.6:
                px[x, y] = color("ember", 4)
    return img


def ui_icons() -> Image.Image:
    """16x16-Symbole: 0 Feenglanz (Stern), 1 Flugenergie (Flügel)."""
    img = Image.new("RGBA", (32, 16), TRANSPARENT)
    img.alpha_composite(_small_star(), (0, 0))
    px = img.load()
    wing = [
        "................",
        "................",
        "..##............",
        ".#ww##..........",
        ".#wwww##....##..",
        "..#wwwww#..#ww#.",
        "...#wwwvv##wwww#",
        "....#wvvvvwwwww#",
        ".....#vvvvvwww#.",
        "......#vvvv##...",
        ".......#vv#.....",
        "........##......",
        "................",
        "................",
        "................",
        "................",
    ]
    for y, row in enumerate(wing):
        for x, ch in enumerate(row):
            if ch == "#":
                px[16 + x, y] = color("sky", 2)
            elif ch == "w":
                px[16 + x, y] = color("sky", 6)
            elif ch == "v":
                px[16 + x, y] = color("fae", 3)
    return img


def _small_star() -> Image.Image:
    img = Image.new("RGBA", (16, 16), TRANSPARENT)
    px = img.load()
    c = 7.5
    for y in range(16):
        for x in range(16):
            v = abs(x - c) ** 0.5 + abs(y - c) ** 0.5
            if v <= 1.3:
                px[x, y] = color("dusk", 6)
            elif v <= 2.1:
                px[x, y] = color("ember", 5)
            elif v <= 2.6:
                px[x, y] = color("ember", 3)
            elif v <= 2.9:
                px[x, y] = color("ember", 1)
    return img


def _pad32(img: Image.Image) -> Image.Image:
    """16x16-Deko auf 32x32 (Kachelraster), unten mittig."""
    out = Image.new("RGBA", (T, T), TRANSPARENT)
    out.alpha_composite(img, (8, 16))
    return out


def build() -> list[GeneratedAsset]:
    out: list[GeneratedAsset] = []
    tdir = ASSETS / "tilesets/mooswiesen"
    grass = [M2.grass_tile(k) for k in range(4)]
    # Atlas: Zeile 0 Gras (4), Zeile 1 Weg (16 Masken), Zeile 2 Wasser (16), Zeile 3 Zaun (16)
    atlas = Image.new("RGBA", (16 * T, 4 * T), TRANSPARENT)
    for k, g in enumerate(grass):
        atlas.alpha_composite(g, (k * T, 0))
    for m in range(16):
        path = _edge_textured(m, 3, M2.path_tile(300 + m), color("moss", 3), color("bark", 3), grass[m % 2])
        atlas.alpha_composite(path, (m * T, T))
        water = _edge_textured(m, 9, _water_inner(500 + m), color("lagoon", 3), color("sky", 4),
                               grass[(m + 1) % 2], inset=5)
        atlas.alpha_composite(water, (m * T, 2 * T))
        atlas.alpha_composite(_fence(m), (m * T, 3 * T))
    p = save_png(atlas, tdir / "meadow_tiles.png")
    out.append(GeneratedAsset(p, "tileset", GEN, "Gras(4), Weg/Wasser/Zaun je 16 Kantenmasken"))
    for name, img, note in (("tree", M2.tree_textured(), "Laubbaum 64x96, Blattballen mit Struktur"),
                            ("bush", M2._leaf_texture(bush().copy(), 5), "Busch 32x32"),
                            ("rock", rock(), "Stein 32x32"), ("flowers", M2.flowers(), "Blumeninsel 32x32"),
                            ("fairy_ring", fairy_ring(), "Feenring 64x32"),
                            ("tall_grass", _pad32(M2.tall_grass(1)), "Hohes Gras (Deko)"),
                            ("pebbles", _pad32(M2.pebble_cluster(2)), "Kiesel (Deko)")):
        p = save_png(img, tdir / f"{name}.png")
        out.append(GeneratedAsset(p, "tileset", GEN, note))
    fdir = ASSETS / "sprites/fx"
    for name, img, note in (("shadow_small", shadow(16, 8), "Schatten Fee/Hund"),
                            ("shadow_medium", shadow(24, 8), "Schatten Klio"),
                            ("shadow_large", shadow(48, 16), "Schatten Pferd"),
                            ("shadow_tree", shadow(56, 16), "Schatten Baum"),
                            ("fx_particles", fx_sheet(), "Partikel 8x8: Funke, Funke groß, Herz, Staub, Licht, Feenstaub"),
                            ("transform_flash", flash(), "Lichtblitz der Verwandlung")):
        p = save_png(img, fdir / f"{name}.png")
        out.append(GeneratedAsset(p, "sprite", GEN, note))
    p = save_png(ui_icons(), ASSETS / "sprites/ui/hud_icons.png")
    out.append(GeneratedAsset(p, "ui", GEN, "HUD-Symbole 16x16: Feenglanz, Flugenergie"))
    return out
