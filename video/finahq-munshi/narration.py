"""Builds the soundtrack for the FINAHQ + Munshi video.

  python3 narration.py --models <dir with kokoro-v1.0.onnx + voices-v1.0.bin> [--voice af_heart]

Writes audio/voice.wav (narration, each line placed at its scene start),
audio/music.wav (original ambient bed, synthesised here, royalty-free) and
audio/mix.wav (music ducked well under the voice). render.js muxes mix.wav.

`say` is what the TTS engine reads: phonetic spellings keep names right.
`text` is the clean line, also written to narration.txt for captions.
"""
import argparse, json, os
import numpy as np
import soundfile as sf

SR = 24000
TOTAL = 120.0

# (scene, start s, duration s, caption text, spoken text)
# Spoken text: "Finna H Q" = FIN-ah, H, Q (as in "finance"); "Moonshee" = Munshi.
LINES = [
    ("intro", 0, 7, "This is FINAHQ, with Munshi. One platform that runs your entire close.",
     "This is Finna H Q, with Moonshee. One platform that runs your entire close."),
    ("problem", 7, 6, "Fifty entities. Five different ledgers. And a deadline that doesn't move.",
     "Fifty entities. Five different ledgers. And a deadline that doesn't move."),
    ("pulls", 13, 10, "Every night, FINAHQ pulls trial balances, ledgers and subledgers from SAP, Oracle, NetSuite, Dynamics and QuickBooks.",
     "Every night, Finna H Q pulls trial balances, ledgers and subledgers from S A P, Oracle, NetSuite, Dynamics, and QuickBooks."),
    ("ico", 23, 11, "Munshi, your AI finance agent, reconciles intercompany balances, explains every difference, and drafts the eliminations for your approval.",
     "Moonshee, your AI finance agent, reconciles intercompany balances, explains every difference, and drafts the eliminations for your approval."),
    ("lease", 34, 11, "Leases are covered too. Under IFRS 16 or US GAAP, FINAHQ builds every schedule, posts the journals, and feeds the disclosures.",
     "Leases are covered too. Under I F R S sixteen, or U S gap, Finna H Q builds every schedule, posts the journals, and feeds the disclosures."),
    ("multi", 45, 10, "Then it consolidates every level, from entity to region to group, and you can drill from any number straight to the account behind it.",
     "Then it consolidates every level, from entity, to region, to group. And you can drill from any number straight to the account behind it."),
    ("dims", 55, 7, "Slice any figure by location, cost centre, product or segment.",
     "Slice any figure by location, cost center, product, or segment."),
    ("std", 62, 8, "Standard statements and board packs are ready from day one.",
     "Standard statements and board packs are ready from day one."),
    ("custom", 70, 11, "And with custom templates, you get your complete financial statements, every note and every disclosure, in exactly the format your auditors expect.",
     "And with custom templates, you get your complete financial statements, every note and every disclosure, in exactly the format your auditors expect."),
    ("wp", 81, 10, "Munshi also prepares your audit working papers, each one tied back to the trial balance.",
     "Moonshee also prepares your audit working papers, each one tied back to the trial balance."),
    ("mcp", 91, 10, "And through the FINAHQ connector for Claude, your team can just ask, and get answers computed from your own books.",
     "And through the Finna H Q connector for Claude, your team can just ask, and get answers computed from your own books."),
    ("sec", 101, 7, "Run it in your own cloud if you prefer. SOC 2 is expected by March 2027.",
     "Run it in your own cloud, if you prefer. Sock two is expected by March, twenty twenty-seven."),
    ("recap", 108, 7, "Pull, reconcile, consolidate, report and audit. All in one platform.",
     "Pull, reconcile, consolidate, report, and audit. All in one platform."),
    ("cta", 115, 5, "FINAHQ and Munshi. Book a demo today.",
     "Finna H Q, and Moonshee. Book a demo today."),
]
LEAD = 0.35    # voice starts this long after the cut
TAIL = 0.35    # and must finish this long before the next cut
GAP = 0.30     # breath between sentences
BASE_SPEED = 0.95


def trim(x, thr=0.004):
    idx = np.where(np.abs(x) > thr)[0]
    return x[idx[0]: idx[-1] + 1] if len(idx) else x


def sentences(t):
    import re
    return [p.strip() for p in re.split(r'(?<=[.?!])\s+', t) if p.strip()]


