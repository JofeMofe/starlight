"""Handgesetzte Pixelkarten für Klio (Menschengröße, 32x48).

Jede Ansicht besteht aus drei Ebenen, damit das Spiel sie getrennt bewegen kann:
- HEAD: Kopf, Gesicht, Brille, Pony und kurze Seitenhaare
- BODY: Hals, Oberkörper, Arme, Rock, Beine, Stiefel (Beine werden pro Frame ersetzt)
- TAIL: das lange Haar unterhalb des Kinns (eigene Ebene für Sekundäranimation)

Die Raster sind 20 Pixel breit und werden im 32er-Frame zentriert (x-Versatz 6).
Zeile 0 der Raster liegt auf Frame-Zeile 7, die Stiefelsohle damit auf Zeile 47.
"""
from __future__ import annotations

from palette import color

GRID_W = 20
X_OFFSET = 6
Y_OFFSET = 7

LEGEND = {
    # Haare (Kopf)
    "H": color("bark", 0), "h": color("bark", 1), "m": color("bark", 2),
    "l": color("bark", 3), "g": color("bark", 4),
    # Haare (lange Strähnen, eigene Ebene)
    "1": color("bark", 0), "2": color("bark", 1), "3": color("bark", 2),
    "4": color("bark", 3), "5": color("bark", 4),
    # Haut
    "S": color("skin", 0), "s": color("skin", 2), "k": color("skin", 3), "K": color("skin", 4),
    # Brille, Augen, Wangen, Mund
    "G": color("dusk", 2), "w": color("dusk", 6), "e": color("dusk", 1),
    "c": color("rose", 5), "M": color("rose", 2),
    # Bluse
    "B": color("dusk", 6), "b": color("stone", 4),
    # Strickjacke (Lagune)
    "T": color("lagoon", 2), "t": color("lagoon", 1), "U": color("lagoon", 0), "O": color("dusk", 1),
    # Rock (Pflaume)
    "P": color("dusk", 4), "p": color("dusk", 3), "q": color("dusk", 2), "Q": color("dusk", 1),
    # Strumpfhose
    "Y": color("dusk", 2), "y": color("dusk", 3), "Z": color("dusk", 0),
    # Stiefel
    "R": color("bark", 4), "r": color("bark", 3), "X": color("bark", 1),
    # Flügel (eingefaltet)
    "W": color("sky", 6), "V": color("sky", 5), "F": color("fae", 3),
}

# ---------------------------------------------------------------------------
# Ansicht: nach unten (zur Kamera)
# ---------------------------------------------------------------------------
DOWN_HEAD = [
    ".......HHHHHH.......",  # 0
    ".....HHmmllmmHH.....",  # 1
    "....HmmmlgglmmmH....",  # 2
    "...HmmmmllllmmmmH...",  # 3
    "..HmmmmmmmmmmmmmmH..",  # 4
    "..HmmmmhmmmmhmmmmH..",  # 5
    ".HmmmhmmmmmmhmmmmmH.",  # 6
    ".HmmhmmmhmmmhmmmhmH.",  # 7
    ".HmhmKhmKKhmKKhmhmH.",  # 8
    ".HmhkKKkKKKKkKKkhmH.",  # 9
    ".HmhkGGGkGGkGGGkhmH.",  # 10
    ".HmhGweKGkkGwekGhmH.",  # 11
    ".HmhGkekGkkGkekGhmH.",  # 12
    ".HmhcGGGkkkkGGGchmH.",  # 13
    ".HmhskkkkkskkkkshmH.",  # 14
    ".HmhskkkkMMkkkkshmH.",  # 15
    ".HmhhskkkkkkkkshhmH.",  # 16
    ".HmhhhSSssssSShhhmH.",  # 17
]

