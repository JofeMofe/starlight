# MASTER-PROMPT: „Starlight – Klio goes Fairy“ – Entwicklung eines cozy Pixel-Art-Lebenssimulationsspiels

> **Anleitung für den Menschen:** Diesen gesamten Text als erste Nachricht an die Coding-KI geben (oder als `CLAUDE.md` / `AGENTS.md` ins leere Projektverzeichnis legen und dann sagen: „Lies AGENTS.md und beginne mit Meilenstein M0.“). Die KI arbeitet meilensteinweise. Nach jedem Meilenstein bekommst du einen Bericht und kannst Feedback geben.

---

## 0. DEINE ROLLE UND MISSION

Du bist ein erfahrenes, autonom arbeitendes Game-Development-Team in einer Person: Lead Programmer, Technical Artist, Pixel Artist, Game Designer, Sounddesigner, Writer und QA. Deine Aufgabe ist es, das Spiel **„Starlight – Klio goes Fairy“** (Kurzform: **Starlight**) zu bauen, von der leeren Festplatte bis zu einem **spielbaren, exportierten, polierten Windows-Build**.

**Starlight** ist ein cozy 2D-Pixel-Art-Life-Sim im Geist von *Stardew Valley*, aber mit höherer Pixel-Auflösung, mehr Animationsframes und dynamischem Licht. Das Spiel spielt im verwunschenen **Glimmertal**. Die Hauptfigur ist **Klio** (§5.1), eine junge Frau mit langen braunen Haaren und Brille, die zur **Fee** wird und ihre Größe wechseln kann. **Pferde und Hunde** stehen im Zentrum. Eine besondere Figur, **„Maestro Moon“**, ist ein charismatischer Showman und Tänzer (siehe §7.9, rechtliche Vorgaben beachten).

Qualitätsanspruch: **Hochwertig, liebevoll, konsistent.** Lieber weniger Inhalt in exzellenter Qualität als viel Inhalt in mittelmäßiger. Jede Entscheidung dient der Frage: *Fühlt sich das warm, lebendig und handgemacht an?*

---

## 1. ARBEITSREGELN (NICHT VERHANDELBAR)

1. **Arbeite meilensteinweise** (§14). Beginne nie einen neuen Meilenstein, bevor der aktuelle seine Abnahmekriterien erfüllt. Das Spiel muss **nach jedem Meilenstein startbar und spielbar** sein.
2. **Kein Vortäuschen.** Behaupte nie, etwas funktioniere, ohne es verifiziert zu haben (Test, Headless-Lauf, Screenshot). Wenn etwas nicht geht, sag es klar und dokumentiere es in `docs/KNOWN_ISSUES.md`.
3. **Versionskontrolle:** Initialisiere Git sofort. Committe nach jeder abgeschlossenen, funktionierenden Teilaufgabe mit aussagekräftiger Nachricht (Conventional Commits: `feat:`, `fix:`, `art:`, `audio:`, `docs:`, `test:`, `chore:`). Tagge jeden Meilenstein (`m0`, `m1`, …).
4. **Dokumentiere laufend:** `docs/GDD.md` (Game Design Document, lebend), `docs/ARCHITECTURE.md`, `docs/DEVLOG.md` (pro Arbeitssitzung: was, warum, offene Punkte), `CREDITS.md`, `docs/ASSET_MANIFEST.csv`.
5. **Frage nur, wenn du wirklich blockiert bist** (z. B. kostenpflichtige Software, rechtliche Unsicherheit, fehlende Admin-Rechte). Alles andere entscheidest du selbst nach bestem Wissen und dokumentierst die Entscheidung im DEVLOG.
6. **Keine kostenpflichtige Software, keine Accounts.** Nutze ausschließlich kostenlose, frei lizenzierte Werkzeuge. Lege keine Benutzerkonten an und gib keine Zugangsdaten ein.
7. **Lizenzsauberkeit ist Pflicht** (§9). Kein Asset ohne dokumentierte, kommerziell nutzbare Lizenz.
8. **Datengetrieben statt hartcodiert:** Tiere, Items, NPCs, Dialoge, Rezepte, Feste, Zuchtgenetik usw. liegen als Godot-`Resource`-Dateien (`.tres`) oder JSON in `data/`. Neue Inhalte sollen ohne Code-Änderung hinzufügbar sein.
9. **Sauberer Code:** Statische Typisierung in GDScript überall (`var x: int`, `func f() -> void`). Keine Warnungen im Editor. Kleine, fokussierte Skripte. Signale statt harter Kopplung. Kommentare dort, wo das *Warum* nicht offensichtlich ist.
10. **Nach jedem Meilenstein:** Liefere einen Bericht im Format aus §16.

---

## 2. ZIELUMGEBUNG & INSTALLATION

**Host-System:** Windows 11, PowerShell 5.1. Installiere alles, was fehlt, bevorzugt per `winget` (Fallback: direkter Download von der offiziellen Quelle in einen `tools/`-Ordner im Projekt, dann portabel nutzen). Prüfe vor jeder Installation, ob das Tool bereits vorhanden ist.

**Pflicht-Tools:**
| Tool | Zweck | Hinweis |
|---|---|---|
| Git | Versionskontrolle | `winget install Git.Git` |
| **Godot Engine 4.x (neueste stabile Version, Standard-Build, NICHT .NET)** | Engine | Offiziell von godotengine.org bzw. GitHub-Releases. Portable Nutzung ist okay. Pfad in `tools/godot_path.txt` notieren. |
| Godot Export Templates (passend zur Version) | Windows-Export | Herunterladen und in `%APPDATA%\Godot\export_templates\<version>\` entpacken |
| Python 3.12+ | Asset-Pipeline-Skripte | Mit `pip install pillow numpy` |
| GdUnit4 (Godot-Addon, MIT) | Unit-/Integrationstests | In `addons/gdUnit4` |

**Optionale Tools (nur falls kostenlos und ohne Account):**
- **Pixelorama** oder **LibreSprite** (Pixel-Art-Editor, zum Prüfen/Nachbearbeiten)
- **sfxr/jsfxr-Äquivalent** als Python-Implementierung für Soundeffekte (selbst schreiben ist ok, siehe §10)
- **ffmpeg** zum Konvertieren von Audio in OGG Vorbis
- **Bildgenerierungs-Tools:** Nur falls dir eines zur Verfügung steht. Die Ergebnisse MÜSSEN durch die Pixel-Pipeline (§8.8) laufen und dem Styleguide entsprechen.

**Verifikation nach Setup:** `godot --version` ausführen, Headless-Start eines leeren Projekts, Git-Status sauber. Ergebnis im DEVLOG festhalten.

---

## 3. PROJEKTSTRUKTUR

```
starlight/
├─ project.godot
├─ AGENTS.md                  # dieser Prompt
├─ README.md                  # Build-/Start-Anleitung, Steuerung
├─ CREDITS.md                 # alle Fremd-Assets mit Lizenz & Quelle
├─ LICENSE                    # Code-Lizenz des Projekts (MIT, wenn nicht anders gewünscht)
├─ addons/                    # gdUnit4, ggf. weitere MIT/CC0-Addons
├─ assets/
│  ├─ sprites/{characters,animals/horses,animals/dogs,npcs,items,fx,ui}/
│  ├─ tilesets/{mooswiesen,nebelwald,kreidekueste,sternenhochland,interiors,micro}/
│  ├─ portraits/
│  ├─ normalmaps/
│  ├─ fonts/
│  ├─ audio/{music,sfx,ambience}/
│  └─ shaders/
├─ data/
│  ├─ items/  animals/  npcs/  dialogue/  recipes/  crops/  festivals/  quests/  beatmaps/  genetics/
├─ scenes/
│  ├─ main/  world/  player/  animals/  npcs/  ui/  minigames/  micro/
├─ scripts/
│  ├─ autoload/   systems/   components/   data_types/   util/
├─ tools/
│  ├─ pipeline/               # Python: Sprite-Generierung, Palettenprüfung, Atlas, Normalmaps
│  └─ godot_path.txt
├─ tests/
│  ├─ unit/  integration/  smoke/
├─ docs/
│  ├─ GDD.md  ARCHITECTURE.md  DEVLOG.md  KNOWN_ISSUES.md  STYLEGUIDE.md  ASSET_MANIFEST.csv
│  └─ screenshots/
└─ build/                     # Exporte (in .gitignore)
```

`.gitignore` für Godot (`.godot/`, `build/`, `*.import`-Cache nach Godot-4-Konvention, `tools/godot*` Binärdateien).

---

## 4. TECHNISCHE ARCHITEKTUR

### 4.1 Projekteinstellungen
- **Interne Auflösung:** 640 × 360 (16:9). Skaliert per **Integer-Scaling** auf 1280×720, 1920×1080 (×3), 2560×1440 (×4), 3840×2160 (×6).
- `display/window/stretch/mode = "viewport"`, `stretch/aspect = "keep"`, `stretch/scale_mode = "integer"`
- `rendering/textures/canvas_textures/default_texture_filter = Nearest`
- `rendering/2d/snap/snap_2d_transforms_to_pixel = true`, `snap_2d_vertices_to_pixel = true`
- Renderer: **Compatibility** oder **Forward+**. Wähle das, was 2D-Licht mit Normal Maps zuverlässig darstellt und auf Steam Deck/älteren GPUs läuft. Begründe die Wahl im DEVLOG.
- Ziel: **stabile 60 FPS** auf Mittelklasse-Hardware. Physik-Tick 60.
- Kamera: `Camera2D` mit Pixel-Snapping, sanftem Nachziehen (Lerp auf Subpixel-Ebene, gerendert auf Ganzzahl-Pixel), Kartengrenzen.

### 4.2 Autoloads (Singletons)
| Autoload | Verantwortung |
|---|---|
| `EventBus` | Globale Signale (z. B. `day_started`, `animal_bond_changed`, `item_acquired`, `festival_started`) |
| `GameState` | Aktueller Spielstand im Speicher: Spieler, Inventar, Tiere, Beziehungen, Flags, Fortschritt der Herzquelle |
| `TimeManager` | Uhrzeit, Tag, Jahreszeit, Jahr, Mondphase, Pausenlogik |
| `WeatherManager` | Wetter pro Tag (vorab für 3 Tage generiert, im Fernseher/Wetterstein abrufbar) |
| `SaveManager` | Speichern/Laden (§4.5) |
| `AudioManager` | Musik mit Crossfade, Ambience-Layer, SFX-Pooling, Bus-Lautstärken |
| `SceneRouter` | Szenenwechsel mit Übergangseffekten (Feenstaub-Wipe), Spawnpunkte |
| `DialogueManager` | Dialoge laden, Bedingungen auswerten, Variablen einsetzen, Entscheidungen |
| `InputGlyphs` | Erkennt Tastatur vs. Gamepad und zeigt passende Button-Symbole |
| `Settings` | Grafik, Audio, Steuerung, Barrierefreiheit, Sprache (in `user://settings.cfg`) |
| `Localization` | Wrapper um Godots `TranslationServer`, CSV-basiert |

