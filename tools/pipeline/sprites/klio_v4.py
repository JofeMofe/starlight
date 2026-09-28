"""Klio v4 – nach den Angaben der Projektinhaber:innen.

Dunkelgrüngraue Augen; dunkelbraune, glatte Haare ohne Pony (Mittelscheitel,
links hinters Ohr gesteckt); schmale, eckige, schwarze Brille; Ohrstecker,
Ketten, Ringe, schwarzer Nagellack; helle Jeansjacke über schwarzem
Band-Shirt (eigenes Stern-Mond-Emblem, kein echtes Logo), lila Pin, dunkle
Jeans, schwarze High-Top-Canvas-Schuhe mit weißer Kappe/Sohle (ohne Logo).
Veilchenkranz und lila Flügel zeigen: Sie ist jetzt eine Fee.
"""
from __future__ import annotations

from palette import color
from sprites import klio_v2 as V2
from sprites import klio_v3 as V3

rows = V2.rows

HAIR_LEGEND = {
    # dunkelbraun: Umriss violett-schwarz, Grundton bark2, Glanz bark4/5
    "O": color("dusk", 0), "1": color("bark", 0), "2": color("bark", 1), "3": color("bark", 2),
    "4": color("bark", 3), "5": color("bark", 4), "6": color("bark", 5),
    # Haut
    "s": color("skin", 0), "d": color("skin", 1), "e": color("skin", 2), "k": color("skin", 3),
    "K": color("skin", 4),
    # Augen dunkelgrüngrau
    "p": color("dusk", 0), "i": color("moss", 1), "j": color("stone", 2), "w": color("dusk", 6),
    # Brille schwarz, schmal
    "G": color("dusk", 0), "g": color("dusk", 1), "r": color("sky", 6),
    # Wangen, Mund
    "b": color("rose", 5), "m": color("rose", 2),
    # Schmuck
    "W": color("dusk", 6), "S": color("stone", 4), "P": color("fae", 3),
}

BODY_LEGEND = {
    "s": color("skin", 0), "e": color("skin", 2), "k": color("skin", 3), "K": color("skin", 4),
    # Shirt schwarz
    "q": color("dusk", 0), "u": color("dusk", 1), "t": color("dusk", 2), "T": color("dusk", 3),
    "Y": color("fae", 3), "y": color("fae", 4),
    # Jeansjacke (hell)
    "Z": color("sky", 1), "z": color("sky", 3), "d": color("sky", 4), "D": color("sky", 5),
    "c": color("ember", 2),
    # Jeans (dunkel)
    "N": color("sky", 0), "n": color("sky", 1), "j": color("sky", 2), "J": color("sky", 3),
    "h": color("sky", 4),
    # Schmuck, Pin
    "W": color("dusk", 6), "S": color("stone", 4), "P": color("fae", 3),
    # Schuhe
    "L": color("dusk", 2), "l": color("dusk", 1),
}

WING_LEGEND = V3.WING_LEGEND
CROWN_LEGEND = V3.CROWN_LEGEND
WINGS_DOWN, WINGS_DOWN_START = V2.WINGS_DOWN, V2.WINGS_DOWN_START
CROWN_DOWN, CROWN_DOWN_START = V2.CROWN_DOWN, V2.CROWN_DOWN_START

