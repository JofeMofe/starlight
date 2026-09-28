"""Setzt Klio v4 zu Animationen zusammen (gleiche Namen wie im Spiel erwartet).

Körper-Sheet: idle_* (6 Frames: Atmen, Blinzeln), walk_* (8 Frames),
ride_* (2 Frames, ohne Beine). Haar-Sheet: tail_* mit 5 Schwungstufen.
Fee: fairy_* (normal, blinzeln), Flügel: wings_down/side (6 Frames, lila).
"""
from __future__ import annotations

from PIL import Image

from atlas import Animation
from palette import color
from sl_common import TRANSPARENT, pixelmap
from sprites import klio_art as OLD
from sprites import klio_v4 as V

W, H = 32, 48
UPPER_ROWS = 13  # Oberkörper-Zeilen 22-34 in BODY_DOWN

HEAD = {"down": V.HEAD_DOWN, "up": V.HEAD_UP, "side": V.HEAD_SIDE}
UPPER = {"down": V.BODY_DOWN[:UPPER_ROWS], "up": V.BODY_UP, "side": V.BODY_SIDE}
BLINK = {"down": V.BLINK_DOWN, "side": V.BLINK_SIDE}
TAIL = {"down": (V.TAIL_DOWN, V.TAIL_DOWN_START), "up": (V.TAIL_UP, V.TAIL_UP_START),
        "side": (V.TAIL_SIDE, V.TAIL_SIDE_START)}

IDLE = [(0, False), (0, False), (1, False), (1, False), (0, False), (0, True)]
IDLE_MS = [420, 300, 360, 300, 380, 130]
# Vorn/hinten: (angehobenes Bein, Höhe, Körperversatz)
WALK_FRONT = [("r", 1, 0), ("r", 2, 0), ("r", 1, 0), (None, 0, 1),
              ("l", 1, 0), ("l", 2, 0), ("l", 1, 0), (None, 0, 1)]
WALK_SIDE = [("stride", 0, "forward"), ("stride", 1, "forward"), ("pass", 0, "neutral"),
             ("pass", 0, "neutral"), ("stride", 0, "back"), ("stride", 1, "back"),
             ("pass", 0, "neutral"), ("pass", 0, "neutral")]
WALK_MS = [110, 90, 90, 110, 110, 90, 90, 110]


def _paste(img: Image.Image, grid: list[str], x: int, y: int, legend: dict) -> None:
    img.alpha_composite(pixelmap(grid, legend), (x, y))


def _legs_front(view: str, lifted: str | None, height: int) -> Image.Image:
    grid = V.LEGS_UP if view == "up" else V.LEGS_DOWN
    legs = pixelmap(grid, V.BODY_LEGEND)
    if lifted is None or height == 0:
        return legs
    out = Image.new("RGBA", legs.size, TRANSPARENT)
    split = 16 - 8  # Spalte 16 im Frame = Mitte; Raster beginnt bei x=0
    left = legs.crop((0, 0, split + 8, legs.height))
    right = legs.crop((split + 8, 0, legs.width, legs.height))
    if lifted == "l":
        out.alpha_composite(left, (0, -height))
        out.alpha_composite(right, (split + 8, 0))
    else:
        out.alpha_composite(left, (0, 0))
        out.alpha_composite(right, (split + 8, -height))
    return out


def _upper(view: str, bob: int, blink: bool, arm: str = "neutral") -> Image.Image:
    img = Image.new("RGBA", (W, H), TRANSPARENT)
    head = list(HEAD[view])
    if blink and view in BLINK:
        for idx, row in BLINK[view].items():
            head[idx] = row.replace("|", "")
    if view == "down":
        _paste(img, V.WINGS_DOWN, 0, V.WINGS_DOWN_START + bob, V.WING_LEGEND)
    elif view == "side":
        _paste(img, V.WINGS_SIDE, 0, V.WINGS_SIDE_START + bob, V.WING_LEGEND)
    _paste(img, UPPER[view], 0, 22 + bob, V.BODY_LEGEND)
    if view == "up":
        _paste(img, V.WINGS_DOWN, 0, V.WINGS_DOWN_START + bob, V.WING_LEGEND)
    if view == "side":
        ax, ay = V.SIDE_ARM_POS
        _paste(img, V.SIDE_ARMS[arm], ax, ay + bob, V.BODY_LEGEND)
    _paste(img, head, 0, bob, V.HAIR_LEGEND)
    _paste(img, V.CROWN_DOWN, 0, V.CROWN_DOWN_START + bob, V.CROWN_LEGEND)
    if view == "down":
        _paste(img, V.STRAND_DOWN, 0, V.STRAND_DOWN_START + bob, V.HAIR_LEGEND)
    return img


