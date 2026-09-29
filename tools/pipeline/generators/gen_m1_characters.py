"""M1-Tiere als Spritesheets mit JSON-Metadaten (atlas.py): Pferd Holunder (LPC-Vorlage) und
Seelenhund (Collie-Mix). Klio liegt in gen_klio.py.
"""
from __future__ import annotations

from atlas import Animation, pack
from sl_common import ASSETS, GeneratedAsset
from sprites import dog_rig as D
from sprites import horse_lpc as H

GEN = "tools/pipeline/generators/gen_m1_characters.py"


def horse_animations() -> list[Animation]:
    """LPC-Pferd: Stehen (mit gelegentlichem Grasen), Schritt, Trab, Galopp; 'hoof' = Hufschlag-Sound."""
    anims: list[Animation] = []
    for v in ("side", "down", "up"):
        stand = H.frame(H.STAND, v, 0)
        frames = [stand] + [H.frame(H.EAT, v, c) for c in (0, 1, 2, 3, 2, 1)]
        anims.append(Animation(f"idle_{v}", frames, [4200, 160, 160, 900, 700, 160, 160], True,
                               {"bob": [0] * 7, "hoof": [0] * 7}))
    for gname, block, ms, hoof in (("walk", H.WALK, 190, [1, 1, 1, 1]), ("trot", H.WALK, 115, [1, 0, 1, 0]),
                                   ("canter", H.GALLOP, 95, [1, 0, 1, 1])):
        for v in ("side", "down", "up"):
            anims.append(Animation(f"{gname}_{v}", [H.frame(block, v, c) for c in range(4)], [ms] * 4, True,
                                   {"bob": [0] * 4, "hoof": hoof}))
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
    png = pack(horse_animations(), ASSETS / "sprites/animals/horses/holunder.png")
    out.append(GeneratedAsset(png, "sprite", GEN, "Pferd Holunder: [LPC] Horses von bluecarrot16 (vendor/lpc_horses), "
                              "auf die Palette umgefärbt", license="OGA-BY-3.0",
                              license_url="docs/licenses/OGA-BY-3.0.txt", author="bluecarrot16", modified=True))
    out.append(GeneratedAsset(png.with_suffix(".json"), "sprite-meta", GEN, "Animationsdaten"))
    png = pack(dog_animations(), ASSETS / "sprites/animals/dogs/collie_mix.png")
    out.append(GeneratedAsset(png, "sprite", GEN, "Seelenhund Border-Collie-Mix"))
    out.append(GeneratedAsset(png.with_suffix(".json"), "sprite-meta", GEN, "Animationsdaten"))
    return out
