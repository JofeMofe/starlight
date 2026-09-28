"""Seelenhund (Tricolor-Collie-Mix), 32x24.

Kopf, Rumpf und Rute sind handgesetzte Pixelkarten (dog_art.py); das Rig
liefert nur die Beine, damit Schritt und Rennen flüssig animiert sind.
Ab M3 kommen Rassen und Fellfarben per Palette-Swap hinzu.
"""
from __future__ import annotations

import math

from PIL import Image

from palette import color
from sprites import dog_art as A
from sprites.rig import Material, Rig, render

W, H = 32, 24
GROUND = 22

MATERIALS_COLLIE = {
    "coat": Material(color("dusk", 0), color("bark", 0), color("stone", 0), color("stone", 1)),
    "coat_far": Material(color("dusk", 0), color("dusk", 0), color("bark", 0), color("stone", 0)),
    "white": Material(color("dusk", 0), color("stone", 4), color("dusk", 6), color("dusk", 6)),
    "white_far": Material(color("dusk", 0), color("stone", 3), color("stone", 4), color("stone", 4)),
}

# Gangarten: (Frames, Amplitude, Beugung, Anheben, Bob pro Frame, Dauern)
GAITS = {
    "idle": (1, 0, 0, 0.0, [0], [1000]),
    "walk": (6, 22, 30, 1.0, [0, 1, 0, 0, 1, 0], [110] * 6),
    "run": (6, 38, 50, 1.6, [0, -1, -1, 0, 1, 1], [70] * 6),
}
PHASES = {
    "walk": {"hl": 0.0, "fl": 0.25, "hr": 0.5, "fr": 0.75},
    "run": {"hl": 0.0, "hr": 0.1, "fl": 0.5, "fr": 0.6},   # Rennen: Sprunggalopp
    "idle": {"hl": 0, "fl": 0, "hr": 0, "fr": 0},
}


def _leg(rig: Rig, mat: str, group: int, jx: float, jy: float, swing: float, flex: float,
         lift: float, white: str) -> None:
    a = math.radians(swing)
    kx, ky = jx - math.sin(a) * 3.2, jy + math.cos(a) * 3.2 - lift * 0.5
    b = a - math.radians(flex)
    fx, fy = kx - math.sin(b) * 3.2, ky + math.cos(b) * 3.2 - lift * 0.5
    fy = min(fy, GROUND - 1.0)
    rig.capsule(mat, group, jx, jy - 1, kx, ky, 1.5, 1.1)
    rig.capsule(white if white else mat, group, kx, ky, fx, fy, 1.1, 1.1)


def _tail_lean(phase: float, amount: float) -> float:
    return amount * math.sin(phase * 2 * math.pi)


def side_frame(gait: str, i: int, tail_phase: float = 0.0, mouth_open: bool = True,
               materials: dict[str, Material] = MATERIALS_COLLIE) -> Image.Image:
    frames, amp, flex, lift, bobs, _ = GAITS[gait]
    t = i / frames
    bob = bobs[i]
    rig = Rig(W, H)
    ph = PHASES[gait]

    def params(leg: str) -> tuple[float, float, float]:
        p = 2 * math.pi * (t + ph[leg])
        sw = max(0.0, math.cos(p))
        return amp * math.sin(p), flex * sw, lift * sw

    for leg, jx in (("hr", 23.0), ("fr", 12.0)):
        s, f, l = params(leg)
        _leg(rig, "coat_far", 1, jx + 1.5, 14 + bob, s, f, l, "white_far")
    for leg, jx, upper in (("hl", 22.0, "coat"), ("fl", 11.0, "white")):
        s, f, l = params(leg)
        _leg(rig, upper, 2 if leg == "hl" else 3, jx, 14 + bob, s, f, l, "white")
    img = render(rig, materials)
    lean = _tail_lean(tail_phase, 1.6)
    if gait == "run":
        lean += 1.0
    tx, ty = A.TAIL_SIDE_POS
    A.paint(img, A.shear(A.TAIL_SIDE, lean, 2), tx - 3, ty + bob)
    A.paint(img, A.SIDE, 0, bob)
    if not mouth_open:
        A.paint(img, ["O", "."], 3, 10 + bob)
    return img


def front_frame(gait: str, i: int, back: bool = False, tail_phase: float = 0.0,
                materials: dict[str, Material] = MATERIALS_COLLIE) -> Image.Image:
    frames, _amp, _flex, _lift, bobs, _ = GAITS[gait]
    t = i / frames
    bob = bobs[i]
    rig = Rig(W, H)
    ll = lr = 0.0
    if frames > 1:
        ll = max(0.0, math.cos(2 * math.pi * t)) * 1.5
        lr = max(0.0, math.cos(2 * math.pi * (t + 0.5))) * 1.5
    upper = "coat" if back else "white"
    for x, lift_v in ((12.5, ll), (19.5, lr)):
        rig.capsule(upper, 1, x, 14 + bob, x, 18 + bob - lift_v * 0.5, 1.6, 1.4)
        rig.capsule("white", 1, x, 18 + bob - lift_v * 0.5, x, 21 - lift_v, 1.4, 1.3)
    img = render(rig, materials)
    if back:
        A.paint(img, A.BACK, 0, bob)
        tx, ty = A.TAIL_BACK_POS
        A.paint(img, A.shear(A.TAIL_BACK, _tail_lean(tail_phase, 2.2), 1, hanging=True), tx - 3, ty + bob)
    else:
        A.paint(img, A.FRONT, 0, bob)
    return img


def sit_frame(view: str, tail_phase: float = 0.0,
              materials: dict[str, Material] = MATERIALS_COLLIE) -> Image.Image:
    """Sitzen: Seitenansicht handgezeichnet, Rute fegt über den Boden."""
    if view != "side":
        return front_frame("idle", 0, back=(view == "up"), tail_phase=tail_phase, materials=materials)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tail = A.TAIL_SIT[0 if math.sin(tail_phase * 2 * math.pi) <= 0 else 1]
    A.paint(img, tail, *A.TAIL_SIT_POS)
    A.paint(img, A.SIT, 0, 0)
    return img
