#!/usr/bin/env bash
# Richtet Hilfswerkzeuge für Export & Checks ein (Linux/Cloud, §2a).
# - rcedit (MIT, electron/rcedit) für Icon + Versionsinfo in der Windows-Exe,
#   ausgeführt über Wine
# - trägt rcedit/wine in die Godot-Editor-Einstellungen ein
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BIN="$ROOT/tools/bin"
RCEDIT_VERSION="v2.0.0"
RCEDIT="$BIN/rcedit-x64.exe"
mkdir -p "$BIN"

if [ ! -f "$RCEDIT" ]; then
  echo "Lade rcedit $RCEDIT_VERSION …"
  curl -sSfL -o "$RCEDIT" "https://github.com/electron/rcedit/releases/download/$RCEDIT_VERSION/rcedit-x64.exe"
fi

GODOT_BIN="${GODOT_BIN:-$(cat "$ROOT/tools/godot_path.txt")}"
VERSION_SHORT="$("$GODOT_BIN" --version | cut -d. -f1-2)"
SETTINGS="$HOME/.config/godot/editor_settings-$VERSION_SHORT.tres"
if [ ! -f "$SETTINGS" ]; then
  # Einmal den Editor headless starten, damit die Datei entsteht
  "$GODOT_BIN" --headless --editor --path "$ROOT" --quit >/dev/null 2>&1 || true
fi
WINE_BIN="$(command -v wine || true)"
if [ -z "$WINE_BIN" ]; then
  echo "WARNUNG: wine nicht gefunden – Windows-Exe bekommt kein eigenes Icon (apt install wine64)"
else
  sed -i "s#^export/windows/rcedit = .*#export/windows/rcedit = \"$RCEDIT\"#" "$SETTINGS"
  sed -i "s#^export/windows/wine = .*#export/windows/wine = \"$WINE_BIN\"#" "$SETTINGS"
fi
echo "setup_tools: fertig (rcedit: $RCEDIT, wine: ${WINE_BIN:-fehlt})"
