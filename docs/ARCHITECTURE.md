# Starlight – Architektur

Stand: M1 (Das Gefühl). Wird mit jedem Meilenstein fortgeschrieben.

## 1. Engine & Projekteinstellungen

| Einstellung | Wert | Begründung |
|---|---|---|
| Engine | Godot 4.4.1 stable (Standard-Build, kein .NET) | neueste stabile Version in der Umgebung, Export-Templates vorhanden |
| Renderer | **Compatibility (OpenGL 3.3 / GLES3)** | 2D-Licht inkl. Normal Maps (CanvasTexture) und Schatten wird unterstützt; läuft auf älteren GPUs, integrierter Grafik und Steam Deck; ermöglicht später Web-Export. Forward+ bringt für reines 2D keinen sichtbaren Vorteil, kostet aber Kompatibilität. |
| Interne Auflösung | 640 × 360 | §4.1 |
| Stretch | `viewport` / `keep` / `integer` | pixelgenaue Integer-Skalierung (×2 bei 720p, ×3 bei 1080p, ×4 bei 1440p, ×6 bei 4K) |
| Texturfilter | Nearest | keine Unschärfe |
| Pixel-Snap | Transforms + Vertices | kein Subpixel-Zittern |
| Physik | 60 Ticks, **Physik-Interpolation an** | §4.1; Interpolation hält Bewegung auf 90/120/144-Hz-Bildschirmen ruckelfrei. Teleports brauchen `reset_physics_interpolation()`; die Kamera läuft im Physik-Takt. |
| GDScript-Warnungen | `untyped_declaration` = Fehler; unsichere Property-/Methodenzugriffe = Warnung | erzwingt statische Typisierung (§1.9). `unsafe_cast` und `unsafe_call_argument` sind aus, weil JSON-Daten zwangsläufig als Variant ankommen und explizit per `int()`/`as` gewandelt werden. |
| Fenster | 1280 × 720 Startgröße | ×2-Skalierung als angenehmer Start |

## 2. Ordner

Siehe CLAUDE.md §3. Ergänzungen:
- `tools/lint/` – GDScript-Warnungs-Scanner (`lint_gdscript.py`)
- `tools/setup_tools.sh` – Hilfswerkzeuge (rcedit) einrichten
- `tools/pipeline/fonts/` – Quelltext der Pixel-Schrift
- `default_bus_layout.tres` im Projektwurzelverzeichnis (Godot-Standardort)
- `scenes/ui/theme/starlight_theme.tres` – globales Theme (Schrift Glimmer)

## 3. Autoloads (Reihenfolge = Ladereihenfolge)

| Autoload | Datei | Stand M0 |
|---|---|---|
| `EventBus` | `scripts/autoload/event_bus.gd` | alle globalen Signale deklariert |
| `App` | `scripts/autoload/app.gd` | *zusätzlich*: Version, Kommandozeile (`--smoke`, `--scene=`, `--screenshot=`), Screenshots in Integer-Auflösung |
| `Settings` | `settings.gd` | `user://settings.cfg`, Bus-Lautstärken, Vollbild, Barrierefreiheits-Werte, InputMap aus `data/config/input_default.json` + Überschreibungen |
| `Localization` | `localization.gd` | Sprache setzen, `text(key, vars)` mit Platzhaltern |
| `InputGlyphs` | `input_glyphs.gd` | erkennt Tastatur/Gamepad und Gamepad-Familie, liefert Tastenbezeichnungen |
| `GameState` | `game_state.gd` | Spielerinnen (Player-ID-basiert, koop-fähig), Hofname, Seelenhund, Flags, Herzquelle, Spielzeit |
| `TimeManager` | `time_manager.gd` | Uhr, Tag, Jahreszeit, Jahr, Wochentag, 8 Mondphasen, Pausenquellen, Einschlafen um 02:00 |
| `WeatherManager` | `weather_manager.gd` | deterministisches Tageswetter aus Seed + Tag, 3-Tage-Vorschau |
| `SaveManager` | `save_manager.gd` | JSON-Slots 1–3 + Autosave, atomisch mit Backup, Migrationen, Meta + Thumbnail |
| `AudioManager` | `audio_manager.gd` | Musik-Crossfade, Ambience-Layer, SFX-Pool mit Variation, Innenraum-Hall |
| `SceneRouter` | `scene_router.gd` | Szenenwechsel mit Blende, Spawnpunkte (Gruppe `spawn_points`) |
| `DialogueManager` | `dialogue_manager.gd` | Gerüst: JSON-Dialoge, Bedingungen (`DialogueConditions`), Zeitpause |

