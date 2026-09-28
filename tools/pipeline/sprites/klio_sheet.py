"""Setzt Klios Pixelkarten zu Animationsframes zusammen."""
from __future__ import annotations

from PIL import Image

from atlas import Animation
from sl_common import TRANSPARENT, pixelmap
from sprites import klio_art as A

FRAME_W, FRAME_H = 32, 48
FAIRY_W, FAIRY_H = 16, 20

VIEWS = ("down", "up", "side")

HEAD = {"down": A.DOWN_HEAD, "up": A.UP_HEAD, "side": A.SIDE_HEAD}
BODY = {"down": A.DOWN_BODY, "up": A.UP_BODY, "side": A.SIDE_BODY}
TAIL = {"down": (A.DOWN_TAIL, A.DOWN_TAIL_START), "up": (A.UP_TAIL, A.UP_TAIL_START),
        "side": (A.SIDE_TAIL, A.SIDE_TAIL_START)}
BLINK = {"down": A.DOWN_BLINK, "side": A.SIDE_BLINK}
WINGS = {"down": A.HUMAN_WINGS_DOWN, "up": A.HUMAN_WINGS_UP, "side": A.HUMAN_WINGS_SIDE}

# Laufzyklus (8 Frames): Beinstellung, Körperversatz (1 = 1 px tiefer), Arm (Seite)
WALK_DOWN = [("left_step", 0), ("left_step", 1), ("stand", 0), ("stand", 0),
             ("right_step", 0), ("right_step", 1), ("stand", 0), ("stand", 0)]
WALK_SIDE = [("stride", 0, "forward"), ("stride", 1, "forward"), ("pass", 0, "neutral"),
             ("pass", 0, "neutral"), ("stride", 0, "back"), ("stride", 1, "back"),
             ("pass", 0, "neutral"), ("pass", 0, "neutral")]
WALK_MS = [110, 90, 90, 110, 110, 90, 90, 110]
# Stehen: Atmen (Körper sinkt 1 px) und kurzes Blinzeln am Ende
IDLE = [(0, False), (0, False), (1, False), (1, False), (0, False), (0, True)]
IDLE_MS = [420, 300, 360, 300, 380, 130]


def _paste(img: Image.Image, rows: list[str], x: int, y: int, legend: dict) -> None:
    img.alpha_composite(pixelmap(rows, legend), (x, y))


def human_frame(view: str, legs: str | None, bob: int, blink: bool = False,
                arm: str = "neutral") -> Image.Image:
    """Körperebene (Kopf, Körper, Flügel, Beine) ohne lange Haare."""
    img = Image.new("RGBA", (FRAME_W, FRAME_H), TRANSPARENT)
    ox, oy = A.X_OFFSET, A.Y_OFFSET
    head = list(HEAD[view])
    if blink and view in BLINK:
        for idx, row in BLINK[view].items():
            head[idx] = row
    wings_y = oy + A.HUMAN_WINGS_Y + bob
    if view != "up":  # Flügel hinter dem Körper
        _paste(img, WINGS[view], ox, wings_y, A.LEGEND)
    if legs is not None:
        leg_rows = (A.SIDE_LEGS if view == "side" else A.DOWN_LEGS)[legs]
        _paste(img, leg_rows, ox, oy + 34, A.LEGEND)
    _paste(img, BODY[view], ox, oy + 18 + bob, A.LEGEND)
    if view == "side":
        ax, ay = A.SIDE_ARM_POS
        _paste(img, A.SIDE_ARMS[arm], ox + ax, oy + ay + bob, A.LEGEND)
    _paste(img, head, ox, oy + bob, A.LEGEND)
    if view == "up":  # auf dem Rücken, unter den Haaren
        _paste(img, WINGS[view], ox, wings_y, A.LEGEND)
    return img


def tail_frame(view: str, sway: int) -> Image.Image:
    """Lange Haare mit seitlichem Nachschwingen. `sway` in Pixeln an der Spitze,
    nach oben hin abnehmend (die Wurzel bleibt am Kopf)."""
    rows, start = TAIL[view]
    img = Image.new("RGBA", (FRAME_W, FRAME_H), TRANSPARENT)
    src = pixelmap(rows, A.LEGEND)
    h = len(rows)
    for i in range(h):
        shift = round(sway * (i / max(h - 1, 1)) ** 1.5)
        line = src.crop((0, i, src.width, i + 1))
        img.alpha_composite(line, (A.X_OFFSET + shift, A.Y_OFFSET + start + i))
    return img


def human_animations() -> list[Animation]:
    anims: list[Animation] = []
    for view in VIEWS:
        frames = [human_frame(view, "stand", bob, blink) for bob, blink in IDLE]
        anims.append(Animation(f"idle_{view}", frames, IDLE_MS, True,
                               {"bob": [b for b, _ in IDLE]}))
    for view in VIEWS:
        if view == "side":
            frames = [human_frame(view, legs, bob, arm=arm) for legs, bob, arm in WALK_SIDE]
            bobs = [b for _, b, _ in WALK_SIDE]
        else:
            frames = [human_frame(view, legs, bob) for legs, bob in WALK_DOWN]
            bobs = [b for _, b in WALK_DOWN]
        anims.append(Animation(f"walk_{view}", frames, WALK_MS, True, {"bob": bobs}))
    # Reiten: Beine verdeckt das Pferd; zwei Frames (normal, blinzeln)
    for view in VIEWS:
        frames = [human_frame(view, None, 0), human_frame(view, None, 0, blink=True)]
        anims.append(Animation(f"ride_{view}", frames, [2600, 140], True, {"bob": [0, 0]}))
    return anims


SWAYS = [-2, -1, 0, 1, 2]


def tail_animations() -> list[Animation]:
    return [Animation(f"tail_{view}", [tail_frame(view, s) for s in SWAYS],
                      [100] * len(SWAYS), False, {"sway": SWAYS}) for view in VIEWS]


# --- Fee -------------------------------------------------------------------

FAIRY_ART = {"down": A.FAIRY_DOWN, "up": A.FAIRY_UP, "side": A.FAIRY_SIDE}
FAIRY_BLINK = {
    "down": {5: ".HmGkkkkGmH."},
    "side": {5: ".SGkhmmmmmH."},
}


def fairy_frame(view: str, blink: bool = False) -> Image.Image:
    img = Image.new("RGBA", (FAIRY_W, FAIRY_H), TRANSPARENT)
    rows = list(FAIRY_ART[view])
    if blink and view in FAIRY_BLINK:
        for idx, row in FAIRY_BLINK[view].items():
            rows[idx] = row
    _paste(img, rows, A.FAIRY_X_OFFSET, A.FAIRY_Y_OFFSET, A.FAIRY_LEGEND)
    return img


def fairy_animations() -> list[Animation]:
    return [Animation(f"fairy_{view}", [fairy_frame(view), fairy_frame(view, True)],
                      [3000, 140], True) for view in VIEWS]


WING_CYCLE = ["up", "mid", "down", "down", "mid", "up"]
WING_MS = [70, 40, 50, 70, 60, 60]


def wing_frame(view: str, pose: str) -> Image.Image:
    img = Image.new("RGBA", (FAIRY_W, FAIRY_H), TRANSPARENT)
    art = A.FAIRY_WINGS_SIDE if view == "side" else A.FAIRY_WINGS_DOWN
    _paste(img, art[pose], 0, A.FAIRY_WINGS_Y - 4, A.LEGEND)
    return img


def wing_animations() -> list[Animation]:
    return [Animation(f"wings_{view}", [wing_frame(view, p) for p in WING_CYCLE], WING_MS, True)
            for view in ("down", "side")]
