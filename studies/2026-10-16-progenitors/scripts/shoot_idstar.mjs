// node shoot_idstar.mjs -> /tmp/idstar/*.png
import { chromium } from 'playwright'; import fs from 'node:fs'; fs.mkdirSync('/tmp/idstar', { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
for (const m of ['star', 'inX', 'interlock']) { const p = await b.newPage({ viewport: { width: 1200, height: 1200 } });
  await p.goto(`http://localhost:8001/progenitors/render_idstar.html?mode=${m}&px=1200`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 300000 });
  await p.screenshot({ path: `/tmp/idstar/${m}.png` }); await p.close(); console.log(m); }
await b.close();
