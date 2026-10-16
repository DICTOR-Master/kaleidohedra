// node shoot_nine.mjs -> /tmp/nine/*.png (render_nine.html + nine-render.json from ~/cleo-hold/progenitors on :8001)
import { chromium } from 'playwright'; import fs from 'node:fs'; fs.mkdirSync('/tmp/nine', { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
async function shot(qs, name, px = 1200) { const p = await b.newPage({ viewport: { width: px, height: px } });
  await p.goto(`http://localhost:8001/progenitors/render_nine.html?${qs}&px=${px}`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 300000 });
  await p.screenshot({ path: `/tmp/nine/${name}.png` }); await p.close(); console.log(name); }
for (const v of ['nested', 'compound']) { await shot(`ver=${v}&mode=cutaway&zoom=1`, `${v}-cutaway`); await shot(`ver=${v}&mode=slice&zoom=1`, `${v}-slice`); }
for (const k of ['I', 'ID', 'O', 'rTI', 'TI', 'H', 'hull', 'RT', 'I·φ³']) await shot(`ver=nested&mode=one&k=${encodeURIComponent(k)}&h=2.6`, `one-${k.replace('·φ³', 'p3')}`, 600);
await shot(`ver=compound&mode=one&k=O&h=2.6`, 'one-O94', 600);


await b.close();
