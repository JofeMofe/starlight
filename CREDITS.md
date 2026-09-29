# Credits

## Starlight – Klio goes Fairy

Design, Code, Pixel-Art, Schrift „Glimmer“: Starlight-Projekt (Code MIT, siehe `LICENSE`).
Grafiken in `assets/` sind selbst erstellt (prozedural bzw. als Pixelkarten in `tools/pipeline/`)
oder aus frei lizenzierten Vorlagen abgeleitet (siehe „Fremd-Assets“); die vollständige Liste steht in
`docs/ASSET_MANIFEST.csv`.

## Engine

- **Godot Engine** 4.4.1 – MIT-Lizenz – © Juan Linietsky, Ariel Manzur und Godot-Mitwirkende –
  https://godotengine.org/license

## Werkzeuge & Bibliotheken

| Name | Zweck | Lizenz | Quelle | Lizenztext |
|---|---|---|---|---|
| gdUnit4 5.0.5 (Mike Schulze) | Unit-/Integrationstests (nur Entwicklung, nicht im Export) | MIT | https://github.com/MikeSchulze/gdUnit4 | `docs/licenses/gdUnit4_MIT.txt` |
| rcedit 2.0.0 (GitHub/Electron) | Icon & Versionsinfo in der Windows-Exe (nur Build-Werkzeug, wird nicht mitgeliefert) | MIT | https://github.com/electron/rcedit | https://github.com/electron/rcedit/blob/master/LICENSE |
| Pillow, NumPy | Asset-Pipeline (nur Entwicklung) | HPND / BSD-3 | pypi.org | – |

## Fremd-Assets

### Welt der Mooswiesen – Sunnyside World

Boden (Gras, Weg, Wasser), Zaun, Bäume (mit Wind-Animation), Büsche, Steine, Blumen, Gräser,
Baumstumpf und die Pilze des Feenrings stammen aus **Sunnyside World** von **Daniel Diggle**,
https://danieldiggle.itch.io/sunnyside (Version 2.1, kostenlos, kommerzielle Nutzung erlaubt,
Weiterverkauf/Weiterverbreitung des Pakets nicht erlaubt, keine Nutzung zum KI-Training).
Lizenztext: `docs/licenses/Sunnyside_World.txt`. Die Übergänge von Weg und Wasser sind im
Sunnyside-Stil aus den Original-Kacheln zusammengesetzt, die Zaunkacheln aus Pfosten und Latten.
Das Originalpaket liegt nicht im Repository; `tools/pipeline/fetch_vendor.py` lädt es bei Bedarf.

### Eigene Figuren im Sunnyside-Stil

Klio (Menschen- und Feengröße, Flügel), das Pferd Holunder und der Seelenhund sind eigene
Pixelkarten (`tools/pipeline/sprites/klio_sunny.py`, `animals_sunny.py`) in der frei verwendbaren
Palette **Endesga 32** (https://lospec.com/palette-list/endesga-32), damit sie zur Sunnyside-Welt passen.
