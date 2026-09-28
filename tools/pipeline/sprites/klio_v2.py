"""Klio v2 – Qualitäts-Durchgang (Ansicht von vorn, 32x48).

Raster sind in 8 Vierergruppen geschrieben ("....|....|..."), damit jede
Spalte eindeutig zählbar ist; die Trennstriche werden beim Laden entfernt.
Ebenen: KOPF (inkl. Haaransatz), KÖRPER (komplett, ohne Haare), SträHNEN
(lange Haare vor den Schultern, eigene Ebene für Sekundäranimation).

Farbidee: warmes Kastanienbraun (7 Stufen), senfgelbe Strickjacke,
cremefarbene Bluse mit roter Schleife, marineblauer Faltenrock,
pflaumenfarbene Strumpfhose, braune Stiefel. Licht von oben links,
selektive Umrisse (hellere Linie an beleuchteten Kanten).
"""
from __future__ import annotations

from palette import color

LEGEND = {
    # Haare: O Umriss, 1..6 dunkel -> Glanz
    "O": color("bark", 0), "1": color("bark", 1), "2": color("bark", 2), "3": color("bark", 3),
    "4": color("bark", 4), "5": color("bark", 5), "6": color("bark", 6),
    # Haut
    "s": color("skin", 0), "d": color("skin", 1), "e": color("skin", 2), "k": color("skin", 3),
    "K": color("skin", 4),
    # Augen, Brille, Wangen, Mund
    "p": color("dusk", 0), "i": color("moss", 2), "j": color("moss", 4), "w": color("dusk", 6),
    "g": color("dusk", 3), "G": color("dusk", 2), "r": color("sky", 6), "b": color("rose", 5), "m": color("rose", 2),
    # Bluse
    "B": color("dusk", 6), "c": color("stone", 5), "C": color("stone", 4),
    # Strickjacke (Senf)
    "Y": color("ember", 3), "y": color("ember", 2), "u": color("ember", 1), "U": color("ember", 0),
    # Rock (Marine)
    "A": color("sky", 3), "a": color("sky", 2), "z": color("sky", 1), "Z": color("sky", 0),
    # Strumpfhose
    "Q": color("dusk", 0), "t": color("dusk", 2), "T": color("dusk", 3),
    # Stiefel
    "x": color("bark", 2), "X": color("bark", 3), "R": color("bark", 5),
    # Schleife hell
    "P": color("rose", 3),
    # Blütenkranz
    "f": color("rose", 6), "h": color("rose", 7), "o": color("ember", 4), "v": color("moss", 4),
    "V": color("moss", 5), "L": color("fae", 4), "l": color("fae", 3),
    # Flügel (hell, wirken durchscheinend): E Kontur, W Rand, n Fläche, N Feen-Rosé
    "E": color("sky", 4), "W": color("sky", 6), "n": color("sky", 5), "N": color("fae", 4),
}


def rows(grid: str) -> list[str]:
    out = []
    for line in grid.strip("\n").splitlines():
        line = line.split("#", 1)[0].strip().replace("|", "")
        if line:
            out.append(line)
    return out


HEAD_DOWN = rows("""
....|....|....|....|....|....|....|....   # 0
....|....|....|....|....|....|....|....   # 1
....|....|....|1OOO|OOOO|....|....|....   # 2
....|....|..14|5543|3332|2O..|....|....   # 3
....|....|.145|6654|3333|22O.|....|....   # 4
....|....|O345|5654|4333|322O|....|....   # 5
....|...O|2344|5543|4333|3321|O...|....   # 6
....|...O|2334|4433|3433|3221|O...|....   # 7
....|..O2|3233|3343|3334|3322|1O..|....   # 8
....|..O2|2322|3332|3323|3322|1O..|....   # 9
....|..O2|322K|22k3|2k23|k223|1O..|....   # 10
....|..O2|3kGG|GGkk|kkGG|GG23|2O..|....   # 11
....|..O2|3grp|pKgG|Ggrp|pKg3|2O..|....   # 12
....|..O4|3gKw|iKgk|kgKw|iKg3|2O..|....   # 13
....|..O4|3gki|jkgk|kgki|jkg3|1O..|....   # 14
....|..O3|4gkk|kkgk|egkk|kkg2|1O..|....   # 15
....|..O2|3bgg|ggkk|ekgg|ggb3|2O..|....   # 16
....|..O2|3kbb|kkek|kekk|bbk3|2O..|....   # 17
....|..O4|3ekk|kkkm|mkkk|kke3|2O..|....   # 18
....|..O4|42ek|kkkk|kkkk|ke22|1O..|....   # 19
....|..O3|421s|ekkk|kkke|s122|1O..|....   # 20
....|..O2|3321|ssdd|ddss|1233|2O..|....   # 21
""")

