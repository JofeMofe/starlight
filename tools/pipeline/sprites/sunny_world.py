"""Welt-Grafiken aus „Sunnyside World“ (Daniel Diggle), 16-px-Kacheln.

Quelle: tools/pipeline/vendor/sunnyside (wird von fetch_vendor.py geladen, nicht
im Repository). Hier entstehen daraus:

- ein Dual-Grid-Bodenatlas (Gras/Weg/Wasser, 16 Eckmasken je Übergang). Die
  Übergänge werden im Sunnyside-Stil gerendert: gerade Kanten mit 45°-Fasen,
  dunkelgrüne Graskante, zweireihiger Schattensaum auf dem Weg. Füllflächen sind
  Original-Kacheln aus dem Tileset.
- Zaunkacheln für alle 16 Nachbarmasken, zusammengesetzt aus Pfosten und Latten.
- Objekte (Bäume mit Wind-Animation, Büsche, Steine, Blumen, Pilz-Feenring).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

SRC = Path(__file__).resolve().parent.parent / "vendor/sunnyside/Sunnyside_World_ASSET_PACK_V2.1/Sunnyside_World_Assets"
T = 16
H = T // 2
TL, TR, BL, BR = 8, 4, 2, 1
N, E, S, W = 1, 2, 4, 8
CHAMFER = 3

GRASS_TILES = [(2, 1), (2, 2), (3, 2), (5, 2), (2, 3), (6, 2)]  # erste = schlicht, Rest mit Tupfen
DIRT_TILES = [(1, 7), (9, 7), (10, 7), (11, 7), (9, 8), (10, 8)]
WATER_TILES = [(30, 8), (31, 8), (32, 8), (33, 8), (30, 8), (32, 8)]
GRASS_EDGE = (79, 167, 72, 255)    # dunkle Graskante zum Weg
PATH_SHADE = (188, 121, 92, 255)   # Schattensaum auf dem Weg
WATER_EDGE = (77, 167, 111, 255)   # Graskante zum Wasser
VARIANTS = 6


def available() -> bool:
    return (SRC / "Tileset/spr_tileset_sunnysideworld_16px.png").exists()


def _sheet() -> Image.Image:
    return Image.open(SRC / "Tileset/spr_tileset_sunnysideworld_16px.png").convert("RGBA")


def tile(sh: Image.Image, xy: tuple[int, int], w: int = 1, h: int = 1) -> Image.Image:
    x, y = xy
    return sh.crop((x * T, y * T, (x + w) * T, (y + h) * T))


def element(rel: str) -> Image.Image:
    return Image.open(SRC / rel).convert("RGBA")


def strip_frames(rel: str, count: int) -> list[Image.Image]:
    im = element(rel)
    fw = im.size[0] // count
    return [im.crop((i * fw, 0, (i + 1) * fw, im.size[1])) for i in range(count)]


# --- Boden -------------------------------------------------------------------

def _mask_pixels(mask: int) -> np.ndarray:
    """Pixel, die zur oberen Geländeart gehören (Quadranten je Ecke, Fasen an der Mitte)."""
    inside = np.zeros((T, T), bool)
    quad = {TL: (0, 0), TR: (H, 0), BL: (0, H), BR: (H, H)}
    for bit, (qx, qy) in quad.items():
        if mask & bit:
            inside[qy:qy + H, qx:qx + H] = True
    # Abstand jedes Quadranten-Pixels zur Kachelmitte (Ecke an der Mitte)
    horiz = {TL: TR, TR: TL, BL: BR, BR: BL}
    vert = {TL: BL, BL: TL, TR: BR, BR: TR}
    for bit, (qx, qy) in quad.items():
        for y in range(qy, qy + H):
            for x in range(qx, qx + H):
                dx = (H - 1 - x) if qx == 0 else (x - H)
                dy = (H - 1 - y) if qy == 0 else (y - H)
                near = dx + dy  # 0 = Pixel direkt an der Mitte
                h_in, v_in = bool(mask & horiz[bit]), bool(mask & vert[bit])
                if mask & bit and not h_in and not v_in and near < CHAMFER:
                    inside[y, x] = False   # konvexe Ecke abfasen
                if not mask & bit and h_in and v_in and near < CHAMFER:
                    inside[y, x] = True    # konkave Ecke auffüllen
    return inside


def _neighbors(m: np.ndarray, x: int, y: int, diag: bool = True) -> list[bool]:
    out = []
    steps = ((1, 0), (-1, 0), (0, 1), (0, -1)) + (((1, 1), (-1, 1), (1, -1), (-1, -1)) if diag else ())
    for dx, dy in steps:
        xx, yy = min(max(x + dx, 0), T - 1), min(max(y + dy, 0), T - 1)
        out.append(bool(m[yy, xx]))
    return out


def _transition(base: Image.Image, top: Image.Image, mask: int, kind: str) -> Image.Image:
    inside = _mask_pixels(mask)
    b = np.array(base)
    t = np.array(top)
    out = b.copy()
    for y in range(T):
        for x in range(T):
            if inside[y, x]:
                out[y, x] = t[y, x]
                if kind == "path":
                    near = _neighbors(~inside, x, y, diag=False)
                    far = any(any(_neighbors(~inside, min(max(x + dx, 0), T - 1), min(max(y + dy, 0), T - 1), diag=False))
                              for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                    if any(near) or far:
                        out[y, x] = PATH_SHADE
            elif any(_neighbors(inside, x, y)):
                out[y, x] = GRASS_EDGE if kind == "path" else WATER_EDGE
    return Image.fromarray(out)


def ground_atlas() -> Image.Image:
    """16 Spalten: Zeile 0 Weg-Übergänge, 1 Wasser-Übergänge, 2 Gras, 3 Weg, 4 Wasser (Füllungen)."""
    sh = _sheet()
    grass = [tile(sh, g) for g in GRASS_TILES]
    dirt = [tile(sh, d) for d in DIRT_TILES]
    water = [tile(sh, w) for w in WATER_TILES]
    atlas = Image.new("RGBA", (16 * T, 5 * T), (0, 0, 0, 0))
    for m in range(16):
        g = grass[0]
        atlas.paste(_transition(g, dirt[m % len(dirt)], m, "path") if m else g, (m * T, 0))
        atlas.paste(_transition(g, water[m % len(water)], m, "water") if m else g, (m * T, T))
    for i in range(VARIANTS):
        atlas.paste(grass[i], (i * T, 2 * T))
        atlas.paste(dirt[i], (i * T, 3 * T))
        atlas.paste(water[i], (i * T, 4 * T))
    return atlas


def logic_atlas() -> Image.Image:
    """Rasterebene (trägt Kollisionen): Zeile 0 Gras, 1 Weg, 2 Wasser (je 16), 3 Zaun (16 Masken)."""
    sh = _sheet()
    atlas = Image.new("RGBA", (16 * T, 4 * T), (0, 0, 0, 0))
    grass = tile(sh, GRASS_TILES[0])
    for i in range(16):
        atlas.paste(grass, (i * T, 0))
        atlas.paste(tile(sh, DIRT_TILES[0]), (i * T, T))
        atlas.paste(tile(sh, WATER_TILES[0]), (i * T, 2 * T))
        atlas.paste(fence(sh, i), (i * T, 3 * T))
    return atlas


def fence(sh: Image.Image, mask: int) -> Image.Image:
    """Zaunkachel: Pfosten in der Mitte, Latten zu verbundenen Nachbarn (N1 O2 S4 W8)."""
    post = tile(sh, (41, 3))
    horiz = tile(sh, (39, 2))
    vert = tile(sh, (40, 3))
    out = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    if mask & W:
        out.alpha_composite(horiz.crop((0, 0, 6, T)), (0, 0))
    if mask & E:
        out.alpha_composite(horiz.crop((10, 0, T, T)), (10, 0))
    if mask & N:
        out.alpha_composite(vert.crop((0, 0, T, 3)), (0, 0))
    out.alpha_composite(post)
    if mask & S:
        out.alpha_composite(vert.crop((0, 12, T, T)), (0, 12))
    return out


# --- Objekte -----------------------------------------------------------------

def _trim(im: Image.Image) -> Image.Image:
    return im.crop(im.getbbox())


def pad_grid(im: Image.Image, grid: int = 16) -> Image.Image:
    """Auf ein Vielfaches des Rasters auffüllen, unten bündig und mittig."""
    w = -(-im.size[0] // grid) * grid
    h = -(-im.size[1] // grid) * grid
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.alpha_composite(im, ((w - im.size[0]) // 2, h - im.size[1]))
    return out


def tree_frames() -> list[Image.Image]:
    return [pad_grid(f) for f in strip_frames("Elements/Plants/spr_deco_tree_01_strip4.png", 4)]


def pine_frames() -> list[Image.Image]:
    return [pad_grid(f) for f in strip_frames("Elements/Plants/spr_deco_tree_02_strip4.png", 4)]


def objects() -> dict[str, Image.Image]:
    sh = _sheet()
    out: dict[str, Image.Image] = {}
    out["bush"] = pad_grid(_trim(tile(sh, (49, 1), 2, 2)))
    out["berry_bush"] = pad_grid(_trim(tile(sh, (49, 3), 2, 2)))
    out["rock"] = pad_grid(_trim(tile(sh, (31, 4))))
    out["pebbles"] = pad_grid(_trim(tile(sh, (34, 4))))
    out["tall_grass"] = pad_grid(_trim(tile(sh, (29, 2))))
    out["stump"] = pad_grid(_trim(tile(sh, (31, 5))))
    flowers = Image.new("RGBA", (T, T), (0, 0, 0, 0))
    for xy in ((32, 1), (32, 2), (32, 3)):
        flowers.alpha_composite(tile(sh, xy))
    out["flowers"] = flowers
    out["fairy_ring"] = fairy_ring()
    return out


def fairy_ring() -> Image.Image:
    """Ring aus roten und blauen Pilzen (Sunnyside-Pilze), 48x32."""
    red = _trim(strip_frames("Elements/Plants/spr_deco_mushroom_red_01_strip4.png", 4)[0])
    blue = _trim(strip_frames("Elements/Plants/spr_deco_mushroom_blue_03_strip4.png", 4)[0])
    blue_big = _trim(strip_frames("Elements/Plants/spr_deco_mushroom_blue_01_strip4.png", 4)[0])
    ring = Image.new("RGBA", (48, 32), (0, 0, 0, 0))
    import math
    spots = 9
    placed = []
    for i in range(spots):
        a = math.tau * i / spots + 0.3
        x = 24 + math.cos(a) * 18
        y = 17 + math.sin(a) * 9
        placed.append((y, x, [red, blue, blue_big][i % 3]))
    for y, x, m in sorted(placed):  # hinten zuerst
        ring.alpha_composite(m, (int(round(x - m.size[0] / 2)), int(round(y - m.size[1] + 4))))
    return ring
