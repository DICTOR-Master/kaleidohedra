// Hero shots straight from DICTO's page "The 4D Permutohedron" (DICTO 11 Nov: the pulled-apart Build view, "the 4D vacuus is its form").
// Build view, cells pulled apart; PULLS and camera distances from env. Canvas only, dark theme, 2x. Writes perm4-<name>.png to $OUT.
import { chromium } from 'playwright';
const OUT = process.env.OUT ?? '/tmp', URL = process.env.URL ?? 'http://127.0.0.1:8019/the-4d-permutohedron.html';
const SHOTS = JSON.parse(process.env.SHOTS ?? '[["apart",500,1.0],["close",500,0.62]]');
const b = await chromium.launch({ args: ['--use-gl=angle', '--enable-webgl', '--ignore-gpu-blocklist'] });
const p = await b.newPage({ viewport: { width: 1500, height: 1100 }, deviceScaleFactor: 2, colorScheme: 'dark' });
const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
await p.goto(URL); await p.waitForTimeout(2500);
await p.evaluate(() => { for (const id of ['tag', 'cap']) { const e = document.getElementById(id); if (e) e.style.visibility = 'hidden'; } });
let ok = 0;
for (const [name, pull, dist] of SHOTS) {
  await p.evaluate(([v, d]) => {
    const sl = document.getElementById('sl'); sl.value = String(v); sl.dispatchEvent(new Event('input'));
    cam.position.set(3.3, 2.2, 3.9).multiplyScalar(d); ctl.target.set(0, 0, 0); ctl.update();
  }, [pull, dist]);
  await p.waitForTimeout(1500);
  await p.locator('#c3').screenshot({ path: `${OUT}/perm4-${name}.png` }); ok++;
  console.log(name, 'pull', pull, 'dist', dist);
}
await b.close();
console.log(errs.length ? 'ERRORS ' + errs.join(' | ') : '', ok === SHOTS.length && !errs.length ? 'FINAL ok' : 'FINAL FAIL');
