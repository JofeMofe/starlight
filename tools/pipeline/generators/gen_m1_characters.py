"""Pferd Holunder und Seelenhund (Border-Collie-Mix) im Sunnyside-Tierstil
(sprites/animals_sunny.py). Klio liegt in gen_klio.py.
"""
from __future__ import annotations

from atlas import Animation, pack
from sl_common import ASSETS, GeneratedAsset
from sprites import animals_sunny as A

GEN = "tools/pipeline/generators/gen_m1_characters.py"
VIEWS = ("side", "down", "up")


def _steps(view: str) -> list[str]:
    return ["reach", "stand", "gather", "stand"] if view == "side" else ["l", "stand", "r", "stand"]


def horse_animations() -> list[Animation]:
    """Stehen, Schritt, Trab, Galopp; 'hoof' = Hufschlag-Sound, 'bob' = Rückenhöhe für den Reiter."""
    anims: list[Animation] = []
    for v in VIEWS:
        anims.append(Animation(f"idle_{v}", [A.horse_frame(v)], [1000], True, {"bob": [0], "hoof": [0]}))
    for gname, ms, hoof, bob in (("walk", 190, [1, 1, 1, 1], [0, 0, 0, 0]),
                                 ("trot", 115, [1, 0, 1, 0], [0, -1, 0, -1]),
                                 ("canter", 95, [1, 0, 1, 1], [0, -1, -1, 0])):
        for v in VIEWS:
            legs = _steps(v) if gname != "canter" or v != "side" else ["gather", "stand", "reach", "stand"]
            frames = [A.horse_frame(v, lg, b) for lg, b in zip(legs, bob)]
            anims.append(Animation(f"{gname}_{v}", frames, [ms] * 4, True, {"bob": bob, "hoof": hoof}))
    return anims


def dog_animations() -> list[Animation]:
    anims: list[Animation] = []
    for v in VIEWS:
        anims.append(Animation(f"idle_{v}", [A.dog_frame(v)], [1000], True))
    for v in VIEWS:
        anims.append(Animation(f"sit_{v}", [A.dog_frame(v, sit=True)], [1000], True))
    for gait, ms, bob in (("walk", 130, [0, 0, 0, 0]), ("run", 80, [0, -1, 0, -1])):
        for v in VIEWS:
            frames = [A.dog_frame(v, lg, b) for lg, b in zip(_steps(v), bob)]
            anims.append(Animation(f"{gait}_{v}", frames, [ms] * 4, True, {"bob": bob}))
    return anims


def build() -> list[GeneratedAsset]:
    out: list[GeneratedAsset] = []
    png = pack(horse_animations(), ASSETS / "sprites/animals/horses/holunder.png")
    out.append(GeneratedAsset(png, "sprite", GEN, "Pferd Holunder (Fuchs), eigene Pixelkarten im Sunnyside-Tierstil"))
    out.append(GeneratedAsset(png.with_suffix(".json"), "sprite-meta", GEN, "Animationsdaten"))
    png = pack(dog_animations(), ASSETS / "sprites/animals/dogs/collie_mix.png")
    out.append(GeneratedAsset(png, "sprite", GEN, "Seelenhund Border-Collie-Mix, eigene Pixelkarten im Sunnyside-Tierstil"))
    out.append(GeneratedAsset(png.with_suffix(".json"), "sprite-meta", GEN, "Animationsdaten"))
    return out
