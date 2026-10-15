import { chromium } from 'playwright';
const b = await chromium.launch({ args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader'] }); const p = await b.newPage({ viewport: { width: 1000, height: 1000 } });
for (const w of ['ends', 'middle']) for (const s of ['whole', 'cut']) {
  await p.goto(`http://localhost:8001/render_toggle.html?${w}#${s}`); await p.reload(); await p.waitForFunction(() => document.title === 'ready', null, { timeout: 60000 });
  await p.screenshot({ path: `/tmp/toggle-${w}-${s}.png` }); console.log(w, s);
}
await b.close();
