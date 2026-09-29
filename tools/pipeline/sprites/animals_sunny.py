"""Pferd und Hund im Sunnyside-Tierstil: handgesetzte Pixelkarten (Endesga 32).

Sunnyside World enthält keine Pferde und Hunde. Diese Figuren folgen dem Aufbau
der Sunnyside-Tiere (rundlich, dunkler Umriss, eine Schattenstufe) und sind so
groß, dass Klio (23 px) darauf reiten kann. Seitenansichten sind nach rechts
gezeichnet und werden beim Export gespiegelt (Grundrichtung im Spiel: links).

Fellfarben liegen als Rampen vor (c/C/L Fell, M/m Mähne), damit spätere
Fellgenetik (M3) nur die Rampe tauschen muss.
"""
from __future__ import annotations

import numpy as np
from PIL import Image

from sprites.klio_sunny import PAL, mirror

HORSE_PAL = dict(PAL, c="733e39", C="b86f50", L="e4a672", M="3e2731", m="733e39", w="ead4aa", k="3e2731")
DOG_PAL = dict(PAL, B="3a4466", b="5a6988", T="b86f50", W="c0cbdc")

HORSE_SIDE_BODY = [
    "....................................",
    "..........................oo..oo....",
    ".........................oCo.oCo....",
    "........................oMMCCCCCo...",
    ".......................oMmMCCCCCCo..",
    "......................oMmMCCCoCCCCo.",  # Auge
    ".....................oMmMcCCCCCwCCCo",
    "....................oMmMcCCCCCCCLLLo",
    "...................oMmMccCCCCCCCLLco",  # Nüster
    ".......ooooooooooooMmMccCCCCCoLLLLo.",
    "......oMMCCCCCCCCCCMcCCCCCCCooooo...",
    ".....oMmMoLLLLLCCCCCCCCCCCCCCo......",
    ".....oMmoCCCCCCCCCCCCCCCCCCCCCo.....",
    "....oMmMoCCCCCCCCCCCCCCCCCCCCCo.....",
    "....oMmMocCCCCCCCCCCCCCCCCCCCco.....",
    "....oMmo.occCCCCCCCCCCCCCCCCcco.....",
    "....oMmo.occcCCCCCCCCCCCCCCCccco....",
    "....oMmo..occcccccccccccccccco......",
]
HORSE_SIDE_LEGS = {
    "stand": [
        "....oMo...ocCo.oco...oco.ocCo.......",
        ".....oo...ocCo.oco...oco.ocCo.......",
        "..........ocCo.oco...oco.ocCo.......",
        "..........ocCo.oko...oko.ocCo.......",
        "..........okko.ooo...ooo.okko.......",
        "..........oooo...........oooo......."],
    "reach": [  # Beine gestreckt (Schritt/Galopp-Sprungphase)
        "....oMo..ocCo..oco...oco..ocCo......",
        ".....oo.ocCo...oco...oco...ocCo.....",
        "........ocCo...oko...oko....ocCo....",
        ".......ocCo....ooo...ooo....okko....",
        ".......okko..................oooo...",
        ".......oooo........................."],
    "gather": [  # Beine untergesetzt
        "....oMo...oco.ocCo.ocCo..oco........",
        ".....oo...oco..ocCo.ocCo.oco........",
        "..........oko..ocCo.ocCo.oko........",
        "..........ooo..okko.okko.ooo........",
        "................oooooooo............",
        "...................................."],
}
HORSE_FRONT_HALF = [
    "..........", ".....oo...", ".....oCo..", "....oCCoMM", "....oCCCMm", "....oCCCCM", "....oCCCCC",
    "....ooCCCw",  # Auge
    "....oCCCCw", ".....oCCCw", ".....oLLLL", ".....oLLcL", "..ooooLLLL", ".oCCCCoooo",
    ".oCCCCCCCC", ".ocCCCCCCC", ".occCCCCCC", "..occccccc",
    "....ocCo..", "....ocCo..", "....ocCo..", "....ocCo..", "....okko..", "....oooo..",
]
HORSE_BACK_HALF = [
    "..........", "..........", "......oo..", ".....oCo..", ".....oCCoM", "......oCCM", ".......oCM",
    "...ooooCCM", "..oCLLCCCC", ".oCLLCCCCC", ".oCCCCCCoM", "oCCCCCCCoM", "oCCCCCCCom", "ocCCCCCCoM",
    "occCCCCCoM", ".occccccoM",
    "..ocCo..om", "..ocCo..oM", "..ocCo..oo", "..ocCo....", "..ocCo....", "..ocCo....", "..okko....", "..oooo....",
]
HORSE_W, HORSE_H = 40, 24
HORSE_LEG_ROW = 18

