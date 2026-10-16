// node shoot_full.mjs -> /tmp/full/*.png
import { chromium } from 'playwright'; import fs from 'node:fs'; fs.mkdirSync('/tmp/full', { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
const ONLY = process.argv[2]; // 'gap': the gap-member shots only
const SHOTS = [['whole', 'mode=cutaway&h=5.9'], ['seam', 'mode=cutaway&h=2.9'], ['inner', 'mode=cutaway&h=1.9'], ['gap-whole', 'mode=cutaway&h=5.9'], ['gap-seam', 'mode=cutaway&h=2.9'], ['gap-seam-nox', 'mode=cutaway&h=2.9&nox=1'], ['gap-clean-whole', 'mode=cutaway&h=2.8&nox=1&clean=1'], ['gap-clean-seam', 'mode=cutaway&h=1.6&nox=1&clean=1']];
for (const [name, qs] of SHOTS.filter(([n]) => !ONLY || n.startsWith(ONLY))) {
  const p = await b.newPage({ viewport: { width: 1400, height: 1400 } });
  await p.goto(`http://localhost:8001/progenitors/render_full.html?${qs}&px=1400`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 300000 });
  await p.screenshot({ path: `/tmp/full/${name}.png` }); await p.close(); console.log(name); }
await b.close();
