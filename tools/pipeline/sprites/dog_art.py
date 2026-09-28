"""Seelenhund (Tricolor-Collie-Mix), handgesetzte Pixelkarten 32x24.

Kopf, Halskrause, Rumpf und Rute sind von Hand gezeichnet; nur die Beine
kommen aus dem Rig (dog_rig.py), damit Schritt und Rennen weich animiert
bleiben. Merkmale: Schlappohren, bernsteinfarbene Augen mit Glanzpunkt,
lohfarbene Brauen und Wangen, weiße Blesse, weiße Halskrause, lila
Halsband mit goldener Marke (passend zu Klio).

Die Rute wird per Scherung gewedelt: obere Zeilen verschieben sich
stärker als die Wurzel.
"""
from __future__ import annotations

from PIL import Image

from palette import color

LEGEND = {
    # schwarzes Fell: Umriss, Schatten, Grund, Licht, Glanz
    "O": color("dusk", 0), "x": color("bark", 0), "b": color("stone", 0), "B": color("stone", 1),
    "h": color("stone", 2),
    # weiß: Spitzlicht, hell, Schatten, tiefer Schatten
    "w": color("dusk", 6), "W": color("stone", 5), "v": color("stone", 4), "V": color("stone", 3),
    # loh
    "t": color("bark", 4), "T": color("bark", 5),
    # Augen, Nase, Zunge
    "e": color("dusk", 0), "a": color("ember", 1), "g": color("dusk", 6), "N": color("dusk", 0),
    "p": color("rose", 3), "P": color("rose", 2),
    # Halsband, Marke
    "c": color("fae", 2), "C": color("fae", 1), "y": color("ember", 4),
}


def rows(grid: str) -> list[str]:
    out = []
    for line in grid.strip("\n").splitlines():
        line = line.split("#", 1)[0].strip().replace("|", "")
        if line:
            out.append(line)
    return out


# Seitenansicht, Blick nach links. Beine fehlen (Rig), Rute eigene Ebene.
SIDE = rows("""
....|....|....|....|....|....|....|....   # 0
....|.OOO|OO..|....|....|....|....|....   # 1
....|OBhB|BbOO|....|....|....|....|....   # 2
...O|BhBb|bbOx|xO..|....|....|....|....   # 3
..Ow|Bbbb|bbOx|bxO.|....|....|....|....   # 4
.Oww|bTTb|bbbO|xxO.|....|....|....|....   # 5
Owww|bgeb|bbbb|OxwO|....|....|....|....   # 6
Nwww|beaT|bbbb|bOww|O...|....|....|....   # 7
NNWw|WTtt|bbbb|bbww|wOOO|OOOO|....|....   # 8
.OOO|WTtt|bbbb|bbwW|wcBB|BhBB|BBO.|....   # 9
..Op|OWtt|tbbb|bwwW|cwbb|bbbb|bBBx|O...   # 10
...O|pOwt|tbbw|wwWc|wwbb|bbbb|bbbb|xO..   # 11
....|O.OW|wwww|wwCW|wvbb|bBbb|bbbb|xO..   # 12
....|...O|wwww|Wywv|xbbb|bbbb|bbbx|xO..   # 13
....|...O|WwWw|WvWv|xxbb|bbbb|bbxx|O...   # 14
....|....|OWvW|vvvO|xxxx|xxxx|xxxO|....   # 15
....|....|.OVv|VOOO|OOOO|OOOO|OOO.|....   # 16
""")

# Rute Seitenansicht: 6 breit, Wurzel unten links auf der Kruppe
TAIL_SIDE = rows("""
..OO..
.OwWO.
.OWvxO
.ObBxO
.ObbxO
ObBbxO
ObbxO.
bbxO..
bxO...
""")
TAIL_SIDE_POS = (25, 1)

# Vorderansicht: linke Hälfte, wird gespiegelt; Asymmetrien danach
_FRONT_LEFT = rows("""
....|....|....|OOOO   # 0
....|....|..OO|Bhbb   # 1
....|....|.OBh|bbbw   # 2
....|....|OxOB|bbbw   # 3
....|...O|xxOT|bbww   # 4
....|...O|xbOg|ebww   # 5
....|...O|xbOe|abww   # 6
....|...O|xxOT|twww   # 7
....|....|OxOt|twwN   # 8
....|....|OxOt|wwWO   # 9
....|....|.OOO|tWww   # 10
....|....|OvWw|OOWw   # 11
....|...O|vWww|wwOw   # 12
....|...O|vWww|wwwc   # 13
....|...O|bvWw|wwWc   # 14
....|...O|bbvW|wwWw   # 15
....|...O|xbOv|Wwww   # 16
....|....|OOOO|OOOO   # 17
""")