HEAD_DOWN = rows("""
....|....|....|....|....|....|....|....   # 0
....|....|....|....|....|....|....|....   # 1
....|....|....|1OOO|OOOO|....|....|....   # 2
....|....|..O3|4541|3433|2O..|....|....   # 3
....|....|.O34|5641|3443|32O.|....|....   # 4
....|....|O345|5431|2343|322O|....|....   # 5
....|...O|3444|3321|1233|3221|O...|....   # 6
....|...O|3443|3211|1123|3221|O...|....   # 7
....|..O2|3433|321K|k123|3222|1O..|....   # 8
....|..O2|3433|21KK|kk12|2322|1O..|....   # 9
....|..O2|3432|1Kkk|kkk1|2322|1O..|....   # 10
....|..O2|3421|11kk|kk11|1222|1O..|....   # 11
....|..O2|3GGG|GGGk|kGGG|GGG2|1O..|....   # 12
....|..O2|3Gkw|prGG|GGkw|prGG|1O..|....   # 13
....|..O2|3Gki|jkGk|kGki|jeGs|2O..|....   # 14
....|..O2|3ggg|gggk|eggg|gggk|2O..|....   # 15
....|..O2|34bb|kkkk|ekkb|beWs|2O..|....   # 16
....|..O2|34kk|kkek|kekk|keP2|2O..|....   # 17
....|..O2|34ek|kkkm|mkkk|ees2|2O..|....   # 18
....|..O2|342e|kkkk|kkke|e222|1O..|....   # 19
....|..O2|3421|sekk|kkes|1222|1O..|....   # 20
....|..O2|3421|1sdd|dds1|1222|1O..|....   # 21
""")

# Glattes, langes Haar hinter dem Körper
TAIL_DOWN = rows("""
....|..O2|3333|3333|3333|3332|2O..|....   # 21
....|.O34|3333|3333|3333|3322|21O.|....   # 22
....|.O34|2222|2222|2222|2222|21O.|....   # 23
....|.O35|2222|2222|2222|2222|21O.|....   # 24
....|.O34|2222|2222|2222|2222|21O.|....   # 25
....|.O34|2222|2222|2222|2222|21O.|....   # 26
....|.O44|2222|2222|2222|2222|21O.|....   # 27
....|.O34|2222|2222|2222|2222|21O.|....   # 28
....|.O34|2222|2222|2222|2222|21O.|....   # 29
....|.O35|2222|2222|2222|2222|21O.|....   # 30
....|.O34|2222|2222|2222|2222|21O.|....   # 31
....|.O33|2222|2222|2222|2222|21O.|....   # 32
....|..OO|O...|....|....|...O|OO..|....   # 33
""")
TAIL_DOWN_START = 21

# Glatte Strähne über der rechten Schulter (vor dem Körper)
STRAND_DOWN = rows("""
....|...O|3432|....|....|....|....|....   # 20
....|...O|3432|O...|....|....|....|....   # 21
....|...O|3442|O...|....|....|....|....   # 22
....|...O|3432|O...|....|....|....|....   # 23
....|...O|3542|O...|....|....|....|....   # 24
....|...O|3432|O...|....|....|....|....   # 25
....|...O|3432|O...|....|....|....|....   # 26
....|...O|3442|O...|....|....|....|....   # 27
....|...O|3432|O...|....|....|....|....   # 28
....|...O|3432|O...|....|....|....|....   # 29
....|...O|3422|O...|....|....|....|....   # 30
....|...O|332O|....|....|....|....|....   # 31
....|....|OO..|....|....|....|....|....   # 32
""")
STRAND_DOWN_START = 20

BODY_DOWN = rows("""
....|....|..Zd|Dqee|eeqz|dZ..|....|....   # 22
....|....|.ZDD|duWS|SWuz|dzZ.|....|....   # 23
....|....|ZDdZ|dutW|Wtuz|ZdzZ|....|....   # 24
....|....|ZDdZ|cuTW|Stuc|ZdzZ|....|....   # 25
....|....|ZDdZ|zuYY|tuuP|ZdzZ|....|....   # 26
....|....|ZDdZ|duYt|tyud|ZdzZ|....|....   # 27
....|....|ZDdZ|dutY|Ytud|ZdzZ|....|....   # 28
....|....|ZDdZ|Zuuu|uuuZ|ZdzZ|....|....   # 29
....|....|ZDDZ|zqqq|qqqz|ZDdZ|....|....   # 30
....|....|.ske|NJjc|jjnN|skes|....|....   # 31
....|....|...N|JcJj|jcnN|skWs|....|....   # 32
....|....|...N|JJjj|jjnn|Nkk.|....|....   # 33
....|....|...N|JJjj|jjnn|Nqq.|....|....   # 34
....|....|...N|JjnN|Njjn|N...|....|....   # 35
....|....|...N|JjN.|.Njn|N...|....|....   # 36
....|....|...N|hjN.|.Njn|N...|....|....   # 37
....|....|...N|JjN.|.Njn|N...|....|....   # 38
....|....|...N|JjN.|.Nhn|N...|....|....   # 39
....|....|..NJ|jjN.|.Njj|nN..|....|....   # 40
....|....|..qL|Llq.|.qLL|lq..|....|....   # 41
....|....|..qL|Wlq.|.qLW|lq..|....|....   # 42
....|....|..qL|Llq.|.qLL|lq..|....|....   # 43
....|....|..qL|Wlq.|.qLW|lq..|....|....   # 44
....|....|.qLW|Wlq.|.qLW|Wlq.|....|....   # 45
....|....|.qWW|WSq.|.qWW|WSq.|....|....   # 46
....|....|.qqq|qqq.|.qqq|qqq.|....|....   # 47
""")
BODY_DOWN_START = 22


