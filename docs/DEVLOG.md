# Starlight – Entwicklungstagebuch

Neueste Sitzung oben. Pro Sitzung: was, warum, offene Punkte.

---

## Sitzung 6 – 2026-09-29 · Neuer Look: Sunnyside World, Klio/Pferd/Hund neu gezeichnet

### Anlass und Entscheidungen

- Nutzer: „Optik von Grund auf neu, so wie es Assets vorgeben, professionell, kostenlos.“ Auswahl
  des Nutzers zunächst **Mana Seed**. Beim Prüfen der Lizenz fiel auf, dass Mana Seed jede Nutzung
  in Projekten mit generativer KI – ausdrücklich auch KI-geschriebenem Code – untersagt. Starlight
  wird von einer KI programmiert, das Repository ist öffentlich → Mana Seed nicht verwendet, die
  heruntergeladenen Dateien gelöscht, nichts davon eingecheckt. Nutzer informiert; neue Wahl:
  **Sunnyside World** (Daniel Diggle): kostenlos, auch kommerziell, nur KI-*Training* ist untersagt.
  Festgehalten in CLAUDE.md §9.
- Sunnyside darf nicht als Paket weiterverbreitet werden. Deshalb liegt es **nicht** im Repository:
  `tools/pipeline/fetch_vendor.py` lädt es bei Bedarf (kostenloser itch.io-Download, ohne Konto)
  nach `tools/pipeline/vendor/sunnyside/` (in `.gitignore`); eingecheckt sind nur die daraus
  zugeschnittenen Spielgrafiken. Ohne Netz bleiben die vorhandenen Grafiken unverändert.
- **Maßstab:** Ein erster Klio-Entwurf mit 31 px war so groß wie die Sunnyside-Bäume (Figuren dort:
  16 px). Klio ist deshalb 23 px hoch – etwas größer als Sunnyside-Figuren, damit Brille und lange
  Haare lesbar bleiben. Kacheln 16 px, **interne Auflösung 480 × 270** (×4 = 1080p exakt) statt
  640 × 360; die Karte behält 40 × 30 Zellen, damit die Welt relativ zur Figur gleich groß bleibt.
  Bewegungswerte (`movement.tres`) und Kamera auf den neuen Maßstab skaliert (≈ ×0,6).

### Was wurde gemacht

- **Welt** (`sprites/sunny_world.py`): Dual-Grid-Bodenatlas mit Weg- und Wasserübergängen im
  Sunnyside-Stil (gerade Kanten, 45°-Fasen, dunkelgrüne Graskante, zweireihiger Schattensaum),
  Füllungen aus Original-Kacheln. Zaun für alle 16 Nachbarmasken aus Pfosten und Latten. Objekte:
  Laubbaum und Tanne mit Wind-Animation (`SwaySprite`, jede Instanz mit eigener Phase), Busch,
  Beerenbusch, Stein, Kiesel, Grasbüschel, Blumen, Baumstumpf, Feenring aus Sunnyside-Pilzen.
  Waldsaum oben zwei Kacheln tiefer, damit die Kronen nicht an der Kamerakante abgeschnitten sind.
  Wege auf zwei Kacheln verbreitert.
- **Klio** (`sprites/klio_sunny.py`): eigene Pixelkarten in Endesga 32: lange dunkelbraune Haare
  mit Mittelscheitel ohne Pony, schmale rechteckige Brille (Rand, Glas, grüngraues Auge),
  offene Jeansjacke über schwarz-lila Top, Jeans, dunkle Converse mit cremiger Sohle. Drei
  Ansichten, Laufzyklus (Kontakt/Hochfedern, Schrittgeräusch über `step`-Daten), Blinzeln,
  Reitpose, zierliche Fee (15 px) mit Libellenflügeln (6-Frame-Schlag).
- **Pferd und Hund** (`sprites/animals_sunny.py`): Sunnyside hat keine Pferde/Hunde → eigene Figuren
  im Sunnyside-Tierstil. Pferd (Fuchs) mit Schritt, Trab und Galopp (Schwebephase als Anheben
  des ganzen Tieres), Hund (Border-Collie-Mix, tricolor) mit Gehen, Rennen, Sitzen.
  Fellfarben als Rampen, damit die Genetik (M3) nur Rampen tauschen muss.
