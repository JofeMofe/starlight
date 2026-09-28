"""Master-Palette von Starlight (64 Farben).

Einzige Quelle der Wahrheit für alle Sprite-Farben. `generators/gen_palette.py`
schreibt daraus `assets/palette/starlight.hex` und den PNG-Swatch.

Regeln (siehe docs/STYLEGUIDE.md §Palette):
- Kein reines Schwarz/Weiß. Dunkelste Farbe ist ein violettes Beinahe-Schwarz,
  hellste ein cremiges Weiß.
- Schatten laufen Richtung Violett/Blau, Lichter Richtung Creme/Gold.
- Rampen sind von dunkel nach hell sortiert, damit Sprite-Generatoren per
  Index "eine Stufe heller/dunkler" greifen können.
"""
from __future__ import annotations

# Reihenfolge = Palettenindex. Rampen jeweils dunkel -> hell.
RAMPS: dict[str, list[str]] = {
    # Nachtviolett: Outlines, tiefe Schatten, Nachthimmel, cremiges Weiß als Spitzlicht
    "dusk": ["1a1423", "2b2140", "3d2f5b", "574577", "7a6394", "a08ab2", "f4ecdf"],
    # Warme Neutraltöne: Stein, Wege, Grauschimmel, Metall
    "stone": ["3b3638", "56504f", "756d69", "968c84", "b6aca0", "d4cbbd"],
    # Braun: Holz, Erde, Klios Haare (idx 2-5), Fellfarben
    "bark": ["2e1d1f", "4a2c28", "6b3f31", "8c5539", "ad6f45", "c98f5a", "ddb07a", "efd3a4"],
    # Haut
    "skin": ["8a5048", "b37560", "d49a7a", "eab999", "f7d9c0"],
    # Rot/Rosé: Maestro-Moon-Jacke, Blüten, Herzen, Flügel-Rosé
    "rose": ["5c1f33", "8e2b3e", "bf3f4a", "e0615a", "f08d7e", "f7b8ae", "e87aa0", "f3b0c8"],
    # Glut/Gold: Laternen, Taler, Morgenlicht, Feenglanz
    "ember": ["7a3f1d", "b8612a", "e08b3a", "f2b14c", "f8d36a", "fbeaa0"],
    # Moos: Gras, Blätter, Mooswiesen
    "moss": ["1f2e2a", "26443a", "2f5e43", "3f7a47", "5a9848", "82b551", "b0cf6a", "dbe6a0"],
    # Himmel/Wasser: Sternenlicht-Blau (Flügel), Wasser, Nacht
    "sky": ["1d2b4f", "253f6e", "2f5a8c", "3d7aab", "5a9cc8", "86c0de", "b8dff0"],
    # Lagune: Türkis, Kreideküste, Tautropfen
    "lagoon": ["2a6e73", "3f9690", "6cbfb0", "a8e0cf"],
    # Magie: Feenzauber, Mondrosen, Glitzer
    "fae": ["4a2d6b", "6e3f94", "9a5cbf", "c287e0", "e0b8f0"],
}


def palette_hex() -> list[str]:
    """Alle Farben als Hex-Strings (ohne '#') in Indexreihenfolge."""
    out: list[str] = []
    for ramp in RAMPS.values():
        out.extend(ramp)
    return out


def palette_rgb() -> list[tuple[int, int, int]]:
    return [tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) for h in palette_hex()]  # type: ignore[misc]


def color(ramp: str, step: int) -> tuple[int, int, int, int]:
    """RGBA-Farbe aus einer benannten Rampe. Negative Indizes zählen von hell."""
    h = RAMPS[ramp][step]
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


def validate() -> None:
    colors = palette_hex()
    assert len(colors) == 64, f"Palette muss 64 Farben haben, hat {len(colors)}"
    assert len(set(colors)) == 64, "Palette enthält Duplikate"
    assert "000000" not in colors and "ffffff" not in colors, "Reines Schwarz/Weiß verboten"


validate()
