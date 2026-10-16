// node shoot_oh.mjs -> /tmp/oh/oh-<show>.png (render_oh.html + oh-render.json served from ~/cleo-hold/progenitors on :8001)
import { chromium } from 'playwright'; import fs from 'node:fs'; fs.mkdirSync('/tmp/oh', { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
for (const s of ['compound', 'core', 'hull', 'both']) {
  const p = await b.newPage({ viewport: { width: 1200, height: 1200 } });
  await p.goto(`http://localhost:8001/progenitors/render_oh.html?show=${s}&px=1200`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 300000 });
  await p.screenshot({ path: `/tmp/oh/oh-${s}.png` }); await p.close(); console.log(s);
}
await b.close();
