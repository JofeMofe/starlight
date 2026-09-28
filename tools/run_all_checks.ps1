# Ein Befehl für alle Prüfungen (§12.7) – Windows 11 / PowerShell 5.1.
#   1. Asset-Pipeline  2. Godot-Import  3. GDScript-Lint  4. Unit-/Integrationstests
#   5. Headless-Smoke-Bot  6. Windows-Export + 60-s-Lauf mit --smoke
# Aufruf:  powershell -ExecutionPolicy Bypass -File tools\run_all_checks.ps1 [-Quick] [-SmokeSeconds 60]
# Hinweis: In der Linux-Cloud-Umgebung wird tools/run_all_checks.sh verwendet (gleiche Schritte).
param(
    [switch]$Quick,
    [int]$SmokeSeconds = 60
)

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$Godot = if ($env:GODOT_BIN) { $env:GODOT_BIN } else { (Get-Content "tools\godot_path.txt" -Raw).Trim() }
$LogDir = Join-Path $Root "build\logs"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$Failed = New-Object System.Collections.Generic.List[string]

function Step($name) { Write-Host ""; Write-Host "=== $name ===" -ForegroundColor Cyan }
function Fail($name) { Write-Host "FEHLGESCHLAGEN: $name" -ForegroundColor Red; $script:Failed.Add($name) }

# Umgebungsrauschen, das nicht vom Projekt stammt
$EnvNoise = 'V-Sync mode|at: (_set_vsync|window_set_vsync_mode)'

function Test-LogClean($logFile, $stepName) {
    $hits = Get-Content $logFile | Where-Object {
        ($_ -match '^(ERROR|WARNING|SCRIPT ERROR)' -or $_ -match '^\s+at: ') -and ($_ -notmatch $EnvNoise)
    }
    if ($hits) {
        $hits | Select-Object -First 20 | ForEach-Object { Write-Host $_ }
        Fail "$stepName (Fehler/Warnungen im Log)"
    }
}

# Godot ist eine GUI-Anwendung; für eingesammelte Ausgabe die _console.exe nutzen, falls vorhanden
$GodotConsole = $Godot -replace '\.exe$', '_console.exe'
if (Test-Path $GodotConsole) { $Godot = $GodotConsole }

Step "1/6 Asset-Pipeline"
python tools\pipeline\build_assets.py
if ($LASTEXITCODE -ne 0) { Fail "Asset-Pipeline" }

Step "2/6 Godot-Import"
& $Godot --headless --path . --import *> "$LogDir\import_1.log"
& $Godot --headless --path . --import *> "$LogDir\import.log"
Test-LogClean "$LogDir\import.log" "Import"

Step "3/6 GDScript-Lint"
python tools\lint\lint_gdscript.py $Godot
if ($LASTEXITCODE -ne 0) { Fail "GDScript-Lint" }

Step "4/6 Unit- und Integrationstests"
$null | & $Godot --headless --path . -d -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd `
    -a res://tests/unit -a res://tests/integration --ignoreHeadlessMode -c *> "$LogDir\tests.log"
$testExit = $LASTEXITCODE
Select-String -Path "$LogDir\tests.log" -Pattern "Overall Summary|Exit code" | ForEach-Object { $_.Line }
if ($testExit -ne 0) { Fail "Tests (Exit $testExit)" }

Step "5/6 Headless-Smoke-Bot"
& $Godot --headless --path . res://tests/smoke/smoke_run.tscn *> "$LogDir\smoke_bot.log"
$smokeExit = $LASTEXITCODE
Select-String -Path "$LogDir\smoke_bot.log" -Pattern "SMOKE_RUN" | ForEach-Object { $_.Line }
if ($smokeExit -ne 0) { Fail "Smoke-Bot (Exit $smokeExit)" }
Test-LogClean "$LogDir\smoke_bot.log" "Smoke-Bot"

if (-not $Quick) {
    Step "6/6 Windows-Export + Start"
    New-Item -ItemType Directory -Force -Path "build\windows" | Out-Null
    & $Godot --headless --path . --export-release "Windows Desktop" build/windows/Starlight.exe *> "$LogDir\export_windows.log"
    Test-LogClean "$LogDir\export_windows.log" "Windows-Export"
    if (Test-Path "build\windows\Starlight.exe") {
        Get-Item "build\windows\Starlight.exe" | Format-Table Name, Length -AutoSize
        $exe = if (Test-Path "build\windows\Starlight.console.exe") { "build\windows\Starlight.console.exe" } else { "build\windows\Starlight.exe" }
        $proc = Start-Process -FilePath $exe -ArgumentList "--smoke", "--smoke-seconds=$SmokeSeconds" `
            -RedirectStandardOutput "$LogDir\run_windows.log" -RedirectStandardError "$LogDir\run_windows_err.log" `
            -PassThru -Wait
        if ($proc.ExitCode -ne 0 -or -not (Select-String -Path "$LogDir\run_windows.log" -Pattern "SMOKE OK" -Quiet)) {
            Fail "Windows-Build startet nicht sauber (Exit $($proc.ExitCode))"
        }
        Test-LogClean "$LogDir\run_windows_err.log" "Windows-Build-Lauf"
    } else {
        Fail "Windows-Exe fehlt"
    }
}

Write-Host ""
if ($Failed.Count -eq 0) {
    Write-Host "run_all_checks: ALLES GRÜN" -ForegroundColor Green
    exit 0
}
Write-Host "run_all_checks: $($Failed.Count) Schritt(e) fehlgeschlagen:" -ForegroundColor Red
$Failed | ForEach-Object { Write-Host "  - $_" }
exit 1