# ===========================================================================
# Beine (Ansicht von vorn/hinten): Zeilen 35-47, Standpose. Schrittposen
# entstehen im Sheet-Builder, indem ein Bein samt Schuh angehoben wird.
# ===========================================================================
LEGS_DOWN = rows("""
....|....|...N|JjnN|Njjn|N...|....|....   # 35
....|....|...N|JjN.|.Njn|N...|....|....   # 36
....|....|...N|hjN.|.Njn|N...|....|....   # 37
....|....|...N|JjN.|.Njn|N...|....|....   # 38
....|....|...N|JjN.|.Nhn|N...|....|....   # 39
....|....|..NJ|jjN.|.Njj|nN..|....|....   # 40
....|....|..qL|Llq.|.qLL|lq..|....|....   # 41
....|....|..qL|Wlq.|.qLW|lq..|....|....   # 42
....|....|..qL|Llq.|.qLL|lq..|....|....   # 43
....|....|..qL|Wlq.|.qLW|lq..|....|....   # 44
....|....|.qLW|Wlq.|.qLW|Wlq.|....|....   # 45
....|....|.qWW|WSq.|.qWW|WSq.|....|....   # 46
....|....|.qqq|qqq.|.qqq|qqq.|....|....   # 47
""")
LEGS_START = 35

# Rückansicht: Schuhe mit weißem Fersenstreifen statt Kappe
LEGS_UP = rows("""
....|....|...N|JjnN|Njjn|N...|....|....   # 35
....|....|...N|JjN.|.Njn|N...|....|....   # 36
....|....|...N|JjN.|.Njn|N...|....|....   # 37
....|....|...N|JjN.|.Njn|N...|....|....   # 38
....|....|...N|JjN.|.Njn|N...|....|....   # 39
....|....|..NJ|jjN.|.Njj|nN..|....|....   # 40
....|....|..qL|Llq.|.qLL|lq..|....|....   # 41
....|....|..qL|Llq.|.qLL|lq..|....|....   # 42
....|....|..qL|WLq.|.qLW|Lq..|....|....   # 43
....|....|..qL|WLq.|.qLW|Lq..|....|....   # 44
....|....|..qL|Llq.|.qLL|lq..|....|....   # 45
....|....|..qW|WSq.|.qWW|Sq..|....|....   # 46
....|....|..qq|qqq.|.qqq|qq..|....|....   # 47
""")

BLINK_DOWN = {13: "....|..O2|3Gkk|kkGG|GGkk|kkGG|1O..|....",
              14: "....|..O2|3Gkp|pkGk|kGkp|peGs|2O..|...."}

