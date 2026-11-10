// Screenshots of heroes.html (served from the app root) at 3x: hero-fill.png and hero-close.png in $OUT (default /tmp).
import { chromium } from 'playwright';
const OUT = process.env.OUT ?? '/tmp', BASE = process.env.BASE ?? 'http://127.0.0.1:8018';
const b = await chromium.launch({ args: ['--use-gl=angle', '--enable-webgl', '--ignore-gpu-blocklist'] });
let ok = 0;
for (const [shot, w, h] of (process.env.SHOTS ?? 'fill,close,apart').split(',').map((k) => [k, k === 'fill' ? 1600 : 1200, k === 'fill' ? 1000 : 1200])) {
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
  const errs = []; p.on('pageerror', (e) => errs.push(String(e))); p.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto(`${BASE}/heroes.html?shot=${shot}`);
  await p.waitForFunction(() => window.__heroDone === true, null, { timeout: 60000 }).catch(() => {});
  await p.waitForTimeout(500);
  await p.screenshot({ path: `${OUT}/hero-${shot}.png` });
  console.log(shot, errs.length ? 'ERRORS ' + errs.join(' | ') : 'ok'); if (!errs.length) ok++;
}
await b.close();
const want = (process.env.SHOTS ?? 'fill,close,apart').split(',').length;
console.log(ok === want ? 'FINAL ok' : 'FINAL FAIL');