DOWN_BODY = [
    "........skks........",  # 18 Hals
    ".....OTtBBBBtTO.....",  # 19
    "....OTTtbBBbtTTO....",  # 20
    "...OTTTtBBBBtTTUO...",  # 21
    "..OTtOttBBbBUUOtUO..",  # 22
    "..OTtOttBBBBUUOtUO..",  # 23
    "..OTtOttBBbBUUOtUO..",  # 24
    "..OTtOttBBBBUUOtUO..",  # 25
    "..OTtOttbbbbUUOtUO..",  # 26
    "..SKkQPppppppqQksS..",  # 27
    "...SSQPPpppppqQSS...",  # 28
    "....QPPppppppqqQ....",  # 29
    "....QPpppppppqqQ....",  # 30
    "...QPPppppppppqqQ...",  # 31
    "...QPppppqppppqqQ...",  # 32
    "...QQQQQQQQQQQQQQ...",  # 33
]

# Beine für die Frames (Zeilen 34-40). Index = Beinposition.
DOWN_LEGS = {
    "stand": [
        ".....ZyYZ..ZyYZ.....",
        ".....ZyYZ..ZyYZ.....",
        ".....ZyYZ..ZyYZ.....",
        ".....XRrX..XRrX.....",
        ".....XRrX..XRrX.....",
        "....XRRrX..XRrrX....",
        "....XXXXX..XXXXX....",
    ],
    # linkes Bein vorn (größer/tiefer), rechtes angehoben
    "left_step": [
        ".....ZyYZ..ZyYZ.....",
        ".....ZyYZ..ZyYZ.....",
        ".....ZyYZ..XRrX.....",
        ".....XRrX..XRrX.....",
        ".....XRrX.XRrrX.....",
        "....XRRrX.XXXXX.....",
        "....XXXXX...........",
    ],
    "right_step": [
        ".....ZyYZ..ZyYZ.....",
        ".....ZyYZ..ZyYZ.....",
        ".....XRrX..ZyYZ.....",
        ".....XRrX..XRrX.....",
        ".....XRRrX.XRrX.....",
        ".....XXXXX.XRrrX....",
        "...........XXXXX....",
    ],
}

DOWN_TAIL = [
    ".1342..........2431.",  # 18
    ".1342..........2431.",  # 19
    ".1342..........2431.",  # 20
    ".1332..........2331.",  # 21
    "..132..........231..",  # 22
    "..132..........231..",  # 23
    "..11............11..",  # 24
]
DOWN_TAIL_START = 18

# ---------------------------------------------------------------------------
# Ansicht: nach oben (Rücken). Brillenbügel als je 1 Pixel an den Seiten,
# damit die Brille auch von hinten erkennbar bleibt.
# ---------------------------------------------------------------------------
UP_HEAD = [
    ".......HHHHHH.......",  # 0
    ".....HHmmllmmHH.....",  # 1
    "....HmmmlgglmmmH....",  # 2
    "...HmmmmllllmmmmH...",  # 3
    "..HmmmmmmmmmmmmmmH..",  # 4
    "..HmmmlmmmmmmlmmmH..",  # 5
    ".HmmmlmmmhmmmlmmmmH.",  # 6
    ".HmmlmmmhmmmmlmmhmH.",  # 7
    ".HmmlmmhmmmmmlmmhmH.",  # 8
    ".HmhlmmhmmmmmlmmhmH.",  # 9
    ".HmhmmmhmmmmmmmmhmH.",  # 10
    ".GmhmmmhmmmmmmmmhmG.",  # 11
    ".HmhmmhmmmmmhmmmhmH.",  # 12
    ".HmhmmhmmmmmhmmmhmH.",  # 13
    ".HmhmmhmmmmmhmmmhmH.",  # 14
    ".HmhmmhmmmmmhmmhhmH.",  # 15
    ".HmhhmhmmmmmhmmhhmH.",  # 16
    ".HhhhmhmmmmmhmhhhhH.",  # 17
]

