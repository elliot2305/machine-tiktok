// Rendu d'un épisode : Playwright capture chaque image (30 i/s), ffmpeg assemble avec l'audio.
// Usage : node tools/render.js <ep> <audio.mp3|-> <out.mp4> [--fps 30] [--workers 4] [--from s] [--to s] [--stills t1,t2]
const { chromium } = require('playwright');
const http = require('http'); const fs = require('fs'); const path = require('path'); const { spawn } = require('child_process');
const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
const [ep, audio, out] = args;
const FPS = +opt('fps', 30), WORKERS = +opt('workers', 4);
const ROOT = path.resolve(__dirname, '..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.woff2': 'font/woff2', '.woff': 'font/woff' };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(ROOT) || !fs.existsSync(p)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res);
});
(async () => {
  await new Promise(r => server.listen(0, r));
  const url = `http://127.0.0.1:${server.address().port}/scene/patate.html?ep=${ep}&rs=${opt('rs', '0.75')}&aa=${opt('aa', '0')}`;
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const open = async () => { const pg = await browser.newPage({ viewport: { width: 1080, height: 1920 } }); pg.on('pageerror', e => console.error('PAGE', e.message)); pg.on('console', m => { if (m.type() === 'error') console.error('CONSOLE', m.text()); }); await pg.goto(url); await pg.waitForFunction('window.__ready === true', null, { timeout: 120000 }); return pg; };
  const stills = opt('stills');
  if (stills) {
    const pg = await open(); fs.mkdirSync(out, { recursive: true });
    for (const t of stills.split(',').map(Number)) { await pg.evaluate(t => window.__seek(t), t); await pg.screenshot({ path: path.join(out, `ep${ep}_${t.toFixed(1)}.jpg`), type: 'jpeg', quality: 80 }); }
    await browser.close(); server.close(); return;
  }
  const probe = await open();
  const dur = await probe.evaluate('window.__duration'); await probe.close();
  const t0 = +opt('from', 0), t1 = +opt('to', dur);
  const N = Math.round((t1 - t0) * FPS);
  const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), `ep${ep}-`));
  let done = 0; const started = Date.now();
  await Promise.all(Array.from({ length: WORKERS }, async (_, w) => {
    const pg = await open();
    for (let i = w; i < N; i += WORKERS) {
      await pg.evaluate(t => window.__seek(t), t0 + i / FPS);
      await pg.screenshot({ path: path.join(tmp, `f${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 92 });
      if (++done % 150 === 0) console.log(`ep${ep} ${done}/${N} images (${((Date.now() - started) / 1000).toFixed(0)} s)`);
    }
    await pg.close();
  }));
  await browser.close(); server.close();
  const ff = ['-y', '-framerate', String(FPS), '-i', path.join(tmp, 'f%05d.jpg')];
  if (audio && audio !== '-') ff.push('-ss', String(t0), '-t', String(t1 - t0), '-i', audio, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '192k', '-af', `afade=t=out:st=${(t1 - t0 - 0.6).toFixed(2)}:d=0.6`);
  ff.push('-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-shortest', out);
  await new Promise((res, rej) => { const p = spawn('ffmpeg', ff, { stdio: ['ignore', 'ignore', 'inherit'] }); p.on('exit', c => c ? rej(new Error('ffmpeg ' + c)) : res()); });
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log('OK', out);
})().catch(e => { console.error(e); process.exit(1); });
