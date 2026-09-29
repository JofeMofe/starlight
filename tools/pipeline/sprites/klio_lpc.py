"""Klio aus Vorlagen des Liberated Pixel Cup (LPC), umgefärbt auf die Master-Palette.

Quellen liegen unter tools/pipeline/vendor/lpc/ (Autor:innen und Lizenzen in
vendor/lpc/CREDITS.csv). Alle verwendeten Teile sind unter OGA-BY 3.0 bzw. CC0
nutzbar; die abgeleiteten Sprites stehen daher unter OGA-BY 3.0 mit Namensnennung.

Anpassungen gegenüber den Vorlagen:
- Farben: Haare dunkelbraun, Augen dunkelgrüngrau, schwarzes Shirt, helle
  Jeansjacke (offen: in der Frontansicht scheint das Shirt durch), dunkle Jeans,
  schwarze Schuhe, schwarze Brille mit durchsichtigen Gläsern
- im Profil wird eine dünne Strähne vor dem Körper entfernt
- Fee: auf halbe Größe verkleinert (Umrisse bleiben erhalten), Brille und Augen
  von Hand gesetzt, neue libellenartige Flügel
"""
from __future__ import annotations

import collections
from pathlib import Path

from PIL import Image

from palette import color, palette_hex
from sprites.rig import Material, Rig, render

VENDOR = Path(__file__).resolve().parent.parent / "vendor" / "lpc"
FRAME = 64
# LPC-Zeilen: 0 = Blick nach oben, 1 = links, 2 = unten, 3 = rechts
ROW = {"up": 0, "side": 1, "down": 2}

RGB = tuple[int, int, int]
_PAL: list[RGB] = [tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) for h in palette_hex()]


def _c(ramp: str, i: int) -> RGB:
    return color(ramp, i)[:3]


def _nearest(c: RGB) -> RGB:
    return min(_PAL, key=lambda p: sum((a - b) ** 2 for a, b in zip(p, c)))


# Standard-Rampe der LPC-Kleidung (hell -> dunkel)
_CLOTH: list[RGB] = [(255, 255, 255), (229, 230, 199), (196, 181, 159), (149, 128, 128), (77, 74, 93), (40, 24, 32)]
_HAIR: list[RGB] = [(255, 138, 0), (229, 86, 0), (191, 64, 0), (164, 38, 0), (106, 17, 8), (38, 13, 20), (0, 0, 0)]


def _ramp(src: list[RGB], dst: list[RGB]) -> dict[RGB, RGB | None]:
    return dict(zip(src, dst))


SCHEMES: dict[str, dict[RGB, RGB | None]] = {
    "hair": _ramp(_HAIR, [_c("bark", 4), _c("bark", 3), _c("bark", 2), _c("bark", 1), _c("bark", 0),
                          _c("dusk", 0), _c("dusk", 0)]),
    "brow": {(164, 38, 0): _c("bark", 1), (106, 17, 8): _c("bark", 0)},
    "skin": {(250, 236, 231): _c("dusk", 6), (249, 213, 186): _c("skin", 4), (228, 164, 124): _c("skin", 3),
             (204, 134, 101): _c("skin", 2), (153, 66, 60): _c("skin", 0), (39, 25, 32): _c("dusk", 0),
             # Augen dunkelgrüngrau
             (242, 247, 248): _c("dusk", 6), (87, 206, 228): _c("moss", 2), (86, 134, 174): _c("moss", 1),
             (42, 60, 73): _c("dusk", 0)},
    "tee": _ramp(_CLOTH, [_c("dusk", 4), _c("dusk", 3), _c("dusk", 2), _c("dusk", 1), _c("dusk", 0), _c("dusk", 0)]),
    "denim_jacket": _ramp(_CLOTH, [_c("sky", 6), _c("sky", 5), _c("sky", 4), _c("sky", 3), _c("sky", 1), _c("dusk", 0)]),
    "jeans": _ramp(_CLOTH, [_c("sky", 4), _c("sky", 3), _c("sky", 2), _c("sky", 1), _c("sky", 0), _c("dusk", 0)]),
    "shoes": _ramp(_CLOTH, [_c("dusk", 6), _c("dusk", 3), _c("dusk", 2), _c("dusk", 1), _c("dusk", 0), _c("dusk", 0)]),
    # Gläser durchsichtig, damit die Augen sichtbar bleiben
    "glasses": {(77, 74, 93): _c("dusk", 0), (29, 19, 30): _c("dusk", 0), (134, 126, 127): _c("dusk", 1),
                (138, 190, 201): None, (164, 221, 219): None, (196, 181, 159): None, (115, 190, 211): None,
                (255, 255, 255): _c("sky", 6)},
    "silver": {},
}

