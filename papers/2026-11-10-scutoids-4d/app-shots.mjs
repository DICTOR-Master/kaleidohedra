// #104 v2 figures from the app's Bitruncated 600-cell world (DICTO 11 Nov: "your beautiful cutaways", the pull-apart he liked).
// Served from the app root (branch with Pull apart). Each shot: open the world in a view, set the sliders through the real inputs,
// hide every overlay so only the 3D canvas shows, 1500x1100 at 2x. Writes bt-<name>.png to $OUT.
import { chromium } from 'playwright';
const OUT = process.env.OUT ?? '/tmp', BASE = process.env.BASE ?? 'http://127.0.0.1:8021';
const P = '#worldbitrunc-panel';
const SHOTS = [
  ['shell1-apart', 'shells', { shells: 2, apart: 1000 }],
  ['cutopen', 'whole', { apart: 0 }],
  ['cutopen-apart', 'whole', { apart: 600 }],
  ['swap', 'swap', {}],
];
const b = await chromium.launch({ args: ['--use-gl=angle', '--enable-webgl', '--ignore-gpu-blocklist'] });
let ok = 0;
for (const [name, view, set] of SHOTS) {
  const p = await b.newPage({ viewport: { width: 1500, height: 1100 }, deviceScaleFactor: 2 });
  const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
  await p.goto(`${BASE}/index.html?open=bitrunc:${view}&site=kaleidohedra`);
  await p.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await p.keyboard.press('Enter');
  await p.waitForSelector(P, { state: 'visible', timeout: 30000 }); await p.waitForTimeout(1500);
  if (set.shells) { await p.locator(`${P} .bt-shells-row input`).fill(String(set.shells)); await p.waitForTimeout(600); }
  if (set.apart !== undefined && await p.locator(`${P} .bt-apart-row input`).isVisible()) { await p.locator(`${P} .bt-apart-row input`).fill(String(set.apart)); await p.waitForTimeout(1200); }
  const st = await p.evaluate(() => window.__bitruncProbe?.());
  await p.addStyleTag({ content: '* { visibility: hidden !important; } canvas, canvas * { visibility: visible !important; }' });
  await p.waitForTimeout(800);
  await p.screenshot({ path: `${OUT}/bt-${name}.png` });
  console.log(name, JSON.stringify({ mode: st?.mode, shells: st?.shells, apart: st?.apart, stop: st?.stop }), errs.length ? 'ERRORS ' + errs.join(' | ') : 'ok');
  if (!errs.length) ok++;
}
await b.close(); console.log(ok === SHOTS.length ? 'FINAL ok' : 'FINAL FAIL');