BODY_DOWN = rows("""
....|....|..Uu|uBBe|eBBu|uU..|....|....   # 22
....|....|.UYy|yBcm|mcBu|uuU.|....|....   # 23
....|....|UYyu|yyBP|ccuu|UyuU|....|....   # 24
....|....|UYyu|YyBB|Bcuu|UyuU|....|....   # 25
....|....|UYyu|yyBB|ccuu|UyuU|....|....   # 26
....|....|UYyu|YyBB|Bcuu|UyuU|....|....   # 27
....|....|UYyu|uuBB|ccuu|UyuU|....|....   # 28
....|....|UYyu|YuBB|ccuu|UyuU|....|....   # 29
....|....|UYyU|yuCC|CCuy|UyuU|....|....   # 30
....|....|UuyU|UUUU|UUUU|UyuU|....|....   # 31
....|....|sKks|ZAaa|aazZ|skes|....|....   # 32
....|....|.ssZ|AAaz|aazz|Zss.|....|....   # 33
....|....|..ZA|Aaaz|aaaz|zZ..|....|....   # 34
....|....|.ZAA|azaa|zaaz|zzZ.|....|....   # 35
....|....|.ZAa|azaa|zaaz|azZ.|....|....   # 36
....|....|ZAAa|zaaa|zaaa|zzzZ|....|....   # 37
....|....|ZAAa|zaaa|zaaz|azzZ|....|....   # 38
....|....|.ZZZ|ZZZZ|ZZZZ|ZZZ.|....|....   # 39
....|....|...Q|tTQ.|.QtT|Q...|....|....   # 40
....|....|...Q|tTQ.|.QtT|Q...|....|....   # 41
....|....|..OX|RxO.|.OXR|xO..|....|....   # 42
....|....|..OX|XxO.|.OXX|xO..|....|....   # 43
....|....|..OX|XxO.|.OXX|xO..|....|....   # 44
....|....|.OXX|XxO.|.OXX|xxO.|....|....   # 45
....|....|.ORX|xxO.|.ORX|xxO.|....|....   # 46
....|....|.OOO|OOO.|.OOO|OOO.|....|....   # 47
""")

# Langes Haar hinter dem Körper (in der Ansicht von vorn sichtbar neben
# Schultern und Armen); eigene Ebene für das Nachschwingen.
TAIL_DOWN = rows("""
....|..O2|3333|3333|3333|3332|2O..|....   # 21
....|.O23|4333|3333|3333|3332|21O.|....   # 22
....|.O34|2222|2222|2222|2222|21O.|....   # 23
....|.O44|2222|2222|2222|2223|21O.|....   # 24
....|O343|2222|2222|2222|2222|321O|....   # 25
....|O342|2222|2222|2222|2222|221O|....   # 26
....|O432|2222|2222|2222|2222|231O|....   # 27
....|.O43|2222|2222|2222|2222|31O.|....   # 28
....|.O34|2222|2222|2222|2222|21O.|....   # 29
....|..O3|4222|2222|2222|2223|1O..|....   # 30
....|..O4|3O22|2222|2222|2O31|O...|....   # 31
....|...O|3O..|....|....|..O2|O...|....   # 32
....|....|O...|....|....|...O|....|....   # 33
""")

# Blütenkranz: wird über den Kopf gelegt ('.' = Kopf bleibt sichtbar)
CROWN_DOWN = rows("""
....|....|....|....|..h.|....|....|....   # 2
....|....|....|..L.|.hof|h...|....|....   # 3
....|....|....|.LoL|vVfh|v...|....|....   # 4
....|....|....|..Lv|....|Vv..|....|....   # 5
""")
CROWN_DOWN_START = 2

# Eingefaltete Feenflügel hinter Haaren und Körper
WINGS_DOWN = rows("""
....|.E..|....|....|....|....|..E.|....   # 12
...E|WE..|....|....|....|....|..EW|E...   # 13
..EW|nE..|....|....|....|....|..En|WE..   # 14
.EWn|nn..|....|....|....|....|..nn|nWE.   # 15
.EWn|nn..|....|....|....|....|..nn|nWE.   # 16
.Enn|nn..|....|....|....|....|..nn|nnE.   # 17
..En|Nn..|....|....|....|....|..nN|nE..   # 18
...E|NN..|....|....|....|....|..NN|E...   # 19
....|E...|....|....|....|....|...E|....   # 20
...E|W...|....|....|....|....|...W|E...   # 21
..EW|n...|....|....|....|....|...n|WE..   # 22
..En|N...|....|....|....|....|...N|nE..   # 23
...E|N...|....|....|....|....|...N|E...   # 24
....|E...|....|....|....|....|...E|....   # 25
""")
WINGS_DOWN_START = 12
