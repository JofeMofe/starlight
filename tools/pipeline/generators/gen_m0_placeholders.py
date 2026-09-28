"""M0-Platzhalter: Test-Grastile, Funkelstern und das App-Icon.

Alle Formen sind parametrisch und mit festem Seed erzeugt, damit ein erneuter
Lauf bytegleiche Dateien liefert.
"""
from __future__ import annotations

import math
import random

from PIL import Image

from palette import color
from sl_common import ASSETS, TRANSPARENT, GeneratedAsset, save_png

GEN = "tools/pipeline/generators/gen_m0_placeholders.py"
SEED = 20260928


def grass_tile() -> Image.Image:
    """32x32 Mooswiesen-Gras mit Halmbüscheln, nahtlos kachelbar."""
    rng = random.Random(SEED)
    img = Image.new("RGBA", (32, 32), color("moss", 3))
    px = img.load()
    # Weiche Farbflecken (dunkler/heller), wrap-around -> nahtlos
    for _ in range(26):
        cx, cy = rng.randrange(32), rng.randrange(32)
        shade = color("moss", 2) if rng.random() < 0.5 else color("moss", 4)
        for dx, dy in ((0, 0), (1, 0), (0, 1), (-1, 0)):
            if rng.random() < 0.8:
                px[(cx + dx) % 32, (cy + dy) % 32] = shade
    # Halmbüschel: dunkler Fuß, heller Spitzenpixel (Licht von oben links)
    for _ in range(9):
        cx, cy = rng.randrange(32), rng.randrange(32)
        for blade in (-1, 0, 1):
            height = 2 + (blade == 0)
            for h in range(height):
                x = (cx + blade + (1 if blade and h == height - 1 else 0) * blade) % 32
                y = (cy - h) % 32
                px[x, y] = color("moss", 5) if h == height - 1 else color("moss", 2)
    return img


def sparkle(size: int = 16) -> Image.Image:
    """Vierzackiger Funkelstern (Feenglanz), Kern creme, Zacken gold."""
    img = Image.new("RGBA", (size, size), TRANSPARENT)
    px = img.load()
    c = (size - 1) / 2
    for y in range(size):
        for x in range(size):
            dx, dy = abs(x - c), abs(y - c)
            # Astroide |x|^0.5 + |y|^0.5 <= r^0.5 ergibt schlanke Zacken
            v = dx ** 0.5 + dy ** 0.5
            if v <= 1.2:
                px[x, y] = color("dusk", -1)
            elif v <= 2.0:
                px[x, y] = color("ember", 5)
            elif v <= 2.6:
                px[x, y] = color("ember", 3)
            elif v <= 2.85:
                px[x, y] = color("ember", 1)
    return img


def icon() -> Image.Image:
    """32x32 App-Icon: Nachtblaue Plakette, goldener Stern mit Libellen-Feenflügeln."""
    img = Image.new("RGBA", (32, 32), TRANSPARENT)
    px = img.load()
    c = 15.5
    for y in range(32):
        for x in range(32):
            d = ((x - c) ** 2 + (y - c) ** 2) ** 0.5
            if d <= 15.6:
                px[x, y] = color("dusk", 0)
            if d <= 14.6:
                # Schattensichel unten rechts (Licht kommt von oben links)
                shadow = d > 12.4 and (x + y) > 33
                px[x, y] = color("sky", 0) if shadow else color("sky", 1)

    def wing(cx: float, cy: float, rx: float, ry: float, angle_deg: float,
             fill: tuple, rim: tuple) -> None:
        a = math.radians(angle_deg)
        ca, sa = math.cos(a), math.sin(a)
        for y in range(32):
            for x in range(32):
                u = (x - cx) * ca + (y - cy) * sa
                v = -(x - cx) * sa + (y - cy) * ca
                e = (u / rx) ** 2 + (v / ry) ** 2
                if e <= 1.0:
                    px[x, y] = rim if e > 0.5 else fill

    # Oberflügel schräg nach oben außen, Unterflügel schräg nach unten außen
    for side in (-1, 1):
        wing(15.5 + side * 7.0, 12.0, 7.0, 3.0, side * -30, color("sky", 5), color("sky", 6))
        wing(15.5 + side * 6.0, 19.5, 5.0, 2.4, side * 30, color("fae", 3), color("fae", 4))
    star = sparkle(22)
    img.alpha_composite(star, (5, 5))
    for (x, y) in ((7, 5), (25, 7), (24, 25), (6, 23)):
        px[x, y] = color("ember", 5)
    return img


def build() -> list[GeneratedAsset]:
    out: list[GeneratedAsset] = []
    grass = save_png(grass_tile(), ASSETS / "tilesets/mooswiesen/placeholder_grass.png")
    out.append(GeneratedAsset(grass, "tileset", GEN, "M0-Platzhalter Gras 32x32"))
    star = save_png(sparkle(16), ASSETS / "sprites/fx/sparkle_16.png")
    out.append(GeneratedAsset(star, "sprite", GEN, "Funkelstern 16x16"))

    ico_src = icon()
    icon_png = save_png(ico_src, ASSETS / "sprites/ui/icon_32.png")
    out.append(GeneratedAsset(icon_png, "icon", GEN, "App-Icon 32x32 (Quelle)"))
    big = ico_src.resize((256, 256), Image.Resampling.NEAREST)
    icon_big = save_png(big, ASSETS / "sprites/ui/icon_256.png")
    out.append(GeneratedAsset(icon_big, "icon", GEN, "App-Icon x8 Nearest"))
    ico_path = ASSETS / "sprites/ui/icon.ico"
    # Nur ganzzahlige Faktoren (keine Mixels). 48 px = 32er-Icon zentriert
    # auf 48er-Fläche, 16 px = Nearest-Halbierung.
    sizes = [16, 32, 48, 64, 128, 256]
    frames = []
    for s in sizes:
        if s == 48:
            frame = Image.new("RGBA", (48, 48), TRANSPARENT)
            frame.paste(ico_src, (8, 8))
        else:
            frame = ico_src.resize((s, s), Image.Resampling.NEAREST)
        frames.append(frame)
    frames[-1].save(ico_path, format="ICO", sizes=[(s, s) for s in sizes], append_images=frames[:-1])
    out.append(GeneratedAsset(ico_path, "icon", GEN, "Windows-Icon 16-256 px"))
    return out
