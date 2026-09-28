"""M1-Soundeffekte, vollständig synthetisch (siehe audio/synth.py).

Organische Laute (Hund, Pferd) sind bewusst weich und stilisiert; sie gelten
als Platzhalter, bis CC0-Aufnahmen oder bessere Synthese folgen (KNOWN_ISSUES).
"""
from __future__ import annotations

import numpy as np

from audio import synth as s
from sl_common import ASSETS, GeneratedAsset

GEN = "tools/pipeline/generators/gen_m1_sfx.py"
OUT = ASSETS / "audio/sfx"

# Pentatonik in C: klingt immer freundlich
C5 = 523.25
PENTA = [1.0, 9 / 8, 5 / 4, 3 / 2, 5 / 3, 2.0, 9 / 4, 5 / 2]


def bell(freq: float, dur: float, bright: float = 0.35) -> np.ndarray:
    e = s.env(dur, 0.003, dur * 0.28)
    x = s.sine(freq, dur) + bright * s.sine(freq * 2.01, dur) * s.env(dur, 0.002, dur * 0.12) \
        + 0.15 * s.sine(freq * 3.02, dur) * s.env(dur, 0.002, dur * 0.06)
    return x * e


def transform(up: bool) -> np.ndarray:
    """Verwandlung: Glitzer-Arpeggio + weiches Pling.
    Zur Fee (kleiner) endet es hoch, zum Menschen tief."""
    steps = [0, 1, 2, 3, 4, 5, 6, 7] if up else [7, 6, 5, 4, 3, 2, 1, 0]
    base = C5 if up else C5 / 2
    parts = []
    for i, k in enumerate(steps):
        parts.append((bell(base * PENTA[k] * 2, 0.18, 0.2) * 0.35, i * 0.035))
    shimmer = s.bandpass(s.noise(0.45, 7), 5000, 9000) * s.env(0.45, 0.05, 0.12) * 0.25
    parts.append((shimmer, 0.0))
    final = base * (PENTA[7] * 2 if up else PENTA[0] * 2)
    parts.append((bell(final, 0.9, 0.45) * 0.9, 0.3))
    return s.echo(s.mix(*parts), 0.11, 0.25, 3)


def blocked() -> np.ndarray:
    """Kein Platz: gedämpftes 'Boing' mit Wackeln."""
    dur = 0.35
    f = 220 * (1 + 0.08 * np.sin(2 * np.pi * 18 * s.t_axis(dur))) * s.sweep(1.0, 0.8, dur)
    x = s.sine(f, dur) * s.env(dur, 0.005, 0.12)
    thump = s.sine(s.sweep(120, 60, 0.12), 0.12) * s.env(0.12, 0.002, 0.04)
    return s.mix((x, 0), (thump * 0.8, 0))


def footstep(seed: int) -> np.ndarray:
    dur = 0.09
    n = s.lowpass(s.noise(dur, seed), 1400 + seed * 90) * s.env(dur, 0.004, 0.022)
    return n + 0.3 * s.sine(s.sweep(160, 90, dur), dur) * s.env(dur, 0.002, 0.015)


def hoof(seed: int) -> np.ndarray:
    dur = 0.14
    thud = s.sine(s.sweep(120 + seed * 7, 55, dur, 0.6), dur) * s.env(dur, 0.002, 0.045)
    click = s.lowpass(s.noise(dur, 100 + seed), 2200) * s.env(dur, 0.001, 0.012)
    return thud * 0.9 + click * 0.5


def wing_flap() -> np.ndarray:
    dur = 0.16
    am = 0.5 + 0.5 * np.sin(2 * np.pi * 34 * s.t_axis(dur))
    return s.bandpass(s.noise(dur, 21), 1500, 5000) * am * s.env(dur, 0.02, 0.05)


def pet_happy() -> np.ndarray:
    return s.echo(s.mix((bell(C5 * 3 / 2 * 2, 0.4, 0.3), 0), (bell(C5 * 2 * 2, 0.5, 0.3) * 0.8, 0.09)),
                  0.09, 0.2, 2)


def whistle(two_note: bool) -> np.ndarray:
    """Pfiff: Pferd (zweitönig) bzw. Hund rufen (kurzer aufsteigender Ruf)."""
    if two_note:
        d1, d2 = 0.22, 0.34
        f = np.concatenate([s.sweep(1500, 1650, d1), s.sweep(2000, 1750, d2)])
        dur = d1 + d2
    else:
        dur = 0.28
        f = s.sweep(1300, 2100, dur, 0.7)
    vib = 1 + 0.012 * np.sin(2 * np.pi * 6 * s.t_axis(dur))
    x = s.sine(f[: int(dur * s.SR)] * vib, dur)
    breath = s.bandpass(s.noise(dur, 5), 2500, 6000) * 0.06
    e = s.env(dur, 0.03, 10.0, 1.0, 0.06)
    return (x + breath) * e


