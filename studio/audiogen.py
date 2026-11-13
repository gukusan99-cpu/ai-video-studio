"""Tự tổng hợp nhạc nền + hiệu ứng âm thanh bằng code (không bản quyền, miễn phí).

Nhạc: thang ngũ cung (C D E G A – màu sắc dân gian Việt), pad êm + tiếng gảy kiểu đàn tranh + trống trầm.
SFX: crash (gỗ vỡ + nước), whoosh (chuyển cảnh), splash, chime (đồng hồ thời gian).
"""
from __future__ import annotations

import numpy as np

SR = 44100
PENTA = [0, 2, 4, 7, 9]


def _note(semi: float, base: float = 261.63) -> float:
    return base * 2 ** (semi / 12)


def _env(n: int, a: float, r: float) -> np.ndarray:
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / r)


def pluck(freq: float, dur: float = 1.4) -> np.ndarray:
    """Karplus–Strong – tiếng dây gảy giống đàn tranh."""
    n = int(dur * SR)
    p = int(SR / freq)
    buf = np.random.default_rng(int(freq)).uniform(-1, 1, p)
    out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.994
    return out * _env(n, 0.002, 0.9)


def pad(freqs: list[float], dur: float) -> np.ndarray:
    t = np.arange(int(dur * SR)) / SR
    s = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.003 * t) for f in freqs)
    fade = np.minimum(1, np.minimum(t / 1.2, (dur - t) / 1.2))
    return s / len(freqs) * fade * 0.5


def drum(dur: float = 0.6) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 55 + 70 * np.exp(-t * 18)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)


def music(duration: float, mood: str = "adventure", seed: int = 7) -> np.ndarray:
    rng = np.random.default_rng(seed)
    bpm = 96 if mood == "adventure" else 78
    beat = 60 / bpm
    n = int((duration + 2) * SR)
    out = np.zeros(n)
    chords = [[0, 7, 16], [9, 16, 21], [2, 9, 14], [7, 14, 19]]  # C – Am – Dm(sus) – G (ngũ cung)
    bar = beat * 4
    k = 0
    t = 0.0
    while t < duration + 1:
        ch = [_note(c - 12) for c in chords[k % 4]]
        seg = pad(ch, bar * 1.05)
        s0 = int(t * SR)
        out[s0:s0 + len(seg)] += seg[: n - s0] * 0.35
        for b in range(4):  # trống trầm phách 1 & 3, nhẹ phách 4
            if b in (0, 2) or (b == 3 and k % 2):
                d = drum()
                p0 = int((t + b * beat) * SR)
                out[p0:p0 + len(d)] += d[: max(0, n - p0)] * (0.5 if b != 3 else 0.25)
        for step in range(8):  # giai điệu gảy ngũ cung, nốt 8
            if rng.random() < 0.55:
                semi = 12 + PENTA[rng.integers(0, 5)] + 12 * (rng.random() < 0.25)
                pl = pluck(_note(semi), 1.2)
                p0 = int((t + step * beat / 2) * SR)
                out[p0:p0 + len(pl)] += pl[: max(0, n - p0)] * 0.28
        t += bar
        k += 1
    out = out[: int(duration * SR)]
    fade = int(1.5 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    return (out / (np.abs(out).max() + 1e-9) * 0.8).astype(np.float32)


def sfx(kind: str) -> np.ndarray:
    rng = np.random.default_rng(len(kind))
    if kind == "crash":  # gỗ gãy + tiếng ùm
        n = int(1.4 * SR)
        t = np.arange(n) / SR
        noise = rng.uniform(-1, 1, n)
        crack = noise * np.exp(-t * 14)
        crack = np.convolve(crack, np.ones(6) / 6, mode="same")
        boom = np.sin(2 * np.pi * np.cumsum(45 + 60 * np.exp(-t * 9)) / SR) * np.exp(-t * 3.5)
        splash = np.convolve(noise, np.ones(30) / 30, mode="same") * np.exp(-((t - .25) ** 2) / .05) * 2
        s = crack * .8 + boom + splash * .6
    elif kind == "whoosh":
        n = int(0.6 * SR)
        t = np.arange(n) / SR
        noise = rng.uniform(-1, 1, n)
        k = np.convolve(noise, np.ones(20) / 20, mode="same")
        s = k * np.sin(np.pi * t / t[-1]) ** 2 * 3
    elif kind == "splash":
        n = int(0.9 * SR)
        t = np.arange(n) / SR
        noise = rng.uniform(-1, 1, n)
        s = np.convolve(noise, np.ones(14) / 14, mode="same") * np.exp(-t * 5) * 2.5
    elif kind == "chime":
        n = int(1.6 * SR)
        t = np.arange(n) / SR
        s = sum(np.sin(2 * np.pi * f * t) * np.exp(-t * (2 + i)) for i, f in enumerate([1318.5, 1975.5, 2637]))
    else:
        raise ValueError(kind)
    return (s / (np.abs(s).max() + 1e-9) * 0.9).astype(np.float32)