- HUD an Bildschirmränder verankert (passt jetzt bei jeder Auflösung), Sitzpunkte, Kollisionen,
  Interaktionsradien, Schatten und Test-Bot auf den neuen Maßstab umgestellt.
- Palette: Endesga 32 zusätzlich erlaubt (`palette.py`), Sunnyside-Grafiken per Whitelist in
  Originalfarben. Alte LPC-Module und -Vorlagen entfernt.

### Verifiziert

- `tools/run_all_checks.sh`: Asset-Checks, Lint (0 Warnungen), 46/46 Tests, 7-Tage-Smoke-Bot,
  Kernmechanik-Bot (Laufen, Verwandeln, Fliegen über die Hecke, Hund reiten, Feenring, Pferd in
  drei Gangarten, Rufen, Streicheln), Windows- und Linux-Export mit 30-s-Startlauf: alles grün.
- Screenshots: `docs/screenshots/m1/sunnyside/` (11 Bilder vom Bot).

### Offen

- Klio, Pferd und Hund sind eine erste Fassung im neuen Stil; Signature-Animationen (Brille
  zurechtschieben, Haare hinters Ohr), Pferde-Idle (Grasen, Schweifschlagen) und Portraits fehlen.
- Nutzer-Feedback zum neuen Look abwarten.

---

## Sitzung 5 – 2026-09-29 · Professioneller Look: LPC-Welt und LPC-Pferd

### Anlass und Entscheidung

Nutzer: Auflösung bleibt, aber das Ergebnis muss professionell werden; alle gängigen Quellen
nutzen, Lizenzen spielen keine Rolle, weil Starlight ein privates Geschenk ist. Festgehalten als
Projektentscheidung in CLAUDE.md §9. Grenze, die ich selbst ziehe: keine aus kommerziellen Spielen
herausgelösten Grafiken.

### Was wurde gemacht

- **Welt:** Boden aus dem LPC-Geländeset von ElizaWy (`vendor/eliza/Terrain`, Originalfarben).
  Die Vorlagen sind eckbasiert; der MapBuilder legt deshalb eine um eine halbe Kachel versetzte
  Bodenebene an („Dual Grid“, `_build_ground`), jede Kachel wählt sich über die vier Kartenzellen
  an ihren Ecken. Ergebnis: runde Ufer mit Uferkante, natürliche Wegränder. Der Baker
  (`sprites/lpc_terrain.py`) setzt die zwei fehlenden Diagonalfälle aus Vierteln zusammen.
  Die Rasterebene darunter trägt weiter die Kollisionen.
- **Objekte:** Laubbaum, blühender Baum (neu, `tree_blossom`), Busch, Stein, Blumen, hohes Gras,
  Kiesel und die Pilze des Feenrings aus demselben Set (`sprites/lpc_objects.py`), auf ein
  32er-Raster aufgefüllt, Fußpunkt unten.
- **Pferd:** [LPC] Horses von bluecarrot16 (über GitHub bezogen), auf die Palette umgefärbt:
  Stehen mit gelegentlichem Grasen, Schritt, Trab (Schritt schneller getaktet), Galopp in drei
  Ansichten, Frames 128×128. Hufschlag-Sounds stehen jetzt als `hoof` in den Animationsdaten.
  Sitzpunkte für Klio neu eingestellt.
- Alte Zeichenfunktionen (Bäume, Büsche, Steine, Pferde-Rig) entfernt.

### Offen

- **Hund:** noch der Eigenbau und damit das einzige Element, das stilistisch herausfällt. Auf GitHub
  gibt es im LPC-Stil nur einen Wolf mit Drohgebärden; die LPC-Hunde liegen auf opengameart.org,
  das in dieser Umgebung gesperrt ist → Nutzer erneut um Freigabe gebeten.
- Zaun und Feenring-Glitzer sind noch Eigenbau; Reiten nutzt die LPC-Sitzpose.

---

## Sitzung 4 – 2026-09-29 · Klio aus frei lizenzierten Vorlagen (LPC)