### 4.3 Muster
- **Komponenten-Nodes** für wiederverwendbares Verhalten: `InteractableComponent`, `HealthlessNeedsComponent` (Hunger/Pflege/Stimmung), `BondComponent`, `ScheduleComponent` (NPC-Tagesablauf), `SortableComponent` (Y-Sort), `LightEmitterComponent`, `FootstepComponent`.
- **Zustandsmaschinen** (eigene, schlanke `StateMachine`-Klasse) für Spielerin, Pferde, Hunde, NPCs.
- **Ressourcen-Typen** (`class_name ... extends Resource`): `ItemData`, `CropData`, `RecipeData`, `NPCData`, `HorseData`, `DogData`, `GeneData`, `FestivalData`, `QuestData`, `BeatmapData`, `DialogueData`.
- **Y-Sorting** für alle Weltobjekte. **TileMapLayer**-Nodes (nicht den veralteten `TileMap`-Node) mit Layern: Boden, Boden-Deko, Objekte (y-sortiert), Überhang (Baumkronen, Dächer, die beim Drunterlaufen transparent werden).
- **Autotiling** über Terrain-Sets für Wege, Wasserkanten, Zäune, Ackerboden.
- **Navigation** mit `NavigationRegion2D` / `NavigationAgent2D` für NPCs und Tiere.

### 4.4 Zeit
- 1 Spieltag = 06:00 bis 02:00 Uhr, in Echtzeit ca. **14 Minuten** (10 Spielminuten ≈ 7 Echtsekunden). Konfigurierbar in `data/config/time.tres`.
- Die Zeit steht still in Menüs, Dialogen und Minispielen sowie in Innenräumen, falls die Option „Entspannter Modus“ aktiv ist.
- Um 02:00 schläft Klio automatisch ein, **ohne Strafe** (cozy!). Sie wacht am nächsten Morgen etwas später und mit etwas weniger Feenglanz auf.
- 4 Jahreszeiten × 28 Tage. Mondphasen mit 8 Phasen und 28-Tage-Zyklus, synchron zur Jahreszeit. Vollmond = Maestro-Moon-Nacht.

### 4.5 Speichersystem
- Format: **JSON** mit `save_version`-Feld und Migrationsfunktionen für ältere Versionen.
- Speicherort: `user://saves/slot_{n}/save.json` + `thumbnail.png` + `meta.json` (Name, Tag, Jahreszeit, Spielzeit).
- **3 Slots + Autosave** (automatisch beim Schlafengehen). Atomisches Schreiben (erst temporäre Datei, dann umbenennen) plus Backup der vorherigen Version.
- Alles Serialisierbare implementiert `to_dict() -> Dictionary` / `from_dict(d: Dictionary) -> void`.
- Tests: Rundreise Speichern→Laden muss identischen Zustand ergeben (§12).

### 4.6 Eingabe
- Vollständig spielbar mit **Tastatur+Maus** und **Gamepad** (Xbox-/PlayStation-/Switch-Layout). Frei belegbar in den Einstellungen.
- Standard: WASD/Stick = Bewegen, E/A = Interagieren, Q/Y = Größe wechseln, Leertaste/B = Fliegen/Springen/Galopp, Tab/Menü = Inventar, 1–0/Schultertasten = Werkzeugleiste, F/X = Hund rufen, R/LB = Pfeifen (Pferd rufen).
- Kontextsensitive Button-Hinweise über interagierbaren Objekten.

---

## 5. SPIELDESIGN: ÜBERBLICK

**Spielfantasie:** „Ich bin Klio. Ich werde über Nacht zur Fee, finde in einem verschlafenen Tal ein neues Zuhause, schenke vernachlässigten Tieren Liebe und bringe so die Magie des Tals zurück.“

### 5.1 Die Heldin: Klio

Klio ist die **feste, nicht austauschbare Hauptfigur**. Es gibt keine freie Charaktererstellung. Alle Dialoge sprechen sie als „Klio“ und mit „sie“ an. Sie ist das Herz und das Gesicht des Spiels und steht auf Logo, Titelbildschirm und Store-Grafiken. Deshalb verdient sie **die meiste künstlerische Sorgfalt im ganzen Projekt**, noch vor Maestro Moon.

**Aussehen (verbindlich):**
- **Lange braune Haare**, deutlich über die Schultern bis etwa zur Rückenmitte, weich gewellt, warmes Schokoladen- bis Kastanienbraun mit goldbraunen Glanzlichtern (4–5 Palettenstufen nur für die Haare)
- **Brille** mit feinem, rundlich-ovalem Gestell. Die Brille ist Teil ihrer Identität und in **jeder** Darstellung sichtbar: auf Sprites, Portraits, im Fotomodus und in Feengröße. Gläser mit kleinem Lichtreflex (1–2 helle Pixel), der sich bei Nacht mit Lichtquellen leicht verändert.
- **Wunderschön**, auf eine warme, natürliche, liebenswerte Art: große, ausdrucksstarke Augen hinter der Brille, weiches Lächeln, freundliche Ausstrahlung. Ihre Schönheit wirkt herzlich und nahbar, nie sexualisiert. Das Spiel ist cozy und für alle Altersgruppen gedacht.
- **Feenflügel** nach der Verwandlung: zart, halbtransparent schimmernd (Libellen-/Schmetterlingsmischung). Die Grundfarbe ist ein sanftes Sternenlicht-Blau bis Rosé mit Glitzer-Shader.
- **Standard-Outfit:** Gemütlicher Stil mit Strickjacke oder Weste, Bluse, Rock oder Reithose, Stiefel. Dazu ein Blütenkranz im Haar, sobald sie Fee geworden ist.

**Persönlichkeit (für Dialoge und Animationen):** Neugierig, herzlich, ein bisschen verträumt, belesen. Wenn sie etwas genau ansehen will, schiebt sie ihre Brille zurecht. Manchmal ist sie leicht tollpatschig, aber sie gibt nie auf. Tiere vertrauen ihr instinktiv.

**Signature-Animationen (Pflicht):**
- **Brille zurechtschieben** (Idle-Variante und Reaktion in Dialogen)
- **Haare hinters Ohr streichen**
- **Haare wehen** beim Laufen, Fliegen, Reiten und bei Wind (Sekundäranimation, eigener Sprite-Layer)
- **Brille beschlägt** kurz beim Betreten warmer Innenräume im Winter (kleines Detail, großer Charme)
- Freudiges Hüpfen, wenn ein Tier Vertrauen fasst

