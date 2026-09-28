"""Mini-Rig für Tier-Sprites: Körper aus Formen, automatisch schattiert und umrandet.

Ein Sprite besteht aus Teilen (Ellipsen, Kapseln, Polygonen) mit Material,
Gruppe und Tiefe. Das Rendering folgt den Styleguide-Regeln:
- Licht von oben links: 1 px Glanz an oberen/linken Kanten, Schattenband
  an unteren/rechten Kanten (pro Gruppe, damit Rumpf+Hals eine Form bilden)
- farbige Außenlinie (dunkelste Stufe des jeweiligen Materials)
- Trennlinie, wo eine vordere Gruppe eine hintere überdeckt
- kein Anti-Aliasing, binäres Alpha
"""
from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, field

import numpy as np
from PIL import Image

RGBA = tuple[int, int, int, int]
# Textur je Material: (x, y, Farbe, liegt_am_Materialrand) -> Farbe
Texture = Callable[[int, int, RGBA, bool], RGBA]


@dataclass
class Material:
    outline: RGBA
    shadow: RGBA
    base: RGBA
    light: RGBA


@dataclass
class Part:
    material: str
    group: int
    shape: str                      # "ellipse" | "capsule" | "poly" | "pixels"
    args: tuple
    shade: bool = True              # False: flache Farbe (z. B. Augen, Nüstern)


@dataclass
class Rig:
    width: int
    height: int
    parts: list[Part] = field(default_factory=list)

    def ellipse(self, mat: str, group: int, cx: float, cy: float, rx: float, ry: float,
                angle: float = 0.0, shade: bool = True) -> None:
        self.parts.append(Part(mat, group, "ellipse", (cx, cy, rx, ry, angle), shade))

    def capsule(self, mat: str, group: int, x0: float, y0: float, x1: float, y1: float,
                r0: float, r1: float | None = None, shade: bool = True) -> None:
        self.parts.append(Part(mat, group, "capsule", (x0, y0, x1, y1, r0, r0 if r1 is None else r1), shade))

    def poly(self, mat: str, group: int, points: list[tuple[float, float]], shade: bool = True) -> None:
        self.parts.append(Part(mat, group, "poly", (tuple(points),), shade))

    def pixels(self, mat: str, group: int, coords: list[tuple[int, int]]) -> None:
        self.parts.append(Part(mat, group, "pixels", (tuple(coords),), False))


def _mask(part: Part, w: int, h: int) -> np.ndarray:
    ys, xs = np.mgrid[0:h, 0:w]
    px, py = xs + 0.5, ys + 0.5
    if part.shape == "ellipse":
        cx, cy, rx, ry, ang = part.args
        c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        u = (px - cx) * c + (py - cy) * s
        v = -(px - cx) * s + (py - cy) * c
        return (u / rx) ** 2 + (v / ry) ** 2 <= 1.0
    if part.shape == "capsule":
        x0, y0, x1, y1, r0, r1 = part.args
        dx, dy = x1 - x0, y1 - y0
        ln2 = dx * dx + dy * dy
        t = np.clip(((px - x0) * dx + (py - y0) * dy) / ln2, 0.0, 1.0) if ln2 > 0 else np.zeros_like(px)
        qx, qy = x0 + t * dx, y0 + t * dy
        r = r0 + (r1 - r0) * t
        return (px - qx) ** 2 + (py - qy) ** 2 <= r * r
    if part.shape == "poly":
        (pts,) = part.args
        inside = np.zeros((h, w), dtype=bool)
        n = len(pts)
        for i in range(n):
            xa, ya = pts[i]
            xb, yb = pts[(i + 1) % n]
            cond = ((ya > py) != (yb > py))
            with np.errstate(divide="ignore", invalid="ignore"):
                xint = (xb - xa) * (py - ya) / (yb - ya) + xa
            inside ^= cond & (px < xint)
        return inside
    if part.shape == "pixels":
        (coords,) = part.args
        m = np.zeros((h, w), dtype=bool)
        for x, y in coords:
            if 0 <= x < w and 0 <= y < h:
                m[y, x] = True
        return m
    raise ValueError(part.shape)


def render(rig: Rig, materials: dict[str, Material], outline: bool = True,
           textures: dict[str, Texture] | None = None) -> Image.Image:
    w, h = rig.width, rig.height
    part_id = np.full((h, w), -1, dtype=int)
    for i, part in enumerate(rig.parts):
        part_id[_mask(part, w, h)] = i
    group = np.full((h, w), -1, dtype=int)
    for i, part in enumerate(rig.parts):
        group[part_id == i] = part.group

    out = np.zeros((h, w, 4), dtype=np.uint8)

    def gat(x: int, y: int) -> int:
        return int(group[y, x]) if 0 <= x < w and 0 <= y < h else -1

    for y in range(h):
        for x in range(w):
            pid = part_id[y, x]
            if pid < 0:
                continue
            part = rig.parts[pid]
            mat = materials[part.material]
            g = group[y, x]
            col = mat.base
            if part.shade:
                if gat(x + 1, y + 1) != g or gat(x, y + 2) != g:
                    col = mat.shadow
                elif gat(x - 1, y) != g or gat(x, y - 1) != g:
                    col = mat.light
            if textures and part.material in textures:
                edge = False
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    npid = part_id[ny, nx] if 0 <= nx < w and 0 <= ny < h else -1
                    if npid < 0 or rig.parts[npid].material != part.material:
                        edge = True
                        break
                col = textures[part.material](x, y, col, edge)
            out[y, x] = col
    if outline:
        opaque = part_id >= 0
        result = out.copy()
        for y in range(h):
            for x in range(w):
                pid = part_id[y, x]
                if pid >= 0:
                    # Trennlinie: hintere Gruppe grenzt an vordere (höherer Index = vorn)
                    g = group[y, x]
                    for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                        if 0 <= nx < w and 0 <= ny < h and part_id[ny, nx] >= 0:
                            if group[ny, nx] != g and part_id[ny, nx] > pid and rig.parts[pid].shade:
                                result[y, x] = materials[rig.parts[pid].material].outline
                                break
                    continue
                # Außenlinie
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if 0 <= nx < w and 0 <= ny < h and opaque[ny, nx]:
                        result[y, x] = materials[rig.parts[part_id[ny, nx]].material].outline
                        break
        out = result
    return Image.fromarray(out, "RGBA").copy()  # beschreibbar für Nachbearbeitung
