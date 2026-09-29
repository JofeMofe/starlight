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

### Klio (Menschen- und Feengröße) – Liberated Pixel Cup (LPC)

Klios Sprites (`assets/sprites/characters/klio_body.png`, `klio_fairy.png`) sind aus Teilen des
[Universal LPC Spritesheet Character Generator](https://github.com/LiberatedPixelCup/Universal-LPC-Spritesheet-Character-Generator)
zusammengesetzt, auf die Starlight-Palette umgefärbt und angepasst (offene Jacke, Haare, Brille, Feengröße).
Verwendete Lizenz: **OGA-BY 3.0** (bzw. CC0 für Kette und Ohrstecker), Lizenztext:
`docs/licenses/OGA-BY-3.0.txt`. Die Originaldateien liegen unter `tools/pipeline/vendor/lpc/`,
die Zuordnung Datei → Autor:innen → Quelle steht in `tools/pipeline/vendor/lpc/CREDITS.csv`.

Künstler:innen: JaidynReiman, Nila122, Benjamin K. Smith (BenCreating), bluecarrot16, TheraHedwig,
Evert, MuffinElZangano, Durrani, Pierre Vigier (pvigier), ElizaWy, Matthew Krohn (makrohn),
Johannes Sjölund (wulax), Stephen Challener (Redshrike), Joe White.
