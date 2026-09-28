"""M1-Figuren als Spritesheets mit JSON-Metadaten (atlas.py):
Klio (Körper, lange Haare, Fee, Feenflügel), Pferd Holunder, Seelenhund (Collie-Mix).
"""
from __future__ import annotations

from atlas import Animation, pack
from sl_common import ASSETS, GeneratedAsset
from sprites import dog_rig as D
from sprites import horse_rig as R
from sprites import klio_sheet as K

GEN = "tools/pipeline/generators/gen_m1_characters.py"


def horse_animations() -> list[Animation]:
    anims: list[Animation] = []
    idle = R.GAITS["idle"]
    tail = [0.0, 1.0, 2.0, 1.0]
    anims.append(Animation("idle_side", [R.side_frame(idle, 0, tail_sway=t) for t in tail],
                           [700, 160, 220, 160], True, {"bob": [0, 0, 0, 0]}))
    anims.append(Animation("idle_down", [R.front_frame(idle, 0)], [1000], True, {"bob": [0]}))
    anims.append(Animation("idle_up", [R.front_frame(idle, 0, back=True)], [1000], True, {"bob": [0]}))
    for gname in ("walk", "trot", "canter"):
        g = R.GAITS[gname]
        anims.append(Animation(f"{gname}_side", [R.side_frame(g, i) for i in range(g.frames)],
                               g.durations_ms, True, {"bob": g.bob}))
        anims.append(Animation(f"{gname}_down", [R.front_frame(g, i) for i in range(g.frames)],
                               g.durations_ms, True, {"bob": g.bob}))
        anims.append(Animation(f"{gname}_up", [R.front_frame(g, i, back=True) for i in range(g.frames)],
                               g.durations_ms, True, {"bob": g.bob}))
    return anims


def dog_animations() -> list[Animation]:
    anims: list[Animation] = []
    wag = [0.0, 0.25, 0.5, 0.75]
    anims.append(Animation("idle_side", [D.side_frame("idle", 0, p) for p in wag], [140] * 4, True))
    anims.append(Animation("idle_down", [D.front_frame("idle", 0)], [1000], True))
    anims.append(Animation("idle_up", [D.front_frame("idle", 0, back=True, tail_phase=p) for p in wag],
                           [140] * 4, True))
    anims.append(Animation("sit_side", [D.sit_frame("side", p) for p in wag], [160] * 4, True))
    anims.append(Animation("sit_down", [D.front_frame("idle", 0)], [1000], True))
    anims.append(Animation("sit_up", [D.front_frame("idle", 0, back=True)], [1000], True))
    for gait in ("walk", "run"):
        frames, *_rest, durations = D.GAITS[gait]
        anims.append(Animation(f"{gait}_side", [D.side_frame(gait, i, i / frames) for i in range(frames)],
                               durations, True, {"bob": D.GAITS[gait][4]}))
        anims.append(Animation(f"{gait}_down", [D.front_frame(gait, i) for i in range(frames)],
                               durations, True, {"bob": D.GAITS[gait][4]}))
        anims.append(Animation(f"{gait}_up",
                               [D.front_frame(gait, i, back=True, tail_phase=i / frames) for i in range(frames)],
                               durations, True, {"bob": D.GAITS[gait][4]}))
    return anims


def build() -> list[GeneratedAsset]:
    out: list[GeneratedAsset] = []
    cdir = ASSETS / "sprites/characters"
    for name, anims, note in (
        ("klio_body", K.human_animations(), "Klio Menschengröße: Körper/Kopf, idle/walk/ride x 3 Ansichten"),
        ("klio_hair", K.tail_animations(), "Klio lange Haare, 5 Schwungstufen je Ansicht"),
        ("klio_fairy", K.fairy_animations(), "Klio Feengröße 16x20"),
        ("klio_wings", K.wing_animations(), "Feenflügel, 6-Frame-Schleife"),
    ):
        png = pack(anims, cdir / f"{name}.png")
        out.append(GeneratedAsset(png, "sprite", GEN, note))
        out.append(GeneratedAsset(png.with_suffix(".json"), "sprite-meta", GEN, "Animationsdaten"))
    png = pack(horse_animations(), ASSETS / "sprites/animals/horses/holunder.png")
    out.append(GeneratedAsset(png, "sprite", GEN, "Pferd Holunder (Fuchs, Flachsmähne), Schritt/Trab/Galopp"))
    out.append(GeneratedAsset(png.with_suffix(".json"), "sprite-meta", GEN, "Animationsdaten"))
    png = pack(dog_animations(), ASSETS / "sprites/animals/dogs/collie_mix.png")
    out.append(GeneratedAsset(png, "sprite", GEN, "Seelenhund Border-Collie-Mix"))
    out.append(GeneratedAsset(png.with_suffix(".json"), "sprite-meta", GEN, "Animationsdaten"))
    return out
