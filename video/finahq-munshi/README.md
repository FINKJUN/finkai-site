# FINAHQ + Munshi — 2-minute overview video

`finahq-munshi.mp4` is 1920×1080 at 30 fps, exactly 2:00 long. It has a narrator and a quiet music bed underneath, and is aimed at international CFOs. It presents FINAHQ as one integrated close platform: Pull → Reconcile (Munshi ICO) → Consolidate (multilevel) → Analyse (dimensions) → Report (standard + custom) → Audit (Munshi WP) → Ask (FINAHQ MCP for Claude) → Trust (SOC 2 expected March 2027).

All companies ("Happy Inc", "Happy UK Ltd" …) and figures are fictional, and the video says so on screen.

## Files

| File | What it is |
|---|---|
| `index.html` | The video itself, an animated page driven by one timeline. Open it in a browser to preview it with play and scrub controls. |
| `narration.py` | Narration script (13 lines, one per scene), the text-to-speech run (Kokoro, voice `af_heart`) and the synthesised music bed. Writes `audio/` and `narration.txt`. |
| `render.js` | Renders the page frame by frame with Playwright and ffmpeg, then mixes the voice (−16 LUFS) with music that ducks under the voice. |
| `narration.txt` | The voiceover script with timestamps, for captions or a human voice-over. |

## Rebuild

```bash
python3 narration.py --models <folder with kokoro-v1.0.onnx and voices-v1.0.bin>
node render.js
```

`node render.js --stills 20,45.5` saves single frames to `stills/` for checking.

Common edits:
- **Wording on screen:** edit `index.html`.
- **Narration:** edit `LINES` in `narration.py`. The `say` column holds phonetic spellings ("Fina H Q", "Moonshee", "Sock two"). Change those if the pronunciation is wrong.
- **Scene lengths:** the `SC` array in `index.html` and the start times in `narration.py` must match.
