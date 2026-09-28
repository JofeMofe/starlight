# Starlight – Klio goes Fairy

Ein cozy 2D-Pixel-Art-Lebenssimulationsspiel im verwunschenen Glimmertal. Klio wird zur Fee,
wechselt ihre Größe und schenkt vernachlässigten Pferden und Hunden Liebe.

**Stand:** Meilenstein M0 – Fundament (Version 0.0.1). Spielbar ist eine Testszene; die
eigentliche Spielmechanik beginnt mit M1. Fortschritt: `docs/DEVLOG.md`.

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

## Steuerung (Testszene M0)

| Taste | Wirkung |
|---|---|
| F2 | Sprache Deutsch ↔ Englisch |
| F12 | Screenshot nach `user://screenshots/` |

Vollständige Belegung: `docs/GDD.md` §6.

## Lizenz

Code: MIT (`LICENSE`). Assets: siehe `CREDITS.md` und `docs/ASSET_MANIFEST.csv`.
