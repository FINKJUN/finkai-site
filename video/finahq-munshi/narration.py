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

# (scene, start s, duration s, on-screen text, spoken text)
LINES = [
    ("intro", 0, 8, "Meet FINAHQ and Munshi: the end-to-end close platform for multi-entity groups.",
     "Meet Fina H Q, and Moonshee. The end-to-end close platform, for multi-entity groups."),
    ("problem", 8, 7, "Fifty entities. Five ERPs. One deadline. FINAHQ runs the whole close.",
     "Fifty entities. Five E R Ps. One deadline. Fina H Q runs the whole close."),
    ("pulls", 15, 11, "It starts by pulling trial balances, general ledgers and subledgers from every ERP, on schedule, and checking each one against the source.",
     "It starts by pulling trial balances, general ledgers and subledgers from every E R P, on schedule, and checking each one against the source."),
    ("ico", 26, 11, "Munshi, your AI finance agent, reconciles intercompany balances, flags every difference, and drafts the elimination journal for your approval.",
     "Moonshee, your A I finance agent, reconciles intercompany balances, flags every difference, and drafts the elimination journal for your approval."),
    ("multi", 37, 11, "FINAHQ consolidates every level, entity to region to group, and drills from the group number down to a single GL account.",
     "Fina H Q consolidates every level, entity to region to group, and drills from the group number down to a single G L account."),
    ("dims", 48, 9, "Slice any number by location, cost centre, product line, segment, or any dimension you define.",
     "Slice any number by location, cost center, product line, segment, or any dimension you define."),
    ("std", 57, 9, "Standard reports are ready on day one: balance sheet, P&L, cash flow, notes and board packs.",
     "Standard reports are ready on day one. Balance sheet, P and L, cash flow, notes, and board packs."),
    ("custom", 66, 9, "Need your own format? Build a custom report in a minute, then schedule it to run on its own.",
     "Need your own format? Build a custom report in a minute, then schedule it to run on its own."),
    ("wp", 75, 11, "Munshi prepares your audit working papers too: ageing, expected credit loss, journals and the PBC list, all tied to the trial balance.",
     "Moonshee prepares your audit working papers too. Aging, expected credit loss, journals, and the P B C list, all tied to the trial balance."),
    ("mcp", 86, 12, "And with the FINAHQ connector for Claude, your team can simply ask, and get answers computed from your books. Never guessed.",
     "And with the Fina H Q connector for Claude, your team can simply ask, and get answers computed from your books. Never guessed."),
    ("sec", 98, 8, "Self-hostable, with a full audit trail. SOC 2 is in progress, expected March 2027.",
     "Self-hostable, with a full audit trail. Sock two is in progress, expected March, twenty twenty-seven."),
    ("recap", 106, 8, "Pull. Reconcile. Consolidate. Analyse. Report. Audit. One integrated platform.",
     "Pull. Reconcile. Consolidate. Analyze. Report. Audit. One integrated platform."),
    ("cta", 114, 6, "FINAHQ and Munshi. Book your demo at finahq.com.",
     "Fina H Q, and Moonshee. Book your demo at Fina H Q dot com."),
]
LEAD = 0.35   # voice starts this long after the cut
TAIL = 0.35   # and must finish this long before the next cut


def trim(x, thr=0.004):
    idx = np.where(np.abs(x) > thr)[0]
    return x[idx[0]: idx[-1] + 1] if len(idx) else x


def voice_track(models, voice):
    from kokoro_onnx import Kokoro
    k = Kokoro(os.path.join(models, "kokoro-v1.0.onnx"), os.path.join(models, "voices-v1.0.bin"))
    out = np.zeros(int(SR * TOTAL), dtype=np.float32)
    report = []
    for scene, start, dur, text, say in LINES:
        avail = dur - LEAD - TAIL
        speed = 1.0
        for _ in range(6):
            a, sr = k.create(say, voice=voice, speed=speed, lang="en-us")
            assert sr == SR
            a = trim(a.astype(np.float32))
            if len(a) / SR <= avail or speed >= 1.2:
                break
            speed = min(1.2, speed * (len(a) / SR) / avail + 0.01)
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
