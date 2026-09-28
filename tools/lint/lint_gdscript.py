"""Führt den GDScript-Warnungs-Scanner aus und schlägt bei jeder Warnung fehl.

Aufruf: python tools/lint/lint_gdscript.py [GODOT_BINARY]
Addons (gdUnit4) werden nicht gescannt; ihre Warnungen sind nicht unsere.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def godot_binary() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1]
    if os.environ.get("GODOT_BIN"):
        return os.environ["GODOT_BIN"]
    path_file = ROOT / "tools" / "godot_path.txt"
    return path_file.read_text(encoding="utf-8").strip() if path_file.exists() else "godot"


def main() -> int:
    cmd = [godot_binary(), "--headless", "--path", str(ROOT), "-d", "-s", "res://tools/lint/gdscript_lint.gd"]
    proc = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=300)
    output = ANSI.sub("", proc.stdout + proc.stderr)
    current = None
    problems: list[str] = []
    done = False
    for line in output.splitlines():
        if line.startswith("LINT_FILE "):
            current = line.split(" ", 1)[1]
        elif line.startswith("LINT_DONE"):
            done = True
            current = None
        elif current and (line.startswith("ERROR:") or line.startswith("WARNING:") or "SCRIPT ERROR" in line):
            problems.append(f"{current}: {line.strip()}")
    for p in problems:
        print("WARNUNG", p)
    if not done:
        print("FEHLER: Scanner lief nicht bis zum Ende")
        print(output[-2000:])
        return 1
    print(f"lint_gdscript: {len(problems)} Warnung(en)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
