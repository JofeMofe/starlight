"""Bringt ein beliebiges Bild auf Starlight-Pixel-Art-Regeln (STYLEGUIDE §Pipeline).

1. Herunterskalieren per Block-Median (oder Nearest) auf die Zielgröße
2. Alpha binär machen (Schwelle 50 %)
3. Deckende Pixel auf die nächste Palettenfarbe quantisieren (ohne Dithering,
   Abstand in gewichtetem RGB, das Grün stärker gewichtet wie das Auge)
4. Einzelne verwaiste Pixel am Rand entfernen ("Kanten säubern")

Das Ergebnis ist nur eine Vorlage: Es muss danach per Pixelkarte von Hand
nachkorrigiert werden. Rohe, generierte Bilder niemals direkt verwenden.

Aufruf: python tools/pipeline/pixelize.py EINGABE.png AUSGABE.png BREITE HOEHE [--nearest]
"""
from __future__ import annotations

import argparse
import sys

import numpy as np
from PIL import Image

from palette import palette_rgb

WEIGHTS = np.array([0.30, 0.59, 0.11]) ** 0.5


def block_median(arr: np.ndarray, width: int, height: int) -> np.ndarray:
    h, w = arr.shape[:2]
    out = np.zeros((height, width, arr.shape[2]), dtype=np.uint8)
    ys = np.linspace(0, h, height + 1).astype(int)
    xs = np.linspace(0, w, width + 1).astype(int)
    for j in range(height):
        for i in range(width):
            block = arr[ys[j]:max(ys[j + 1], ys[j] + 1), xs[i]:max(xs[i + 1], xs[i] + 1)]
            out[j, i] = np.median(block.reshape(-1, arr.shape[2]), axis=0)
    return out


def quantize(arr: np.ndarray) -> np.ndarray:
    pal = np.array(palette_rgb(), dtype=float)
    rgb = arr[..., :3].astype(float)
    diff = (rgb[..., None, :] - pal[None, None, :, :]) * WEIGHTS
    idx = np.argmin((diff ** 2).sum(axis=-1), axis=-1)
    out = arr.copy()
    out[..., :3] = pal[idx].astype(np.uint8)
    return out


def clean_orphans(arr: np.ndarray) -> np.ndarray:
    """Entfernt deckende Pixel ohne deckenden 4er-Nachbarn."""
    alpha = arr[..., 3] > 0
    padded = np.pad(alpha, 1)
    neighbours = padded[:-2, 1:-1] | padded[2:, 1:-1] | padded[1:-1, :-2] | padded[1:-1, 2:]
    out = arr.copy()
    out[alpha & ~neighbours, 3] = 0
    return out


def pixelize(img: Image.Image, width: int, height: int, nearest: bool = False) -> Image.Image:
    arr = np.asarray(img.convert("RGBA"))
    if nearest:
        small = np.asarray(Image.fromarray(arr).resize((width, height), Image.Resampling.NEAREST))
    else:
        small = block_median(arr, width, height)
    small = small.copy()
    small[..., 3] = np.where(small[..., 3] >= 128, 255, 0)
    small = quantize(small)
    small[small[..., 3] == 0] = 0
    return Image.fromarray(clean_orphans(small), "RGBA")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("width", type=int)
    ap.add_argument("height", type=int)
    ap.add_argument("--nearest", action="store_true")
    a = ap.parse_args()
    pixelize(Image.open(a.src), a.width, a.height, a.nearest).save(a.dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