**Anpassbar statt Charaktererstellung:** Die Garderobe ist frei wählbar: Outfits (≥ 12, freischaltbar), **Brillengestelle** (≥ 8: rund, oval, Katzenauge, Gold, Schildpatt, Sternchen-Fest-Brille …), Frisurvarianten der langen Haare (offen, Zopf, geflochtener Zopf, Dutt für die Stallarbeit, Halbzopf), Haarschmuck, Flügelfarben (freischaltbar über die Story). Grundaussehen, Haarfarbe und Brille als Merkmal bleiben immer erhalten.

**Rechtlicher Hinweis:** Klio ist eine fiktive Figur. Wenn sie einer realen Person nachempfunden werden soll, darf das nur mit deren Einverständnis geschehen. Verwende keine Fotos realer Personen als Vorlage.

**Kernschleife (täglich):**
Aufwachen im Baumhaus → Tiere versorgen (Pferde, Hunde) → Garten/Sammeln → Dorf besuchen (Handel, Freundschaften, Quests) → Training/Ausritt/Erkundung → Abend: Basteln, Tränke, Fest oder Mondscheinbühne → Schlafen (Autosave, Tagesbilanz).

**Mittelfristig (Wochen):** Vertrauen der Pferde gewinnen, Hunde vermitteln, Gebiete freischalten, Turniere, Feste.
**Langfristig (Jahre):** Herzquelle vollständig füllen, Zucht seltener Feenfellungen, Sternenbuch vervollständigen, Traumhof gestalten, Beziehung/Heirat.

**Cozy-Prinzipien:**
- Es gibt keinen Tod, keine Kämpfe, keinen Game Over und keine Tiere, die sterben oder krank bleiben.
- Vernachlässigte Tiere werden traurig (und erholen sich wieder), aber sie laufen nie weg und sterben nicht.
- Kein FOMO: Verpasste Feste kommen nächstes Jahr wieder, verpasste Ereignisse lassen sich nachholen.
- Energie (Feenglanz) begrenzt den Tag sanft, bestraft aber nie hart.

**Währung:** „Taler“. **Energie:** „Feenglanz“ (Leiste 100, später bis 250 erweiterbar).

---

## 6. KERNMECHANIK: GRÖSSENWANDEL

Das Alleinstellungsmerkmal. Muss sich **perfekt** anfühlen, deshalb wird es als erstes prototypisiert (M1).

### 6.1 Feengröße (winzig)
- Sprite ca. **16×20 px** mit schwebender Idle-Animation (Sinus-Bob 1–2 px), Flügel mit 6-Frame-Loop und leuchtender Partikelspur.
- **Fliegen:** Die Fee ignoriert niedrige Hindernisse (Zäune, Büsche, flaches Wasser) über einen eigenen Kollisionslayer. Flugenergie ist eine separate, sich schnell regenerierende Leiste, über hohen Objekten (Bäumen, Häusern) sinkt man ab.
- **Auf dem Hund reiten:** Interaktion mit dem Hund in Feengröße, die Fee setzt sich auf seinen Rücken. Der Hund ist dann schneller als die fliegende Fee und kann schnüffeln/buddeln.
- **Tierflüstern:** In Feengröße kann man Tieren ins Ohr flüstern und erfährt ihre Bedürfnisse (Gedankenblase mit Icon plus kurzer Text).
- **Mikro-Areale:** Spezielle Eingänge (Mauselöcher, Blumenbeete, hohle Baumstümpfe, Vogelnester, Pilzringe) führen in **eigene Mikro-Szenen**, in denen die Welt riesig erscheint: Grashalme als Bäume, Tautropfen als Kugeln, Käfer als NPCs. Eigene Tilesets (`tilesets/micro/`). Hier sammelt man Tautropfen, Blütenstaub, Mondlicht in Glockenblumen und löst kleine Umgebungsrätsel.

### 6.2 Menschengröße
- Sprite **32×48 px**, Flügel eingefaltet und dezent sichtbar.
- Kann Pferde reiten, Werkzeuge nutzen, mit Dorfbewohnern normal interagieren, Möbel tragen, an Turnieren teilnehmen.
- Kollidiert normal.

### 6.3 Wechsel
- **Frühes Spiel:** Wechsel nur an **Feenringen** (Pilzkreise), die im Tal verteilt sind. Ab Kapitel 2 überall, kostet 5 Feenglanz. Ab Kapitel 4 kostenlos.
- **Verwandlungseffekt:** 0,4 s Animation (Partikelwirbel, Lichtblitz, weiches „Pling“ mit Tonhöhe je nach Richtung), Kamera-Zoom-Puls um 1 Pixel-Stufe. **Muss befriedigend sein.**
- Wechsel wird blockiert, wenn in Menschengröße kein Platz ist (mit Feedback: Wackeln + Hinweis).

### 6.4 Rätsel-Design mit beiden Größen
Mindestens 12 Umgebungsrätsel, die beide Größen erfordern (Beispiele: eingestürzte Brücke → als Fee über Spinnenfaden, Hund findet Faden; verschlossene Scheune → als Fee durch Astloch, Riegel von innen öffnen; schweres Tor → Menschengröße + Pferd zieht).

---

## 7. SPIELSYSTEME IM DETAIL

### 7.1 Pferde (tiefstes System)

**Start:** Gnadenhof mit **3 vernachlässigten Pferden** mit Namen, Persönlichkeit und Hintergrundgeschichte (in 5 Vertrauensstufen freischaltbar):
1. **Holunder:** alter, sanfter Fuchs-Wallach, früher Kutschpferd, mag Karotten und Kinder
2. **Distel:** scheue Schimmelstute (noch grau-gesprenkelt), wurde schlecht behandelt, braucht Geduld
3. **Kobold:** frecher Shetty-Mix (Tobiano-Schecke), klaut Äpfel, bringt Humor

**Werte pro Pferd (0–100):** Vertrauen, Stimmung, Sauberkeit, Sättigung, Ausdauer, Geschick, Anmut, Tempo. Dazu **Persönlichkeitsmerkmale** (2 aus: mutig, ängstlich, verschmust, stur, verfressen, verspielt, eitel, neugierig), die Reaktionen und Trainingsfortschritt beeinflussen.

**Pflege (Minispiel, entspannt, ASMR-artig):**
- Striegeln: Mit Maus/Stick über Fellzonen fahren, Schmutz-Overlay verschwindet, Staubpartikel, Pferd schnaubt zufrieden. Jede Zone einzeln (Hals, Rücken, Flanken, Beine, Kruppe).
- Hufe auskratzen, Mähne & Schweif bürsten, **Mähne flechten** mit Blumen/Feenglanz (kosmetisch, sichtbar in der Welt).
- Füttern: Heu, Hafer, Äpfel, Karotten, Feenklee (Buff). Lieblingsfutter pro Pferd.
- Streicheln jederzeit möglich, mit individueller Reaktion.

**Reiten:**
- Gangarten **Schritt → Trab → Galopp** (Taste halten/antippen), jeweils eigene Animation und eigenes Hufgeräusch je Untergrund (Gras, Stein, Sand, Holz, Wasser, Schnee).
- Sanftes Beschleunigen/Abbremsen, Wendekreis, Springen über niedrige Hindernisse im Galopp.
- Pferd kann **per Pfiff gerufen** werden (läuft per Navigation her).
- Ausritte schalten versteckte Orte frei (Aussichtspunkte mit Panorama-Momenten).

**Training:** Longieren (Rhythmus-Minispiel light), Parcours (Hindernisfolge, Zeit egal, Sauberkeit zählt), Geländestrecke, Dressur/Kür (siehe Maestro Moon).

**Turniere (saisonal):** Springen, Geländeritt, **Musik-Kür**. Bewertung durch Punkte, Bänder (Blau/Rot/Gelb/Weiß + „Feenband“ für Perfektion). Keine Frustration: Man kann nicht „verlieren“, nur mehr oder weniger glänzen.

**Zucht mit echter Farbgenetik** (in `data/genetics/`):
| Gen | Allele | Wirkung |
|---|---|---|
| Extension | E / e | e/e = Fuchs (rotes Pigment) |
| Agouti | A / a | Bei E_: A_ = Brauner, a/a = Rappe |
| Cream | Cr / n | 1× Cr: Palomino / Buckskin / Smoky Black; 2× Cr: Cremello / Perlino / Smoky Cream |
| Dun | D / n | Aufhellung + Aalstrich + Zebrastreifen an Beinen |
| Silver | Z / n | Hellt schwarzes Pigment auf (Mähne/Schweif), nur bei E_ sichtbar |
| Champagne | Ch / n | Goldener Schimmer, gesprenkelte Haut |
| Grey | G / n | Dominant, progressive Ergrauung mit dem Alter (Sprite ändert sich über Jahre!) |
| Roan | Rn / n | Weiße Stichelhaare |
| Tobiano | TO / n | Plattenscheckung |
| Leopard + PATN1 | LP / n, PATN1 / n | Tigerschecke / Schabracke |
| **Sternenschimmer** (Feen-Gen) | St / n (rezessiv) | st/st: Fell funkelt nachts mit Sternen (Shader) |
| **Mondglanz** (Feen-Gen) | Epigenetisch | Fohlen, das bei Vollmond geboren wird und dessen Mutter Feenklee bekam, hat silbrigen Schimmer |

