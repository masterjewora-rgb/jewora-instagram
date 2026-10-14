"""Generate original background music tracks (no copyright) into music/. Usage: python3 make_music.py"""
import os
import numpy as np
from scipy.io import wavfile

SR = 44100
HERE = os.path.dirname(os.path.abspath(__file__))


def note(midi): return 440.0 * 2 ** ((midi - 69) / 12)


def env(n, a, d):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
    return e


def pluck(f, dur, d=0.6, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum((bright ** (h - 1)) / h * np.sin(2 * np.pi * f * h * t) for h in range(1, 6))
    return s * env(n, 0.005, d)


def pad(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for f in freqs:
        for det in (-0.25, 0.0, 0.25):
            s += np.sin(2 * np.pi * (f + det) * t + det)
    a = np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 0.6)
    return s * a / (len(freqs) * 3)


def kick(dur=0.35):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 110 * np.exp(-t * 18) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def shaker(dur=0.06, rng=np.random.default_rng(1)):
    n = int(dur * SR)
    x = rng.standard_normal(n); x = np.diff(np.concatenate([[0], x]))  # brighter noise
    return x * np.exp(-np.arange(n) / SR * 60)


def add(buf, sig, at, gain):
    i = int(at * SR); j = min(len(buf), i + len(sig))
    if i < len(buf): buf[i:j] += sig[: j - i] * gain


def track(name, root, prog, bpm, seconds=24, arp=(0, 7, 12, 16, 12, 7), seed=0):
    beat = 60 / bpm; bar = beat * 4
    buf = np.zeros(int(seconds * SR) + SR)
    rng = np.random.default_rng(seed)
    t, k = 0.0, 0
    while t < seconds:
        chord = prog[k % len(prog)]
        tones = [root + chord + x for x in (0, 4 if chord not in (9, 2, 4) else 3, 7)]
        add(buf, pad([note(m - 12) for m in tones], bar + 0.6), t, 0.22)
        add(buf, pluck(note(root + chord - 24), bar, d=1.2, bright=0.3), t, 0.35)            # bass
        for s in range(8):                                                               # arpeggio 8ths
            iv = arp[s % len(arp)]
            m = root + chord + iv + (0 if chord not in (9, 2, 4) or iv not in (4, 16) else -1)
            add(buf, pluck(note(m), beat, d=0.35, bright=0.55), t + s * beat / 2, 0.16 * (0.85 + 0.3 * rng.random()))
        if k >= 1:
            for b in (0, 2): add(buf, kick(), t + b * beat, 0.5)
            for s in range(8): add(buf, shaker(), t + s * beat / 2, 0.05 if s % 2 else 0.03)
        t += bar; k += 1
    # simple reverb-ish smear
    out = buf.copy()
    for dly, g in ((0.11, 0.25), (0.23, 0.15), (0.37, 0.08)):
        d = int(dly * SR); out[d:] += buf[:-d] * g
    out = out[: int(seconds * SR)]
    out /= np.max(np.abs(out)) * 1.15
    st = np.stack([out, np.roll(out, 300)], axis=1)
    os.makedirs(os.path.join(HERE, "music"), exist_ok=True)
    wavfile.write(os.path.join(HERE, "music", name), SR, (st * 32767).astype(np.int16))


if __name__ == "__main__":
    track("jewora_glow.wav", 60, [9, 5, 0, 7], 96, seed=1)        # Am F C G — warm, festive pop
    track("jewora_royal.wav", 62, [0, 7, 9, 5], 84, seed=2)       # D A Bm G — calm, elegant
    track("jewora_sparkle.wav", 64, [0, 9, 5, 7], 108, arp=(0, 12, 7, 16, 7, 12), seed=3)  # E C#m A B — upbeat
    print(sorted(os.listdir(os.path.join(HERE, "music"))))
