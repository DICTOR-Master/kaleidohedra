// Figures for the DICTO 13-Atom Clusters paper (run on dicto-node: node shots.mjs in papers/thirteens/fig).
import { chromium } from 'playwright';
import http from 'http'; import fs from 'fs'; import path from 'path';
const srv = http.createServer((q, r) => { const f = path.join(process.cwd(), q.url.split('?')[0]); fs.readFile(f, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200); r.end(d); }); }).listen(8098);
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const p = await b.newPage({ viewport: { width: 1000, height: 1000 } });
await p.goto('http://localhost:8098/render.html'); await p.waitForFunction(() => window.ready, null, { timeout: 60000 });
const V = {
  'icosa13-closed': { kind: 'icosa13', view: 'pieces' }, 'icosa13-open': { kind: 'icosa13', view: 'pieces', apart: 0.5 },
  'dodeca13-closed': { kind: 'dodeca13', view: 'pieces' }, 'dodeca13-open': { kind: 'dodeca13', view: 'pieces', apart: 0.5 },
  'bodhi-closed': { kind: 'bodhi', view: 'seed' }, 'bodhi-open': { kind: 'bodhi', view: 'kitB', apart: 0.55, glass: ['copy'] },
  'unity-closed': { kind: 'unity', view: 'venus' }, 'unity-open': { kind: 'unity', view: 'venus', apart: 0.5 },
  'dictostar-closed': { kind: 'dictoStar', view: 'star' }, 'dictostar-open': { kind: 'dictoStar', view: 'star', apart: 0.5 },
  'deshi-closed': { kind: 'deshi', view: 'deshi' }, 'deshi-open': { kind: 'deshi', view: 'deshi', apart: 0.5 },
  'rd13-plain': { kind: 'rd13', view: 'plain' }, 'rd13-rounded': { kind: 'rd13', view: 'rounded' }, 'rd13-rounded-open': { kind: 'rd13', view: 'rounded', apart: 0.45 },
  'rd13-blocks': { kind: 'rd13', view: 'blocks' },
  'hexed-closed': { kind: 'hexed', view: 'cluster' }, 'hexed-open': { kind: 'hexed', view: 'cluster', apart: 0.45 }, 'hexed-blocks': { kind: 'hexed', view: 'blocks' },
  'to13-closed': { kind: 'to13', view: 'cluster' }, 'to13-open': { kind: 'to13', view: 'cluster', apart: 0.45 }, 'to13-blocks': { kind: 'to13', view: 'blocks' },
  'skewedrd13-closed': { kind: 'skewedRd13', view: 'cluster' }, 'skewedrd13-blocks': { kind: 'skewedRd13', view: 'blocks' },
  'bainrd13-closed': { kind: 'bainRd13', view: 'cluster' }, 'bainrd13-blocks': { kind: 'bainRd13', view: 'blocks' },
  'bilinski13-closed': { kind: 'bilinski13', view: 'cluster' }, 'bilinski13-blocks': { kind: 'bilinski13', view: 'blocks' },
  'jewel13-closed': { kind: 'jewel13', view: 'cluster' }, 'jewel13-stellas': { kind: 'jewel13', view: 'withStellas' }, 'jewel13-open': { kind: 'jewel13', view: 'cluster', apart: 0.45 },
};
for (const [n, o] of Object.entries(V)) { await p.evaluate((o) => window.view(o), o); await p.waitForTimeout(500); await p.screenshot({ path: `${n}.png` }); }
await b.close(); srv.close();