DOG_SIDE_BODY = [
    "............ooo.....",
    "...........oBBBoo...",
    "...........oBBbBBo..",
    "..........oBBBBBBBo.",
    "..........oBBBBoBWo.",  # Auge
    "..........oBBTTBWWWo",
    "..oo......oBTTWWWWoo",  # Nase
    ".oWWo.....ooBWWWWo..",
    ".oBBo.ooooooBWWWo...",
    "..oBBoBBbbBBBWWWo...",
    "...oBBBBBBBBBWWWo...",
    "....oBBBBBBBBBWWo...",
    "....oBTBBBBBBTWo....",
]
DOG_SIDE_LEGS = {
    "stand": ["....oWWo...oWWo.....", "....oWWo...oWWo.....", "....oooo...oooo....."],
    "reach": ["...oWWo.....oWWo....", "..oWWo.......oWWo...", "..ooo.........ooo..."],
    "gather": [".....oWWo.oWWo......", "......oWWoWWo.......", "......ooooooo......."],
}
DOG_SIT_SIDE_LEGS = ["....oWWBBBoWWo......", "...oWWWWooooWWo.....", "...oooooo..ooo......"]
DOG_FRONT_HALF = [
    ".ooo..", ".oBBoo", ".oBBBB", "oBBBBB", "oBBoBW", "oBTBWW", "oTTWWW", ".oTWWo",
    "..oWWW", "..ooWW", ".oBBWW", ".oBBWW", ".oBTWW", "..oWWo", "..oWWo", "..oooo",
]
DOG_BACK_HALF = [
    ".ooo..", ".oBBoo", ".oBBBB", "oBBBBB", "oBBBBB", "oBBBBB", "oBBBBB", ".oBBBB",
    ".oBBBo", ".oBBoW", ".oBBoB", ".oBBoB", ".oBTBo", "..oWWo", "..oWWo", "..oooo",
]
DOG_W, DOG_H = 20, 16
DOG_LEG_ROW = 13


def _render(rows: list[str], pal: dict[str, str]) -> np.ndarray:
    w = max(len(r) for r in rows)
    a = np.zeros((len(rows), w, 4), np.uint8)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != ".":
                h = pal[ch]
                a[y, x] = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
    return a


def _canvas(a: np.ndarray, w: int, h: int, dy: int = 0) -> np.ndarray:
    out = np.zeros((h, w, 4), np.uint8)
    x0 = (w - a.shape[1]) // 2
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            if a[y, x, 3] and 0 <= y + dy < h:
                out[y + dy, x0 + x] = a[y, x]
    return out


def _lift(a: np.ndarray, leg_row: int, side: str) -> np.ndarray:
    """Hebt in Front-/Rückansicht die Beine einer Körperhälfte um 1 px (Schritt)."""
    out = a.copy()
    half = a.shape[1] // 2
    xs = range(0, half) if side == "l" else range(half, a.shape[1])
    for x in xs:
        col = a[leg_row:, x].copy()
        out[leg_row:, x] = 0
        out[leg_row:leg_row + col.shape[0] - 1, x] = col[1:]
    return out


def _shift(a: np.ndarray, dy: int) -> np.ndarray:
    """Ganzes Tier anheben (Schwebephase im Trab/Galopp)."""
    if dy == 0:
        return a
    out = np.zeros_like(a)
    out[:dy] = a[-dy:] if dy < 0 else out[:dy]
    return out if dy < 0 else a


def _img(a: np.ndarray, flip: bool) -> Image.Image:
    img = Image.fromarray(a)
    return img.transpose(Image.FLIP_LEFT_RIGHT) if flip else img


def horse_frame(view: str, legs: str = "stand", bob: int = 0) -> Image.Image:
    """view: side/down/up; legs: stand/reach/gather (Seite) bzw. stand/l/r (Front/Rücken)."""
    if view == "side":
        body = _render(HORSE_SIDE_BODY, HORSE_PAL)
        leg = _render(HORSE_SIDE_LEGS[legs], HORSE_PAL)
        a = np.zeros((HORSE_H, HORSE_W, 4), np.uint8)
        x0 = (HORSE_W - leg.shape[1]) // 2
        a[HORSE_LEG_ROW:, x0:x0 + leg.shape[1]] = leg
        for y in range(body.shape[0]):
            for x in range(body.shape[1]):
                if body[y, x, 3]:
                    a[y, x0 + x] = body[y, x]
        return _img(_shift(a, bob), True)
    rows = mirror(HORSE_FRONT_HALF if view == "down" else HORSE_BACK_HALF)
    a = _render(rows, HORSE_PAL)
    if legs in ("l", "r"):
        a = _lift(a, HORSE_LEG_ROW, legs)
    return _img(_canvas(a, HORSE_W, HORSE_H, bob), False)


def dog_frame(view: str, legs: str = "stand", bob: int = 0, sit: bool = False) -> Image.Image:
    if view == "side":
        body = _render(DOG_SIDE_BODY, DOG_PAL)
        leg = _render(DOG_SIT_SIDE_LEGS if sit else DOG_SIDE_LEGS[legs], DOG_PAL)
        a = np.zeros((DOG_H, DOG_W, 4), np.uint8)
        a[DOG_LEG_ROW:] = leg
        for y in range(body.shape[0]):
            for x in range(body.shape[1]):
                if body[y, x, 3] and 0 <= y + (1 if sit else 0) < DOG_H:
                    a[y + (1 if sit else 0), x] = body[y, x]
        return _img(_shift(a, bob), True)
    rows = mirror(DOG_FRONT_HALF if view == "down" else DOG_BACK_HALF)
    a = _render(rows, DOG_PAL)
    if legs in ("l", "r"):
        a = _lift(a, DOG_LEG_ROW, legs)
    return _img(_canvas(a, DOG_W, DOG_H, bob), False)