Autoloads haben keinen `class_name` (Namenskonflikt). Reine Logik, die ohne Szenenbaum testbar sein
soll, liegt in `class_name`-Klassen unter `scripts/systems/` bzw. `scripts/util/`
(`DialogueConditions`, `InputBinding`).

## 4. Datenfluss & Muster

- **Signale über EventBus** statt direkter Referenzen zwischen Systemen.
- **Daten statt Code:** Konfiguration als `.tres` mit eigenem Resource-Typ (`TimeConfig` →
  `data/config/time.tres`) oder JSON (`weather.json`, `input_default.json`). JSON wird per
  `include_filter="data/*.json"` in den Export übernommen.
- **Serialisierung:** Jedes zustandsbehaftete System implementiert `to_dict()`/`from_dict()`.
  `SaveManager.collect_state()` sammelt `game_state`, `time`, `weather`; neue Systeme hängen sich dort an.
- **Spielstand-Versionierung:** `save_version` + Methoden `_migrate_<n>_to_<n+1>()`.
- **Wetter wird nicht gespeichert**, nur der Seed: `weather_for_day(tag)` ist rein und deterministisch,
  dadurch sind Vorschau und tatsächliches Wetter immer konsistent.
- **Mondphasen** (8 Phasen, 28 Tage = eine Jahreszeit): Längen `[1,6,1,6,1,6,1,6]` in `time.tres`,
  dadurch genau **eine** Vollmondnacht pro Jahreszeit (Tag 15) → Maestro-Moon-Nacht.
- **Zeit:** 06:00–02:00 = 1200 Spielminuten × 0,7 s = 14 min Echtzeit. Die Uhr läuft nur, wenn eine
  Spielszene `TimeManager.running = true` setzt; Menüs/Dialoge melden Pausenquellen an.

## 5. Eingabe

`data/config/input_default.json` definiert alle Aktionen im Format `key:W`, `mouse:left`,
`joy_button:a`, `joy_axis:left_y-`. `Settings.rebind()` speichert Überschreibungen in
`user://settings.cfg`. Tasten sind **physische** Keycodes (QWERTZ/AZERTY-fest).

Abweichung von §4.6 (Konfliktauflösung): „R/LB = Pfeifen“ und „Schultertasten = Werkzeugleiste“
kollidieren auf LB. Entscheidung: **LB = Pfeifen**, Werkzeugleiste auf **LT/RT** (Trigger),
Werkzeug benutzen **RB** bzw. linke Maustaste, Inventar **Tab/Menu(Start)**, Pause **Esc/View(Back)**.

## 6. Tests & Checks

| Ebene | Ort | Werkzeug |
|---|---|---|
| Unit | `tests/unit/` | gdUnit4 5.0.5 |
| Integration | `tests/integration/` | gdUnit4: alle Szenen instanziierbar, Referenzen, Übersetzungen DE/EN, JSON gültig, Projekteinstellungen |
| Smoke | `tests/smoke/smoke_run.tscn` | Bot spielt 7 Tage, Autosave-Rundreise, Szenenwechsel |
| M1-Bot | `tests/smoke/m1_bot.tscn` | spielt die Kernmechanik mit simulierten Tasten durch (22 Prüfungen), misst CPU-Zeit pro Frame; `-- --shots=ORDNER` erzeugt QA-Screenshots |
| Lint | `tools/lint/lint_gdscript.py` | lädt jedes Skript im Debug-Modus neu, jede Analyzer-Warnung = Fehler |
| Assets | `tools/pipeline/build_assets.py` | Palette, Maße, Lizenzen/Manifest |
| Export | `run_all_checks` | Windows-Export + 60-s-Lauf mit `--smoke` (unter Linux via Wine) |

