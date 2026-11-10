// Screenshots of cutaways.html at 2x: SHOTS = JSON list of [name, query]; writes cut-<name>.png to $OUT.
import { chromium } from 'playwright';
const OUT = process.env.OUT ?? '/tmp', BASE = process.env.BASE ?? 'http://127.0.0.1:8020';
const SHOTS = JSON.parse(process.env.SHOTS ?? '[["heart","shot=heart&az=12&el=10"],["vacuus","shot=vacuus&az=-36&el=26"]]');
const b = await chromium.launch({ args: ['--use-gl=angle', '--enable-webgl', '--ignore-gpu-blocklist'] });
let ok = 0;
for (const [name, query] of SHOTS) {
  const p = await b.newPage({ viewport: { width: 1200, height: 1200 }, deviceScaleFactor: 2 });
  const errs = []; p.on('pageerror', (e) => errs.push(String(e))); p.on('console', (m) => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto(`${BASE}/cutaways.html?${query}`);
  await p.waitForFunction(() => window.__done === true, null, { timeout: 60000 }).catch(() => errs.push('not done'));
  await p.waitForTimeout(400); await p.screenshot({ path: `${OUT}/cut-${name}.png` });
  console.log(name, errs.length ? 'ERRORS ' + errs.join(' | ') : 'ok'); if (!errs.length) ok++;
}
await b.close(); console.log(ok === SHOTS.length ? 'FINAL ok' : 'FINAL FAIL');