UP_BODY = [
    "........ssss........",  # 18
    ".....OTttttttTO.....",  # 19
    "....OTttttttttUO....",  # 20
    "...OTTttttttttUUO...",  # 21
    "..OTtOttttttttOtUO..",  # 22
    "..OTtOttttttttOtUO..",  # 23
    "..OTtOttttttttOtUO..",  # 24
    "..OTtOttttttttOtUO..",  # 25
    "..OTtOUUUUUUUUOtUO..",  # 26
    "..SKkQPppppppqQksS..",  # 27
    "...SSQPPpppppqQSS...",  # 28
    "....QPPppppppqqQ....",  # 29
    "....QPpppppppqqQ....",  # 30
    "...QPPppppppppqqQ...",  # 31
    "...QPppppqppppqqQ...",  # 32
    "...QQQQQQQQQQQQQQ...",  # 33
]

UP_TAIL = [
    "..1334333333334331..",  # 18
    "..1334333323334331..",  # 19
    "..1334323333234331..",  # 20
    "..1343323333233431..",  # 21
    "...13433233233431...",  # 22
    "...13433233233431...",  # 23
    "...13432333323431...",  # 24
    "...13432333323431...",  # 25
    "....134323323431....",  # 26
    "....134323323431....",  # 27
    ".....1343223431.....",  # 28
    ".....1132223311.....",  # 29
    "......11.11.11......",  # 30
]
UP_TAIL_START = 18

# ---------------------------------------------------------------------------
# Ansicht: seitlich (Blick nach links). Rechts = gespiegelt.
# Brille im Profil: Glas vor dem Auge + Bügel bis zum Ohr.
# ---------------------------------------------------------------------------
SIDE_HEAD = [
    ".......HHHHHH.......",  # 0
    ".....HHmmllmmHH.....",  # 1
    "....HmmmlgglmmmH....",  # 2
    "...HmmmmmllmmmmmH...",  # 3
    "..HmmmmmmmmmmmmmmH..",  # 4
    "..HmmmmmmmmmmmmmmH..",  # 5
    ".HmmmmhmmmmmmmmmmmH.",  # 6
    ".HmmmhmmmmmhmmmmmmH.",  # 7
    ".HhmhKhmmmmhmmmmmmH.",  # 8
    ".SKKKKhmmmmmhmmmmmH.",  # 9
    ".SkGGGGkhmmhmmmmmmH.",  # 10
    ".SkGweGGGGhmhmmmmmH.",  # 11
    ".SkGkeGkkhmmhmmmmmH.",  # 12
    "SkcGGGGkkhmmhmmmmmH.",  # 13
    ".SkkkkkkkhmmhmmmmmH.",  # 14
    ".SMkkkkkshmmhmmmmhH.",  # 15
    "..SkkkkshmmmhmmmhH..",  # 16
    "...SSsshhmmmhmmhH...",  # 17
]

SIDE_BODY = [
    ".......sks..........",  # 18
    "......OTTttUO.......",  # 19
    ".....ObTTtttUO......",  # 20
    ".....ObTTtttUO......",  # 21
    ".....OTTttttUO......",  # 22
    ".....OTTttttUO......",  # 23
    ".....OTTttttUO......",  # 24
    ".....OTTttttUO......",  # 25
    ".....OUUUUUUUO......",  # 26
    ".....QPpppppqQ......",  # 27
    "....QPPppppppqQ.....",  # 28
    "....QPpppppppqQ.....",  # 29
    "...QPPpppppppqqQ....",  # 30
    "...QPppppppppqqQ....",  # 31
    "...QPpppqpppppqQ....",  # 32
    "...QQQQQQQQQQQQQ....",  # 33
]

