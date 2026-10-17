// node shoot_cleo.mjs -> /tmp/cleo/*.png (render_cleo.html + cleo-build.json from ~/cleo-hold/progenitors on :8001)
import { chromium } from 'playwright'; import fs from 'node:fs'; fs.mkdirSync('/tmp/cleo', { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
async function shot(qs, name, px = 1200) { const p = await b.newPage({ viewport: { width: px, height: px } });
  await p.goto(`http://localhost:8001/progenitors/render_cleo.html?${qs}&px=${px}`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 300000 });
  await p.screenshot({ path: `/tmp/cleo/${name}.png` }); await p.close(); console.log(name); }
for (const m of (process.argv[2] ? process.argv[2].split(',') : ['exploded', 'assembled', 'cycle'])) await shot(`mode=${m}`, m);
if (!process.argv[2]) for (const k of ['I', 'star', 'Dp', 'ID', 'O', 'rTI', 'TI', 'H', 'hull', 'RT', 'M', 'I·φ³']) await shot(`mode=one&k=${encodeURIComponent(k)}`, `one-${k.replace('·φ³', 'p3')}`, 500);
await b.close();