# (Pfad unter vendor/lpc, Farbschema) von hinten nach vorn
LAYERS: list[tuple[str, str]] = [
    ("hair/xlong/adult/bg", "hair"),
    ("body/bodies/female", "skin"),
    ("head/heads/human/female", "skin"),
    ("eyes/eyebrows/thin/adult", "brow"),
    ("legs/pants/thin", "jeans"),
    ("feet/shoes/basic/thin", "shoes"),
    ("torso/clothes/shortsleeve/tshirt/female", "tee"),
    ("torso/clothes/longsleeve/longsleeve2_cardigan/female", "denim_jacket"),
    ("neck/necklace/chain/female", "silver"),
    ("facial/earrings/stud/female", "silver"),
    ("hair/xlong/adult/fg", "hair"),
    ("facial/glasses/glasses/adult", "glasses"),
]
FAIRY_SKIP = ("neck/", "facial/")   # zu fein für die halbe Größe; Brille wird von Hand gesetzt


def recolor(im: Image.Image, scheme: dict[RGB, RGB | None]) -> Image.Image:
    im = im.convert("RGBA")
    px = im.load()
    cache: dict[RGB, RGB | None] = {}
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            k = (r, g, b)
            if k not in cache:
                cache[k] = scheme[k] if k in scheme else _nearest(k)
            v = cache[k]
            px[x, y] = (0, 0, 0, 0) if v is None else v + (255,)
    return im