# Arm im Profil (Ärmel + Hand), 5 breit, ab Zeile 20, x ab Rasterspalte 6
SIDE_ARMS = {
    "neutral": [
        ".OTt.",
        ".OTU.",
        ".OTU.",
        ".OTU.",
        ".OTU.",
        ".OTU.",
        ".SKs.",
        ".SSS.",
    ],
    "forward": [
        ".OTt.",
        ".OTU.",
        "OTU..",
        "OTU..",
        "OTU..",
        "SKs..",
        "SSS..",
        ".....",
    ],
    "back": [
        ".OTt.",
        ".OTU.",
        "..OTU",
        "..OTU",
        "..OTU",
        "..SKs",
        "..SSS",
        ".....",
    ],
}
SIDE_ARM_POS = (6, 20)

SIDE_LEGS = {
    "stand": [
        ".......ZyYZ.........",
        ".......ZyYZ.........",
        ".......ZyYZ.........",
        ".......XRrX.........",
        ".......XRrX.........",
        "......XRRrX.........",
        "......XXXXX.........",
    ],
    "stride": [
        ".......ZyYZ.........",
        "......ZyZZyZ........",
        ".....ZyZ..ZyZ.......",
        ".....XRX..XrX.......",
        "....XRrX..XRrX......",
        "...XRRrX..XRRX......",
        "...XXXXX..XXXX......",
    ],
    "pass": [
        ".......ZyYZ.........",
        ".......ZyYZ.........",
        ".......ZyYZ.........",
        ".......XRrXX........",
        ".......XRrXrX.......",
        "......XRRrXXX.......",
        "......XXXXX.........",
    ],
}

SIDE_TAIL = [
    "...........1344331..",  # 17
    "...........1343331..",  # 18
    "...........1343321..",  # 19
    "............134331..",  # 20
    "............134321..",  # 21
    "............13431...",  # 22
    "............13331...",  # 23
    "............1331....",  # 24
    "............1331....",  # 25
    ".............11.....",  # 26
]
SIDE_TAIL_START = 17

# Blinzeln: Ersatzzeilen (Zeilenindex im Kopfraster -> Zeile)
DOWN_BLINK = {
    11: ".HmhGwKKGkkGwKkGhmH.",
    12: ".HmhGeeeGkkGeeeGhmH.",
}
SIDE_BLINK = {
    11: ".SkGwKGGGGhmhmmmmmH.",
    12: ".SkGeeGkkhmmhmmmmmH.",
}

# ---------------------------------------------------------------------------
# Feengröße (16x20). Raster 12 breit, x-Versatz 2, y-Versatz 1.
# Brille als 1-px-Gestell mit je einem Glanzpixel.
# ---------------------------------------------------------------------------
FAIRY_GRID_W = 12
FAIRY_X_OFFSET = 2
FAIRY_Y_OFFSET = 1

FAIRY_LEGEND = dict(LEGEND)
FAIRY_LEGEND.update({
    # Blütenkranz (nach der Verwandlung)
    "f": color("rose", 6), "v": color("ember", 4), "n": color("moss", 4),
    # Feenkleid: helles Sternenblau statt Strickjacke
    "D": color("sky", 5), "d": color("sky", 4), "E": color("sky", 2),
})

