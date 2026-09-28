"""Pferd aus Segmenten (96x64), Blick nach links / vorn / hinten.

Gangarten über Beinphasen:
- Schritt: Viertakt (HL, VL, HR, VR je 1/4 versetzt), kleine Amplitude
- Trab:    Zweitakt, diagonale Beinpaare gleichzeitig, deutlicher Schwebe-Bob
- Galopp:  Dreitakt (Linksgalopp: HR | HL+VR | VL), großer Schwung, Schaukeln
Farben kommen aus einem Materialsatz; ab M3 ersetzt der Palette-Swap-Shader
die Fellfarbe anhand des Genotyps.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from palette import color
from sprites.rig import Material, Rig, render

W, H = 96, 64
GROUND = 61

MATERIALS_CHESTNUT_FLAXEN = {
    "coat": Material(color("bark", 1), color("bark", 3), color("bark", 4), color("bark", 5)),
    "coat_far": Material(color("bark", 1), color("bark", 2), color("bark", 3), color("bark", 4)),
    "mane": Material(color("bark", 2), color("bark", 5), color("bark", 6), color("bark", 7)),
    "mane_far": Material(color("bark", 2), color("bark", 4), color("bark", 5), color("bark", 6)),
    "white": Material(color("stone", 3), color("stone", 5), color("dusk", 6), color("dusk", 6)),
    "hoof": Material(color("dusk", 0), color("stone", 1), color("stone", 2), color("stone", 3)),
    "eye": Material(color("dusk", 0), color("dusk", 0), color("dusk", 0), color("dusk", 0)),
    "glint": Material(color("dusk", 6), color("dusk", 6), color("dusk", 6), color("dusk", 6)),
    "nostril": Material(color("bark", 1), color("bark", 1), color("bark", 1), color("bark", 1)),
}


@dataclass
class Gait:
    name: str
    frames: int
    amp_deg: float        # Schwung des Oberschenkels
    flex_deg: float       # Beugung in der Schwungphase
    lift: float           # Anheben des Hufs in der Schwungphase (px)
    phases: dict[str, float]  # Phase je Bein: hl, fl, hr, fr
    bob: list[int]        # Körperversatz pro Frame (px, positiv = tiefer)
    nod: list[int]        # Kopfnicken pro Frame
    durations_ms: list[int]


GAITS = {
    "idle": Gait("idle", 1, 0, 0, 0, {"hl": 0, "fl": 0, "hr": 0, "fr": 0}, [0], [0], [1000]),
    "walk": Gait("walk", 8, 16, 26, 2.0, {"hl": 0.0, "fl": 0.25, "hr": 0.5, "fr": 0.75},
                 [0, 1, 1, 0, 0, 1, 1, 0], [0, 1, 1, 0, 0, 1, 1, 0],
                 [130] * 8),
    "trot": Gait("trot", 8, 22, 40, 3.0, {"fl": 0.0, "hr": 0.0, "fr": 0.5, "hl": 0.5},
                 [1, 0, -1, 0, 1, 0, -1, 0], [0, 0, 1, 0, 0, 0, 1, 0],
                 [80] * 8),
    "canter": Gait("canter", 8, 30, 52, 4.0, {"hr": 0.0, "hl": 0.3, "fr": 0.3, "fl": 0.55},
                   [1, 1, 0, -1, -2, -1, 0, 0], [1, 1, 0, -1, -1, 0, 0, 1],
                   [85, 75, 70, 70, 80, 80, 75, 85]),
}

# Gelenkpositionen (Blick nach links); x wächst nach hinten
FRONT_JOINT = (35.0, 39.0)
HIND_JOINT = (64.0, 38.0)
UPPER, LOWER = 10.0, 10.0


def _leg(rig: Rig, mat: str, group: int, joint: tuple[float, float], swing: float,
         flex: float, lift: float, hind: bool, white_lower: bool, bob: int) -> None:
    jx, jy = joint[0], joint[1] + bob
    a = math.radians(swing)
    kx, ky = jx - math.sin(a) * UPPER, jy + math.cos(a) * UPPER - lift * 0.5
    b = a - math.radians(flex) * (1.0 if not hind else -0.6)
    fx, fy = kx - math.sin(b) * LOWER, ky + math.cos(b) * LOWER - lift * 0.5
    # Stehbein: auf den Boden ziehen (keine schwebenden Hufe)
    if lift <= 0.01:
        fy = max(fy, GROUND - 2.0)
    fy = min(fy, GROUND - 2.0)
    width_top = 4.0 if hind else 3.5
    rig.capsule(mat, group, jx, jy - 3, kx, ky, width_top, 2.3)
    lower_mat = "white" if white_lower else mat
    rig.capsule(lower_mat, group, kx, ky, fx, fy, 2.1, 1.8)
    rig.ellipse("hoof", group, fx - 0.5, fy + 1.2, 2.2, 1.4)


def side_frame(gait: Gait, i: int, materials: dict[str, Material] = MATERIALS_CHESTNUT_FLAXEN,
               tail_sway: float = 0.0) -> "Image.Image":
    t = i / gait.frames
    bob = gait.bob[i]
    nod = gait.nod[i]
    rig = Rig(W, H)

    def leg_params(leg: str) -> tuple[float, float, float]:
        ph = 2 * math.pi * (t + gait.phases[leg])
        swing = gait.amp_deg * math.sin(ph)
        # Schwungphase: Bein bewegt sich nach vorn (cos > 0) -> beugen und anheben
        swing_phase = max(0.0, math.cos(ph))
        return swing, gait.flex_deg * swing_phase, gait.lift * swing_phase

    # Ferne Beine (hinter dem Körper, dunkler)
    for leg, joint, hind in (("hr", HIND_JOINT, True), ("fr", FRONT_JOINT, False)):
        s, f, l = leg_params(leg)
        _leg(rig, "coat_far", 1, (joint[0] + 2, joint[1]), s, f, l, hind, False, bob)
    # Schweif
    sway = tail_sway + (2.0 * math.sin(2 * math.pi * t) if gait.frames > 1 else 0.0)
    rig.capsule("mane_far", 2, 75, 24 + bob, 79 + sway * 0.5, 34 + bob, 3.0, 3.2)
    rig.capsule("mane_far", 2, 79 + sway * 0.5, 34 + bob, 80 + sway, 46 + bob, 3.2, 2.2)
    # Körper (eine Gruppe -> durchgehende Form)
    g = 3
    rig.ellipse("coat", g, 50, 31 + bob, 20, 10.5)              # Rumpf
    rig.ellipse("coat", g, 35, 31 + bob, 9, 10.5)               # Brust/Schulter
    rig.ellipse("coat", g, 65, 29 + bob, 11, 11.5)              # Hinterhand
    rig.capsule("coat", g, 36, 27 + bob, 25, 13 + bob + nod, 7.5, 5.0)  # Hals
    hx, hy = 23, 11 + bob + nod
    rig.capsule("coat", g, hx, hy, 12, hy + 10, 5.0, 3.6)       # Kopf
    rig.poly("coat", g, [(hx + 0.5, hy - 4), (hx + 2.5, hy - 9), (hx + 3.5, hy - 3)])  # Ohr
    # Blesse
    rig.capsule("white", g, hx - 5, hy + 0.5, 12.5, hy + 8, 1.1, 1.4)
    # Mähne (vorn am Hals) und Stirnschopf
    rig.capsule("mane", 4, 38, 22 + bob, 26, 7 + bob + nod, 2.6, 2.2)
    rig.capsule("mane", 4, 24, 6 + bob + nod, 21, 9 + bob + nod, 1.8, 1.4)
    # Nahe Beine
    for leg, joint, hind, white in (("hl", HIND_JOINT, True, True), ("fl", FRONT_JOINT, False, False)):
        s, f, l = leg_params(leg)
        _leg(rig, "coat", g, joint, s, f, l, hind, white, bob)
    # Auge mit Glanz, Nüster
    rig.pixels("eye", 6, [(20, hy + 1), (21, hy + 1), (20, hy + 2), (21, hy + 2)])
    rig.pixels("glint", 6, [(20, hy + 1)])
    rig.pixels("nostril", 6, [(12, hy + 9)])
    return render(rig, materials)


def front_frame(gait: Gait, i: int, materials: dict[str, Material] = MATERIALS_CHESTNUT_FLAXEN,
                back: bool = False) -> "Image.Image":
    """Ansicht von vorn (Blick zur Kamera) bzw. von hinten (back=True)."""
    t = i / gait.frames
    bob = gait.bob[i]
    nod = gait.nod[i]
    rig = Rig(W, H)
    cx = 48
    lift_l = lift_r = 0.0
    if gait.frames > 1:
        ph_l = 2 * math.pi * (t + gait.phases["fl" if not back else "hl"])
        ph_r = 2 * math.pi * (t + gait.phases["fr" if not back else "hr"])
        lift_l = max(0.0, math.cos(ph_l)) * gait.lift * 1.2
        lift_r = max(0.0, math.cos(ph_r)) * gait.lift * 1.2
    if back:
        # hintere Beine vorn im Bild, Kruppe, Schweif; Kopf ragt oben hervor
        rig.capsule("coat_far", 1, cx, 20 + bob + nod, cx, 10 + bob + nod, 3.5, 3.0)    # Kopf von hinten
        rig.poly("coat_far", 1, [(cx - 4, 9 + bob + nod), (cx - 3, 4 + bob + nod), (cx - 1, 9 + bob + nod)])
        rig.poly("coat_far", 1, [(cx + 1, 9 + bob + nod), (cx + 3, 4 + bob + nod), (cx + 4, 9 + bob + nod)])
        rig.capsule("mane_far", 1, cx, 12 + bob + nod, cx, 24 + bob, 2.0, 2.4)
        rig.ellipse("coat", 3, cx, 32 + bob, 13, 12)
        for side, lift in ((-1, lift_l), (1, lift_r)):
            x = cx + side * 6
            rig.capsule("coat", 3, x, 38 + bob, x, 50 + bob - lift, 4.2, 2.6)
            rig.capsule("white" if side < 0 else "coat", 4, x, 50 + bob - lift, x, 58 - lift, 2.4, 2.0)
            rig.ellipse("hoof", 4, x, 59.5 - lift, 2.6, 1.4)
        sway = 1.5 * math.sin(2 * math.pi * t) if gait.frames > 1 else 0.0
        rig.capsule("mane", 5, cx, 23 + bob, cx + sway, 44 + bob, 3.0, 2.2)
    else:
        rig.ellipse("coat_far", 1, cx, 34 + bob, 11, 9)                  # Rumpf dahinter
        for side, lift in ((-1, lift_l), (1, lift_r)):
            x = cx + side * 5
            rig.capsule("coat", 2, x, 38 + bob, x, 50 + bob - lift, 3.6, 2.4)
            rig.capsule("coat", 2, x, 50 + bob - lift, x, 58 - lift, 2.2, 1.9)
            rig.ellipse("hoof", 2, x, 59.5 - lift, 2.5, 1.4)
        rig.ellipse("coat", 3, cx, 33 + bob, 9, 10)                      # Brust
        rig.capsule("coat", 3, cx, 26 + bob, cx, 15 + bob + nod, 5.5, 4.5)    # Hals
        hy = 8 + bob + nod
        rig.capsule("coat", 5, cx, hy, cx, hy + 14, 4.6, 3.4)            # Kopf frontal
        rig.poly("coat", 5, [(cx - 5, hy + 1), (cx - 4, hy - 5), (cx - 2, hy)])
        rig.poly("coat", 5, [(cx + 2, hy), (cx + 4, hy - 5), (cx + 5, hy + 1)])
        rig.capsule("white", 5, cx, hy + 2, cx, hy + 13, 1.2, 1.6)       # Blesse
        rig.capsule("mane", 6, cx, hy - 2, cx + 1, hy + 3, 2.0, 1.4)     # Stirnschopf
        rig.pixels("eye", 7, [(cx - 4, hy + 4), (cx + 3, hy + 4), (cx - 4, hy + 5), (cx + 3, hy + 5)])
        rig.pixels("glint", 7, [(cx - 4, hy + 4), (cx + 3, hy + 4)])
        rig.pixels("nostril", 7, [(cx - 2, hy + 13), (cx + 1, hy + 13)])
    return render(rig, materials)