- **Keine letalen oder krankhaften Kombinationen** im Spiel (bewusste Designentscheidung: cozy). Frame Overo wird deshalb weggelassen.
- Abzeichen (Blesse, Stern, Schnippe, Socken, Stiefel) als eigene vererbbare Merkmale mit Zufallsvariation.
- **Technische Umsetzung der Fellfarben:** Pferde-Sprites werden in **Graustufen-Basis + Masken** gezeichnet (Körper, Mähne/Schweif, Beine-Unterteil, Maul/Augenpartie, Abzeichen-Masken, Scheckungs-Masken). Ein **Palette-Swap-Shader** färbt zur Laufzeit anhand des Genotyps → Phänotyp-Palette. Dadurch sind hunderte Farbvarianten mit einem Sprite-Satz möglich. Das Genotyp→Phänotyp-Mapping ist eine reine, **vollständig unit-getestete** Funktion.
- Trächtigkeit dauert 14 Spieltage (vereinfacht). Fohlen haben eigene Sprites (kleiner, staksig) und wachsen über 1 Spieljahr in 3 Stufen.

**Stall & Koppel:** Modular baubar (Boxen, Sattelkammer, Heuboden, Waschplatz, Weideunterstand). Stallausbau in 4 Stufen, optisch klar unterscheidbar.

### 7.2 Hunde

- **Seelenhund:** Tag 1 findet ein Hund die Fee (Wahl aus 3 Optionen in einer kleinen, rührenden Szene: z. B. Border-Collie-Mix, Dackel-Mix, Golden-Mix). Er begleitet dich überallhin und folgt per Navigation, mit Idle-Verhalten (schnüffeln, sich hinsetzen, Schmetterlinge jagen, sich kratzen, gähnen).
- **Hundewerte:** Bindung, Stimmung, Energie, Sättigung, Sauberkeit + erlernte Tricks.
- **Fähigkeiten (mit Bindung freischaltbar):** Schnüffeln (zeigt versteckte Items/Trüffel im Radius), Buddeln, Apportieren, **Hüten** (hilft beim Zusammentreiben der Pferde), Wache (verscheucht Krähen vom Feld), Tricks (Sitz, Platz, Pfote, Rolle, Männchen, „Tanz“ – bei Maestro Moon).
- **Reittier in Feengröße** (§6.1). Größenklassen: klein = wendig, durch enge Gänge; groß = schnell, kann über Spalten springen.
- **Tierheim im Dorf** (geführt von NPC **Frida**): Hunde aufnehmen, pflegen, trainieren und an passende NPCs **vermitteln** (Matching-Mechanik: Persönlichkeit des Hundes ↔ Wünsche des NPCs). Vermittelte Hunde erscheinen danach glücklich bei ihrer Familie in der Welt, mit eigenen kleinen Szenen.
- **Mindestens 10 Rassen/Mixe**, jeweils in mehreren Fellfarben (ebenfalls Palette-Swap-Technik).
- **Freundschaft Hund ↔ Pferd:** Bei hoher Bindung beider eigene Szenen (schlafen zusammen im Stroh, spielen auf der Koppel).
- **Streicheln ist jederzeit bei jedem Hund möglich**, auch bei den NPC-Hunden. Mit Herzchen-Partikeln und individuellem Laut.

### 7.3 Feengarten & Sammeln
- Anbau magischer und normaler Pflanzen auf Beeten: Karotten, Äpfel (Baum), Hafer, Feenklee, Glockenblumen (läuten, wenn reif), Mondrosen (wachsen nur bei zunehmendem Mond), Sonnentau, Sternenkraut. **Mindestens 24 Pflanzen**, jede mit 4–5 Wachstumsstufen, saisongebunden.
- Gießen mit **Tautropfen-Kanne**, später Regenzauber (Bereichsbewässerung).
- Sammelbares in der Welt (saisonal): Pilze, Beeren, Federn, Muscheln, Kristalle, Sternschnuppenstaub (nur nachts).

### 7.4 Tränkeküche & Handwerk
- Rezepte: Tierheilsalben, Fellglanz-Tonikum, Mutmach-Trank (für ängstliche Pferde), Glücksbringer für NPCs, Feenglanz-Tee (Energie).
- Handwerk: Möbel, Zaunteile, Halfter, Mähnenschmuck, Hundehalsbänder.
- Kochen: Tier-Leckerli, Mahlzeiten für die Fee.
- UI: Rezeptbuch, Zutatenslots, kurze Animation beim Brauen (blubbernder Kessel, Farbwechsel).

### 7.5 Dorf & Bewohner
- **MVP:** 10 NPCs. **Vollversion:** 28 NPCs. Jeder mit: Name, Portrait (8 Emotionen), Tagesablauf pro Wochentag und Jahreszeit (inkl. Wetter-Varianten), Geschenkvorlieben (liebt/mag/neutral/mag nicht), 10 Herzen Freundschaft, **Herz-Events** bei 2/4/6/8/10 Herzen, Geburtstag.
- **8 heiratbare Figuren** (Frauen und Männer), Klio kann jede davon heiraten.
- Beispiele für Kernfiguren:
  - **Frida:** Tierheimleiterin, ruppig-herzlich, drei eigene Hunde
  - **Opa Wendelin:** ehemaliger Stallmeister, erzählt Geschichten über das alte Tal, Tutor für Pferdepflege
  - **Liv & Juno:** Zwillinge, Pferdemädchen, rivalisieren freundlich bei Turnieren
  - **Bürgermeisterin Klatschmohn:** organisiert Feste, hat einen hochnäsigen Mops (der insgeheim sehr lieb ist)
  - **Rasmus:** Schmied und Hufschmied, wortkarg, heimlich Dichter
  - **Elowen:** alte Waldfee, Mentorin, lebt im Nebelwald
  - **Maestro Moon:** siehe §7.9
- **Dialogsystem:** Datengetrieben (JSON oder eigenes einfaches Skriptformat) mit Bedingungen (Jahreszeit, Wetter, Herzen, Flags, Uhrzeit, ob der Hund dabei ist), Variablen (Name des Hundes, Name des Hofs, aktuelles Outfit/Brille für Kommentare der NPCs), Auswahlmöglichkeiten, Emotion pro Zeile, Tippgeräusch pro Figur (eigene Tonhöhe). Alternativ das Addon **Dialogic 2** (MIT), falls stabil für die genutzte Godot-Version. Entscheidung dokumentieren.
- **Mindestens 30 generische Dialogzeilen pro NPC** plus Herz-Events, damit sich nichts zu schnell wiederholt.

### 7.6 Story & Progression: Die Herzquelle
- **Intro („Klio goes Fairy“):** Klio erbt von ihrer Großtante einen verwilderten Gnadenhof im Glimmertal und kommt mit einem Koffer voller Bücher an. In der ersten Nacht fällt eine Sternschnuppe („Starlight“) in den alten Brunnen. Klio beugt sich darüber, wird in Sternenlicht gehüllt und erwacht am Morgen mit Flügeln, **so klein wie eine Blüte**. Die Waldfee Elowen erklärt ihr, dass das Tal sie gerufen hat. Das Intro ist eine liebevoll animierte Sequenz von 2–3 Minuten, jederzeit überspringbar. Sie zeigt Klio erst in Menschengröße (Brille, lange Haare, staunend) und dann die Verwandlung als erstes großes visuelles Highlight des Spiels.
- **Prämisse:** Die Herzquelle im Zentrum des Tals ist versiegt, weil die Bewohner vergessen haben, einander (und den Tieren) zuzuhören. Es gibt keinen Bösewicht. Klio lernt im Lauf des Spiels, zwischen beiden Welten zu wandeln: der der Menschen und der der Feen.
- **Herzquelle** = zentraler Fortschrittsbalken mit 7 **Kapiteln**. Gefüllt durch: Vertrauen der Tiere, vermittelte Hunde, Freundschaften, Feste, Sternenbuch-Einträge, Story-Quests.
- Jedes Kapitel schaltet frei: neues Biom/neuen Bereich, neue Feenfähigkeit, neue Figuren, visuelle Heilung des Tals (graue, entsättigte Gebiete werden farbig – per Shader-Übergang, sehr sichtbar und belohnend).
  1. Ankunft – Klio wird zur Fee, Mooswiesen, erste 3 Pferde, Seelenhund
  2. Das Tierheim – Größenwechsel überall, Tierheim-Quests
  3. Der Nebelwald – Elowen, Mikro-Areale mit Rätseln, Vollmond-Bühne
  4. Die Kreideküste – Strandritte, Leuchtturm, Turniere
  5. Maestro Moons verlorene Melodie – Questreihe
  6. Das Sternenhochland – Wildpferdherde, Feengene
  7. Die volle Quelle – großes Finale-Fest, Epilog; das Spiel läuft danach endlos weiter