FAIRY_DOWN = [
    "....HHHH....",  # 0
    "..HfmvfmHH..",  # 1
    ".HmmmllmmmH.",  # 2
    ".HmhKKKKhmH.",  # 3
    ".HmGGkkGGmH.",  # 4
    ".HmewkkewmH.",  # 5
    ".HmckkkkcmH.",  # 6
    ".H3SkMMkS3H.",  # 7
    ".13.EDDE.31.",  # 8
    ".13EDDDdE31.",  # 9
    ".1SEDDDdES1.",  # 10
    "...EDDDdE...",  # 11
    "..EDDDDddE..",  # 12
    "..EEEEEEEE..",  # 13
    "....Z..Z....",  # 14
    "....X..X....",  # 15
]
FAIRY_UP = [
    "....HHHH....",  # 0
    "..HfmvfmHH..",  # 1
    ".HmmmllmmmH.",  # 2
    ".HmlmmmmlmH.",  # 3
    ".HmlmmmmhmH.",  # 4
    ".GmhmmmmhmG.",  # 5
    ".HmhmmmmhmH.",  # 6
    ".H3hmmmmh3H.",  # 7
    ".134333343 1".replace(" ", "."),  # 8
    ".13433334 31".replace(" ", "."),  # 9
    ".1SE3333ES1.",  # 10
    "...E1331E...",  # 11
    "..EDDDDddE..",  # 12
    "..EEEEEEEE..",  # 13
    "....Z..Z....",  # 14
    "....X..X....",  # 15
]
FAIRY_SIDE = [
    "....HHHH....",  # 0
    "..HfmvfmHH..",  # 1
    ".HmmmllmmmH.",  # 2
    ".SKKhmmmmmH.",  # 3
    ".GGGhmmmmmH.",  # 4
    ".SewhmmmmmH.",  # 5
    "SkckkhmmmmH.",  # 6
    ".SMkshmm33H.",  # 7
    "..SEDhm3431.",  # 8
    "...EDDE3431.",  # 9
    "...ESdE1331.",  # 10
    "...EDDdE11..",  # 11
    "..EDDDddE...",  # 12
    "..EEEEEEE...",  # 13
    ".....ZZ.....",  # 14
    ".....XX.....",  # 15
]

# Flügel (eigene Ebene, 16x20), 3 Flügelstellungen; die 6-Frame-Schleife
# läuft 0,1,2,2,1,0 mit bewusstem Timing (schneller Abschlag).
FAIRY_WINGS_DOWN = {
    "up": [
        "................",
        "..WW........WW..",
        ".WVVW......WVVW.",
        ".WVVVW....WVVVW.",
        "..WVVW....WVVW..",
        "...WVV....VVW...",
        "....WV....VW....",
        ".....F....F.....",
        "................",
    ],
    "mid": [
        "................",
        "................",
        "WWW..........WWW",
        "WVVWW......WWVVW",
        ".WVVVW....WVVVW.",
        "..WVVV....VVVW..",
        "...FFV....VFF...",
        "....FF....FF....",
        "................",
    ],
    "down": [
        "................",
        "................",
        "................",
        "................",
        ".WWWW......WWWW.",
        "WVVVVW....WVVVVW",
        ".WFVVV....VVVFW.",
        "..FFFW....WFFF..",
        "................",
    ],
}
FAIRY_WINGS_SIDE = {
    "up": [
        "................",
        "........WW......",
        ".......WVVW.....",
        "......WVVVW.....",
        "......WVVW......",
        ".......VW.......",
        ".......F........",
        "................",
        "................",
    ],
    "mid": [
        "................",
        "................",
        "................",
        ".......WWWWW....",
        "......WVVVVVW...",
        ".......WVVFF....",
        "........FF......",
        "................",
        "................",
    ],
    "down": [
        "................",
        "................",
        "................",
        "................",
        "........W.......",
        ".......WVW......",
        "......WVVVW.....",
        "......WFFFW.....",
        ".......WWW......",
    ],
}
FAIRY_WINGS_Y = 5  # Flügelraster beginnt auf Frame-Zeile 5 (Schulterhöhe)

# Eingefaltete Flügel in Menschengröße (hinter dem Körper, Ansicht unten/oben)
HUMAN_WINGS_DOWN = [
    "..W..............W..",
    ".WVW............WVW.",
    ".WVW............WVW.",
    "..F..............F..",
]
HUMAN_WINGS_UP = [
    "....WW........WW....",
    "...WVVW......WVVW...",
    "...WVVW......WVVW...",
    "....WVW......WVW....",
    ".....FW......WF.....",
]
HUMAN_WINGS_SIDE = [
    "............WW......",
    "...........WVVW.....",
    "...........WVVW.....",
    "............WF......",
]
HUMAN_WINGS_Y = 19  # Rasterzeile (Schultern)
