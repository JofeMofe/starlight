"""Klio im Sunnyside-Stil: handgesetzte Pixelkarten in der Endesga-32-Palette.

Die Welt nutzt „Sunnyside World“ (Daniel Diggle, Endesga-32-Farben). Klio ist
etwas größer als die Sunnyside-Figuren (23 px statt 16 px), damit Brille, lange Haare
und Kleidung lesbar bleiben; Umriss, Farbflächen und Schattierung folgen dem
Sunnyside-Aufbau (dunkelvioletter Umriss, flache Flächen, eine Schattenstufe).

Karten: ein Zeichen = ein Pixel, `.` = transparent. Front- und Rückansicht sind
als linke Hälfte notiert und werden gespiegelt. Die Seitenansicht schaut nach
rechts und wird beim Export gespiegelt (das Spiel erwartet links als Grundrichtung).
"""
from __future__ import annotations

import numpy as np
from PIL import Image

# Endesga 32 (Sunnyside-Palette)
PAL: dict[str, str] = {
    "o": "181425",  # Umriss
    "h": "3e2731", "H": "733e39",  # Haare dunkles Schokobraun, Glanz
    "s": "e8b796", "S": "c28569", "p": "f6757a", "G": "b86f50",  # Haut, Schatten, Wange, Mund
    "g": "265c42", "L": "c0cbdc", "r": "5a6988",  # Augen grüngrau, Brillenglas, unterer Rand
    "t": "68386c", "T": "3e2731", "u": "b55088",  # Top schwarz-lila, Akzent
    "j": "8b9bb4", "J": "5a6988", "k": "c0cbdc",  # Jeansjacke hell verwaschen
    "n": "124e89", "N": "262b44",  # Jeans
    "c": "3a4466", "W": "ead4aa",  # Converse: dunkler Stoff, cremige Sohle/Kappe
}

FRONT_HALF = [
    "....oooo",  # 0
    "..oohhhh",  # 1
    ".ohhhHHh",  # 2
    ".ohhHHhs",  # 3  Mittelscheitel
    "ohhHhsss",  # 4
    "ohhhssss",  # 5
    "ohhooooo",  # 6  Brille: oberer Rand
    "ohhoLgLo",  # 7  Glas, Auge, Steg
    "ohhsrrrs",  # 8  unterer Rand (hell, schmale Rechteckbrille)
    "ohhspsss",  # 9  Wange
    "ohhhsssG",  # 10 Mund
    "ohhhSsss",  # 11 Kinn
    "ohhhhhos",  # 12 Hals
    "ohhjjjkt",  # 13 Jeansjacke offen über lila Top
    "ohhjJjkt",  # 14
    "ohhjJjku",  # 15
    ".ohsJokt",  # 16 Hände
    ".oooonnn",  # 17 Jeans
    "...onnnN",  # 18
    "...onnNo",  # 19
    "...occco",  # 20 Converse
    "..oWWWWo",  # 21
    "..oooooo",  # 22
]
BACK_HALF = [
    "....oooo", "..oohhhh", ".ohhhHHh", ".ohhHHhh", "ohhHhhhh", "ohhhhhHh", "ohhhhhHh",
    "ohhHhhhh", "ohhHhhHh", "ohhhhhHh", "ohhhHhhh", "ohhhHhhh", "oohhhhHh",
    "ojohhhHh", "ojohHhhh", "ojohHhhh", ".osohhHh", ".oo.ohhh",
    "...ooohh", "...onnoo", "...occco", "..oWWWWo", "..oooooo",
]
SIDE = [
    ".....oooooo.....",  # 0
    "...oohhhhhhoo...",  # 1
    "..ohhhhHHHhhho..",  # 2
    ".ohhhhHHhhhhsso.",  # 3
    ".ohhhHhhhhsssso.",  # 4
    ".ohhhhhhhssssso.",  # 5
    ".ohhhhhhssoooo..",  # 6  Brille
    ".ohhhhhoooLgLo..",  # 7  Bügel, Glas, Auge
    ".ohhhhhhsssrrso.",  # 8  Nase
    ".ohhhhhhspssso..",  # 9
    ".ohhhhhhhsssGo..",  # 10
    ".ohhhhhhhSsso...",  # 11
    "..ohhhhhhhoso...",  # 12
    "..ohhhhhojjjjo..",  # 13
    "..ohhhhhojJjto..",  # 14
    "...ohhhhojJjto..",  # 15
    "...ohhhhojsjjo..",  # 16
    "....ohhhonnnno..",  # 17
    ".....ooooonnNo..",  # 18
    ".........onnNo..",  # 19
    ".........occco..",  # 20
    ".........oWWWWo.",  # 21
    ".........oooooo.",  # 22
]
# Beinposen Seitenansicht (Frame-Breite, ab Kartenzeile 19); Umriss wird automatisch gezogen
SIDE_LEGS = {
    "pass": [
        "............nnN.....",
        "............ccc.....",
        "............WWWW....",
        "...................."],
    "contact_a": [
        "..........NN.nnn....",
        "..........ccc..ccc..",
        "..........WWW..WWWW.",
        "...................."],
    "contact_b": [
        "..........nn.NNN....",
        "..........ccc..ccc..",
        "..........WWW..WWWW.",
        "...................."],
}
RIDE_SIDE_LEG = [
    "............nnnn....",
    "..............nn....",
    "..............ccc...",
    "..............WWW...",
]
RIDE_FRONT_LEGS = [
    "..nnn..........nnn..",
    "..ccc..........ccc..",
    "..WWW..........WWW..",
    "....................",
]