# ===========================================================================
# Rückansicht
# ===========================================================================
HEAD_UP = rows("""
....|....|....|....|....|....|....|....   # 0
....|....|....|....|....|....|....|....   # 1
....|....|....|1OOO|OOOO|....|....|....   # 2
....|....|..O3|4443|3332|2O..|....|....   # 3
....|....|.O34|5543|3433|32O.|....|....   # 4
....|....|O345|5654|4543|322O|....|....   # 5
....|...O|3456|6555|5543|3321|O...|....   # 6
....|...O|3444|4443|4433|3221|O...|....   # 7
....|..O2|3433|3323|3323|3222|1O..|....   # 8
....|..O2|3432|3323|3322|3322|1O..|....   # 9
....|..O2|3432|4323|4322|3322|1O..|....   # 10
....|..O2|3432|4323|4322|3322|1O..|....   # 11
....|..O2|3432|3323|3322|3322|1O..|....   # 12
....|..G2|3432|3323|3322|3322|1G..|....   # 13
....|..O2|3432|4323|4322|3322|1O..|....   # 14
....|..O2|3432|3323|3322|3322|1O..|....   # 15
....|..O2|3432|3323|4322|3322|1O..|....   # 16
....|..O2|3432|4323|3322|3322|1O..|....   # 17
....|..O2|3432|3323|3322|3322|1O..|....   # 18
....|..O2|3432|3323|4322|3322|1O..|....   # 19
....|..O2|3432|3323|3322|3322|1O..|....   # 20
....|..O2|3432|4323|3322|3322|1O..|....   # 21
""")

BODY_UP = rows("""
....|....|..Zd|DDdd|dddz|dZ..|....|....   # 22
....|....|.ZDD|DDdd|dddd|zzZ.|....|....   # 23
....|....|ZDdZ|dddd|dddd|ZdzZ|....|....   # 24
....|....|ZDdZ|zzzz|zzzz|ZdzZ|....|....   # 25
....|....|ZDdZ|dddd|dddz|ZdzZ|....|....   # 26
....|....|ZDdZ|dcdd|ddcz|ZdzZ|....|....   # 27
....|....|ZDdZ|dddd|dddz|ZdzZ|....|....   # 28
....|....|ZDdZ|dddd|dddz|ZdzZ|....|....   # 29
....|....|ZDDZ|ZZZZ|ZZZZ|ZDdZ|....|....   # 30
....|....|sKks|NJjj|jjnN|skes|....|....   # 31
....|....|sWks|NJcc|ccnN|skWs|....|....   # 32
....|....|.qq.|NJjj|jjnN|.qq.|....|....   # 33
....|....|...N|JJjj|jjnn|N...|....|....   # 34
""")

# Rückansicht: das lange Haar fällt über den Rücken (vor dem Körper)
TAIL_UP = rows("""
....|...O|3432|3323|3322|3322|O...|....   # 22
....|....|O432|4323|3322|332O|....|....   # 23
....|....|.O32|3323|4322|32O.|....|....   # 24
....|....|.O32|4323|3322|32O.|....|....   # 25
....|....|.O42|3323|3322|32O.|....|....   # 26
....|....|.O32|3323|4322|32O.|....|....   # 27
....|....|.O32|4323|3322|32O.|....|....   # 28
....|....|..O3|3323|3322|2O..|....|....   # 29
....|....|..O3|4323|4322|2O..|....|....   # 30
....|....|...O|3323|3322|O...|....|....   # 31
....|....|....|O323|3322|O...|....|....   # 32
....|....|....|.OO3|32OO|....|....|....   # 33
....|....|....|...O|OO..|....|....|....   # 34
""")
TAIL_UP_START = 22

# ===========================================================================
# Seitenansicht (Blick nach links; rechts = gespiegelt)
# Brille im Profil: Glas vor dem Auge, Bügel ins Haar
# ===========================================================================
HEAD_SIDE = rows("""
....|....|....|....|....|....|....|....   # 0
....|....|....|....|....|....|....|....   # 1
....|....|....|1OOO|OOOO|....|....|....   # 2
....|....|..O3|4543|3332|2O..|....|....   # 3
....|....|.O34|5543|3333|22O.|....|....   # 4
....|....|O344|4433|3332|222O|....|....   # 5
....|...O|3444|3333|3322|2221|O...|....   # 6
....|....|sK33|3333|3222|2221|O...|....   # 7
....|...s|KK23|3333|3222|2221|O...|....   # 8
....|...s|KKk2|3333|3222|2221|O...|....   # 9
....|...s|Kkk1|2333|3222|2221|O...|....   # 10
....|...s|11kk|1233|3222|2221|O...|....   # 11
....|...G|ppGG|G233|3222|2221|O...|....   # 12
....|...G|wpkk|1233|3222|2221|O...|....   # 13
....|...g|ggke|1233|3222|2221|O...|....   # 14
....|..sk|kbke|2233|3222|2221|O...|....   # 15
....|.skk|kkee|2333|3222|2221|O...|....   # 16
....|..sk|kkee|2333|3222|2221|O...|....   # 17
....|...m|kkke|1233|3222|2221|O...|....   # 18
....|...s|kkee|1233|3222|2221|O...|....   # 19
....|....|seed|1233|3222|2221|O...|....   # 20
....|....|.sdd|d233|3222|2221|O...|....   # 21
""")

