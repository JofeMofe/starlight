"""Klio im Sunnyside-Stil (sprites/klio_sunny.py): Körper, Haar-Ebene, Fee, Feenflügel.

Die Haare sind in die Körper-Frames gezeichnet; die separate Haar-Ebene bleibt
als leeres Sheet bestehen, damit Szene und Code unverändert funktionieren.
"""
from __future__ import annotations

from PIL import Image

from atlas import Animation, pack
from sl_common import ASSETS, GeneratedAsset
from sprites import klio_sunny as K

GEN = "tools/pipeline/generators/gen_klio.py"
VIEWS = ("down", "up", "side")
# Schrittfolge: Kontakt links, Hochfedern, Kontakt rechts, Hochfedern
WALK = [("contact_a", 0), ("pass", -1), ("contact_b", 0), ("pass", -1)]
WALK_MS = [150, 120, 150, 120]
WING_SPREAD = [1.0, 0.66, 0.33, 0.0, 0.33, 0.66]
WING_MS = [70, 45, 45, 70, 45, 45]


def human_animations() -> list[Animation]:
    anims: list[Animation] = []
    for v in VIEWS:
        blink = [K.human_frame(v), K.human_frame(v, blink=True)] if v != "up" else [K.human_frame(v)] * 2
        anims.append(Animation(f"idle_{v}", blink, [2800, 140], True, {"bob": [0, 0]}))
    for v in VIEWS:
        anims.append(Animation(f"walk_{v}", [K.human_frame(v, p, b) for p, b in WALK], WALK_MS, True,
                               {"bob": [0] * 4, "step": [1, 0, 1, 0]}))
    for v in VIEWS:
        blink = [K.ride_frame(v), K.ride_frame(v, blink=v != "up")]
        anims.append(Animation(f"ride_{v}", blink, [2600, 140], True, {"bob": [0, 0]}))
    return anims


def hair_animations() -> list[Animation]:
    empty = Image.new("RGBA", (16, K.H), (0, 0, 0, 0))
    return [Animation(f"tail_{v}", [empty] * 5, [100] * 5, False, {"sway": [-2, -1, 0, 1, 2]}) for v in VIEWS]


def fairy_animations() -> list[Animation]:
    return [Animation(f"fairy_{v}", [K.fairy_frame(v), K.fairy_frame(v, blink=v != "up")], [3000, 140], True)
            for v in VIEWS]


def wing_animations() -> list[Animation]:
    return [Animation(f"wings_{v}", [K.wing_frame(v, s) for s in WING_SPREAD], WING_MS, True)
            for v in ("down", "side")]


def build() -> list[GeneratedAsset]:
    out: list[GeneratedAsset] = []
    cdir = ASSETS / "sprites/characters"
    for name, anims, note in (
        ("klio_body", human_animations(), "Klio Menschengröße (Sunnyside-Stil, eigene Pixelkarten): idle/walk/ride x 3 Ansichten"),
        ("klio_hair", hair_animations(), "Haar-Ebene (leer, Haare sind in klio_body enthalten)"),
        ("klio_fairy", fairy_animations(), "Klio Feengröße, eigene Pixelkarten"),
        ("klio_wings", wing_animations(), "Libellenflügel, 6-Frame-Schleife"),
    ):
        png = pack(anims, cdir / f"{name}.png")
        out.append(GeneratedAsset(png, "sprite", GEN, note))
        out.append(GeneratedAsset(png.with_suffix(".json"), "sprite-meta", GEN, "Animationsdaten"))
    return out