### Anlass

Feedback zu Klio v4 und dem neuen Hund: Beim Reiten fehlten die Beine, die Fee wirkte wie ein
Gnom, der Hund „derpy“ und kaum als Hund erkennbar, das Profil nicht hübsch. Wunsch des Nutzers:
Vorlagen aus dem Netz verwenden und sich daran orientieren.

### Was wurde gemacht

- **Quelle:** [Universal LPC Spritesheet Character Generator](https://github.com/LiberatedPixelCup/Universal-LPC-Spritesheet-Character-Generator)
  (Liberated Pixel Cup). Jede Datei hat dort eigene Lizenzangaben; verwendet werden nur Teile, die
  wahlweise unter **OGA-BY 3.0** oder **CC0** stehen (§9: Namensnennung, kein Share-Alike).
  Originale unter `tools/pipeline/vendor/lpc/`, Zuordnung Datei → Autor:innen → Lizenz in
  `vendor/lpc/CREDITS.csv`, Lizenztext `docs/licenses/OGA-BY-3.0.txt`, Namensnennung in `CREDITS.md`.
- **Klio** (`sprites/klio_lpc.py`, `generators/gen_klio.py`): weiblicher Körper, Frisur „xlong“
  (lang, glatt, Mittelscheitel, kein Pony), Brille, T-Shirt, Strickjacke als offene Jeansjacke,
  Hose, Schuhe, Kette, Ohrstecker. Automatisch auf die Master-Palette umgefärbt (Haare dunkelbraun,
  Augen dunkelgrüngrau, Shirt schwarz, Jacke hell-, Hose dunkelblau, Brille schwarz mit
  durchsichtigen Gläsern). Im Profil wird eine dünne Strähne vor dem Körper entfernt.
  Frames 64×64 (LPC-Standard), Laufzyklus 8 Frames, Stehen 2 Frames, Reiten = LPC-Sitzpose.
- **Fee:** dieselbe Figur auf halbe Größe verkleinert (Umrisse bleiben erhalten), Brille und
  Augen von Hand gesetzt → erwachsene, schlanke Proportionen statt Kopffüßer. Neue libellenartige
  Flügel (zwei schlanke Paare, lila/hellblau, leicht transparent). Frames 32×32.
- Spielszene: Sprite-Offsets und Sitzpunkte auf dem Pferd an die neuen Maße angepasst.
- Alte handgezeichnete Klio-Module (v1–v4) entfernt (bleiben in der Git-Historie).
- `check_licenses.py` erlaubt jetzt zusätzlich OGA-BY-3.0; `GeneratedAsset` kann Lizenz,
  Autor:innen und „modifiziert“ für abgeleitete Assets angeben.

### Entscheidungen

- **LPC statt Eigenbau:** Der LPC-Stil ist erprobt, hat genau unseren Maßstab (32er-Kacheln,
  ca. 48 px große Figuren) und bietet Laufzyklen in vier Richtungen. Die Anpassung an Palette
  und Klios Merkmale läuft reproduzierbar über die Pipeline.
- **Haare im Körper-Sheet:** LPC zeichnet das Haar-Wippen beim Laufen bereits in jeden Frame.
  Die separate Haar-Ebene bleibt als leeres Sheet bestehen, damit Szene und Code gleich bleiben.
- **Fee 32×32 statt 16×20:** Mit 16×20 ließen sich nur Chibi-Proportionen darstellen (Feedback
  „Gnom“). Die Figur selbst ist ca. 12×24 px groß, die Flügel brauchen den Rest.

### Netzwerk

opengameart.org, itch.io und kenney.nl sind in dieser Cloud-Umgebung per Richtlinie gesperrt.
Die passenden LPC-Pferde, -Reitposen und -Hunde liegen auf opengameart.org → Nutzer gebeten,
die Domain freizugeben. Bis dahin bleiben Pferd und Hund die bisherigen Eigenbauten.

---

## Sitzung 3 – 2026-09-28 · Grafik-Durchgang nach Nutzer-Feedback (M1-Nachbesserung)

### Anlass

Feedback nach M1: Die Grafik wirke „0815“, flach und austauschbar. Klio soll der Freundin des
Nutzers nachempfunden sein: dunkelbraune, glatte Haare ohne Pony, dunkelgrüngraue Augen, eckige,
schmale, schwarze Brille, viel Schwarz und Lila, Jeans statt Rock, Jeansjacke, Converse-artige
Stoffschuhe, Ringe, Ketten, Ohrstecker, schwarzer Nagellack.

### Was wurde gemacht

- **Klio v4** (`tools/pipeline/sprites/klio_v4.py`, `klio_v4_sheet.py`): komplett neu gezeichnet,
  handgesetzte Pixelkarten in allen drei Ansichten (vorn, hinten, Profil), Mittelscheitel, Haare über
  den Schläfen, Glanzband auf dem Hinterkopf, schwarzes Shirt mit eigenem lila Stern-Mond-Emblem,
  Jeansjacke, Jeans, Stoffschuhe, Ohrstecker, Ringe, Kette. Fee in demselben Look (Brille mit
  Glanzpixeln statt schwarzem Balken), Flügel in Lila. Idle, Laufen (mit Schrittanhebung und
  Armschwung im Profil), Reiten.
- **Wiese v2** (`meadow_v2.py`): Gras mit gestempelten Halmbüscheln, Wegkanten mit Gras-Fransen,
  texturiertes Wasser, Bäume aus 13 Blattbüscheln, Blumen, hohes Gras, Kiesel; Objektschatten;
  deterministische Deko-Streuung (`scatter` in den Map-JSONs, `MapBuilder._scatter`).
- **Pferd**: Muskelglanz an Schulter, Rücken, Hinterhand und Wange (weich ausgefranst), dunkleres
  Maul, Nüstern, strähnige Mähne und Schweif; Kruppenglanz von hinten, Brustmuskel von vorn.
- **Hund neu** (`sprites/dog_art.py`): Tricolor-Collie-Mix mit handgesetzten Pixelkarten für Kopf,
  Rumpf, Rute (vorn, hinten, Seite, Sitzen): Schlappohren, bernsteinfarbene Augen mit Glanzpunkt,
  lohfarbene Brauen und Wangen, weiße Blesse und Halskrause, lila Halsband mit goldener Marke
  (passend zu Klio). Die Beine kommen weiter aus dem Rig, die Rute wedelt per Scherung.
- `rig.render` hat jetzt einen Textur-Haken pro Material und liefert ein beschreibbares Bild.
- Sitzplatz der Fee auf dem Hund etwas nach hinten auf den Rücken verschoben.

### Entscheidungen

- **Keine echten Bandlogos, Namen oder Bilder realer Künstler** (§7.9, §9): Das Fan-Sein wird über
  ein eigenes Stern-Mond-Emblem und die Farbwelt Schwarz/Lila ausgedrückt.
- **Reale Person als Vorbild:** Klio wird nur aus Beschreibungen gestaltet, nicht aus Fotos. Als
  persönliches Geschenk unproblematisch; vor einer öffentlichen Veröffentlichung braucht es das
  Einverständnis der dargestellten Person (§5.1).
- **Hybrid aus Pixelkarte und Rig beim Hund:** Bei 32×24 Pixeln wirkte die rein geometrische Form
  klobig; von Hand gesetzte Köpfe tragen den Charme, das Rig behält die weichen Beinbewegungen.

### Verifikation

- `tools/run_all_checks.sh` → **ALLES GRÜN**: Assets 0 Fehler, Lint 0 Warnungen, Tests 46/46,
  Smoke-Bot 7 Tage, M1-Bot OK (Frame-CPU headless Ø 2,4 ms), Windows-Exe unter Wine 60 s und
  Linux-Build 60 s ohne Fehler.
- Screenshots: `docs/screenshots/m1/art_pass_*.png` (Klio v1–v4, Wiese, Tiere, Szenen im Spiel).
  Selbst geprüft: Silhouetten lesbar, Brille in allen Ansichten sichtbar, keine Mixels.

### Offen

- Teichufer noch eckig (Autotiling-Ecken, M2), Rückansicht des Hundes am schwächsten,
  Pferd weiterhin aus Formen (Palette-Swap-Basis für M3), Portraits und Signature-Animationen (M6).
- Nutzer-Feedback zum neuen Look abwarten, dann M2 „Die Welt lebt“.

---

## Sitzung 2 – 2026-09-28 · Meilenstein M1 „Das Gefühl“ ✅

### Was wurde gemacht

1. **Klio als Pixel-Figur** (handgesetzte Pixelkarten, `tools/pipeline/sprites/klio_art.py`):
   Menschengröße 32×48 in drei Ansichten mit getrennten Ebenen für Kopf/Körper und lange Haare,
   Laufzyklus (8 Frames), Stehen mit Atmen und Blinzeln, Reitpose; Feengröße 16×20 mit 1-px-Brille,
   Blütenkranz und separater Flügelschleife. Jede Version visuell geprüft und nachgebessert
   (Brille wirkte zuerst wie eine Sonnenbrille, Fee-Gesicht wie eine Maske, Seitenansicht streifig).
2. **Tier-Rig** (`sprites/rig.py`): Tiere aus Formen mit automatischer Schattierung (Licht oben
   links), farbiger Außenlinie und Trennlinien. Pferd Holunder (Schritt/Trab/Galopp über
   Beinphasen: Vier-, Zwei-, Dreitakt) und Collie-Mix (Laufen, Rennen, Sitzen) in drei Ansichten.
3. **Wiese**: Kachelatlas mit Gras-Varianten und je 16 Kantenmasken für Weg, Wasser, Zaun; Baum,
   Busch, Stein, Blumen, Feenring; Partikel, Schatten, HUD-Symbole.
4. **Synthesizer + 18 Soundeffekte** (`tools/pipeline/audio/synth.py`), bitgenau reproduzierbar.
5. **Spielmechanik** (siehe GDD §2a/2b): Zustandsmaschine für Klio, Größenwechsel mit vollem
   Effekt und Regeln, Fliegen über niedrige Hindernisse, Seelenhund (Folgen per Navigation, Rufen,
   Streicheln, Reiten als Fee), Pferd (Pfeifen, Streicheln, Reiten mit drei Gangarten, Wendekreis,
   Sprung), Haar-Feder, Pixel-Kamera, HUD mit Kontexthinweisen und Hilfe.
6. **MapBuilder**: Karte und Kachelsatz komplett aus JSON (ASCII-Raster), Navigationsnetz zur Laufzeit.
7. **Tests**: 46 Unit-/Integrationstests (9 neu), M1-Bot mit 22 Prüfungen und CPU-Messung, in
   `run_all_checks` eingebunden. Physik-Interpolation für Bildschirme über 60 Hz.

### Entscheidungen

- **Kamera-„Zoom-Puls“ als 1-px-Stoß** statt echtem Zoom: Nicht-ganzzahliger Zoom erzeugt Mixels (§8.4).
- **Verwandlungseffekt ohne Skalierung**: Flackern zwischen beiden Gestalten, Blitz, Funkenwirbel –
  alles pixelgenau.
- **Prototyp in Kapitel 2**: Größenwechsel überall (5 Feenglanz), am Feenring gratis; die
  Kapitel-1-Regel „nur am Ring“ ist implementiert und getestet.
- **Pferdesteuerung**: Leertaste antippen = eine Gangart schneller, Richtung loslassen = sanft
  langsamer werden, im Galopp springen. Sprung nur bei freier Landestelle (keine Frustration).
- **Leertaste am Pferd = Aufsteigen** (sekundäre Aktion), E = Streicheln: beide gleichzeitig
  angezeigt. Als Fee am Hund ist E = Aufsitzen (§6.1).
- **Physik-Interpolation an**: sonst ruckelt 60-Hz-Physik auf 144-Hz-Monitoren.
- **Navigationsradius 13 px**: mit 8 px blieb das Pferd an den Torpfosten hängen.
- **Tiles zur Laufzeit aus JSON statt .tres**: Ich arbeite ohne Editor; ASCII-Karten sind für mich
  der zuverlässigste Weg, und neue Karten brauchen keinen Code.

### Verifikation

- `tools/run_all_checks.sh` → ALLES GRÜN: Assets 0 Fehler (24 PNGs, 52 Manifest-Einträge), Lint 0,
  Tests 46/46, Smoke-Bot 7 Tage, **M1-Bot OK** (Laufen/Bremsen, Verwandlung mit Kosten, Hecke zu
  Fuß blockiert und fliegend überquert, Verwandlung ohne Platz abgelehnt, Hund reiten schneller
  als Fliegen, Feenring gratis, Pferd Schritt→Trab→Galopp→Halt, Absteigen, Pfiff, Zuruf, Streicheln),
  Windows-Exe unter Wine 60 s, Linux-Build 60 s.
- CPU-Zeit (Skripte + Physik, headless, ohne Ladephase): Ø 2,6–2,8 ms, 95 % < 5 ms, max. 6,3 ms
  (Ziel < 8 ms). Im Fenster nicht aussagekräftig messbar (Software-Rendering).
- Screenshots `docs/screenshots/m1/` (11 Bilder vom Bot). Befunde daraus behoben: Meldung wurde von
  der Hilfe verdeckt, Pferd blieb am Tor hängen.

### Offen / nächste Schritte (M2 „Die Welt lebt“)

- Echte Tilesets mit Terrain-Autotiling, Baumhaus-Innenraum, Tag-Nacht-Farbrampe, Licht und
  Normal Maps, Wetter, Wind-/Gras-Shader, Überhang-Transparenz, Zeit im Spiel, Schlafen,
  Speicher-Slots im Menü, HUD-Uhr, Pausemenü, Einstellungen.
- Feedback aus dem Nutzertest von M1 (Gefühl, Geräusche) einarbeiten.

---

## Sitzung 1 – 2026-09-28 · Meilenstein M0 „Fundament“ ✅

### Umgebung (Abweichungen zu §2)

Die Arbeit läuft in einer **Linux-Cloud-Umgebung** (Ubuntu 24.04, 4 Kerne, 15 GB RAM), nicht auf
Windows 11. Der Auftrag verweist auf einen §2a für diesen Fall; **in der CLAUDE.md existiert kein §2a**.
Ich habe die Anpassungen daher selbst festgelegt:

| §2 verlangt | Umgesetzt in der Cloud |
|---|---|
| winget / PowerShell 5.1 | apt/pip bzw. Bash; `tools/run_all_checks.ps1` für Windows existiert zusätzlich (ungetestet, s. u.) |
| Godot 4.x stable | **Godot 4.4.1 stable** (vorinstalliert unter `/root/godot/godot`, Pfad in `tools/godot_path.txt`) |
| Export-Templates in `%APPDATA%` | vorhanden unter `~/.local/share/godot/export_templates/4.4.1.stable/` (inkl. Windows) |
| Python 3.12+ | **Python 3.11.15** (vorinstalliert) mit Pillow 12.3, NumPy 2.4 – alle Skripte laufen damit; 3.12 ist nicht nötig |
| GdUnit4 | **gdUnit4 5.0.5** (letzte Version für Godot 4.4) per `git clone` nach `addons/gdUnit4` (ohne dessen Selbsttests) |
| Windows-Build starten | **Wine 9.0** + Xvfb: Die echte `Starlight.exe` wird unter Wine gestartet und läuft 60 s im Smoke-Modus |
| ffmpeg | vorhanden (für spätere Audio-Konvertierung) |
| – | **rcedit 2.0.0** (MIT) über `tools/setup_tools.sh` nach `tools/bin/` (nicht im Git), damit Icon und Versionsinfo in die Exe kommen |

Verifikation Setup: `godot --version` → `4.4.1.stable.official.49a5bc7b6`; Headless-Start ok;
Git sauber. Freier Speicher 28 GB.

### Was wurde gemacht

1. **Projektstruktur** nach §3, `.gitignore` (Godot 4: `.godot/` ignoriert, `.import`/`.uid` versioniert),
   `.gitattributes`, MIT-`LICENSE`, `AGENTS.md` (Verweis auf CLAUDE.md), `.gdignore` in `docs/`,
   `tools/pipeline/` und `build/`.
2. **project.godot** nach §4.1: 640 × 360, `viewport`/`keep`/`integer`, Nearest, Pixel-Snap,
   Compatibility-Renderer, 60 Physik-Ticks, Start 1280 × 720, eigener Nutzerordner `Starlight`.
3. **12 Autoloads** (alle aus §4.2 plus `App`), siehe `docs/ARCHITECTURE.md`. Echte Logik bereits
   für Zeit/Kalender/Mond, Wetter, Speichern/Laden, Einstellungen, Eingabebelegung, Lokalisierung;
   Gerüste für Audio, Szenenwechsel, Dialog.
4. **Master-Palette** (64 Farben, 10 Rampen) als Python-Quelle → `.hex`, Swatch, 64×1-Lookup.
5. **Asset-Pipeline** `tools/pipeline/`: `build_assets.py` (ein Befehl), Generatoren mit festem
   Seed, `check_palette.py`, `check_sizes.py`, `check_licenses.py`, `pixelize.py`, `normalmap.py`,
   `atlas.py`. Das Manifest wird für generierte Assets automatisch gepflegt.
6. **Pixel-Schrift „Glimmer“** selbst gezeichnet (118 Glyphen + Leerzeichen, inkl. Umlaute, ß, „“, €, ♥, ★),
   als BMFont generiert, globales Theme.
7. **App-Icon** (Stern mit Feenflügeln auf Nachtblau), PNG + ICO (16–256 px, nur ganzzahlig skaliert).
8. **M0-Testszene** (DE/EN, F2 wechselt Sprache, F12 Screenshot) zeigt Skalierung, Palette, Schrift.
9. **Tests:** 37 gdUnit4-Fälle (Zeit/Mond, Speichern inkl. Backup/Korruption/Migration, Eingabe,
   Wetter, Dialogbedingungen, Einstellungen, Lokalisierung, Integrität aller Szenen/Referenzen/
   Übersetzungen/JSON/Projekteinstellungen).
10. **GDScript-Lint:** Godot druckt Analyzer-Warnungen nur im Debug-Modus und ohne Dateinamen.
    `tools/lint/gdscript_lint.gd` lädt jedes Skript einzeln neu; `lint_gdscript.py` ordnet zu und
    schlägt bei jeder Warnung fehl.
11. **Smoke-Bot** `tests/smoke/smoke_run.tscn`: 7 Spieltage, Schlafen → Autosave → Laden →
    Zustandsvergleich, einmal Einschlafen um 02:00, Szenenwechsel.
12. **Export** Windows (x86_64, PCK eingebettet, Icon, Produktname, Version 0.0.1.0) und Linux.
13. **`tools/run_all_checks.sh`** (Cloud) und **`tools/run_all_checks.ps1`** (Windows).
14. Doku: STYLEGUIDE, ARCHITECTURE, GDD, KNOWN_ISSUES, CREDITS, README.

### Entscheidungen (mit Begründung)

- **Renderer Compatibility statt Forward+:** unterstützt 2D-Licht mit Normal Maps und Schatten,
  läuft auf älteren GPUs/Steam Deck und hält den Web-Export offen. Für reines 2D bringt Forward+
  keinen sichtbaren Gewinn.
- **Mondphasen 1/6/1/6/1/6/1/6 Tage:** genau eine Vollmondnacht pro Jahreszeit (Tag 15) statt
  mehrerer „Vollmondtage“ bei gleich langen Phasen – Maestro Moons Nacht ist so planbar.
- **Wetter deterministisch** aus Seed + Tag, gespeichert wird nur der Seed → Vorschau stimmt immer.
- **Eingabe als Daten** (`input_default.json`, physische Tasten). Konflikt in §4.6 (LB für Pfeifen
  *und* Werkzeugleiste) gelöst: LB = Pfeifen, Werkzeugleiste LT/RT, Werkzeug benutzen RB.
- **Eigene Pixel-Schrift statt Fremdfont:** volle Stilkontrolle, garantierte Umlaute, keine Lizenzfragen.
- **GDScript-Warnungen:** untypisierte Deklarationen = Fehler; `unsafe_cast`/`unsafe_call_argument`
  aus, weil JSON-Daten zwangsläufig als Variant ankommen (explizite Umwandlung per `int()`/`as`).
- **`App`-Autoload zusätzlich** zu §4.2: Kommandozeilen-Schalter (`--smoke`, `--screenshot`)
  gehören weder zu Szenenwechsel noch zu Einstellungen.
- **Eigener Nutzerordner „Starlight“** statt des Projektnamens mit „–“: unter Wine scheiterte das
  Anlegen des Ordners am Gedankenstrich; ein schlichter Name ist auch unter Windows robuster.
- **Autosave** läuft beim Tageswechsel nur, wenn die Uhr läuft (also in der Spielwelt, nicht im Menü).

### Verifikation

- `tools/run_all_checks.sh` → **ALLES GRÜN** (Laufzeit ≈ 2:50 min):
  Assets 0 Fehler · Lint 0 Warnungen · Tests 37/37 · Smoke-Bot „7 Tage, 157 Frames“ ·
  Windows-Exe 93 MB, unter Wine 60 s: `SMOKE OK – 12350 Frames` (≈ 205 FPS mit
  Software-Rendering llvmpipe) · Linux-Build 60 s: `SMOKE OK – 12856 Frames`.
- Versionsinfo der Exe per `pefile` ausgelesen: Produktname „Starlight – Klio goes Fairy“,
  Version 0.0.1.0, 6 Icon-Größen eingebettet.
- Screenshots `docs/screenshots/m0/`: `windows_build_1280x720.png` (×2), `windows_build_1920x1080.png`
  (×3) aus der Windows-Exe unter Wine, `test_scene_1280x720.png` aus dem Projekt.
  Visuelle Prüfung: Schrift pixelscharf, keine Mixels, Integer-Skalierung korrekt, Farben nur aus
  der Palette. Befund: Platzhalter-Gras kachelt sichtbar diagonal → KNOWN_ISSUES (M2).
- Erwartete Fehlermeldungen im Testlog: „Parse JSON failed“ und „unbekannter Slot '99'“ stammen aus
  Negativtests (beschädigter Spielstand, ungültiger Slot) und sind gewollt.

### Probleme unterwegs (gelöst)

- `SceneTree.scene_changed` gibt es in 4.4 noch nicht → auf Frame-Warten umgestellt.
- `ConfigFile.get_value` ohne Default wirft Fehler → vorher `has_section_key` prüfen.
- Smoke-Bot war selbst die aktuelle Szene und wurde beim Szenenwechsel gelöscht → Platzhalter-Szene.
- Autosave-Vergleich schlug fehl, weil die Uhr zwischen Speichern und Vergleich weiterlief →
  Vergleich gegen den Dateiinhalt.
- rcedit unter Wine zerstörte „–“/„©“ ohne UTF-8-Locale → `LC_ALL=C.UTF-8` beim Export.
- Godot importierte `docs/ASSET_MANIFEST.csv` als Übersetzung → `.gdignore` in `docs/`.

### Test auf echtem Windows (2026-09-28)

Der Windows-Build (`Starlight.exe`, als 7z übergeben) wurde auf echter Hardware getestet: Start,
pixelscharfe Darstellung, Sprachwechsel F2, maximiertes Fenster mit Integer-Skalierung,
Screenshot F12 nach `%APPDATA%\Starlight\screenshots` und Programm-Infos → **alles in Ordnung**.

### Offene Punkte / nächste Schritte (M1 „Das Gefühl“)

- Test-Wiese 40 × 30 Tiles, Klio als erkennbare Figur in beiden Größen (Haare als eigener Layer,
  Brille, Flügel), Größenwechsel mit vollem Effekt, Fliegen mit eigenem Kollisionslayer,
  Hund (folgen, streicheln, reiten), Pferd (streicheln, reiten, 3 Gangarten), Kamera mit
  Subpixel-Glättung, erste SFX.
- `run_all_checks.ps1` ist auf Windows weiterhin ungetestet (braucht Godot + Python beim Nutzer; niedrige Priorität).
