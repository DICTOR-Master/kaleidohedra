// The truncated octahedron 13 seen from above, straight down its window axis: the gold centre's square at the middle (DICTO 2026-10-13).
import { chromium } from 'playwright';
import http from 'http'; import fs from 'fs'; import path from 'path';
const srv = http.createServer((q, r) => { const f = path.join(process.cwd(), q.url.split('?')[0]); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200); r.end(d); }); }).listen(8095);
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const p = await b.newPage({ viewport: { width: 1000, height: 1000 } });
await p.goto('http://localhost:8095/render.html'); await p.waitForFunction(() => window.ready, null, { timeout: 60000 });
await p.evaluate(() => window.view({ kind: 'to13', view: 'cluster', dir: [0.0001, 0.00001, 1] })); await p.waitForTimeout(500); await p.screenshot({ path: 'to13-top.png' });
await b.close(); srv.close();