_BACK_LEFT = rows("""
....|....|....|OOOO   # 0
....|....|..OO|Bhbb   # 1
....|....|.OBh|bbbb   # 2
....|....|OxOB|bbbb   # 3
....|...O|xxOB|bbbb   # 4
....|...O|xbOb|bbbb   # 5
....|...O|xbOb|bbbb   # 6
....|...O|xxOx|bbbb   # 7
....|....|OxOx|xbbb   # 8
....|....|OWwW|wWww   # 9
....|...O|vccc|Cccc   # 10
....|...O|WwwW|wwWw   # 11
....|...O|bBBh|hBBb   # 12
....|...O|bbbb|bbbb   # 13
....|...O|bbbb|bbbb   # 14
....|...O|xbbb|bbbb   # 15
....|...O|xxbb|bbbb   # 16
....|....|OOOO|OOOO   # 17
""")

# Rute von hinten: hängt entspannt zwischen den Hinterbeinen, Spitze pendelt
TAIL_BACK = rows("""
.bb.
ObbO
ObBO
ObbO
OxbO
OWvO
OwWO
.OO.
""")
TAIL_BACK_POS = (14, 13)


# Sitzen, Seitenansicht (Kopf wie SIDE, Körper aufrecht)
SIT = rows("""
....|....|....|....|....|....|....|....   # 0
....|.OOO|OO..|....|....|....|....|....   # 1
....|OBhB|BbOO|....|....|....|....|....   # 2
...O|BhBb|bbOx|xO..|....|....|....|....   # 3
..Ow|Bbbb|bbOx|bxO.|....|....|....|....   # 4
.Oww|bTTb|bbbO|xxO.|....|....|....|....   # 5
Owww|bgeb|bbbb|OxwO|....|....|....|....   # 6
Nwww|beaT|bbbb|bOww|O...|....|....|....   # 7
NNWw|WTtt|bbbb|bbww|wO..|....|....|....   # 8
.OOO|WTtt|bbbb|bbwW|wcOO|....|....|....   # 9
..Op|OWtt|tbbb|bwwW|cwBh|OO..|....|....   # 10
...O|pOwt|tbbw|wwWc|wwbB|hbO.|....|....   # 11
....|O.OW|wwww|wwCW|wvbb|BbbO|....|....   # 12
....|...O|wwww|Wywv|xbbb|bBbb|O...|....   # 13
....|...O|WwWw|WvWv|xbbb|bbbb|bO..|....   # 14
....|...O|WwWv|vWvO|xbbb|bbbb|bxO.|....   # 15
....|....|OWwv|OWwv|Oxbb|bbbb|bxO.|....   # 16
....|....|OWwv|OWwv|Oxbb|bbbb|bxO.|....   # 17
....|....|OWwv|OWwv|Oxxb|bbbb|xxO.|....   # 18
....|....|OWwv|OWwv|OxxW|wvxx|xxO.|....   # 19
....|....|OWWv|OWWv|OWwW|wvOx|xO..|....   # 20
....|....|OWWv|OWWv|OWWw|vvOO|O...|....   # 21
....|....|OOOO|OOOO|OOOO|OOO.|....|....   # 22
""")

# Rute im Sitzen: liegt am Boden und fegt hin und her
TAIL_SIT = [
    rows("""
........
.OOOOOO.
ObbbbwwO
.OOOOOO.
"""),
    rows("""
......OO
.OOOOOwO
ObbbBvO.
.OOOOO..
"""),
]
TAIL_SIT_POS = (22, 19)


def _mirror(left: list[str]) -> list[str]:
    out = []
    for r in left:
        r = r.ljust(16, ".")
        out.append(r + r[::-1])
    return out


def _front() -> list[str]:
    grid = [list(r) for r in _mirror(_FRONT_LEFT)]
    # Glanzpunkt oben links in beiden Augen (Licht von oben links)
    grid[5][19], grid[5][20] = "g", "e"
    # Zunge leicht asymmetrisch, Marke am Halsband
    grid[10][15], grid[10][16] = "p", "p"
    grid[11][15], grid[11][16] = "p", "P"
    grid[14][16] = "y"
    return ["".join(r) for r in grid]


FRONT = _front()
BACK = _mirror(_BACK_LEFT)


def paint(img: Image.Image, grid: list[str], x0: int, y0: int) -> None:
    px = img.load()
    for y, r in enumerate(grid):
        for x, ch in enumerate(r):
            if ch == ".":
                continue
            X, Y = x0 + x, y0 + y
            if 0 <= X < img.width and 0 <= Y < img.height:
                px[X, Y] = LEGEND[ch]


def shear(grid: list[str], lean: float, fixed_rows: int, hanging: bool = False) -> list[str]:
    """Obere Zeilen seitlich versetzen (Wedeln); die untersten fixed_rows bleiben.
    hanging=True: umgekehrt, die Wurzel sitzt oben und die Spitze pendelt."""
    if hanging:
        return shear(grid[::-1], lean, fixed_rows)[::-1]
    n = len(grid) - fixed_rows
    pad = 3
    out = []
    for i, r in enumerate(grid):
        s = round(lean * (n - i) / n) if i < n else 0
        out.append("." * (pad + s) + r + "." * (pad - s))
    return out
