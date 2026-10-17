// Fable 2026-10-17: SVG -> PNG with headless Chromium (ImageMagick here drops SVG strokes). node fable_shoot.mjs a.svg b.svg ...
import { chromium } from 'playwright'; import fs from 'node:fs'; import path from 'node:path';
const b = await chromium.launch();
for (const f of process.argv.slice(2)) {
  const svg = fs.readFileSync(f, 'utf8'); const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/); const w = Math.ceil(+m[1]), h = Math.ceil(+m[2]);
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1.5 });
  await p.setContent(`<html><body style="margin:0">${svg}</body></html>`); await p.screenshot({ path: f.replace(/\.svg$/, '.png') }); await p.close(); console.log(f);
}
await b.close();
