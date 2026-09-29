"""Welt der Mooswiesen: Boden, Zaun und Objekte aus Sunnyside World (sprites/sunny_world.py),
dazu eigene Effekte (Funkeln, Herz, Staub, Blitz), Schatten und HUD-Symbole.

Zaun-Varianten: Index = Bitmaske der gleichartigen Nachbarn N=1, O=2, S=4, W=8
(so wählt der MapBuilder im Spiel die passende Kachel).
"""
from __future__ import annotations

from PIL import Image

from palette import color
from sl_common import ASSETS, TRANSPARENT, GeneratedAsset, save_png
from sprites import sunny_world as SW

GEN = "tools/pipeline/generators/gen_m1_world.py"
T = 32  # Größe des Verwandlungsblitzes


def shadow(w: int, h: int, cw: int, ch: int) -> Image.Image:
    """Einfarbige Schattenellipse w x h, mittig auf einer cw x ch-Fläche (Effekt-Raster 8 px).
    Die Transparenz kommt im Spiel per Modulate."""
    img = Image.new("RGBA", (cw, ch), TRANSPARENT)
    px = img.load()
    ox, oy = (cw - w) // 2, (ch - h) // 2
    for y in range(h):
        for x in range(w):
            if ((x + 0.5 - w / 2) / (w / 2)) ** 2 + ((y + 0.5 - h / 2) / (h / 2)) ** 2 <= 1.0:
                px[ox + x, oy + y] = color("dusk", 0)
    return img


def fx_sheet() -> Image.Image:
    """8x8-Effekte in einer Reihe: Funken klein, Funken groß, Herz, Staub, Punkt, Note."""
    img = Image.new("RGBA", (8 * 6, 8), TRANSPARENT)
    px = img.load()
    cream, gold, gold_d = color("dusk", 6), color("ember", 5), color("ember", 3)
    # 0: kleiner Funke
    for x, y, c in ((3, 3, cream), (3, 2, gold), (3, 4, gold), (2, 3, gold), (4, 3, gold)):
        px[x, y] = c
    # 1: großer Funke
    ox = 8
    for d in range(1, 4):
        c = gold if d < 3 else gold_d
        for x, y in ((3, 3 - d), (3, 3 + d), (3 - d, 3), (3 + d, 3)):
            px[ox + x, y] = c
    px[ox + 3, 3] = cream
    # 2: Herz
    ox = 16
    heart = ["........", ".##.##..", "#hh#rr#.", "#hrrrr#.", ".#rrr#..", "..#r#...", "...#....", "........"]
    for y, row in enumerate(heart):
        for x, ch in enumerate(row):
            if ch == "#":
                px[ox + x, y] = color("rose", 1)
            elif ch == "r":
                px[ox + x, y] = color("rose", 3)
            elif ch == "h":
                px[ox + x, y] = color("rose", 5)
    # 3: Staubwölkchen
    ox = 24
    dust = ["........", "..##....", ".#ll#...", "#llll##.", "#lllll#.", ".######.", "........", "........"]
    for y, row in enumerate(dust):
        for x, ch in enumerate(row):
            if ch == "#":
                px[ox + x, y] = color("bark", 5)
            elif ch == "l":
                px[ox + x, y] = color("bark", 7)
    # 4: Lichtpunkt (2x2)
    for x, y in ((3, 3), (4, 3), (3, 4), (4, 4)):
        px[32 + x, y] = cream
    # 5: Feenstaub (zart violett)
    for x, y, c in ((3, 3, color("fae", 4)), (3, 2, color("fae", 3)), (2, 3, color("fae", 3)),
                    (4, 3, color("fae", 3)), (3, 4, color("fae", 3))):
        px[40 + x, y] = c
    return img


def flash() -> Image.Image:
    """32x32 Lichtblitz der Verwandlung (Sternform, cremig mit Goldrand)."""
    img = Image.new("RGBA", (T, T), TRANSPARENT)
    px = img.load()
    c = 15.5
    for y in range(T):
        for x in range(T):
            dx, dy = abs(x - c), abs(y - c)
            v = dx ** 0.5 + dy ** 0.5
            d = (dx * dx + dy * dy) ** 0.5
            if v <= 2.3 or d <= 3.5:
                px[x, y] = color("dusk", 6)
            elif v <= 3.1 or d <= 5:
                px[x, y] = color("ember", 5)
            elif v <= 3.6:
                px[x, y] = color("ember", 4)
    return img


