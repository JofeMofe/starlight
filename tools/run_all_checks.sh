#!/usr/bin/env bash
# Ein Befehl für alle Prüfungen (§12.7), Linux/Cloud-Variante von run_all_checks.ps1.
#   1. Asset-Pipeline (Generieren + Palette/Maße/Lizenzen)
#   2. Godot-Import
#   3. GDScript-Lint (jede Warnung = Fehler)
#   4. Unit- + Integrationstests (gdUnit4)
#   5. Headless-Smoke-Bot (7 Spieltage)
#   6. Windows-Export + 60-s-Lauf mit --smoke (via Wine, falls vorhanden)
#   7. Linux-Export + Smoke-Lauf
# Optionen: --quick (ohne Exporte), --smoke-seconds=N (Standard 60)
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
GODOT_BIN="${GODOT_BIN:-$(cat tools/godot_path.txt)}"
LOG_DIR="$ROOT/build/logs"
mkdir -p "$LOG_DIR"
QUICK=0
SMOKE_SECONDS=60
for arg in "$@"; do
  case "$arg" in
    --quick) QUICK=1 ;;
    --smoke-seconds=*) SMOKE_SECONDS="${arg#*=}" ;;
  esac
done

FAILED=()
step() { echo; echo "=== $1 ==="; }
fail() { echo "FEHLGESCHLAGEN: $1"; FAILED+=("$1"); }

# Fehler-/Warnungszeilen in Godot-Logs, die nichts mit dem Projekt zu tun
# haben (fehlende Soundkarte/VSync in der Container-/Xvfb-Umgebung).
ENV_NOISE='ALSA lib|audio_driver_alsa|audio_driver_wasapi|WASAPI|All audio drivers failed|falling back to the dummy driver|V-Sync mode|Condition "hr != ..HRESULT.0x00000000|at: (init_output_device|initialize|init|audio_device_init|_set_vsync|set_use_vsync|window_set_vsync_mode) '

check_log_clean() {  # $1 = Logdatei, $2 = Schrittname
  local hits
  hits="$(sed 's/\x1b\[[0-9;]*m//g' "$1" | grep -E '^(ERROR|WARNING|SCRIPT ERROR)|^\s+at: ' | grep -Ev "$ENV_NOISE" || true)"
  if [ -n "$hits" ]; then
    echo "$hits" | head -20
    fail "$2 (Fehler/Warnungen im Log)"
  fi
}

step "1/7 Asset-Pipeline"
python3 tools/pipeline/build_assets.py || fail "Asset-Pipeline"
if [ -n "$(git status --porcelain assets docs/ASSET_MANIFEST.csv 2>/dev/null)" ]; then
  echo "Hinweis: build_assets hat Dateien verändert (bitte committen)."
fi

step "2/7 Godot-Import"
# Beim allerersten Import eines frischen Klons meldet Godot das Projekt-Theme,
# bevor die Schrift importiert ist -> zweimal importieren, nur der zweite Lauf zählt.
"$GODOT_BIN" --headless --path . --import > "$LOG_DIR/import_1.log" 2>&1
"$GODOT_BIN" --headless --path . --import > "$LOG_DIR/import.log" 2>&1 || fail "Import"
check_log_clean "$LOG_DIR/import.log" "Import"

step "3/7 GDScript-Lint"
python3 tools/lint/lint_gdscript.py "$GODOT_BIN" || fail "GDScript-Lint"

step "4/7 Unit- und Integrationstests"
"$GODOT_BIN" --headless --path . -d -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd \
  -a res://tests/unit -a res://tests/integration --ignoreHeadlessMode -c \
  < /dev/null > "$LOG_DIR/tests.log" 2>&1
TEST_EXIT=$?
sed 's/\x1b\[[0-9;]*m//g' "$LOG_DIR/tests.log" | grep -E "Overall Summary|Exit code" || true
[ "$TEST_EXIT" -eq 0 ] || fail "Tests (Exit $TEST_EXIT, siehe build/logs/tests.log)"

step "5/7 Headless-Smoke-Bot"
"$GODOT_BIN" --headless --path . res://tests/smoke/smoke_run.tscn > "$LOG_DIR/smoke_bot.log" 2>&1
SMOKE_EXIT=$?
grep -E "SMOKE_RUN" "$LOG_DIR/smoke_bot.log" || true
[ "$SMOKE_EXIT" -eq 0 ] || fail "Smoke-Bot (Exit $SMOKE_EXIT)"
check_log_clean "$LOG_DIR/smoke_bot.log" "Smoke-Bot"

if [ "$QUICK" -eq 0 ]; then
  step "6/7 Windows-Export + Start"
  mkdir -p build/windows
  # UTF-8-Locale, damit rcedit (über Wine) „–“ und „©“ korrekt schreibt
  LC_ALL=C.UTF-8 LANG=C.UTF-8 WINEDEBUG=-all \
    "$GODOT_BIN" --headless --path . --export-release "Windows Desktop" build/windows/Starlight.exe \
    > "$LOG_DIR/export_windows.log" 2>&1 || fail "Windows-Export"
  check_log_clean "$LOG_DIR/export_windows.log" "Windows-Export"
  if [ -f build/windows/Starlight.exe ]; then
    ls -la build/windows/Starlight.exe
    if command -v wine > /dev/null && command -v xvfb-run > /dev/null; then
      LC_ALL=C.UTF-8 WINEDEBUG=-all timeout $((SMOKE_SECONDS + 120)) xvfb-run -a -s "-screen 0 1920x1080x24" \
        wine build/windows/Starlight.exe --resolution 1280x720 --smoke --smoke-seconds="$SMOKE_SECONDS" \
        > "$LOG_DIR/run_windows.log" 2>&1
      WIN_EXIT=$?
      grep -E "SMOKE OK" "$LOG_DIR/run_windows.log" || fail "Windows-Build startet nicht sauber (Exit $WIN_EXIT)"
      check_log_clean "$LOG_DIR/run_windows.log" "Windows-Build-Lauf"
    else
      echo "Hinweis: wine/xvfb fehlen – Windows-Build nur exportiert, nicht gestartet."
    fi
  else
    fail "Windows-Exe fehlt"
  fi

  step "7/7 Linux-Export + Start"
  mkdir -p build/linux
  "$GODOT_BIN" --headless --path . --export-release "Linux" build/linux/Starlight.x86_64 \
    > "$LOG_DIR/export_linux.log" 2>&1 || fail "Linux-Export"
  check_log_clean "$LOG_DIR/export_linux.log" "Linux-Export"
  timeout $((SMOKE_SECONDS + 60)) xvfb-run -a -s "-screen 0 1920x1080x24" \
    build/linux/Starlight.x86_64 --audio-driver Dummy --resolution 1280x720 --smoke --smoke-seconds="$SMOKE_SECONDS" \
    > "$LOG_DIR/run_linux.log" 2>&1
  grep -E "SMOKE OK" "$LOG_DIR/run_linux.log" || fail "Linux-Build startet nicht sauber"
  check_log_clean "$LOG_DIR/run_linux.log" "Linux-Build-Lauf"
fi

echo
if [ "${#FAILED[@]}" -eq 0 ]; then
  echo "run_all_checks: ALLES GRÜN"
  exit 0
fi
echo "run_all_checks: ${#FAILED[@]} Schritt(e) fehlgeschlagen:"
printf '  - %s\n' "${FAILED[@]}"
exit 1