BLINK_SIDE = {13: "....|...G|kpkk|1233|3222|2221|O...|...."}

BODY_SIDE = rows("""
....|....|..qe|eDdZ|....|....|....|....   # 22
....|....|.quW|DDdd|zZ..|....|....|....   # 23
....|....|.qtz|Dddd|zZ..|....|....|....   # 24
....|....|.qTz|dddd|zZ..|....|....|....   # 25
....|....|.qtz|Dddd|zZ..|....|....|....   # 26
....|....|.qTz|dddd|zZ..|....|....|....   # 27
....|....|.qtz|dddd|zZ..|....|....|....   # 28
....|....|.qtZ|dddz|zZ..|....|....|....   # 29
....|....|.qqZ|ZZZZ|Z...|....|....|....   # 30
....|....|..NJ|jjjj|nN..|....|....|....   # 31
....|....|..NJ|jjcc|nN..|....|....|....   # 32
....|....|..NJ|jjjj|nN..|....|....|....   # 33
....|....|..NJ|jjjj|nN..|....|....|....   # 34
""")

# Haare hinter dem Rücken (Seitenansicht)
TAIL_SIDE = rows("""
....|....|....|.O33|3322|221O|....|....   # 22
....|....|....|..O3|3322|221O|....|....   # 23
....|....|....|..O3|4322|221O|....|....   # 24
....|....|....|..O3|3322|221O|....|....   # 25
....|....|....|..O3|3322|221O|....|....   # 26
....|....|....|..O3|4322|221O|....|....   # 27
....|....|....|..O3|3322|221O|....|....   # 28
....|....|....|..O3|3322|21O.|....|....   # 29
....|....|....|..O3|4322|21O.|....|....   # 30
....|....|....|..O3|3322|21O.|....|....   # 31
....|....|....|..O3|3322|21O.|....|....   # 32
....|....|....|..OO|OOOO|OO..|....|....   # 33
""")
TAIL_SIDE_START = 22

# Arm im Profil (Ärmel, Hand mit Ring und schwarzem Nagellack), 7 breit ab x=11, Zeile 23
SIDE_ARMS = {
    "neutral": [
        "..ZDZ..", "..ZDdZ.", "..ZDdZ.", "..ZDdZ.", "..ZDdZ.", "..ZDdZ.", "..ZDDZ.",
        "..sKks.", "..sWks.", "...qq..",
    ],
    "forward": [
        "..ZDZ..", "..ZDdZ.", ".ZDdZ..", ".ZDdZ..", "ZDdZ...", "ZDdZ...", "ZDDZ...",
        "sKks...", "sWks...", ".qq....",
    ],
    "back": [
        "..ZDZ..", "..ZDdZ.", "..ZDdZ.", "...ZDdZ", "...ZDdZ", "...ZDdZ", "...ZDDZ",
        "...sKks", "...sWks", "....qq.",
    ],
}
SIDE_ARM_POS = (11, 23)

