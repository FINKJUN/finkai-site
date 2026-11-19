// Renders index.html to MP4, frame-accurately.
//   node render.js                      -> finahq-munshi.mp4 (1080p30)
//   node render.js --stills 5,20,40     -> stills/t005.png ... for checking
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const FPS = 30;
const WORKERS = 4;
const here = __dirname;
const url = 'file://' + path.join(here, 'index.html') + '?render=1';
const arg = (k) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };

async function openPage(browser) {
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.evaluate(() => window.ready);
  return page;
}

async function stills(times) {
  const browser = await chromium.launch();
  const page = await openPage(browser);
  const dir = path.join(here, 'stills');
  fs.mkdirSync(dir, { recursive: true });
  for (const t of times) {
    await page.evaluate((t) => window.seek(t), t);
    const f = path.join(dir, 't' + String(t).padStart(5, '0') + '.png');
    await page.screenshot({ path: f });
    console.log(f);
  }
  await browser.close();
}

async function renderChunk(browser, k, from, to, segPath) {
  const page = await openPage(browser);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', '-r', String(FPS), segPath], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = from; f < to; f++) {
    await page.evaluate((t) => window.seek(t), f / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
    if ((f - from) % 300 === 0) console.log(`worker ${k}: frame ${f}/${to}`);
  }
  ff.stdin.end();
  await new Promise((r) => ff.on('close', r));
  await page.close();
}

async function full() {
  const browser = await chromium.launch();
  const probe = await openPage(browser);
  const total = await probe.evaluate(() => window.TOTAL);
  await probe.close();
  const frames = Math.round(total * FPS);
  const per = Math.ceil(frames / WORKERS);
  const segs = [];
  const jobs = [];
  for (let k = 0; k < WORKERS; k++) {
    const from = k * per, to = Math.min(frames, from + per);
    const seg = path.join(here, `.seg${k}.mp4`);
    segs.push(seg);
    jobs.push(renderChunk(browser, k, from, to, seg));
  }
  await Promise.all(jobs);
  await browser.close();
  const list = path.join(here, '.segs.txt');
  fs.writeFileSync(list, segs.map((s) => `file '${s}'`).join('\n'));
  const out = path.join(here, 'finahq-munshi.mp4');
  await new Promise((r, j) => spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', '-movflags', '+faststart', out], { stdio: 'inherit' })
    .on('close', (c) => (c === 0 ? r() : j(new Error('concat failed')))));
  for (const s of [...segs, list]) fs.unlinkSync(s);
  console.log('wrote', out, `(${frames} frames, ${total}s)`);
  await addAudio(out);
}

// Voice levelled to -16 LUFS; music kept low and ducked further whenever the narrator speaks.
async function addAudio(video) {
  const voice = path.join(here, 'audio', 'voice.wav'), music = path.join(here, 'audio', 'music.wav');
  if (!fs.existsSync(voice)) { console.log('no audio/voice.wav — run narration.py first; video left silent'); return; }
  const tmp = video.replace(/\.mp4$/, '.silent.mp4');
  fs.renameSync(video, tmp);
  const fc = '[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000,asplit=2[v][sc];' +
    '[2:a]aresample=48000,volume=0.16[m];' +
    '[m][sc]sidechaincompress=threshold=0.015:ratio=6:attack=30:release=600[md];' +
    '[v][md]amix=inputs=2:normalize=0:duration=first[a]';
  await new Promise((r, j) => spawn('ffmpeg', ['-y', '-loglevel', 'error', '-i', tmp, '-i', voice, '-i', music, '-filter_complex', fc,
    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', video], { stdio: 'inherit' })
    .on('close', (c) => (c === 0 ? r() : j(new Error('audio mux failed')))));
  fs.unlinkSync(tmp);
  console.log('added narration + music to', video);
}

const st = arg('--stills');
(st ? stills(st.split(',').map(Number)) : full()).catch((e) => { console.error(e); process.exit(1); });
