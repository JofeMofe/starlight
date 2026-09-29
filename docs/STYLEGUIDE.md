# Starlight – Styleguide

Verbindlich für alle Grafik-, UI- und Audio-Assets. **Konsistenz schlägt Einzelbrillanz.**
Quelle der Wahrheit für Farben ist `tools/pipeline/palette.py`; alles andere wird daraus generiert.

## 1. Grundstimmung

Warm, weich, nostalgisch, handgemacht. Jede Entscheidung beantwortet die Frage:
*Fühlt sich das warm, lebendig und handgemacht an?*

Qualitätsmaßstäbe (nur als Maßstab, nie kopieren): Lesbarkeit und Charme wie *Stardew Valley*,
Detailgrad und Licht wie *Eastward*, dynamisches Licht auf Pixel-Art wie *Sea of Stars*,
liebevolle Objekte wie *Unpacking*.

## 2. Auflösung & Maße

> **Stilwechsel 2026-09-29:** Die Welt nutzt jetzt *Sunnyside World* (16-px-Kacheln, Endesga-32-Farben).
> Alle Maße unten folgen diesem Raster; die ursprünglichen Werte (32-px-Kacheln, 640 × 360) sind überholt.

| Element | Größe | Raster-Prüfung (`size_rules.json`) |
|---|---|---|
| Interne Auflösung | 480 × 270, Integer-Scaling (×4 = 1920 × 1080, ×8 = 3840 × 2160) | – |
| Tile | 16 × 16 | Vielfache von 16 |
| Klio Menschengröße | 23 px hoch im Frame 20 × 24 (Sunnyside-Figuren: 16 px) | Vielfache von 16 × 4 |
| Klio Feengröße | 15 px hoch im Frame 24 × 20 (mit Flügeln), Brille als Rand + Glas | dito |
| NPCs | ca. 16–23 px hoch (Sunnyside-Proportionen, großer Kopf) | Vielfache von 32 × 12 |
| Hunde | Frame 20 × 16 | Vielfache von 16 × 8 |
| Pferde | Frame 40 × 24 (Körper 36 × 24) | Vielfache von 32 × 16 |
| Portraits | 128 × 128 (Klio ≥ 12 Emotionen, NPCs 8) | Vielfache von 128 |
| Item-Icons | 16 × 16 (Sunnyside) bzw. 32 × 32 | Vielfache von 32 |
| UI-Grundraster | 8 px | Vielfache von 8 |

