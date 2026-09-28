"""Hund aus Segmenten (32x24): Border-Collie-Mix (schwarz-weiß), der Seelenhund
für den M1-Prototyp. Ab M3 kommen Rassen und Fellfarben per Palette-Swap hinzu.
"""
from __future__ import annotations

import math

from PIL import Image

from palette import color
from sprites.rig import Material, Rig, render

W, H = 32, 24
GROUND = 22

MATERIALS_COLLIE = {
    "coat": Material(color("dusk", 0), color("bark", 0), color("stone", 0), color("stone", 1)),
    "coat_far": Material(color("dusk", 0), color("dusk", 0), color("bark", 0), color("stone", 0)),
    "white": Material(color("stone", 2), color("stone", 4), color("dusk", 6), color("dusk", 6)),
    "nose": Material(color("dusk", 0), color("dusk", 0), color("dusk", 0), color("dusk", 0)),
    "glint": Material(color("dusk", 6), color("dusk", 6), color("dusk", 6), color("dusk", 6)),
    "tongue": Material(color("rose", 2), color("rose", 3), color("rose", 4), color("rose", 4)),
    "collar": Material(color("rose", 0), color("rose", 2), color("rose", 3), color("rose", 4)),
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
         lift: float, white: bool) -> None:
    a = math.radians(swing)
    kx, ky = jx - math.sin(a) * 3.2, jy + math.cos(a) * 3.2 - lift * 0.5
    b = a - math.radians(flex)
    fx, fy = kx - math.sin(b) * 3.2, ky + math.cos(b) * 3.2 - lift * 0.5
    fy = min(fy, GROUND - 1.0)
    rig.capsule(mat, group, jx, jy - 1, kx, ky, 1.5, 1.1)
    rig.capsule("white" if white else mat, group, kx, ky, fx, fy, 1.1, 1.1)


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
        _leg(rig, "coat_far", 1, jx + 1, 15 + bob, s, f, l, True)
    # Schwanz (wedelt über tail_phase)
    wag = math.sin(tail_phase * 2 * math.pi) * 2.5
    rig.capsule("coat", 2, 25, 12 + bob, 28 + wag * 0.4, 8 + bob, 1.6, 1.4)
    rig.capsule("white", 2, 28 + wag * 0.4, 8 + bob, 29 + wag, 5 + bob, 1.4, 1.1)
    g = 3
    rig.ellipse("coat", g, 18, 13 + bob, 7.5, 4.2)                 # Rumpf
    rig.ellipse("white", g, 12, 14 + bob, 3.2, 3.2)                # Brust
    rig.capsule("coat", g, 13, 12 + bob, 9, 8 + bob, 3.2, 3.0)     # Hals
    hx, hy = 8, 7 + bob
    rig.ellipse("coat", g, hx, hy, 3.8, 3.4)                        # Kopf
    rig.capsule("white", g, hx - 1, hy + 1, 3, hy + 2, 1.6, 1.4)  # Schnauze
    rig.capsule("white", g, hx - 1, hy - 3, hx - 1, hy + 1, 0.7, 0.7)  # Blesse
    rig.poly("coat", g, [(hx + 0.5, hy - 2), (hx + 2.5, hy - 6), (hx + 3.5, hy - 1)])  # Ohr
    rig.capsule("collar", 4, 12, 9 + bob, 12, 12 + bob, 0.9, 0.9, shade=False)
    for leg, jx in (("hl", 23.0), ("fl", 12.0)):
        s, f, l = params(leg)
        _leg(rig, "coat", g, jx, 15 + bob, s, f, l, True)
    rig.pixels("nose", 5, [(2, hy + 1), (3, hy + 1)])
    rig.pixels("glint", 5, [(7, hy - 1)])  # Auge: Glanzpunkt auf dunklem Fell
    if mouth_open:
        rig.pixels("tongue", 5, [(4, hy + 3), (5, hy + 3), (5, hy + 4)])
    return render(rig, materials)