# Beine im Profil (12 breit ab x=8, Zeilen 35-47)
SIDE_LEGS = {
    "stand": [
        "...NJjjnN...", "...NJjnN....", "...NJjnN....", "...NhjnN....", "...NJjnN....",
        "...NJjnN....", "..NJjjnN....", "..qLLlq.....", "..qLWlq.....", "..qLLlq.....",
        ".qLWLlq.....", "qWLLLlq.....", "qWWWWSq.....",
    ],
    "stride": [
        "...NJjjjnN..", "..NJjnNNjnN.", "..NhjN.NjnN.", ".NJjN..NjnN.", ".NJjN...NjnN",
        "NJjjN...NjnN", "qLLlq...NnnN", "qLWlq...qLlq", "qLLLlq..qWlq", "qWLLlq..qLLq",
        "qWWWSq..qLlq", "qqqqqq..qWSq", "........qqqq",
    ],
    "pass": [
        "...NJjjnN...", "...NJjnN....", "...NhjnNN...", "...NJjnNjN..", "...NJjnNjnN.",
        "..NJjjnNnnN.", "..qLLlqqLlq.", "..qLWlqqWlq.", "..qLLlq.qqq.", ".qLWLlq.....",
        "qWLLLlq.....", "qWWWWSq.....", "qqqqqqq.....",
    ],
}
SIDE_LEGS_X = 8

# ===========================================================================
# Feengröße (16x20), Raster 12 breit, x-Versatz 2, y-Versatz 1
# ===========================================================================
FAIRY_LEGEND = dict(HAIR_LEGEND)
FAIRY_LEGEND.update({k: v for k, v in BODY_LEGEND.items() if k in "ZzdDNnjJqtuTLlc"})
FAIRY_LEGEND.update({"f": color("fae", 3), "o": color("ember", 4)})

FAIRY_DOWN = [
    "....OOOO....",
    "..Of3oo3fO..",
    ".O33311333O.",
    ".O321KK123O.",
    ".O3GGkkGG3O.",
    ".O3wgkkwg3O.",
    ".O3kbkkbk3O.",
    ".O2skemks2O.",
    ".O2.sdds.2O.",
    ".O2DqWqqD2O.",
    ".O2DdqqdD2O.",
    "..OsDqqDsO..",
    "...NjjjjN...",
    "...NjNNjN...",
    "...Nj..jN...",
    "...qW..Wq...",
]
FAIRY_UP = [
    "....OOOO....",
    "..O3f3o3fO..",
    ".O34333343O.",
    ".O34333343O.",
    ".G34333343G.",
    ".O33333333O.",
    ".O32333323O.",
    ".O32333323O.",
    ".O22333322O.",
    ".ODd3333dDO.",
    ".ODd3333dDO.",
    "..sDO22ODs..",
    "...NjjjjN...",
    "...NjNNjN...",
    "...Nj..jN...",
    "...qq..qq...",
]
FAIRY_SIDE = [
    "....OOOO....",
    "...Of3o3fO..",
    "..O3343333O.",
    ".sK1333333O.",
    ".GGg233333O.",
    ".sGw233333O.",
    "skbk233333O.",
    ".skm233332O.",
    "..sdD23332O.",
    "..qDd33332O.",
    "..qDd23321..",
    "..sDdD321...",
    "...NjjN1....",
    "...NjjN.....",
    "..qqWq......",
    "..qqqq......",
]
FAIRY_BLINK = {"down": {5: ".O3ggkkgg3O."}, "side": {5: ".sGg233333O."}}

# Eingefaltete Flügel in der Seitenansicht (hinter Kopf und Rücken)
WINGS_SIDE = rows("""
....|....|....|....|....|...E|....|....   # 13
....|....|....|....|....|..EW|E...|....   # 14
....|....|....|....|....|..En|WE..|....   # 15
....|....|....|....|....|..En|nWE.|....   # 16
....|....|....|....|....|..En|nnE.|....   # 17
....|....|....|....|....|...E|NnE.|....   # 18
....|....|....|....|....|....|ENE.|....   # 19
....|....|....|....|....|....|.E..|....   # 20
....|....|....|....|....|....|EWE.|....   # 21
....|....|....|....|....|....|EnWE|....   # 22
....|....|....|....|....|....|ENnE|....   # 23
....|....|....|....|....|....|.ENE|....   # 24
....|....|....|....|....|....|..E.|....   # 25
""")
WINGS_SIDE_START = 13
