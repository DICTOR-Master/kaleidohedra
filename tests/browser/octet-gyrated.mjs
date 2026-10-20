// Octet ↔ gyrated in The OG on the Octet Truss (DICTO 2026-10-20; paper #37a) through the real UI on an iPad: the ?open=octetTruss:gyrated
// link (OG + caps on the gyrated octet, network); the lattice switch shown only in this family; the twin pair offered on the gyrated octet
// and not on the octet; every solid (OG, OG + caps, OCD Stella, DBT) described; pull apart in the set and twin pair, size in the network;
// a tapped piece named; the #37 families keep no lattice switch; no errors. Screenshots.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const panel = '#worldoctettruss-panel';
const note = () => page.locator(`${panel} .ot-note`).textContent();
const visible = (sel) => page.locator(`${panel} ${sel}`).isVisible();
await page.goto(`${BASE}/index.html?site=kaleidohedra&open=octetTruss:gyrated`);
await page.waitForFunction(() => /One exact kit for every stacking/.test(document.querySelector('#worldoctettruss-panel .ot-note')?.textContent ?? ''), null, { timeout: 20000 });
await page.waitForTimeout(1200);
if (await page.locator('#welcome-overlay').isVisible()) { await page.keyboard.press('Enter'); await page.waitForTimeout(600); }   // the first-visit welcome covers the panel
if (await page.locator('.dim-wizard-overlay.open').count()) { await page.keyboard.press('Escape'); await page.waitForTimeout(400); }
assert.ok(await visible('.ot-lattices'), 'lattice switch shown in the twins family');
assert.match(await page.locator(`${panel} [data-ot-lattice="gyrated"]`).getAttribute('class'), /active/, 'gyrated chosen by the link');
assert.ok(await visible('[data-ot-show="pair"]'), 'twin pair offered on the gyrated octet'); assert.ok(!(await visible('[data-ot-show="round"]')), 'no round-one-OG view here');
assert.ok(await visible('.ot-size-row'), 'network: size offered'); assert.ok(!(await visible('.ot-apart-row')), 'network: no pull apart');
await page.screenshot({ path: `${SH}/gy-caps-net.png` });
// the twin pair, pulled apart, and a tapped piece named
await page.tap(`${panel} [data-ot-show="pair"]`); await page.waitForTimeout(1200);
assert.ok(await visible('.ot-apart-row'), 'pair: pull apart offered');
await page.screenshot({ path: `${SH}/gy-caps-pair.png` });
const box = await page.locator('canvas').first().boundingBox(); let hud = '';
for (const [fx, fy] of [[0.5, 0.42], [0.45, 0.38], [0.55, 0.46], [0.5, 0.5]]) {
  await page.touchscreen.tap(box.x + box.width * fx, box.y + box.height * fy); await page.waitForTimeout(600);
  hud = await page.evaluate(() => [...document.querySelectorAll('body *')].map((e) => (e.childElementCount ? '' : e.textContent)).find((s) => /Ogdoecontahedron \(OG\)|Left cap|Right cap|Tetrahedron of the octet/.test(s)) ?? '');
  if (hud) break;
}
console.log('tapped:', hud); assert.ok(hud, 'a piece named');
// on the octet the twin pair is not offered, and the view falls back
await page.tap(`${panel} [data-ot-lattice="octet"]`); await page.waitForTimeout(1200);
assert.ok(!(await visible('[data-ot-show="pair"]')), 'no twin pair on the octet');
assert.match(await page.locator(`${panel} [data-ot-show="set"]`).getAttribute('class'), /active/, 'pair falls back to the set');
await page.tap(`${panel} [data-ot-show="network"]`); await page.waitForTimeout(1500); await page.screenshot({ path: `${SH}/gy-caps-octet-net.png` });
await page.tap(`${panel} [data-ot-lattice="gyrated"]`); await page.waitForTimeout(1500);
// every solid
for (const [k, re] of [['gOG', /spinel law/], ['gCaps', /One exact kit/], ['gStella', /77\.44%/], ['gDBT', /55\.02% of space/], ['gOTT', /52\.89% of space/]]) {
  await page.tap(`${panel} [data-ot-kit="${k}"]`); await page.waitForTimeout(1500);
  assert.match(await note(), re, `${k} described`); await page.screenshot({ path: `${SH}/gy-${k}-net.png` });
  await page.tap(`${panel} [data-ot-show="pair"]`); await page.waitForTimeout(1200); await page.screenshot({ path: `${SH}/gy-${k}-pair.png` });
  await page.tap(`${panel} [data-ot-show="network"]`); await page.waitForTimeout(1000);
  console.log(k, 'ok');
}
// the #37 families keep no lattice switch
await page.tap(`${panel} [data-ot-family="keys"]`); await page.waitForTimeout(1200);
assert.ok(!(await visible('.ot-lattices')), 'no lattice switch for the #37 kits'); assert.ok(await visible('[data-ot-show="round"]'), '#37 kits keep round one OG');
assert.deepEqual(errors, []); console.log('Octet ↔ gyrated: ok'); await b.close();
