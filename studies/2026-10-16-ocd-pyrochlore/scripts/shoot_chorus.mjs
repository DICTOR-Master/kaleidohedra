// Stills of the spatial chorus, and the animation frames + MP4 (bundled ffmpeg in ~/plotenv).
import { chromium } from 'playwright'; import { execFileSync } from 'node:child_process'; import fs from 'node:fs';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 1000 } });
for (const s of ['top', 'tilt', 'cut']) { await p.goto(`http://localhost:8001/ocdnet/render_chorus.html?space#${s}`); await p.reload(); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 120000 }); await p.screenshot({ path: `/tmp/chorus-space-${s}.png` }); }
const dir = '/tmp/chorus-anim'; fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir);
await p.goto('http://localhost:8001/ocdnet/render_chorus.html?anim'); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 120000 });
const n = 240; for (let i = 0; i < n; i++) { await p.evaluate((t) => window.frame(t), i / n); await p.screenshot({ path: `${dir}/f${String(i).padStart(4, '0')}.png` }); }
for (const k of [0, 1, 2, 3, 4]) fs.copyFileSync(`${dir}/f${String(k * 48 + 10).padStart(4, '0')}.png`, `/tmp/chorus-voice-${k + 1}.png`);
await b.close();
const ff = execFileSync(process.env.HOME + '/plotenv/bin/python', ['-c', 'import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())']).toString().trim();
execFileSync(ff, ['-y', '-loglevel', 'error', '-framerate', '24', '-i', `${dir}/f%04d.png`, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '/tmp/dicto-frog-chorus.mp4']);
console.log('done');
