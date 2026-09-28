"""Kleiner Synthesizer für Soundeffekte (sfxr-Idee, aber additiv/subtraktiv).

Alles deterministisch (fester Seed), 44,1 kHz mono, Export als OGG Vorbis
über ffmpeg mit Bitexact-Flags (gleiche Eingabe -> gleiche Datei).
"""
from __future__ import annotations

import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np

SR = 44100


def t_axis(dur: float) -> np.ndarray:
    return np.arange(int(dur * SR)) / SR


def sine(freq: np.ndarray | float, dur: float) -> np.ndarray:
    f = np.broadcast_to(np.asarray(freq, dtype=float), (int(dur * SR),))
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def saw(freq: np.ndarray | float, dur: float) -> np.ndarray:
    f = np.broadcast_to(np.asarray(freq, dtype=float), (int(dur * SR),))
    ph = np.cumsum(f) / SR
    return 2.0 * (ph - np.floor(ph + 0.5))


def noise(dur: float, seed: int) -> np.ndarray:
    return np.random.default_rng(seed).uniform(-1, 1, int(dur * SR))


def sweep(f0: float, f1: float, dur: float, curve: float = 1.0) -> np.ndarray:
    x = np.linspace(0, 1, int(dur * SR)) ** curve
    return f0 * (f1 / f0) ** x


def env(dur: float, attack: float, decay: float, sustain: float = 0.0, release: float = 0.0,
        hold: float = 0.0) -> np.ndarray:
    """ADSR mit exponentiellem Abklingen (natürlicher als linear)."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    e = np.ones(n)
    a = t < attack
    e[a] = t[a] / max(attack, 1e-6)
    d = t >= attack + hold
    e[d] = sustain + (1 - sustain) * np.exp(-(t[d] - attack - hold) / max(decay, 1e-6))
    if release > 0:
        r = t > dur - release
        e[r] *= np.linspace(1, 0, r.sum())
    return e


def lowpass(x: np.ndarray, cutoff: np.ndarray | float) -> np.ndarray:
    c = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    alpha = 1 - np.exp(-2 * np.pi * c / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += alpha[i] * (x[i] - acc)
        y[i] = acc
    return y


def highpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    return x - lowpass(x, cutoff)


def bandpass(x: np.ndarray, low: float, high: float) -> np.ndarray:
    return lowpass(highpass(x, low), high)


def echo(x: np.ndarray, delay: float, feedback: float, taps: int = 4) -> np.ndarray:
    d = int(delay * SR)
    y = np.concatenate([x, np.zeros(d * taps)])
    for k in range(1, taps + 1):
        y[d * k:d * k + len(x)] += x * feedback ** k
    return y


def mix(*parts: tuple[np.ndarray, float]) -> np.ndarray:
    n = max(len(p) + int(off * SR) for p, off in parts)
    out = np.zeros(n)
    for p, off in parts:
        s = int(off * SR)
        end = min(n, s + len(p))
        out[s:end] += p[:end - s]
    return out


def pad(x: np.ndarray, total: float) -> np.ndarray:
    n = int(total * SR)
    return np.concatenate([x, np.zeros(max(0, n - len(x)))])[:max(n, len(x))]


def normalize(x: np.ndarray, peak_db: float = -3.0) -> np.ndarray:
    peak = np.max(np.abs(x)) or 1.0
    return x / peak * (10 ** (peak_db / 20))


def fade_edges(x: np.ndarray, ms: float = 4.0) -> np.ndarray:
    n = int(ms / 1000 * SR)
    if len(x) > 2 * n:
        x = x.copy()
        x[:n] *= np.linspace(0, 1, n)
        x[-n:] *= np.linspace(1, 0, n)
    return x


def write_ogg(x: np.ndarray, path: Path, peak_db: float = -3.0) -> Path:
    x = fade_edges(normalize(x, peak_db))
    pcm = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "a.wav"
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes(pcm.tobytes())
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-c:a", "libvorbis",
                        "-q:a", "5", "-fflags", "+bitexact", "-flags:a", "+bitexact",
                        "-map_metadata", "-1", str(path)], check=True)
    return path
