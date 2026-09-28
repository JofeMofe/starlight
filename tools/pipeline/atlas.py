"""Packt Einzelframes zu einem Spritesheet (Raster) mit JSON-Metadaten.

Alle Frames einer Animation haben dieselbe Größe; das Sheet ist ein Raster
aus Zeilen (= Animationen/Richtungen) und Spalten (= Frames). Die JSON-Datei
neben dem PNG beschreibt Framegröße, Animationen und Frame-Dauern, damit
Godot-Skripte daraus SpriteFrames bauen können.

Godot-Import: Filter aus, Mipmaps aus, verlustfreie Kompression (siehe
project.godot / .import-Defaults).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

from sl_common import save_png


@dataclass
class Animation:
    name: str
    frames: list[Image.Image]
    # Dauer pro Frame in Millisekunden (bewusstes Timing statt gleich lang)
    durations_ms: list[int] = field(default_factory=list)
    loop: bool = True
    # Zusätzliche Daten pro Animation (z. B. "bob": Körperversatz pro Frame)
    extra: dict = field(default_factory=dict)


def pack(animations: list[Animation], out_png: Path) -> Path:
    if not animations:
        raise ValueError("Keine Animationen übergeben")
    fw, fh = animations[0].frames[0].size
    for anim in animations:
        for i, frame in enumerate(anim.frames):
            if frame.size != (fw, fh):
                raise ValueError(f"{anim.name}[{i}] hat {frame.size}, erwartet {(fw, fh)}")
        if anim.durations_ms and len(anim.durations_ms) != len(anim.frames):
            raise ValueError(f"{anim.name}: Anzahl Dauern != Anzahl Frames")
    cols = max(len(a.frames) for a in animations)
    sheet = Image.new("RGBA", (cols * fw, len(animations) * fh), (0, 0, 0, 0))
    meta: dict = {"frame_size": [fw, fh], "animations": {}}
    for row, anim in enumerate(animations):
        for col, frame in enumerate(anim.frames):
            sheet.paste(frame, (col * fw, row * fh))
        meta["animations"][anim.name] = {
            "row": row,
            "frames": len(anim.frames),
            "durations_ms": anim.durations_ms or [100] * len(anim.frames),
            "loop": anim.loop,
            **anim.extra,
        }
    save_png(sheet, out_png)
    out_png.with_suffix(".json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return out_png
