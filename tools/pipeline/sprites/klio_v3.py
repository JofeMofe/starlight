"""Klio v3 – nach Feedback: Schwarz und Lila, Jeans statt Rock, mehr Charakter.

Outfit: schwarzes Shirt mit eigenem lila Stern-Mond-Emblem (keine echten
Bandlogos, §9/§7.9), offenes lila Karohemd mit hochgekrempelten Ärmeln,
Jeans mit goldener Ziernaht und umgeschlagenem Saum, schwarze Stiefel mit
lila Schnürsenkeln. Schwarze Brille, Veilchenkranz, lila Feenflügel.
Haltung: eine Hand in der Hosentasche, eine Haarsträhne über der rechten
Schulter (asymmetrisch, lebendiger als eine starre Frontalpose).

Jede Ebene hat ihre eigene Legende; Raster in 8 Vierergruppen.
"""
from __future__ import annotations

from palette import color
from sprites import klio_v2 as V2

rows = V2.rows

HAIR_LEGEND = dict(V2.LEGEND)
HAIR_LEGEND.update({
    "G": color("dusk", 0), "g": color("dusk", 1),   # schwarze Brille
})

CROWN_LEGEND = {
    "f": color("fae", 3), "h": color("fae", 4), "o": color("ember", 4),
    "v": color("moss", 4), "V": color("moss", 5), "L": color("fae", 2), "l": color("fae", 1),
}

WING_LEGEND = {
    "E": color("fae", 2), "W": color("fae", 4), "n": color("fae", 3), "N": color("sky", 6),
}

BODY_LEGEND = {
    # Haut
    "s": color("skin", 0), "e": color("skin", 2), "k": color("skin", 3), "K": color("skin", 4),
    # schwarzes Shirt (violett-schwarze Rampe)
    "q": color("dusk", 0), "u": color("dusk", 1), "t": color("dusk", 2), "T": color("dusk", 3),
    # Emblem
    "Y": color("fae", 3), "y": color("fae", 4),
    # Karohemd lila
    "F": color("fae", 2), "f": color("fae", 1), "v": color("fae", 0), "x": color("dusk", 1),
    # Jeans
    "N": color("sky", 0), "n": color("sky", 1), "j": color("sky", 2), "J": color("sky", 3),
    "h": color("sky", 4), "c": color("ember", 3),
    # Stiefel
    "L": color("dusk", 2), "l": color("dusk", 1), "W": color("dusk", 4),
}

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
....|..O2|322K|22k3|2k23|e223|1O..|....   # 10
....|..O2|3kGG|GGkk|keGG|GG23|2O..|....   # 11
....|..O4|3grp|pKgG|Ggrp|pkg3|2O..|....   # 12
....|..O4|3gKw|iKgk|egKw|ikg3|2O..|....   # 13
....|..O4|3gki|jkgk|egki|jeg3|1O..|....   # 14
....|..O3|4gkk|kkgk|egkk|keg2|1O..|....   # 15
....|..O2|3bgg|ggkk|ekgg|ggb2|1O..|....   # 16
....|..O2|3kbb|kkek|kekk|bbe3|2O..|....   # 17
....|..O4|3ekk|kkkm|mkkk|kee3|2O..|....   # 18
....|..O4|42ek|kkkk|kkke|ee22|1O..|....   # 19
....|..O3|421s|ekkk|kkee|s122|1O..|....   # 20
....|..O2|3321|ssdd|ddss|1233|2O..|....   # 21
""")
TAIL_DOWN = V2.TAIL_DOWN
CROWN_DOWN = V2.CROWN_DOWN
CROWN_DOWN_START = V2.CROWN_DOWN_START
WINGS_DOWN = V2.WINGS_DOWN
WINGS_DOWN_START = V2.WINGS_DOWN_START

BODY_DOWN = rows("""
....|....|...F|fqee|eeqf|F...|....|....   # 22
....|....|.qFF|futt|ttuf|vvq.|....|....   # 23
....|....|qFfx|fuTt|ttuf|xfvq|....|....   # 24
....|....|qxxv|xutY|ytux|vxxq|....|....   # 25
....|....|qFfx|fuYt|tYuf|xfvq|....|....   # 26
....|....|qFfx|futY|Ytuf|xfvq|....|....   # 27
....|....|qFfx|fuTt|ttuf|xfvq|....|....   # 28
....|....|qFFx|xutt|ttux|xFFq|....|....   # 29
....|....|sKkf|fuuu|uuuf|fkes|....|....   # 30
....|....|.skf|NJjc|jjnN|fkks|....|....   # 31
....|....|..vv|NJcj|jcnN|vss.|....|....   # 32
....|....|...N|JJjj|jjnn|N...|....|....   # 33
....|....|...N|JJjj|jjnn|N...|....|....   # 34
....|....|...N|JjnN|Njjn|N...|....|....   # 35
....|....|...N|JjN.|.Njn|N...|....|....   # 36
....|....|...N|hjN.|.Njn|N...|....|....   # 37
....|....|...N|JjN.|.Njn|N...|....|....   # 38
....|....|...N|JjN.|.Nhn|N...|....|....   # 39
....|....|..NJ|hjN.|.Nhj|jN..|....|....   # 40
....|....|..qW|Llq.|.qWL|lq..|....|....   # 41
....|....|..qL|YLq.|.qLY|Lq..|....|....   # 42
....|....|..qW|Llq.|.qWL|lq..|....|....   # 43
....|....|..qL|YLq.|.qLY|Lq..|....|....   # 44
....|....|.qWL|Llq.|.qWL|Llq.|....|....   # 45
....|....|.qLL|llq.|.qLL|llq.|....|....   # 46
....|....|.qqq|qqq.|.qqq|qqq.|....|....   # 47
""")
BODY_DOWN_START = 22

# Haarsträhne über der rechten Schulter (vor dem Körper)
STRAND_DOWN = rows("""
....|....|342.|....|....|....|....|....   # 20
....|...O|3432|....|....|....|....|....   # 21
....|...O|4432|....|....|....|....|....   # 22
....|..O3|4432|....|....|....|....|....   # 23
....|..O3|543O|....|....|....|....|....   # 24
....|..O4|432O|....|....|....|....|....   # 25
....|...O|3432|O...|....|....|....|....   # 26
....|...O|3432|O...|....|....|....|....   # 27
....|..O3|431O|....|....|....|....|....   # 28
....|..O4|32O.|....|....|....|....|....   # 29
....|...O|42O.|....|....|....|....|....   # 30
....|...O|3O..|....|....|....|....|....   # 31
....|....|O...|....|....|....|....|....   # 32
""")
STRAND_DOWN_START = 20