def voice_track(models, voice):
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(models, "kokoro-v1.0.onnx"), os.path.join(models, "voices-v1.0.bin"))
    out = np.zeros(int(SR * TOTAL), dtype=np.float32)
    report = []
    for scene, start, dur, text, say in LINES:
        avail = dur - LEAD - TAIL
        speed = BASE_SPEED
        for _ in range(6):
            parts = []
            for sent in sentences(say):
                a, sr = k.create(sent, voice=voice, speed=speed, lang="en-us")
                assert sr == SR
                parts += [trim(a.astype(np.float32)), np.zeros(int(GAP * SR), np.float32)]
            a = np.concatenate(parts[:-1])
            if len(a) / SR <= avail or speed >= 1.1:
                break
            speed = min(1.1, speed * (len(a) / SR) / avail + 0.01)
        i = int((start + LEAD) * SR)
        out[i: i + len(a)] += a[: len(out) - i]
        report.append({"scene": scene, "start": start, "spoken_s": round(len(a) / SR, 2), "available_s": round(avail, 2),
                       "speed": round(speed, 3), "fits": len(a) / SR <= avail})
    return out, report


def music_track(seed=7):
    """Slow ambient pad + soft bell arpeggio. Original, generated here."""
    rng = np.random.default_rng(seed)
    t = np.arange(int(SR * TOTAL)) / SR
    out = np.zeros_like(t)
    midi = lambda m: 440.0 * 2 ** ((m - 69) / 12)
    # I - vi - IV - V in D major, 8 s per chord, voiced as maj7/m7 colours
    chords = [[50, 57, 61, 64, 66], [47, 54, 57, 62, 64], [43, 50, 54, 57, 62], [45, 52, 57, 61, 64]]
    bar = 8.0
    n = int(TOTAL / bar) + 1
    for b in range(n):
        ch = chords[b % 4]
        s0, s1 = b * bar, min(TOTAL, (b + 1) * bar + 2.5)
        seg = (t >= s0) & (t < s1)
        tt = t[seg] - s0
        env = np.minimum(1, tt / 2.5) * np.minimum(1, np.maximum(0, (s1 - s0 - tt)) / 2.5)
        for j, m in enumerate(ch):
            f = midi(m)
            det = [0.997, 1.0, 1.003]
            for d in det:
                ph = rng.uniform(0, 2 * np.pi)
                out[seg] += env * (0.6 * np.sin(2 * np.pi * f * d * tt + ph) + 0.12 * np.sin(4 * np.pi * f * d * tt + ph)) / (len(ch) * len(det))
    # bell arpeggio, 8th notes at 96 bpm, sparse and soft
    step = 60 / 96 / 2
    k = 0
    tt0 = 0.0
    while tt0 < TOTAL - 1:
        b = int(tt0 // bar)
        ch = chords[b % 4]
        pattern = [2, 3, 4, 3, 2, 4, 3, 1]
        m = ch[pattern[k % 8]] + 12
        if rng.random() < 0.8:
            seg = (t >= tt0) & (t < tt0 + 1.6)
            tt = t[seg] - tt0
            f = midi(m)
            out[seg] += 0.11 * np.exp(-tt * 3.2) * (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2.01 * f * tt))
        tt0 += step
        k += 1
    # gentle low-pass + simple stereo-free reverb tail (comb)
    from numpy.fft import rfft, irfft
    F = rfft(out)
    freqs = np.fft.rfftfreq(len(out), 1 / SR)
    F *= 1 / np.sqrt(1 + (freqs / 3500) ** 4)
    out = irfft(F, len(out))
    for d, g in [(0.113, 0.32), (0.241, 0.22), (0.377, 0.15)]:
        D = int(d * SR)
        out[D:] += g * out[:-D]
    # fade in/out
    fade = np.minimum(1, t / 2.0) * np.minimum(1, (TOTAL - t) / 3.0)
    out *= fade
    out /= np.max(np.abs(out)) + 1e-9
    return out.astype(np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", required=True)
    ap.add_argument("--voice", default="af_heart")
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    adir = os.path.join(here, "audio")
    os.makedirs(adir, exist_ok=True)

    voice, report = voice_track(a.models, a.voice)
    music = music_track()
    sf.write(os.path.join(adir, "voice.wav"), voice, SR)
    sf.write(os.path.join(adir, "music.wav"), music, SR)
    with open(os.path.join(here, "narration.txt"), "w") as f:
        for scene, start, dur, text, _ in LINES:
            f.write(f"[{int(start)//60}:{int(start)%60:02d}] {text}\n")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