def human_frame(view: str, legs: tuple, bob: int, blink: bool = False, arm: str = "neutral",
                with_legs: bool = True) -> Image.Image:
    img = Image.new("RGBA", (W, H), TRANSPARENT)
    if with_legs:
        if view == "side":
            _paste(img, V.SIDE_LEGS[legs[0]], V.SIDE_LEGS_X, V.LEGS_START, V.BODY_LEGEND)
        else:
            img.alpha_composite(_legs_front(view, legs[0], legs[1]), (0, V.LEGS_START))
    img.alpha_composite(_upper(view, bob, blink, arm))
    return img


def human_animations() -> list[Animation]:
    anims: list[Animation] = []
    for view in ("down", "up", "side"):
        stand = ("stand",) if view == "side" else (None, 0)
        frames = [human_frame(view, stand, bob, blink and view != "up") for bob, blink in IDLE]
        anims.append(Animation(f"idle_{view}", frames, IDLE_MS, True, {"bob": [b for b, _ in IDLE]}))
    for view in ("down", "up"):
        frames = [human_frame(view, (side, h), bob) for side, h, bob in WALK_FRONT]
        anims.append(Animation(f"walk_{view}", frames, WALK_MS, True, {"bob": [b for _, _, b in WALK_FRONT]}))
    frames = [human_frame("side", (legs,), bob, arm=arm) for legs, bob, arm in WALK_SIDE]
    anims.append(Animation("walk_side", frames, WALK_MS, True, {"bob": [b for _, b, _ in WALK_SIDE]}))
    for view in ("down", "up", "side"):
        frames = [human_frame(view, (None, 0), 0, False, with_legs=False),
                  human_frame(view, (None, 0), 0, view != "up", with_legs=False)]
        anims.append(Animation(f"ride_{view}", frames, [2600, 140], True, {"bob": [0, 0]}))
    # Reihenfolge wie im Spiel-Sheet erwartet: idle_down, idle_up, idle_side, walk_down, ...
    order = ["idle_down", "idle_up", "idle_side", "walk_down", "walk_up", "walk_side",
             "ride_down", "ride_up", "ride_side"]
    by_name = {a.name: a for a in anims}
    return [by_name[n] for n in order]


SWAYS = [-2, -1, 0, 1, 2]


def tail_frame(view: str, sway: int) -> Image.Image:
    grid, start = TAIL[view]
    src = pixelmap(grid, V.HAIR_LEGEND)
    img = Image.new("RGBA", (W, H), TRANSPARENT)
    h = len(grid)
    for i in range(h):
        shift = round(sway * (i / max(h - 1, 1)) ** 1.5)
        img.alpha_composite(src.crop((0, i, src.width, i + 1)), (shift, start + i))
    return img


def tail_animations() -> list[Animation]:
    return [Animation(f"tail_{view}", [tail_frame(view, s) for s in SWAYS], [100] * 5, False,
                      {"sway": SWAYS}) for view in ("down", "up", "side")]


FAIRY = {"down": V.FAIRY_DOWN, "up": V.FAIRY_UP, "side": V.FAIRY_SIDE}


def fairy_frame(view: str, blink: bool) -> Image.Image:
    img = Image.new("RGBA", (16, 20), TRANSPARENT)
    grid = list(FAIRY[view])
    if blink and view in V.FAIRY_BLINK:
        for idx, row in V.FAIRY_BLINK[view].items():
            grid[idx] = row
    _paste(img, grid, 2, 1, V.FAIRY_LEGEND)
    return img


def fairy_animations() -> list[Animation]:
    return [Animation(f"fairy_{view}", [fairy_frame(view, False), fairy_frame(view, True)],
                      [3000, 140], True) for view in ("down", "up", "side")]


WING_LEGEND = {"W": color("fae", 4), "V": color("fae", 3), "F": color("sky", 6)}
WING_CYCLE = ["up", "mid", "down", "down", "mid", "up"]
WING_MS = [70, 40, 50, 70, 60, 60]


def wing_animations() -> list[Animation]:
    out = []
    for view in ("down", "side"):
        art = OLD.FAIRY_WINGS_SIDE if view == "side" else OLD.FAIRY_WINGS_DOWN
        frames = []
        for pose in WING_CYCLE:
            img = Image.new("RGBA", (16, 20), TRANSPARENT)
            _paste(img, art[pose], 0, OLD.FAIRY_WINGS_Y - 4, WING_LEGEND)
            frames.append(img)
        out.append(Animation(f"wings_{view}", frames, WING_MS, True))
    return out
