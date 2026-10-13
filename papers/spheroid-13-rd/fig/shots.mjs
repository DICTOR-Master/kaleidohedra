// The graded centres of the DICTO Spheroid-13 RD, at true relative size (one fit for all), from the side and along the axis.
import { chromium } from 'playwright';
import http from 'http'; import fs from 'fs'; import path from 'path';
const srv = http.createServer((q, r) => { const f = path.join(process.cwd(), q.url.split('?')[0]); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200); r.end(d); }); }).listen(8097);
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const p = await b.newPage({ viewport: { width: 520, height: 520 } });
await p.goto('http://localhost:8097/render.html'); await p.waitForFunction(() => window.ready, null, { timeout: 60000 });
for (const t of ['0.08', '0.15', '0.25', '0.35']) {
  await p.evaluate((t) => window.view({ kind: 'centre', view: t, fit: 1.75, dir: [1, 0.35, 0.18] }), t); await p.waitForTimeout(400); await p.screenshot({ path: `centre-${t}.png` });
  await p.evaluate((t) => window.view({ kind: 'centre', view: t, fit: 1.75, dir: [0.3, 1, 0.55] }), t); await p.waitForTimeout(400); await p.screenshot({ path: `centre-${t}-axis.png` });
}
await b.close(); srv.close();