Figuren und Tiere folgen dem Sunnyside-Aufbau: dunkelvioletter Umriss (#181425), flache Farbflächen,
eine Schattenstufe, großer Kopf, kurze Beine. Seitenansichten werden nach rechts gezeichnet und beim
Export gespiegelt (Grundrichtung im Spiel: links).

Spritesheets von `atlas.py` tragen ihre Framegröße in der JSON-Nachbardatei; `check_sizes.py` prüft,
dass das Sheet ein ganzzahliges Vielfaches davon ist.

## 3. Palette (Endesga 32 + 64 Farben der Master-Palette)

Neue Grafiken verwenden **Endesga 32** (Sunnyside-Palette, `palette.py: ENDESGA32`, ohne reines Weiß).
Die ursprüngliche 64er-Master-Palette gilt weiter für Effekte, UI und Schrift.

Datei: `assets/palette/starlight.hex`, Swatch `starlight_swatch.png` (eine Zeile pro Rampe),
Shader-Lookup `starlight_strip.png` (64 × 1, Index = Palettenindex).

| Rampe | Einsatz | Stufen (dunkel → hell) |
|---|---|---|
| `dusk` | Outlines, tiefe Schatten, Nachthimmel, cremiges Spitzlicht | 7 |
| `stone` | Stein, Wege, Grauschimmel, Metall | 6 |
| `bark` | Holz, Erde, **Klios Haare (Stufe 2–5, Glanz 5–6)**, Fell | 8 |
| `skin` | Haut | 5 |
| `rose` | Maestro-Moon-Jacke, Blüten, Herzen, Flügel-Rosé | 8 |
| `ember` | Laternen, Taler, Morgenlicht, Feenglanz | 6 |
| `moss` | Gras, Blätter, Mooswiesen | 8 |
| `sky` | Sternenlicht-Blau (Flügel), Wasser, Nacht | 7 |
| `lagoon` | Türkis, Kreideküste, Tautropfen | 4 |
| `fae` | Feenmagie, Mondrosen, Glitzer | 5 |

Regeln:
- **Kein #000000, kein #FFFFFF.** Dunkelste Farbe `#1a1423`, hellste `#f4ecdf`.
- Schatten wandern Richtung Violett/Blau (Hue-Shift), Lichter Richtung Creme/Gold.
- Alpha ist binär (0 oder 255). Halbtransparenz entsteht per Shader/Modulate, nie im PNG.
- Ausnahmen (Normal Maps, Lichttexturen, Masken, Schrift-Glyphenmasken, UI-Overlays) stehen mit
  Begründung in `tools/pipeline/palette_whitelist.txt`.

## 4. Zeichenregeln

- Grundlicht **von oben links**.
- Außenlinien farbig (dunklere Stufe der Füllfarbe, meist `dusk` 0–1), selektiv aufgehellt, wo Licht trifft.
- Kein Pillow-Shading, kein Anti-Aliasing gegen Transparenz, **keine Mixels**:
  Sprites werden nie skaliert; jedes Pixel ist gleich groß. Vergrößern nur per Integer-Nearest
  für Vorschauen/Screenshots.
- Dithering sparsam und nur bewusst (z. B. Himmelsverläufe, Stoffstrukturen).
- Klio hat die höchste künstlerische Priorität: Brille in **jeder** Darstellung sichtbar
  (Gestell + 1–2 Glanzpixel), lange braune, weich gewellte Haare mit 4–5 eigenen Stufen.

## 5. Animation

- Mindest-Framezahlen laut AGENTS/CLAUDE.md §8.5. Timing bewusst setzen (Frame-Dauern in der
  Atlas-JSON, nicht alle gleich lang), Squash & Stretch, Nachschwingen (Haare, Mähne, Flügel, Kleidung).
- Sekundäranimation per Shader nur mit Pixel-Snap (UV auf Texel-Raster), damit nichts verschmiert.

## 6. Licht & Shader

- Tag-Nacht über `CanvasModulate` mit handkuratierter `Gradient`-Rampe (Morgengold → Mittag neutral
  → Abendrosa → Nachtblau), nicht bloßes Abdunkeln.
- Normal Maps aus `normalmap.py`: abgeflachte, 4–8-stufige Normalen, Godot-Konvention (+Y unten).
- Alle Shader bleiben pixelgenau.

## 7. UI & Schrift

- Motive: Holz, Pergament, Blüten. 9-Slice-Rahmen, Verläufe nur über Palettenstufen.
- **Schrift „Glimmer“** (selbst gezeichnet, `tools/pipeline/fonts/glimmer.txt`):
  Zeilenhöhe 12 px, Versalhöhe 7 px, x-Höhe 5 px, Unterlängen 2 px, Grundlinie bei 9.
  Enthält ASCII, ÄÖÜäöüß, é/è, „ “ ” ‚ ‘ ’, – —, …, ·, ×, °, €, ♥, ★. Ziffern einheitlich 5 px
  (Tabellenziffern für rollende Zähler). Textfarbe Creme `#f4ecdf`, Schatten `#1a1423` 1 px nach rechts unten.
- Neue Zeichen: Glyphe in `glimmer.txt` ergänzen, `python tools/pipeline/build_assets.py`.
- Geplant: Überschriften-Schrift (größere Versalhöhe) und Barrierefreiheits-Variante (M2/M6).
- Textboxen müssen 30 % längere Texte (Englisch/andere Sprachen) aufnehmen.

## 8. Audio (Kurzfassung, Details §10)

Akustisch-warm (Harfe, Gitarre, Holzbläser, Glockenspiel); Mondscheinbühne funky 80er, **komplett originell**.
OGG Vorbis, Musik ≈ −16 LUFS, SFX −14…−18 LUFS, nahtlose Loops, leichte Zufallsvariation bei Wiederholungen.

## 9. Visuelle QA-Checkliste (nach jedem Meilenstein)

1. Silhouetten lesbar? 2. Farbharmonie / nur Palette? 3. Keine Mixels, keine Unschärfe?
4. Y-Sort korrekt? 5. Lichtstimmung passend zur Uhrzeit? 6. UI-Überlappungen, abgeschnittene Texte?
