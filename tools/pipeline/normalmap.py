"""Erzeugt pixel-art-taugliche Normal Maps (STYLEGUIDE §Licht).

Statt verrauschter Sobel-Karten auf Farbwerten wird eine Höhe aus der
Silhouette (Abstand zum Rand, optional plus Höhen-Hinweis-Bild) berechnet,
daraus die Normale abgeleitet und auf wenige Stufen quantisiert. So entstehen
flache, klar abgegrenzte Facetten, die zu handgesetzten Pixeln passen.

Aufruf: python tools/pipeline/normalmap.py SPRITE.png AUSGABE.png [--hint HOEHE.png] [--levels 6]
"""
from __future__ import annotations

import argparse
import sys

import numpy as np
from PIL import Image


def distance_to_edge(mask: np.ndarray, max_steps: int = 8) -> np.ndarray:
    """Chebyshev-Abstand jedes deckenden Pixels zum nächsten transparenten."""
    dist = np.zeros(mask.shape, dtype=float)
    current = mask.copy()
    for step in range(1, max_steps + 1):
        padded = np.pad(current, 1)
        eroded = current.copy()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                eroded &= padded[1 + dy:padded.shape[0] - 1 + dy, 1 + dx:padded.shape[1] - 1 + dx]
        dist[current] = step
        current = eroded
        if not current.any():
            break
    return dist


def normal_map(sprite: Image.Image, hint: Image.Image | None = None, levels: int = 6,
               strength: float = 1.0) -> Image.Image:
    arr = np.asarray(sprite.convert("RGBA"))
    mask = arr[..., 3] > 0
    height = distance_to_edge(mask)
    height = np.sqrt(height)  # abgerundete statt pyramidale Wölbung
    if hint is not None:
        height = height + np.asarray(hint.convert("L"), dtype=float) / 255.0 * height.max()
    gy, gx = np.gradient(height)
    nx, ny, nz = -gx * strength, -gy * strength, np.ones_like(height)
    length = np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
    n = np.stack([nx / length, ny / length, nz / length], axis=-1)
    # Quantisieren -> wenige, saubere Facetten
    n = np.round(n * (levels / 2)) / (levels / 2)
    length = np.linalg.norm(n, axis=-1, keepdims=True)
    n = n / np.maximum(length, 1e-6)
    rgb = ((n * 0.5 + 0.5) * 255).astype(np.uint8)
    out = np.zeros(arr.shape, dtype=np.uint8)
    out[..., :3] = rgb
    # Godot erwartet +Y nach unten (OpenGL-Konvention ist Y hoch -> G invertieren)
    out[..., 1] = 255 - out[..., 1]
    out[..., 3] = np.where(mask, 255, 0)
    out[~mask] = (128, 128, 255, 0)
    return Image.fromarray(out, "RGBA")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--hint")
    ap.add_argument("--levels", type=int, default=6)
    a = ap.parse_args()
    hint = Image.open(a.hint) if a.hint else None
    normal_map(Image.open(a.src), hint, a.levels).save(a.dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
