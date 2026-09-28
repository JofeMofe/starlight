"""Klio (v4, nach Vorgaben): Körper, lange Haare, Fee, Feenflügel als Spritesheets."""
from __future__ import annotations

from atlas import pack
from sl_common import ASSETS, GeneratedAsset
from sprites import klio_v4_sheet as K

GEN = "tools/pipeline/generators/gen_klio.py"


def build() -> list[GeneratedAsset]:
    out: list[GeneratedAsset] = []
    cdir = ASSETS / "sprites/characters"
    for name, anims, note in (
        ("klio_body", K.human_animations(), "Klio v4 Menschengröße: idle/walk/ride x 3 Ansichten"),
        ("klio_hair", K.tail_animations(), "Klio v4 lange Haare, 5 Schwungstufen je Ansicht"),
        ("klio_fairy", K.fairy_animations(), "Klio v4 Feengröße 16x20"),
        ("klio_wings", K.wing_animations(), "Feenflügel lila, 6-Frame-Schleife"),
    ):
        png = pack(anims, cdir / f"{name}.png")
        out.append(GeneratedAsset(png, "sprite", GEN, note))
        out.append(GeneratedAsset(png.with_suffix(".json"), "sprite-meta", GEN, "Animationsdaten"))
    return out