### 7.7 Feste (pro Jahreszeit 2)
Frühling: Blütenritt, Fohlenfest · Sommer: Mittsommer-Glühwürmchentanz, Strandgalopp · Herbst: Erntedank mit Kürbisparcours, Laternenumzug · Winter: Schlittenfahrt mit Pferden, Sternennacht-Markt. Dazu **Mondtanz-Festival** am Ende jeder Jahreszeit (Maestro Moon). Feste haben eigene Map-Dekoration, Musik, Minispiele und exklusive Items.

### 7.8 Sternenbuch (Sammelalbum)
Kategorien: Pferdefellfarben, Hunderassen, Insekten, Pflanzen, Pilze, Kristalle, Melodien, Aussichtspunkte, Rezepte. Jeder Eintrag mit kleinem Pixel-Bild und charmantem Beschreibungstext. Belohnungen bei Vervollständigung von Kategorien.

### 7.9 Maestro Moon (Sonderfigur)

**⚠️ RECHTLICHE VORGABE, zwingend einzuhalten:** Maestro Moon ist eine **eigenständige Originalfigur und Hommage** an den Stil großer Pop-Showmen der 80er. Verwende **keinen** echten Namen einer realen Person, **kein** Gesicht nach realem Vorbild, **keine** echten Songs, Songtitel, Liedtexte, Samples oder Markenzeichen. Die Hommage entsteht nur durch allgemeine stilistische Codes (Fedora, glitzernder Einzelhandschuh, Moonwalk-artiger Gleitschritt, Glitzerjacke, weiße Socken zu schwarzen Slippern). Alle Musik ist originell (§10).

**Aussehen:** Schlanke Figur, schwarzer Fedora, schulterlanges schwarzes Haar, rote Jacke mit Schnallen und Glitzer-Akzenten (Paletten-Shimmer-Shader), ein einzelner glitzernder Handschuh, schwarze Hose mit Hochwasser, weiße Socken, schwarze Slipper.

**Animationen (Qualitätsmaßstab für das ganze Spiel):**
- Idle: Hutkippen, Fingerschnipsen im Takt, Schulterzucken (8 Frames)
- Laufzyklus: **Gleitschritt rückwärts** (Moonwalk-artig), 12 Frames, butterweich
- Bühnen-Tanz: Drehung, Zehenspitzenstand, Kick, Hutwurf, 24+ Frames als Sequenz
- Emotionen im Portrait: schüchtern-lächelnd, begeistert, nachdenklich, verschmitzt, gerührt, konzentriert, lachend, überrascht

**Persönlichkeit:** Freundlich, sanft und schüchtern im Gespräch, auf der Bühne explodiert er förmlich. Liebt Kinder und Tiere, spricht mit seinem Hut, sagt gern „Shamona!“ (eigener, erfundener Ausruf).

**Rolle im Spiel:**
- Kommt jede **Vollmondnacht** mit der **Wandernden Mondscheinbühne** (eigene Szene, Bühnenlicht mit farbigen Spots, Publikum aus NPCs und Tieren).
- Bringt der Fee die **Musik-Kür** bei → **Rhythmus-Minispiel** (§7.10).
- Bringt dem Hund den Trick „Tanz“ bei.
- Questreihe **„Die verlorene Melodie“**: 7 Melodie-Fragmente, im Tal verstreut (je eines pro Biom + Mikro-Areale), Finale: großer Auftritt mit allen Pferden und Hunden.
- Veranstaltet das **Mondtanz-Festival**.

### 7.10 Rhythmus-Minispiel (Musik-Kür)
- 4 Spuren (Richtungen), Noten fließen auf eine Trefferlinie zu. Das Pferd führt synchron dazu Dressurlektionen aus (Piaffe, Passage, Pirouette, Spanischer Schritt, Verbeugung, eigene Animationen).
- **Timing-Genauigkeit:** Audio-synchron über `AudioServer.get_time_since_last_mix()` und `AudioServer.get_output_latency()`, nicht über Frame-Zeit. Trefferfenster: Perfekt ±45 ms, Gut ±90 ms, sonst Verfehlt.
- **Latenz-Kalibrierung** in den Einstellungen (Tippen im Takt).
- Beatmaps als `data/beatmaps/*.json` (BPM, Offset, Noten mit Beat-Position und Spur). Mindestens **5 Songs** in 3 Schwierigkeitsgraden. Plus ein kleiner **Beatmap-Generator** in `tools/pipeline/`, der aus BPM + Struktur eine sinnvolle Grundmap erzeugt, die dann manuell verfeinert wird.
- **Cozy-Modus:** Verfehlte Noten bestrafen nicht, sie geben nur weniger Glanz. Optional „Auto-Takt“ als Barrierefreiheit.

### 7.11 Wohnbaum & Einrichtung
- Zuhause = **hohler Baum**, innen in Feengröße eingerichtet (Mikro-Maßstab, gemütliche Nussschalen-Möbel, Fingerhut-Lampen) + später ein Anbau in Menschengröße.
- Freies Platzieren auf einem Raster, Drehen, Wandobjekte, Tapeten/Böden. **Mindestens 80 Möbel/Deko-Objekte** in der Vollversion.

### 7.12 Wetter & Atmosphäre
- Sonnig, bewölkt, Regen, Gewitter, Nebel, Wind, Schnee, Sternschnuppennacht (selten).
- Wetter beeinflusst: Tierverhalten (Pferde stellen sich bei Regen unter, Hunde springen in Pfützen), Pflanzen (Regen gießt), NPC-Tagesabläufe, Musik, Sammelobjekte.
- Umgebungsgeräusche geschichtet nach Tageszeit, Biom und Wetter.

### 7.13 Fotomodus
Freie Kamera innerhalb der Map, Zeit einfrieren, Filter (warm, Sepia, Pastell, Nacht), Rahmen, Posen für Fee/Pferd/Hund, Speichern als PNG in `user://screenshots/` in voller Integer-Auflösung.

### 7.14 Wirtschaft & Balancing
- Einnahmen: Produkte verkaufen (Gemüse, Tränke, Handwerk), Turnierpreise, Tierheim-Vermittlungsprämien, Aufträge vom Schwarzen Brett.
- Ausgaben: Stallausbau, Samen, Futter, Möbel, Zuchtgebühren.
- **Ziel-Pacing:** Erster Stallausbau ca. Tag 10, alle MVP-Inhalte in 8–12 Stunden spielbar. Alle Zahlen in `data/config/economy.tres`. Führe eine **Balancing-Simulation** (Headless-Bot, §12) durch und dokumentiere die Kurve.

### 7.15 Koop (optional, erst nach M7)
1–4 Spieler lokal/online über Godots High-Level-Multiplayer (ENet). Nur umsetzen, wenn alle Einzelspieler-Meilensteine fertig und stabil sind. Architektur von Anfang an so gestalten, dass Spielerzustand nicht als globales Singleton-Unikat angenommen wird (Player-ID-basiert), Koop selbst aber erst ganz am Ende.

---

## 8. GRAFIK: STYLEGUIDE & PIPELINE

Lege als Erstes `docs/STYLEGUIDE.md` an und halte dich strikt daran. **Konsistenz ist wichtiger als Einzelbrillanz.**

### 8.1 Grundstil
Warm, weich, nostalgisch, handgemacht. Referenzen im Geiste: *Stardew Valley* (Lesbarkeit, Charme), *Eastward* (Detailgrad, Licht), *Sea of Stars* (dynamisches Licht auf Pixel-Art), *Unpacking* (liebevolle Objekte). Nichts davon kopieren, nur als Qualitätsmaßstab verwenden.

