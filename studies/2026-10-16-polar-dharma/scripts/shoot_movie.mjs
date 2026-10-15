// Frames for the two loops, then an MP4 each (bundled ffmpeg in ~/plotenv). Usage: node shoot_movie.mjs <toggle|zoom> <frames>
import { chromium } from 'playwright'; import { execFileSync } from 'node:child_process'; import fs from 'node:fs';
const [mode, n] = [process.argv[2], +process.argv[3]], dir = `/tmp/movie-${mode}`; fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir);
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 960, height: 960 } });
await p.goto(`http://localhost:8001/render_movie.html?${mode}`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 180000 });
for (let i = 0; i < n; i++) { await p.evaluate((t) => window.frame(t), i / n); await p.screenshot({ path: `${dir}/f${String(i).padStart(4, '0')}.png` }); if (i % 24 === 0) console.log(mode, i); }
await b.close();
const ff = execFileSync(process.env.HOME + '/plotenv/bin/python', ['-c', 'import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())']).toString().trim();
execFileSync(ff, ['-y', '-loglevel', 'error', '-framerate', '24', '-i', `${dir}/f%04d.png`, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', `/tmp/dharma-${mode}.mp4`]);
console.log('done', `/tmp/dharma-${mode}.mp4`);