def dog_bark() -> np.ndarray:
    """Freundliches, weiches 'Wuff' (stilisiert)."""
    dur = 0.2
    f = s.sweep(330, 220, dur, 0.5)
    body = s.lowpass(s.saw(f, dur), 1300) * s.env(dur, 0.006, 0.06)
    breath = s.bandpass(s.noise(dur, 3), 500, 2200) * s.env(dur, 0.002, 0.03) * 0.5
    return s.mix((body + breath, 0), ((body + breath) * 0.55, 0.23))


def horse_snort() -> np.ndarray:
    """Zufriedenes Schnauben: Luftstoß mit flatternden Nüstern."""
    dur = 0.55
    flutter = 0.6 + 0.4 * np.sin(2 * np.pi * 26 * s.t_axis(dur))
    air = s.lowpass(s.noise(dur, 13), s.sweep(1800, 500, dur)) * flutter * s.env(dur, 0.03, 0.18)
    rumble = s.sine(s.sweep(90, 70, dur), dur) * s.env(dur, 0.02, 0.15) * 0.4
    return air + rumble


def gait_up() -> np.ndarray:
    dur = 0.18
    return s.bandpass(s.noise(dur, 17), 600, 3000) * s.env(dur, 0.06, 0.05) * \
        (0.4 + 0.6 * np.linspace(0, 1, int(dur * s.SR)))


def mount() -> np.ndarray:
    dur = 0.25
    cloth = s.bandpass(s.noise(dur, 31), 800, 4000) * s.env(dur, 0.01, 0.06) * 0.6
    thump = s.sine(s.sweep(140, 70, 0.15), 0.15) * s.env(0.15, 0.003, 0.05)
    return s.mix((cloth, 0), (thump, 0.08))


def ring_hum() -> np.ndarray:
    """Feenring in der Nähe: kurzes, helles Summen."""
    dur = 0.6
    x = s.sine(C5 * 2, dur) * 0.5 + s.sine(C5 * 3, dur) * 0.3 + s.sine(C5 * 4.01, dur) * 0.2
    return x * s.env(dur, 0.15, 0.2, 0.0, 0.2)


SOUNDS = {
    "transform_to_fairy": (lambda: transform(True), -2.0, "Verwandlung zur Fee (hoch)"),
    "transform_to_human": (lambda: transform(False), -2.0, "Verwandlung zum Menschen (tief)"),
    "transform_blocked": (blocked, -6.0, "Kein Platz zum Verwandeln"),
    "step_grass_1": (lambda: footstep(1), -14.0, "Schritt Gras"),
    "step_grass_2": (lambda: footstep(2), -14.0, "Schritt Gras"),
    "step_grass_3": (lambda: footstep(3), -14.0, "Schritt Gras"),
    "hoof_grass_1": (lambda: hoof(1), -9.0, "Huf Gras"),
    "hoof_grass_2": (lambda: hoof(2), -9.0, "Huf Gras"),
    "hoof_grass_3": (lambda: hoof(3), -9.0, "Huf Gras"),
    "wing_flap": (wing_flap, -16.0, "Flügelschlag Fee"),
    "pet_happy": (pet_happy, -8.0, "Streicheln/Freude"),
    "whistle_horse": (lambda: whistle(True), -8.0, "Pfiff für das Pferd"),
    "call_dog": (lambda: whistle(False), -9.0, "Hund rufen"),
    "dog_bark": (dog_bark, -8.0, "Bellen (Platzhalter, stilisiert)"),
    "horse_snort": (horse_snort, -8.0, "Schnauben (Platzhalter, stilisiert)"),
    "gait_up": (gait_up, -12.0, "Gangart schneller"),
    "mount": (mount, -8.0, "Auf-/Absteigen"),
    "ring_hum": (ring_hum, -12.0, "Feenring summt"),
}


def build() -> list[GeneratedAsset]:
    out: list[GeneratedAsset] = []
    for name, (fn, peak, note) in SOUNDS.items():
        p = s.write_ogg(fn(), OUT / f"{name}.ogg", peak)
        out.append(GeneratedAsset(p, "sfx", GEN, note))
    return out