def ui_icons() -> Image.Image:
    """16x16-Symbole: 0 Feenglanz (Stern), 1 Flugenergie (Flügel)."""
    img = Image.new("RGBA", (32, 16), TRANSPARENT)
    img.alpha_composite(_small_star(), (0, 0))
    px = img.load()
    wing = [
        "................",
        "................",
        "..##............",
        ".#ww##..........",
        ".#wwww##....##..",
        "..#wwwww#..#ww#.",
        "...#wwwvv##wwww#",
        "....#wvvvvwwwww#",
        ".....#vvvvvwww#.",
        "......#vvvv##...",
        ".......#vv#.....",
        "........##......",
        "................",
        "................",
        "................",
        "................",
    ]
    for y, row in enumerate(wing):
        for x, ch in enumerate(row):
            if ch == "#":
                px[16 + x, y] = color("sky", 2)
            elif ch == "w":
                px[16 + x, y] = color("sky", 6)
            elif ch == "v":
                px[16 + x, y] = color("fae", 3)
    return img


def _small_star() -> Image.Image:
    img = Image.new("RGBA", (16, 16), TRANSPARENT)
    px = img.load()
    c = 7.5
    for y in range(16):
        for x in range(16):
            v = abs(x - c) ** 0.5 + abs(y - c) ** 0.5
            if v <= 1.3:
                px[x, y] = color("dusk", 6)
            elif v <= 2.1:
                px[x, y] = color("ember", 5)
            elif v <= 2.6:
                px[x, y] = color("ember", 3)
            elif v <= 2.9:
                px[x, y] = color("ember", 1)
    return img


SUNNY = dict(license="Sunnyside-World-V1", license_url="docs/licenses/Sunnyside_World.txt", modified=True,
             author="Daniel Diggle (Sunnyside World, danieldiggle.itch.io/sunnyside)")


def _sunny_world(tdir) -> list[GeneratedAsset]:
    """Bodenatlanten und Objekte aus Sunnyside World (Quelle: vendor/sunnyside, siehe fetch_vendor.py)."""
    names = ["meadow_tiles", "meadow_ground", "tree", "tree_pine", "bush", "berry_bush", "rock", "pebbles",
             "tall_grass", "stump", "flowers", "fairy_ring"]
    notes = {
        "meadow_tiles": "Rasterebene 16 px: Gras, Weg, Wasser (Kollision), Zaun (16 Nachbarmasken aus Sunnyside-Pfosten/Latten)",
        "meadow_ground": "Boden (Dual Grid) 16 px: Übergänge im Sunnyside-Stil gerendert, Füllungen = Sunnyside-Kacheln",
        "tree": "Laubbaum mit Wind-Animation (4 Frames)", "tree_pine": "Tanne mit Wind-Animation (4 Frames)",
        "bush": "Busch", "berry_bush": "Beerenbusch", "rock": "Stein", "pebbles": "Kiesel",
        "tall_grass": "Grasbüschel", "stump": "Baumstumpf", "flowers": "Blumen (drei Farben)",
        "fairy_ring": "Feenring aus Sunnyside-Pilzen",
    }
    try:
        import fetch_vendor
        fetch_vendor.ensure("sunnyside")
    except Exception as exc:  # noqa: BLE001 - offline: vorhandene Dateien bleiben gültig
        print(f"    Sunnyside nicht verfügbar ({exc}); vorhandene Welt-Grafiken bleiben unverändert")
    if SW.available():
        save_png(SW.logic_atlas(), tdir / "meadow_tiles.png")
        save_png(SW.ground_atlas(), tdir / "meadow_ground.png")
        for name, frames in (("tree", SW.tree_frames()), ("tree_pine", SW.pine_frames())):
            strip = Image.new("RGBA", (frames[0].size[0] * len(frames), frames[0].size[1]), TRANSPARENT)
            for i, f in enumerate(frames):
                strip.alpha_composite(f, (i * f.size[0], 0))
            save_png(strip, tdir / f"{name}.png")
        for name, img in SW.objects().items():
            save_png(img, tdir / f"{name}.png")
    return [GeneratedAsset(tdir / f"{n}.png", "tileset", GEN, notes[n], **SUNNY) for n in names]


def build() -> list[GeneratedAsset]:
    out: list[GeneratedAsset] = []
    tdir = ASSETS / "tilesets/mooswiesen"
    out.extend(_sunny_world(tdir))
    fdir = ASSETS / "sprites/fx"
    for name, img, note in (("shadow_small", shadow(10, 4, 16, 8), "Schatten Fee/Hund"),
                            ("shadow_medium", shadow(14, 5, 16, 8), "Schatten Klio"),
                            ("shadow_large", shadow(30, 7, 32, 8), "Schatten Pferd"),
                            ("fx_particles", fx_sheet(), "Partikel 8x8: Funke, Funke groß, Herz, Staub, Licht, Feenstaub"),
                            ("transform_flash", flash(), "Lichtblitz der Verwandlung")):
        p = save_png(img, fdir / f"{name}.png")
        out.append(GeneratedAsset(p, "sprite", GEN, note))
    p = save_png(ui_icons(), ASSETS / "sprites/ui/hud_icons.png")
    out.append(GeneratedAsset(p, "ui", GEN, "HUD-Symbole 16x16: Feenglanz, Flugenergie"))
    return out
