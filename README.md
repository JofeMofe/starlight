# Starlight – Klio goes Fairy

Ein cozy 2D-Pixel-Art-Lebenssimulationsspiel im verwunschenen Glimmertal. Klio wird zur Fee,
wechselt ihre Größe und schenkt vernachlässigten Pferden und Hunden Liebe.

**Stand:** Meilenstein M1 – Das Gefühl (Version 0.1.1). Spielbar ist eine Test-Wiese mit Klio
(Mensch und Fee), ihrem Hund und dem Pferd Holunder. Fortschritt: `docs/DEVLOG.md`.

## Starten

**Fertiger Build (Windows):** `build/windows/Starlight.exe` doppelklicken (wird lokal erzeugt, s. u.).

**Aus dem Quellcode:**
1. Godot 4.4.1 (Standard-Build, nicht .NET) installieren, Pfad in `tools/godot_path.txt` eintragen.
2. `godot --path .` (oder Projekt im Editor öffnen und F5).

## Bauen & prüfen

| Zweck | Windows (PowerShell) | Linux |
|---|---|---|
| Hilfswerkzeuge (rcedit) | rcedit-x64.exe nach `tools\bin\` legen, Pfad im Editor unter *Export > Windows > rcedit* | `tools/setup_tools.sh` |
| Alle Checks | `powershell -ExecutionPolicy Bypass -File tools\run_all_checks.ps1` | `tools/run_all_checks.sh` |
| Nur Assets | `python tools\pipeline\build_assets.py` | `python3 tools/pipeline/build_assets.py` |
| Windows-Export | `godot --headless --path . --export-release "Windows Desktop" build/windows/Starlight.exe` | dito (mit `LC_ALL=C.UTF-8`) |

Voraussetzungen für die Asset-Pipeline: Python 3.11+ mit `pillow` und `numpy`.

## Kommandozeilen-Schalter

| Schalter | Wirkung |
|---|---|
| `--smoke` / `--smoke-seconds=N` | läuft N Sekunden (Standard 60) und beendet sich mit Exit-Code 0 |
| `--scene=res://…` | andere Startszene |
| `--screenshot=PFAD` / `--screenshot-delay=N` | Screenshot in voller Integer-Auflösung, dann Ende |

## Steuerung (Test-Wiese M1)

| Taste (Gamepad) | Wirkung |
|---|---|
| WASD / Pfeile (linker Stick) | Laufen, Fliegen, Reiten lenken |
| Q (Y) | Größe wechseln (am Feenring gratis, sonst 5 Feenglanz) |
| Leertaste (B) halten | als Fee fliegen – über Zäune, Büsche, Wasser |
| E (A) | Streicheln · als Fee auf den Hund · absteigen · am Feenring verwandeln |
| Leertaste (B) am Pferd | aufsteigen; beim Reiten antippen = schneller, im Galopp = springen |
| F (X) · R (LB) | Hund rufen · Pferd herpfeifen |
| F1 · F3 | Hilfe ein/aus · Bildrate |

Vollständige Belegung: `docs/GDD.md` §6.

## Lizenz

Code: MIT (`LICENSE`). Assets: siehe `CREDITS.md` und `docs/ASSET_MANIFEST.csv`.
