// DICTO 2026-10-19 #36 cover renders (dicto-node). usage: node shoot_cover.mjs <base url of scripts/> <out dir> <name=query> ...
import { chromium } from 'playwright'; import fs from 'node:fs';
const [BASE, OUT, ...jobs] = process.argv.slice(2); fs.mkdirSync(OUT, { recursive: true });
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] });
for (const j of jobs) {
  const i = j.indexOf('='), n = j.slice(0, i), qs = j.slice(i + 1); const px = +(new URLSearchParams(qs).get('px') || 1200);
  const p = await b.newPage({ viewport: { width: px, height: px } });
  await p.goto(`${BASE}/render_cover.html?${qs}`); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 180000 });
  await p.screenshot({ path: `${OUT}/${n}.png` }); await p.close(); console.log(n);
}
await b.close();
