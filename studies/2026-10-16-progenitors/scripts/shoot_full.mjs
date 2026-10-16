// node shoot_full.mjs -> /tmp/full/*.png
import { chromium } from 'playwright'; import fs from 'node:fs'; fs.mkdirSync('/tmp/full', { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
for (const [name, qs] of [['whole', 'mode=cutaway&h=5.9'], ['seam', 'mode=cutaway&h=2.9'], ['inner', 'mode=cutaway&h=1.9']]) {
  const p = await b.newPage({ viewport: { width: 1400, height: 1400 } });
  await p.goto(`http://localhost:8001/progenitors/render_full.html?${qs}&px=1400`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 300000 });
  await p.screenshot({ path: `/tmp/full/${name}.png` }); await p.close(); console.log(name); }
await b.close();