Ein Befehl: `tools/run_all_checks.ps1` (Windows) bzw. `tools/run_all_checks.sh` (Linux/Cloud).

## 7. Export

`export_presets.cfg`: „Windows Desktop“ (x86_64, PCK eingebettet, Icon `icon.ico`, Produktname,
Version `0.<meilenstein>.<build>`) und „Linux“ (x86_64, Steam Deck).
Icon und Versionsinfo schreibt Godot 4.4 über **rcedit** in die Exe (`tools/setup_tools.sh`
lädt es und trägt es in die Editor-Einstellungen ein; unter Linux läuft rcedit über Wine und
muss mit UTF-8-Locale gestartet werden, sonst werden „–“/„©“ zerstört).

## 8. Gameplay-Bausteine (ab M1)

| Baustein | Ort | Zweck |
|---|---|---|
| `StateMachine` | `scripts/systems/state_machine.gd` | schlanke Zustandsmaschine (Callables für enter/update/exit, Zeit im Zustand) |
| `SheetAnimator` | `scripts/components/sheet_animator.gd` | spielt Pipeline-Spritesheets anhand der JSON (Frame-Dauern, `bob`), Phase beim Richtungswechsel behalten, feste Frames für Code-gesteuerte Ebenen |
| `Interactable` | `scripts/components/interactable.gd` | Area2D auf Ebene „interact“; Besitzer liefert Hinweise per `prompt_provider`, primäre (E) und sekundäre (Leertaste) Aktion |
| `PixelCamera` | `scripts/components/pixel_camera.gd` | pixelfeste Kamera mit Vorausblick, 1-px-Puls, Kartengrenzen |
| `MapBuilder` | `scripts/systems/map_builder.gd` | Karte aus JSON: Kachelsatz zur Laufzeit (TileSet + Kollisionen), Kantenmasken, Objekte, Randwände, Startpunkte |
| `FlightEnergy`, `SizeChangeRules`, `HorseGait` | `scripts/systems/` | reine, unit-getestete Spiellogik |
| `MovementConfig` | `scripts/data_types/` + `data/config/movement.tres` | alle Bewegungswerte |
| `PhysicsLayers` | `scripts/util/physics_layers.gd` | Kollisionsebenen: 1 hoch, 2 niedrig (Fee überfliegt), 3 Spielerin, 4 Tiere, 5 Interaktion |

**Szenen:** `scenes/player/klio.tscn` (Körper-, Haar-, Feen- und Flügelebene, Partikel, Sensor),
`scenes/animals/dog.tscn`, `horse.tscn` (je mit NavigationAgent2D, Interactable, Partikel),
`scenes/world/test_meadow.tscn` (NavigationRegion2D → Boden, Deko, y-sortierte Welt mit
Zaun-TileMapLayer und Figuren), `scenes/ui/hud.tscn`.

**Reiten:** Das Reittier bewegt sich und ruft danach `Klio.sync_to_mount()` auf (keine
Verzögerung um einen Frame). Klio liegt 1 px vor bzw. hinter dem Tier in der Y-Sortierung
(in der Ansicht von vorn sitzt sie hinter dem Pferdekopf).

**Navigation:** Das Navigationsnetz wird nach dem Kartenaufbau aus allen statischen Kollisionen
(hoch + niedrig) mit 13 px Agentenradius gebacken, damit auch das Pferd nicht an Zaunecken hängt.

**Sprites:** Füße liegen auf dem Knotenursprung (Y-Sortierung nach Fußpunkt). Figuren werden nie
skaliert; Richtungswechsel links/rechts per `flip_h`.