def front_frame(gait: str, i: int, back: bool = False, tail_phase: float = 0.0,
                materials: dict[str, Material] = MATERIALS_COLLIE) -> Image.Image:
    frames, amp, flex, lift, bobs, _ = GAITS[gait]
    t = i / frames
    bob = bobs[i]
    rig = Rig(W, H)
    cx = 16
    ll = lr = 0.0
    if frames > 1:
        ll = max(0.0, math.cos(2 * math.pi * t)) * 1.5
        lr = max(0.0, math.cos(2 * math.pi * (t + 0.5))) * 1.5
    if back:
        rig.ellipse("coat", 1, cx, 5 + bob, 3.4, 3.0)             # Kopf von hinten
        rig.poly("coat", 1, [(cx - 4, 4 + bob), (cx - 3, 0 + bob), (cx - 1, 3 + bob)])
        rig.poly("coat", 1, [(cx + 1, 3 + bob), (cx + 3, 0 + bob), (cx + 4, 4 + bob)])
        rig.capsule("collar", 2, cx - 3, 8 + bob, cx + 3, 8 + bob, 0.8, 0.8, shade=False)
        rig.ellipse("coat", 3, cx, 13 + bob, 5.5, 5.5)
        for side, lift_v in ((-1, ll), (1, lr)):
            x = cx + side * 3
            rig.capsule("white", 3, x, 16 + bob, x, 21 - lift_v, 1.4, 1.2)
        wag = math.sin(tail_phase * 2 * math.pi) * 3
        rig.capsule("coat", 4, cx, 11 + bob, cx + wag, 6 + bob, 1.5, 1.3)
        rig.capsule("white", 4, cx + wag, 6 + bob, cx + wag * 1.2, 4 + bob, 1.3, 1.0)
    else:
        rig.ellipse("coat_far", 1, cx, 13 + bob, 5, 4)
        for side, lift_v in ((-1, ll), (1, lr)):
            x = cx + side * 3
            rig.capsule("white", 2, x, 15 + bob, x, 21 - lift_v, 1.4, 1.2)
        rig.ellipse("white", 3, cx, 13 + bob, 3.8, 4.2)             # Brust
        hy = 6 + bob
        rig.ellipse("coat", 4, cx, hy, 4.2, 3.8)                    # Kopf
        rig.poly("coat", 4, [(cx - 5, hy - 1), (cx - 4, hy - 6), (cx - 2, hy - 3)])
        rig.poly("coat", 4, [(cx + 2, hy - 3), (cx + 4, hy - 6), (cx + 5, hy - 1)])
        rig.capsule("white", 4, cx, hy - 3, cx, hy + 2, 0.8, 1.8)   # Blesse + Schnauze
        rig.capsule("collar", 5, cx - 3, hy + 4, cx + 3, hy + 4, 0.8, 0.8, shade=False)
        rig.pixels("nose", 6, [(cx - 1, hy + 1), (cx, hy + 1)])
        rig.pixels("glint", 6, [(cx - 3, hy - 1), (cx + 2, hy - 1)])
        rig.pixels("tongue", 6, [(cx - 1, hy + 3), (cx, hy + 3)])
    return render(rig, materials)


def sit_frame(view: str, tail_phase: float = 0.0,
              materials: dict[str, Material] = MATERIALS_COLLIE) -> Image.Image:
    """Sitzen (Seite): Hinterteil am Boden, Vorderbeine gestreckt."""
    rig = Rig(W, H)
    if view != "side":
        img = front_frame("idle", 0, back=(view == "up"), tail_phase=tail_phase, materials=materials)
        return img
    wag = math.sin(tail_phase * 2 * math.pi) * 2
    rig.capsule("coat", 2, 22, 19, 27 + wag * 0.3, 20, 1.5, 1.3)
    rig.capsule("white", 2, 27 + wag * 0.3, 20, 29 + wag * 0.5, 19, 1.3, 1.0)
    g = 3
    rig.ellipse("coat", g, 19, 16, 5.5, 5)                          # Hinterteil
    rig.ellipse("coat", g, 15, 12, 4.5, 5.5, angle=-30)             # Oberkörper aufrecht
    rig.ellipse("white", g, 12, 13, 2.8, 3.8)
    rig.capsule("coat", g, 13, 9, 10, 5, 3.0, 2.8)
    hx, hy = 9, 5
    rig.ellipse("coat", g, hx, hy, 3.8, 3.4)
    rig.capsule("white", g, hx - 1, hy + 1, 4, hy + 2, 1.6, 1.4)
    rig.capsule("white", g, hx - 1, hy - 3, hx - 1, hy + 1, 0.7, 0.7)
    rig.poly("coat", g, [(hx + 0.5, hy - 2), (hx + 2.5, hy - 6), (hx + 3.5, hy - 1)])
    rig.capsule("collar", 4, 12, 8, 12, 11, 0.9, 0.9, shade=False)
    rig.capsule("white", g, 12, 15, 12, 21, 1.2, 1.1)              # Vorderbein
    rig.capsule("white", g, 21, 19, 17, 21, 1.4, 1.1)              # Hinterpfote
    rig.pixels("nose", 5, [(3, hy + 1), (4, hy + 1)])
    rig.pixels("glint", 5, [(8, hy - 1)])
    rig.pixels("tongue", 5, [(5, hy + 3), (6, hy + 3), (6, hy + 4)])
    return render(rig, materials)