# Feengestalt: so klein wie eine Blüte, Blütenkleid in Lila, Brille bleibt sichtbar
FAIRY_FRONT_HALF = [
    "..ooo", ".ohhh", "ohhHs", "ohsss",
    "ohooo",  # 4 Brille
    "ohLgo",  # 5
    "ohsss", "ohhos", "ohott", ".ootu", ".ottt", "otTtT", ".oooo", "...os", "...oo",
]
FAIRY_BACK_HALF = [
    "..ooo", ".ohhh", "ohhHh", "ohHhh", "ohhhh", "ohhhH", "ohHhh", "ohhhh", "ohhht",
    ".ohht", ".ottt", "otTtT", ".oooo", "...os", "...oo",
]
FAIRY_SIDE = [
    "..oooo....", ".ohhhhoo..", "ohhHHhhso.", "ohhhhssso.",
    "ohhhoooo..",  # 4 Brille
    "ohhhoLgos.",  # 5
    "ohhhhsso..", ".ohhhoso..", ".ohhottuo.", "..oootto..", "...otttuo.", "..otTtTto.",
    "...ooooo..", ".....os...", ".....oo...",
]
# Libellenflügel: r = zarte Kontur, k = Flügelhaut, j = Ader
WING_UP = ["rr....", "rkrr..", ".rkkkr", ".rkjkr", "..rrrr"]
WING_LOW = ["..rrrr", ".rkjkr", "rkkkr.", "rrr..."]
WING_SIDE_UP = ["rrr...", "rkkrr.", ".rkjkr", "..rrrr"]
WING_SIDE_LOW = ["..rrrr", "rrkjkr", "rkkrr.", "rr...."]

W, H = 20, 24          # Frame Menschengröße
OX, OY = 2, 1          # Lage der 16x23-Karten im Frame (Füße auf der untersten Zeile)
LEG_ROW = 19           # ab dieser Kartenzeile beginnen die Beine
FW, FH = 24, 20        # Frame Feengröße (Körper und Flügel gleich groß)
EYES = {"down": [(5, 7), (10, 7)], "side": [(11, 7)]}
FAIRY_EYES = {"down": [(3, 5), (6, 5)], "side": [(6, 5)]}


def rgba(key: str) -> tuple[int, int, int, int]:
    h = PAL[key]
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


def mirror(half: list[str]) -> list[str]:
    return [r + r[::-1] for r in half]


def render(rows: list[str]) -> np.ndarray:
    w = max(len(r) for r in rows)
    a = np.zeros((len(rows), w, 4), np.uint8)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != ".":
                a[y, x] = rgba(ch)
    return a


def paste(dst: np.ndarray, src: np.ndarray, x: int, y: int) -> None:
    for yy in range(src.shape[0]):
        for xx in range(src.shape[1]):
            if src[yy, xx, 3] and 0 <= y + yy < dst.shape[0] and 0 <= x + xx < dst.shape[1]:
                dst[y + yy, x + xx] = src[yy, xx]


def outlined(rows: list[str]) -> np.ndarray:
    """Füllung plus automatischer 1-px-Umriss; oben offen, damit die Beine an der Hüfte ansetzen."""
    a = render(rows)
    m = a[:, :, 3] > 0
    out = a.copy()
    h, w = m.shape
    for y in range(h):
        for x in range(w):
            if not m[y, x] and any(0 <= x + dx < w and 0 <= y + dy < h and m[y + dy, x + dx]
                                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y, x] = rgba("o")
    out[0][~m[0]] = 0
    return out