def _open_front(jacket: Image.Image, tee: Image.Image) -> Image.Image:
    """Offene Jacke: in der Frontansicht scheint das Shirt in der Mitte durch."""
    j = jacket.copy()
    jp, tp = j.load(), tee.load()
    fy = ROW["down"]
    if j.height < (fy + 1) * FRAME:
        return j
    for fx in range(j.width // FRAME):
        for y in range(fy * FRAME + 34, fy * FRAME + 50):
            for x in range(fx * FRAME + 30, fx * FRAME + 34):
                if jp[x, y][3] and tp[x, y][3]:
                    jp[x, y] = tp[x, y]
    return j


def _trim_side_strand(hair: Image.Image) -> Image.Image:
    """Im Profil hängt eine dünne Strähne vor dem Körper: unterhalb des Kinns entfernen."""
    h = hair.copy()
    px = h.load()
    for row, front_left in ((1, True), (3, False)):
        if h.height < (row + 1) * FRAME:
            continue
        for fx in range(h.width // FRAME):
            for y in range(row * FRAME + 29, (row + 1) * FRAME):
                for lx in range(FRAME):
                    if (front_left and lx < 30) or (not front_left and lx > 33):
                        px[fx * FRAME + lx, y] = (0, 0, 0, 0)
    return h


def _layer(path: str, anim: str) -> Image.Image | None:
    f = VENDOR / path / f"{anim}.png"
    if f.exists():
        return Image.open(f)
    # Schmuck gibt es nur als Laufzyklus: Standbild (Frame 0) für jede Pose wiederverwenden
    w = VENDOR / path / "walk.png"
    if not w.exists():
        return None
    base = _layer("body/bodies/female", anim)
    if base is None:
        return None
    src = Image.open(w).convert("RGBA")
    out = Image.new("RGBA", base.size, (0, 0, 0, 0))
    for row in range(base.height // FRAME):
        cell = src.crop((0, row * FRAME, FRAME, (row + 1) * FRAME))
        for fx in range(base.width // FRAME):
            out.alpha_composite(cell, (fx * FRAME, row * FRAME))
    return out


def compose(anim: str, skip: tuple[str, ...] = ()) -> Image.Image:
    """Setzt ein komplettes LPC-Sheet (walk/idle/sit) umgefärbt zusammen."""
    out: Image.Image | None = None
    tee: Image.Image | None = None
    for path, scheme in LAYERS:
        if path.startswith(skip):
            continue
        src = _layer(path, anim)
        if src is None:
            continue
        im = recolor(src, SCHEMES[scheme])
        if scheme == "tee":
            tee = im
        if scheme == "denim_jacket" and tee is not None:
            im = _open_front(im, tee)
        if path.endswith("/fg"):
            im = _trim_side_strand(im)
        if out is None:
            out = Image.new("RGBA", im.size, (0, 0, 0, 0))
        out.alpha_composite(im)
    assert out is not None
    return out


def frame(sheet: Image.Image, view: str, col: int) -> Image.Image:
    r = ROW[view]
    return sheet.crop((col * FRAME, r * FRAME, (col + 1) * FRAME, (r + 1) * FRAME))


# ---------------------------------------------------------------------------
# Fee: halbe Größe
# ---------------------------------------------------------------------------

def _lum(c: tuple[int, ...]) -> float:
    return 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]


def half(im: Image.Image) -> Image.Image:
    """2x-Verkleinerung für Pixel-Art: Umrisse bleiben erhalten, sonst häufigste Farbe."""
    w, h = im.width // 2, im.height // 2
    src = im.load()
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dst = out.load()
    for y in range(h):
        for x in range(w):
            blk = [src[2 * x + dx, 2 * y + dy] for dy in (0, 1) for dx in (0, 1)]
            op = [p for p in blk if p[3] > 0]
            if len(op) < 2:
                continue
            dark = [p for p in op if _lum(p) < 45]
            if len(dark) >= 2 and len(op) < 4:
                dst[x, y] = dark[0]
                continue
            dst[x, y] = collections.Counter(op).most_common(1)[0][0]
    return out


_D0 = color("dusk", 0)
_EYE = color("moss", 1)
_GLARE = color("sky", 6)
_LID = color("skin", 2)

# Von Hand gesetzte Brille/Augen in der Feengröße (Koordinaten im 32x32-Frame)
FAIRY_FACE: dict[str, list[tuple[list[tuple[int, int]], tuple[int, int, int, int]]]] = {
    "down": [([(13, 14), (14, 14), (15, 14), (16, 14), (17, 14), (18, 14), (19, 14)], _D0),
             ([(13, 15), (19, 15)], _D0), ([(14, 15), (17, 15)], _EYE), ([(15, 15), (18, 15)], _GLARE)],
    "side": [([(11, 14), (12, 14), (13, 14), (14, 14), (15, 14), (16, 14)], _D0),
             ([(11, 15)], _D0), ([(12, 15)], _EYE), ([(13, 15)], _GLARE)],
    "up": [],
}
FAIRY_BLINK: dict[str, list[tuple[int, int]]] = {"down": [(14, 15), (17, 15)], "side": [(12, 15)]}


def fairy_frame(view: str, blink: bool = False) -> Image.Image:
    sheet = half(compose("walk", FAIRY_SKIP))
    r = ROW[view]
    fr = sheet.crop((0, r * 32, 32, (r + 1) * 32))
    px = fr.load()
    for pts, col in FAIRY_FACE[view]:
        for p in pts:
            px[p] = col
    if blink:
        for p in FAIRY_BLINK.get(view, []):
            px[p] = _LID
    return fr


_WING = {"wing": Material(color("fae", 3), color("fae", 4), color("sky", 6), color("dusk", 6))}


def wing_frame(view: str, spread: float) -> Image.Image:
    """Libellenartige Flügel: zwei schlanke Paare mit heller Kontur; spread 0..1 = Schlag."""
    rig = Rig(32, 32)
    cx, cy = 16, 18
    if view == "side":
        rig.ellipse("wing", 1, cx + 4 + 2 * spread, cy - 6, 2.0 + 2.2 * spread, 7.0, angle=25)
        rig.ellipse("wing", 1, cx + 4 + 1 * spread, cy + 1, 1.6 + 1.6 * spread, 4.5, angle=-30)
    else:
        up = 1 - spread
        for s in (-1, 1):
            rig.ellipse("wing", 1, cx + s * (3 + 6 * spread), cy - 5 - 3 * up, 1.5 + 6 * spread, 2.2,
                        angle=s * -(25 + 40 * up))
            rig.ellipse("wing", 1, cx + s * (3 + 4 * spread), cy + 1 - up, 1.2 + 4.2 * spread, 1.7,
                        angle=s * (20 - 20 * up))
    return render(rig, _WING)
