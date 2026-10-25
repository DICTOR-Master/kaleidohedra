// The OG on the Octet Truss (DICTO 2026-10-19; paper #37) through the real UI on an iPad: opened from the DICTO wizard (first of DICTO's
// worlds, newest work), the preset (golden-key octet round one OG), every family and kit button, set / round / network with the
// pull-apart and size sliders (each shown only where it applies), the chamber with no view buttons, a tapped piece named, Reset, and the
// ?open=octetTruss:starW link; no errors. Screenshots.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const panel = '#worldoctettruss-panel';
const note = () => page.locator(`${panel} .ot-note`).textContent();
const visible = (sel) => page.locator(`${panel} ${sel}`).isVisible();
await page.goto(`${BASE}/index.html?site=kaleidohedra`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-action="tool:octetTrussWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((a) => /World$/.test(a)));
console.log('first DICTO worlds:', worlds.slice(0, 3).join(', '));
assert.equal(worlds[0], 'tool:dictonicWorld', 'new work first (DICTONIC, 2026-10-23)'); assert.equal(worlds[1], 'tool:globalWebWorld', 'then The Global Web of Bonds (2026-10-25)'); assert.equal(worlds[2], 'tool:platonicMixWorld', 'then Every Mix of the Platonic Solids (#47)'); assert.equal(worlds[3], 'tool:reuleauxWorld', 'then The Reuleaux Platonic Solids (#45)'); assert.equal(worlds[4], 'tool:aristotleWorld', "then Aristotle's Pyramid (#44)"); assert.equal(worlds[5], 'tool:octetTrussWorld', 'then the octet truss'); assert.equal(worlds.filter((a) => a === 'tool:octetTrussWorld').length, 1, 'listed once');
await page.locator('[data-action="tool:octetTrussWorld"]').first().tap();
await page.waitForTimeout(500);
if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
await page.waitForFunction(() => /golden-section points/.test(document.querySelector('#worldoctettruss-panel .ot-note')?.textContent ?? ''), null, { timeout: 15000 });
console.log('preset:', (await note()).slice(0, 60));
assert.ok(await visible('.ot-apart-row'), 'pull apart offered round one OG'); assert.ok(!(await visible('.ot-size-row')), 'size hidden round one OG');
assert.ok(!(await visible('[data-ot-kit="keys"]')), 'a family of one kit shows no kit buttons');
await page.screenshot({ path: `${SH}/ot-keys.png` });
// a piece named by a tap at the centre
const box = await page.locator('canvas').first().boundingBox();
await page.touchscreen.tap(box.x + box.width / 2, box.y + box.height * 0.42); await page.waitForTimeout(600);
const hud = await page.evaluate(() => [...document.querySelectorAll('body *')].map((e) => (e.childElementCount ? '' : e.textContent)).find((s) => /Keyed octahedron|Dented tetrahedron/.test(s)) ?? '');
console.log('tapped:', hud); assert.ok(hud, 'a piece named');
// network: the size slider replaces pull apart
await page.tap(`${panel} [data-ot-show="network"]`); await page.waitForTimeout(900);
assert.ok(await visible('.ot-size-row'), 'size offered'); assert.ok(!(await visible('.ot-apart-row')), 'pull apart hidden');
const size = page.locator(`${panel} .ot-size`); await size.fill('3'); await size.dispatchEvent('change'); await page.waitForTimeout(1200);
assert.match(await page.locator(`${panel} .ot-size-label`).textContent(), /Size: 3/); await page.screenshot({ path: `${SH}/ot-keys-net.png` });
// every family and kit
const kits = { penrose: ['penrose', 'cores'], envelopes: ['grown', 'halves', 'one', 'chamber'], glue: ['envW', 'ogW', 'starW'] };
for (const [fam, list] of Object.entries(kits)) {
  await page.tap(`${panel} [data-ot-family="${fam}"]`); await page.waitForTimeout(900);
  for (const k of list) {
    await page.tap(`${panel} [data-ot-kit="${k}"]`); await page.waitForTimeout(1200);
    const n = await note(); assert.ok(n.length > 40, `${k} described`);
    if (k === 'chamber') { assert.ok(!(await visible('.ot-shows')), 'the chamber has no view buttons'); assert.match(n, /Outside the plan/); }
    else assert.ok(await visible('.ot-shows'), `${k} has its views`);
    await page.screenshot({ path: `${SH}/ot-${k}.png` }); console.log(k, 'ok');
  }
}
// set view of the star-centred W, then reset
await page.tap(`${panel} [data-ot-show="set"]`); await page.waitForTimeout(900); await page.screenshot({ path: `${SH}/ot-starW-set.png` });
await page.tap(`${panel} [data-ot="reset"]`); await page.waitForTimeout(900);
assert.match(await note(), /golden-section points/); assert.ok(!(await visible('[data-ot="reset"]')), 'reset hidden at the preset');
// the link
await page.goto(`${BASE}/index.html?site=kaleidohedra&open=octetTruss:starW`);
await page.waitForFunction(() => /Penrose star \(DICTO\)/.test(document.querySelector('#worldoctettruss-panel .ot-note')?.textContent ?? ''), null, { timeout: 20000 });
console.log('link: W on the Penrose star');
assert.deepEqual(errors, []); console.log('The OG on the Octet Truss: ok'); await b.close();