def _upper(view: str) -> np.ndarray:
    rows = {"down": mirror(FRONT_HALF), "up": mirror(BACK_HALF), "side": SIDE}[view]
    return render(rows[:LEG_ROW])


def _straight_legs(view: str, lift: str | None) -> np.ndarray:
    """Front-/Rückbeine; lift = 'l'/'r' hebt einen Fuß um 1 px (Schritt)."""
    rows = (mirror(FRONT_HALF) if view == "down" else mirror(BACK_HALF))[LEG_ROW:]
    src = render(rows)
    a = np.zeros((len(rows), W, 4), np.uint8)
    for side, (x0, x1) in (("l", (0, 8)), ("r", (8, 16))):
        dy = -1 if lift == side else 0
        for yy in range(src.shape[0]):
            for xx in range(x0, x1):
                if src[yy, xx, 3] and yy + dy >= 0:
                    a[yy + dy, OX + xx] = src[yy, xx]
        if dy:
            for xx in range(x0, x1):
                if src[0, xx, 3] and not a[0, OX + xx, 3]:
                    a[0, OX + xx] = src[0, xx]
    return a


def _finish(a: np.ndarray, view: str) -> Image.Image:
    img = Image.fromarray(a)
    # Seitenansicht zeigt im Spiel standardmäßig nach links
    return img.transpose(Image.FLIP_LEFT_RIGHT) if view == "side" else img


def human_frame(view: str, pose: str = "pass", bob: int = 0, blink: bool = False) -> Image.Image:
    f = np.zeros((H, W, 4), np.uint8)
    if view == "side":
        paste(f, outlined(SIDE_LEGS[pose]), 0, OY + LEG_ROW)
    else:
        lift = {"pass": None, "contact_a": "l", "contact_b": "r"}[pose]
        paste(f, _straight_legs(view, lift), 0, OY + LEG_ROW)
    up = _upper(view)
    if bob < 0:  # Hüftzeile doppeln, damit beim Hochfedern keine Lücke entsteht
        paste(f, up[-1:], OX, OY + LEG_ROW - 1)
    paste(f, up, OX, OY + bob)
    if blink:
        for x, y in EYES.get(view, []):
            f[OY + y + bob, OX + x] = rgba("r")
    return _finish(f, view)


def ride_frame(view: str, blink: bool = False) -> Image.Image:
    f = np.zeros((H, W, 4), np.uint8)
    paste(f, outlined(RIDE_SIDE_LEG if view == "side" else RIDE_FRONT_LEGS), 0, OY + LEG_ROW)
    paste(f, _upper(view), OX, OY)
    if blink:
        for x, y in EYES.get(view, []):
            f[OY + y, OX + x] = rgba("r")
    return _finish(f, view)


def fairy_frame(view: str, blink: bool = False, bob: int = 0) -> Image.Image:
    rows = {"down": mirror(FAIRY_FRONT_HALF), "up": mirror(FAIRY_BACK_HALF), "side": FAIRY_SIDE}[view]
    body = render(rows)
    f = np.zeros((FH, FW, 4), np.uint8)
    x0 = (FW - body.shape[1]) // 2
    paste(f, body, x0, 4 + bob)
    if blink:
        for x, y in FAIRY_EYES.get(view, []):
            f[4 + bob + y, x0 + x] = rgba("r")
    return _finish(f, view)


def wing_frame(view: str, spread: float) -> Image.Image:
    """Flügelpaare; spread 1 = offen, 0 = angelegt. Halbtransparenz setzt die Szene (modulate)."""
    f = np.zeros((FH, FW, 4), np.uint8)
    d = round((1 - spread) * 2)
    cx = FW // 2
    if view == "side":
        # Seitenansicht (nach rechts): beide Flügel hinter dem Rücken
        up, low = render(WING_SIDE_UP), render(WING_SIDE_LOW)
        paste(f, up, cx - 2 - up.shape[1] + d, 6 + d)
        paste(f, low, cx - 2 - low.shape[1] + d, 11)
    else:
        up, low = render(WING_UP), render(WING_LOW)
        paste(f, up, cx - 3 - up.shape[1] + d, 6 + d)
        paste(f, low, cx - 3 - low.shape[1] + d, 11)
        paste(f, up[:, ::-1], cx + 3 - d, 6 + d)
        paste(f, low[:, ::-1], cx + 3 - d, 11)
    return _finish(f, view)
