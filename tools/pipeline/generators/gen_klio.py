"""Klio aus LPC-Vorlagen (sprites/klio_lpc.py): Körper, Haar-Ebene, Fee, Feenflügel.

Die Haare sind in die LPC-Frames eingezeichnet (inklusive Schwung beim Laufen);
die separate Haar-Ebene bleibt als leeres Sheet bestehen, damit Szene und Code
unverändert funktionieren.
"""
from __future__ import annotations

from PIL import Image

from atlas import Animation, pack
from sl_common import ASSETS, GeneratedAsset
from sprites import klio_lpc as K

GEN = "tools/pipeline/generators/gen_klio.py"
VIEWS = ("down", "up", "side")
WALK_MS = [95] * 8
WING_SPREAD = [1.0, 0.8, 0.55, 0.35, 0.55, 0.8]
WING_MS = [70, 40, 50, 70, 60, 60]
# Reiten: Sitzpose "auf dem Stuhl" (Spalte 2 im LPC-Sitz-Sheet)
RIDE_COL = 2


def human_animations() -> list[Animation]:
    idle, walk, sit = K.compose("idle"), K.compose("walk"), K.compose("sit")
    anims: list[Animation] = []
    for v in VIEWS:
        anims.append(Animation(f"idle_{v}", [K.frame(idle, v, 0), K.frame(idle, v, 1)], [900, 700], True,
                               {"bob": [0, 0]}))
    for v in VIEWS:
        anims.append(Animation(f"walk_{v}", [K.frame(walk, v, i) for i in range(1, 9)], WALK_MS, True,
                               {"bob": [0] * 8}))
    for v in VIEWS:
        f = K.frame(sit, v, RIDE_COL)
        anims.append(Animation(f"ride_{v}", [f, f], [2600, 140], True, {"bob": [0, 0]}))
    order = ["idle_down", "idle_up", "idle_side", "walk_down", "walk_up", "walk_side",
             "ride_down", "ride_up", "ride_side"]
    by_name = {a.name: a for a in anims}
    return [by_name[n] for n in order]


def hair_animations() -> list[Animation]:
    empty = Image.new("RGBA", (K.FRAME, K.FRAME), (0, 0, 0, 0))
    return [Animation(f"tail_{v}", [empty] * 5, [100] * 5, False, {"sway": [-2, -1, 0, 1, 2]}) for v in VIEWS]


def fairy_animations() -> list[Animation]:
    return [Animation(f"fairy_{v}", [K.fairy_frame(v), K.fairy_frame(v, blink=True)], [3000, 140], True)
            for v in VIEWS]


def wing_animations() -> list[Animation]:
    return [Animation(f"wings_{v}", [K.wing_frame(v, s) for s in WING_SPREAD], WING_MS, True)
            for v in ("down", "side")]


LPC_NOTE = "abgeleitet aus LPC-Vorlagen (tools/pipeline/vendor/lpc/CREDITS.csv), umgefärbt und angepasst"


def build() -> list[GeneratedAsset]:
    out: list[GeneratedAsset] = []
    cdir = ASSETS / "sprites/characters"
    for name, anims, note, lpc in (
        ("klio_body", human_animations(), "Klio Menschengröße: idle/walk/ride x 3 Ansichten", True),
        ("klio_hair", hair_animations(), "Haar-Ebene (leer, Haare sind in klio_body enthalten)", False),
        ("klio_fairy", fairy_animations(), "Klio Feengröße 32x32", True),
        ("klio_wings", wing_animations(), "Libellenflügel lila/hellblau, 6-Frame-Schleife", False),
    ):
        png = pack(anims, cdir / f"{name}.png")
        if lpc:
            out.append(GeneratedAsset(png, "sprite", GEN, f"{note}; {LPC_NOTE}", license="OGA-BY-3.0",
                                      license_url="docs/licenses/OGA-BY-3.0.txt",
                                      author="LPC-Autor:innen (siehe vendor/lpc/CREDITS.csv); Starlight-Projekt",
                                      modified=True))
        else:
            out.append(GeneratedAsset(png, "sprite", GEN, note))
        out.append(GeneratedAsset(png.with_suffix(".json"), "sprite-meta", GEN, "Animationsdaten"))
    return out