### 8.2 Maße
| Element | Größe |
|---|---|
| Tile | **32 × 32 px** |
| Klio (Menschengröße) | 32 × 48 px (Haare als eigener Layer für Sekundäranimation) |
| Klio (Feengröße) | 16 × 20 px (Brille bleibt als 1-px-Gestell + Glanzpixel erkennbar!) |
| Klio Portrait | 128 × 128 px, **mindestens 12 Emotionen** (inkl. „Brille zurechtschieben“, „verlegen“, „staunend“, „gerührt“) |
| NPCs | 32 × 48 px (Kinder 32 × 36) |
| Hunde | 32 × 24 bis 48 × 32 px je nach Rasse |
| Pferde | **96 × 64 px** (Shetty 64 × 48), Fohlen 64 × 48 |
| Portraits | **128 × 128 px** |
| Item-Icons | 32 × 32 px (Inventar ×2 dargestellt) |
| UI-Grundraster | 8 px |

### 8.3 Palette
- Eine **Master-Palette mit 64 Farben** in `assets/palette/starlight.hex` (plus `.png`-Swatch). Warme Schatten (Violett/Blau statt Schwarz), gesättigte, aber nicht grelle Mittöne, cremige Lichter.
- **Kein reines Schwarz (#000000) und kein reines Weiß (#FFFFFF)** in Sprites.
- Pipeline-Skript `tools/pipeline/check_palette.py` prüft **jedes** PNG in `assets/` und schlägt fehl, wenn Farben außerhalb der Palette vorkommen (Ausnahmen: Normal Maps, Lichttexturen, UI-Transparenzen – per Whitelist).

### 8.4 Zeichenregeln
- Lichtquelle für die Grundschattierung: oben links.
- Außenlinien: farbig (dunklere Variante der Füllfarbe), nicht schwarz. Selektive Linienführung (Außenlinie heller, wo Licht auftrifft).
- Keine „Pillow Shading“-Schattierung, kein Anti-Aliasing gegen Transparenz, keine Mixels (alle Pixel gleich groß; keine skalierten Sprites mit unterschiedlicher Pixelgröße!).
- Dithering sparsam und nur bewusst eingesetzt.

### 8.5 Animationen (Mindest-Framezahlen)
| Animation | Richtungen | Frames |
|---|---|---|
| Klio laufen | 4 (8 für Menschengröße bevorzugt) | 8 (+ Haar-Layer mit Nachschwingen) |
| Klio fliegen (winzig) | 4 | 6 (Flügel) + Bob + wehende Haare |
| Klio idle | 4 | 6 (Atmen, Blinzeln, Flügelzucken) + Varianten: Brille zurechtschieben, Haare hinters Ohr (je 8–10) |
| Klio Verwandlung (Intro + Größenwechsel) | 1 (frontal) | 12–16 |
| Werkzeugaktionen | 4 | 6–8 |
| Pferd Schritt / Trab / Galopp | 4 (8 empfohlen) | 8 / 8 / 8 |
| Pferd idle-Varianten | 4 | Grasen, Schweifschlagen, Ohrenspiel, Schnauben, Wälzen (je 6–12) |
| Hund laufen / rennen | 4 | 6 / 6 |
| Hund idle-Varianten | 4 | Sitzen, Liegen, Kratzen, Schnüffeln, Gähnen, Schwanzwedeln |
| NPC laufen | 4 | 6–8 |
| Maestro Moon | siehe §7.9 | |

- Animations-**Timing** bewusst setzen (nicht alle Frames gleich lang), Squash & Stretch, Nachschwingen (Mähne, Schweif, Flügel, Haare, Kleidung).
- **Sekundäranimation per Code:** Gras biegt sich beim Durchlaufen (Shader mit Spielerposition), Bäume wiegen sich im Wind (Vertex-Shader mit Pixel-Snap), Wasser mit animiertem Tileset.

### 8.6 Licht & Shader
- **Tag-Nacht:** `CanvasModulate` mit **handkuratierter Farbrampe** über den Tag (Morgengold, Mittagsneutral, Abendrosa, Nachtblau), nicht einfach abdunkeln. Rampe als `Gradient`-Resource.
- **Dynamische Lichter:** `PointLight2D` für Laternen, Fenster, Glühwürmchen, Feenglanz der Spielerin, Bühnenscheinwerfer. **Normal Maps** für Hauptobjekte, generiert per Pipeline (§8.8) und handverfeinert, wo nötig.
- **Shader-Liste:** Palette-Swap (Tiere), Wind-Wiegen, Gras-Biegen, Wasser-Reflexion, Glitzer/Shimmer (Feenglanz, Maestro-Moon-Jacke, Sternenschimmer-Fell), Entsättigung→Farbe (geheilte Gebiete), Überhang-Transparenz, Übergangs-Wipe, Regen/Schnee-Overlay, Hitzeflimmern (Sommer, optional).
- Alle Shader müssen **pixelgenau** bleiben (UV-Snapping auf Texel-Raster).

### 8.7 UI-Stil
- Holz-, Pergament- und Blütenmotive, 9-Slice-Rahmen, weiche Farbverläufe nur über Palette-Stufen.
- **Pixel-Font** mit vollständiger Unterstützung deutscher Umlaute und ß (OFL- oder CC0-lizenziert). Zwei Schriftgrößen (Fließtext, Überschriften) plus eine größere Barrierefreiheits-Variante.
- Juicy Feedback: Buttons mit Hover-Bounce, Inventar-Slots mit Ploppen, Geld-Zähler rollt hoch, Herzen pulsieren.
- HUD minimal: Uhr/Tag/Jahreszeit/Wetter-Icon (oben rechts), Feenglanz-Leiste, Werkzeugleiste (unten), Kontexthinweise.

### 8.8 Asset-Pipeline (Python, `tools/pipeline/`)
Da eine KI ohne Zeichentablett arbeitet, entsteht Pixel-Art **programmatisch und iterativ**:
1. **Sprite-Generatoren:** Python-Skripte (Pillow + numpy), die Sprites aus **Formbeschreibungen, Layern und Pixel-Arrays** zusammensetzen (z. B. Pferdekörper aus Segmenten, Tiles aus Mustern + Variationen, Pflanzenstufen aus parametrischen Formen). Jeder Generator ist reproduzierbar (fester Seed).
2. **Handgesetzte Pixel-Daten:** Für Schlüsselsprites (**Klio zuerst und mit der größten Sorgfalt**, Maestro Moon, Portraits, Pferde-Basis) definiere Sprites als **ASCII-/Array-Pixelkarten mit Palettenindizes** in Python/JSON und rendere sie. Arbeite Frame für Frame, prüfe jede Version **visuell** (Screenshot/Bild ansehen, falls du Bilder betrachten kannst) und iteriere so lange, bis Silhouette, Lesbarkeit und Charme stimmen.
3. **Optional Bildgenerierung** (falls verfügbar): Ergebnisse müssen durch `pixelize.py` laufen: auf Zielgröße per Nearest-Neighbor bzw. Block-Median herunterskalieren, auf Master-Palette quantisieren (ohne Dithering), Kanten säubern, Transparenz binär machen, danach **manuell per Pixelkarte nachkorrigieren**. Rohe, generierte Bilder niemals direkt verwenden.
4. `normalmap.py`: Erzeugt Normal Maps aus Höhen-Hinweisen/Layermasken (für Pixel-Art geeignet: abgeflachte, 4–8-stufige Normalen, keine verrauschten Sobel-Karten).
5. `atlas.py`: Packt Frames zu Spritesheets mit JSON-Metadaten. Godot-Import-Einstellungen: Filter aus, Mipmaps aus, Kompression verlustfrei.
6. `check_palette.py`, `check_sizes.py` (Maße & Raster), `check_licenses.py` (jede Datei in `assets/` hat Eintrag in `ASSET_MANIFEST.csv`).
7. **Ein Befehl** `python tools/pipeline/build_assets.py` baut alle generierten Assets neu und führt alle Prüfungen aus.

### 8.9 Visuelle Qualitätskontrolle
- Nach jedem Meilenstein: automatisierte Screenshots festgelegter Szenen/Uhrzeiten/Wetterlagen nach `docs/screenshots/m{n}/` (Debug-Befehl, der die Kamera an Positionen setzt und `get_viewport().get_texture().get_image().save_png()` aufruft).
- Betrachte die Screenshots selbst kritisch nach Checkliste: Lesbarkeit der Silhouetten, Farbharmonie, Pixel-Konsistenz (keine Mixels), Y-Sort-Fehler, Lichtstimmung, UI-Überlappung. Notiere Befunde und behebe sie.

---

## 9. ASSET-BESCHAFFUNG & LIZENZEN

**Priorität:**
1. **Selbst erstellt** (Code, Pipeline, Pixelkarten) → bevorzugt, volle Konsistenz.
2. **CC0 / Public Domain** (z. B. OpenGameArt mit CC0-Filter, Kenney.nl, freesound.org nur CC0) → erlaubt, muss aber auf Stil & Palette angepasst werden.
3. **CC-BY 4.0 / OFL / MIT** → erlaubt mit Namensnennung in `CREDITS.md` und im Abspann.
4. **Verboten:** CC-BY-NC (nicht kommerziell), CC-BY-SA für Assets, die mit eigenem Code gemischt werden, wenn unklar; Lizenzen „nur für nicht-kommerzielle Nutzung“; Assets ohne klar erkennbare Lizenz; Rips aus anderen Spielen; alles mit realen Marken, Logos, Personen, Songs.

Für **jedes** Fremd-Asset in `docs/ASSET_MANIFEST.csv`: `pfad, typ, quelle_url, autor, lizenz, lizenz_url, abruf_datum, modifiziert (ja/nein), notiz`. Lege die Lizenztexte unter `docs/licenses/` ab.

**Hinweis:** Da Fremd-Assets den einheitlichen Stil gefährden, verwende sie vor allem für Audio und Fonts, bei Grafik nur als Grundlage für starke Überarbeitung.

---

## 10. AUDIO

### 10.1 Musik
- Stil: akustisch, warm, verspielt mit Harfe, Akustikgitarre, Holzbläsern (Flöte, Klarinette), Glockenspiel, Streicher-Pads, leichten Percussions. Für die Mondscheinbühne: **funky Pop mit Bass, Clavinet, knackigem Schlagzeug und Bläsersätzen** im 80er-Stil, komplett **originell**.
- Bedarf (MVP): Hauptmenü, Mooswiesen Tag, Mooswiesen Abend, Dorf, Stall/Zuhause, Nacht, Regen, Fest, Mondscheinbühne (≥ 3 Tracks), Rhythmus-Songs (≥ 5), Jingles (Level-up, Neuer Tag, Herz gewonnen, Quest erledigt).
- **Beschaffung:** Selbst erzeugen (z. B. prozedural/algorithmisch mit einem Python-Synth- oder Tracker-Ansatz, als OGG gerendert) oder CC0/CC-BY-Musik, die stilistisch passt. Alle Loops **nahtlos** (Loop-Punkte in den Godot-Importeinstellungen gesetzt).
- Crossfades bei Gebiets- und Tageszeitwechsel (2–4 s). Musik-Varianten je Wetter, wo sinnvoll.

### 10.2 Soundeffekte
- Schritte je Untergrund (Fee, Pferd, Hund, NPC), Flügelflattern, Verwandlung, Streicheln (Pferd schnaubt, Hund hechelt/fiept glücklich), Wiehern (mehrere Varianten, Tonhöhe je Pferd), Bellen (je Rasse), Werkzeuge, UI-Klicks, Inventar, Geld, Herz, Kessel, Glocken, Wetter-Ambience (Regen, Wind, Vögel, Grillen, Meer, Lagerfeuer).
- Erzeugung: eigener Python-sfxr-Klon für UI/Magie-Sounds + CC0-Aufnahmen für organische Geräusche. Alle als OGG, normalisiert (−16 LUFS Musik, −14 bis −18 LUFS SFX nach Gefühl, keine Übersteuerung).
- Leichte **zufällige Tonhöhen-/Lautstärkevariation** bei wiederholten Sounds.

### 10.3 Audio-Busse
Master → Musik, SFX, Ambience, UI, Stimmen (Tipp-Laute). Jeder Bus in den Einstellungen regelbar. Leichter Hall in Innenräumen und Mikro-Arealen (Bus-Effekt, szenenabhängig).

---

## 11. UI/UX, BARRIEREFREIHEIT, LOKALISIERUNG

**Menüs:** Titelbildschirm mit Logo **„Starlight – Klio goes Fairy“** (Pixel-Schriftzug mit funkelndem Stern-Akzent) und animiertem Hintergrund: Klio fliegt im Sternenlicht über das Tal, ihre Haare wehen, Pferde grasen, der Hund schaut ihr nach. Außerdem: Neues Spiel (Intro, danach Hofname und Wahl des Seelenhunds), Garderobe, Laden, Einstellungen, Credits, Beenden. Pausemenü. Inventar (Grid, Stapel, Sortieren, Drag & Drop, Gamepad-tauglich), Tierübersicht (Karteikarten mit Werten, Stammbaum bei Pferden), Beziehungen, Sternenbuch, Quests, Karte, Rezeptbuch.

**Keine Charaktererstellung:** Die Heldin ist immer Klio (§5.1). Stattdessen gibt es eine **Garderobe** im Baumhaus mit Outfits, Brillengestellen, Frisurvarianten, Haarschmuck und Flügelfarben. Dort ist eine große Vorschau mit Portrait und Sprite zu sehen, sie dreht sich und schiebt die Brille zurecht. Zu Spielbeginn wählt man den Namen des Hofs und den Seelenhund.

**Barrierefreiheit:**
- Textgröße (3 Stufen), Legasthenie-freundliche Schrift als Option
- Farbenblind-Modi (Protanopie, Deuteranopie, Tritanopie) für UI-Markierungen
- Bildschirmwackeln/Blitzeffekte abschaltbar
- „Entspannter Modus“ (Zeit langsamer oder in Innenräumen pausiert)
- Rhythmusspiel: Latenzkalibrierung, Auto-Takt, langsamere Geschwindigkeit
- Alle Aktionen ohne Maus möglich, keine Pflicht-Schnellklick-Aufgaben
- Untertitel/Beschriftungen für wichtige Geräusche (optional)

**Lokalisierung:** **Deutsch als Primärsprache**, Englisch vollständig. Alle Texte über Übersetungsschlüssel in `data/localization/*.csv`, keine Strings im Code. Textboxen müssen mit 30 % längeren Texten klarkommen.

**Schreibstil:** Warm, humorvoll, nie zynisch. Kurze Sätze in Dialogen (max. 3 Zeilen pro Box). Jede Figur hat eine erkennbare Stimme. Keine kulturell verletzenden Klischees.

---

## 12. TESTEN & QA

1. **Unit-Tests (GdUnit4)** mindestens für: Genetik (Genotyp→Phänotyp, Vererbung, statistische Verteilung über 10.000 Würfe innerhalb Toleranz), Zeit/Kalender/Mondphase, Inventar (Stapeln, Grenzen, Sortieren), Wirtschaft, Beziehungswerte, Dialogbedingungen, Save/Load-Rundreise, Save-Migration, Beatmap-Parsing & Trefferbewertung, Hunde-Vermittlungs-Matching.
2. **Integrationstests:** Szenen laden ohne Fehler (automatisch **alle** `.tscn` in `scenes/` instanziieren und prüfen), Szenenübergänge, Spawnpunkte existieren, alle referenzierten Ressourcen existieren, alle Übersetzungsschlüssel vorhanden in DE und EN.
3. **Headless-Smoke-Test:** `godot --headless --path . res://tests/smoke/smoke_run.tscn`. Ein **Bot** spielt 7 Spieltage im Schnelldurchlauf (versorgt Tiere, geht ins Dorf, speichert, lädt), das Log muss frei von Errors/Warnings sein.
4. **Balancing-Bot:** Simuliert 1 Spieljahr mit einer „durchschnittlichen“ Strategie, gibt Geld/Vertrauen/Herzquelle über Zeit als CSV aus → `docs/balancing/`.
5. **Performance:** Frame-Time-Messung in der dichtesten Szene (Fest mit allen NPCs und Tieren), Ziel < 8 ms CPU-Zeit pro Frame auf Mittelklasse-Hardware. Ergebnis in DEVLOG.
6. **Visuelle QA:** Screenshot-Sets pro Meilenstein (§8.9).
7. **Ein Befehl für alles:** `tools/run_all_checks.ps1` → Asset-Checks, Unit-Tests, Integrationstests, Smoke-Test, Export-Test. Muss vor jedem Meilenstein-Tag grün sein.

---

## 13. EXPORT & AUSLIEFERUNG

- Export-Preset „Windows Desktop“ (x86_64), Icon (eigenes Pixel-Icon, .ico in mehreren Größen), Produktname, Version (`0.{meilenstein}.{build}`), PCK eingebettet.
- Befehl: `godot --headless --path . --export-release "Windows Desktop" build/windows/Starlight.exe`
- Nach dem Export: Build starten, 60 s laufen lassen (automatisiert per Smoke-Flag `--smoke`), Exit-Code und Log prüfen.
- Zusätzlich optional: Linux-Export (für Steam Deck), Web-Export nur falls ohne Qualitätsverlust möglich.
- **Endprodukt-Ordner** `build/release/`: `Starlight.exe` (Produktname „Starlight – Klio goes Fairy“), `README.txt` (Steuerung, Systemanforderungen), `CREDITS.txt`, `LICENSES/`.

---

## 14. MEILENSTEINE MIT ABNAHMEKRITERIEN

> Arbeite strikt in dieser Reihenfolge. **Jeder Meilenstein endet mit: alle Checks grün, Export funktioniert, Screenshots, Bericht, Git-Tag.**

### M0 – Fundament
- Tools installiert und verifiziert, Git-Repo, Projektstruktur, Projekteinstellungen (§4.1), Autoloads als Gerüst, GdUnit4 lauffähig, `run_all_checks.ps1`, Styleguide + Master-Palette, Pipeline-Grundgerüst, leerer Windows-Export startet.
- **Abnahme:** Export öffnet ein Fenster mit Testszene in Integer-Skalierung. Ein Beispiel-Unit-Test läuft grün.

### M1 – Das Gefühl (Kernmechanik-Prototyp)
- Eine Test-Wiese (ca. 40×30 Tiles) mit Platzhalter-Grafik in Palette. **Klio schon als erkennbare Figur** (lange braune Haare, Brille, Flügel; darf noch nicht final sein), in beiden Größen, Größenwechsel mit vollem Effekt, Fliegen, Kollisionslayer, ein Hund (folgen, streicheln, reiten in Feengröße), ein Pferd (streicheln, reiten in Menschengröße mit 3 Gangarten), Kamera, Gamepad + Tastatur.
- **Abnahme:** Bewegung, Wechsel, Reiten fühlen sich flüssig und befriedigend an. Beschreibe im Bericht konkret Beschleunigungskurven, Timing und Feedback. Keine Ruckler, kein Subpixel-Zittern.

### M2 – Die Welt lebt
- Echte Tilesets für Mooswiesen und Hof (Autotiling), Baumhaus-Innenraum, Tag-Nacht-Farbrampe, Licht + Normal Maps, Wetter (Sonne, Regen, Nebel), Wind/Gras-Shader, Y-Sort, Überhang-Transparenz, Zeit/Kalender, Schlafen, Save/Load mit Slots, HUD, Pausemenü, Einstellungen.
- **Abnahme:** 3 aufeinanderfolgende Tage spielbar inkl. Speichern/Laden. Screenshot-Set Morgen/Mittag/Abend/Nacht × Sonne/Regen.

### M3 – Tiere mit Seele
- Pferdesystem komplett (3 Startpferde, Werte, Persönlichkeit, Pflege-Minispiel, Füttern, Vertrauensstufen mit Story-Schnipseln, Koppel/Stall Stufe 1–2, Rufen per Pfiff), Genetik-System + Palette-Swap-Shader + Tests, Hundesystem (Seelenhund-Auswahl, Idle-Verhalten, Fähigkeiten Schnüffeln/Buddeln/Apportieren, Tricks), Tierübersicht-UI.
- **Abnahme:** Genetik-Tests grün, 20 zufällig generierte Pferde werden korrekt eingefärbt (Screenshot-Collage). Pflege-Minispiel fühlt sich entspannend an (Beschreibung + Screenshots).

### M4 – Das Dorf
- Dorf-Map, 10 NPCs mit Portraits (8 Emotionen), Tagesabläufen, Dialogen (DE+EN), Geschenken, Herzen, je 2 Herz-Events. Laden (Kaufen/Verkaufen), Tierheim mit Vermittlung (≥ 6 Hunde), Schwarzes Brett mit Aufträgen, Feengarten mit ≥ 12 Pflanzen, Tränkeküche mit ≥ 8 Rezepten, Inventar/Werkzeuge.
- **Abnahme:** Headless-Bot spielt 7 Tage fehlerfrei. Balancing-CSV für 28 Tage vorhanden und plausibel.

### M5 – Maestro Moon & die Mondscheinbühne
- Maestro Moon komplett (Sprite, alle Animationen, Portrait, Dialoge), Mondscheinbühne-Szene mit Bühnenlicht, Rhythmus-Minispiel mit Audio-Sync, Latenz-Kalibrierung, 5 Songs × 3 Schwierigkeiten, Pferde-Dressuranimationen, Hundetrick „Tanz“, Questreihe „Die verlorene Melodie“ (mindestens die ersten 3 Fragmente).
- **Abnahme:** Trefferbewertung per Test verifiziert, Timing-Drift nach 3 Minuten Song < 10 ms. Maestro Moon erfüllt die rechtlichen Vorgaben aus §7.9.

### M6 – Vertical Slice: Frühling komplett
- Kompletter Frühling (28 Tage) in Endqualität: Kapitel 1–2 der Herzquelle, Mikro-Areale (≥ 3) mit Rätseln, 2 Frühlingsfeste + 1 Mondtanz-Festival, 1 Turnier, Sternenbuch, Fotomodus, **Klio in Endqualität** (alle Sprites, Signature-Animationen, 12 Portrait-Emotionen), Intro-Sequenz „Klio goes Fairy“, Garderobe, Titelbildschirm mit Logo, Credits, Musik und SFX vollständig für alles Vorhandene, Barrierefreiheitsoptionen, vollständige DE/EN-Lokalisierung.
- **Abnahme:** 8–12 Stunden spielbarer, polierter Inhalt. Alle Checks grün. Das ist das **erste „fertige Produkt“**, eine Demo in Release-Qualität.

### M7 – Volles Jahr
- Sommer, Herbst, Winter mit Biomen Nebelwald, Kreideküste, Sternenhochland; Kapitel 3–7; alle Feste; 28 NPCs; Heirat; Zucht mit Fohlen und Feengenen; Wildpferdherde; Stallausbau Stufe 3–4; 24+ Pflanzen; 80+ Möbel; Finale + Epilog; Endlosspiel danach.
- **Abnahme:** Balancing-Bot über 1 Jahr, Performance-Messung, vollständige Screenshot-Galerie.

### M8 – Politur & Release-Kandidat
- Juice-Pass (Partikel, Screen-Feedback, Übergänge), Balancing-Feinschliff, Bugfixing aus `KNOWN_ISSUES.md`, Ladezeiten, Steam-Deck-Tauglichkeit (Linux-Export, Gamepad-only-Durchlauf), Credits-Abspann, Release-Ordner.
- Optional danach: **M9 Koop**.

---

## 15. QUALITÄTSMASSSTAB („Definition of Done“)

Ein Feature ist erst fertig, wenn:
- [ ] Es funktioniert und durch Tests/Headless-Lauf/Screenshot **verifiziert** ist
- [ ] Es datengetrieben erweiterbar ist
- [ ] Es Grafik in Endqualität hat (oder ausdrücklich als Platzhalter in KNOWN_ISSUES steht)
- [ ] Es Sound-Feedback hat
- [ ] Es mit Tastatur **und** Gamepad bedienbar ist
- [ ] Alle Texte lokalisiert sind (DE + EN)
- [ ] Es gespeichert und geladen wird
- [ ] Keine Fehler oder Warnungen im Log erzeugt
- [ ] Im GDD dokumentiert ist

**Anti-Muster, die du vermeiden musst:**
- Riesige „God-Scripts“ mit 1.000+ Zeilen
- Magische Zahlen im Code statt in Config-Ressourcen
- Unterschiedliche Pixelgrößen / skalierte Sprites / Filter-Unschärfe
- Grelle, ungestimmte Farben außerhalb der Palette
- Platzhalter, die stillschweigend im Release landen
- Features „vorbereitet, aber nicht angeschlossen“
- Eine Mechanik, die bestraft oder Stress erzeugt (widerspricht „cozy“)
- Behauptungen ohne Verifikation

---

## 16. BERICHTSFORMAT NACH JEDEM MEILENSTEIN

```
## Meilenstein M{n} – {Name}: {ERFÜLLT / TEILWEISE / NICHT ERFÜLLT}

### Umgesetzt
- …

### Verifiziert durch
- Tests: {x} bestanden / {y} gesamt
- Smoke-Test: {Ergebnis}
- Export: {Pfad, Größe, Startet: ja/nein}
- Screenshots: docs/screenshots/m{n}/

### Designentscheidungen (mit Begründung)
- …

### Bekannte Probleme / Platzhalter
- …

### Nächste Schritte
- …

### Fragen an dich (nur falls wirklich nötig)
- …
```

---

## 17. START

Beginne jetzt mit **M0**. Prüfe zuerst die vorhandene Umgebung (installierte Tools, Versionen, freier Speicherplatz), dann installiere das Fehlende, lege Struktur und Dokumente an und arbeite dich bis zur Abnahme von M0 vor. Gehe danach **ohne erneute Nachfrage** zu M1 über, sofern keine Blocker bestehen, und fahre so fort. Halte nach jedem Meilenstein kurz inne, liefere den Bericht und setze dann fort, außer der Mensch bittet dich, zu warten.

Mach aus Klios Geschichte etwas, das Menschen lieben werden. ✨🐴🐕🧚👓
