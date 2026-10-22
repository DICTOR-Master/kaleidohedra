// A fresh start and small faults (DICTO's app audit 2026-10-22, items 1 and 11) through the real UI on an iPad with touch:
//   - nothing saved: a world opens with no question;
//   - a saved build (Every Mix with layers in; the 3D lattices with a cell): entering asks "Continue where you left off" /
//     "Start fresh"; Start fresh empties it and ↶ brings it back; Continue keeps it; moving within the 3D lattice space asks once;
//   - the RHOMBIS hint in Settings only on the Rhombiverse door; on Rhombiverse, tapping 3D+ in the menu opens and closes it;
//   - ?from=dicto behaves as ?dicto (no welcome card).
// Screenshot (SHOTS): the prompt. No console errors.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const b = await chromium.launch();
const T0 = Date.now();
b.on('disconnected', () => console.log('BROWSER DISCONNECTED at', (Date.now() - T0) / 1000, 's'));
const errors = [];
let lastCtx = null;
async function door() {
  await lastCtx?.close(); // one door at a time (memory)
  lastCtx = await b.newContext({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
  const page = await lastCtx.newPage();
  page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('dialog', (d) => d.accept());
  page.on('crash', () => console.log('PAGE CRASHED'));
  return page;
}
const asked = async (page) => page.locator('#leave-dialog:not([hidden]) [data-choice="fresh"]').count();
async function go(page, url) {
  await page.goto(`${BASE}/index.html?${url}`); await page.waitForTimeout(1200);
  if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
  await page.waitForTimeout(1800);
}

// ---- Kaleidohedra: Every Mix of the Platonic Solids
console.log((Date.now() - T0) / 1000, '--', 'Kaleidohedra: Every Mix of the Platonic ');
let page = await door('kaleidohedra');
await go(page, 'site=kaleidohedra&open=platonicMix&probe');
assert.equal(await asked(page), 0, 'nothing saved: no question');
const mix = () => page.evaluate(() => window.__platonicMixProbe().mix);
for (const w of ['D', 'I']) { await page.locator(`[data-pm-world="${w}"]`).tap(); await page.waitForTimeout(800); }
assert.equal(await mix(), 'DI');
await go(page, 'site=kaleidohedra&open=platonicMix&probe');
assert.equal(await asked(page), 1, 'saved build: asked first');
assert.equal(await page.evaluate(() => window.__sceneHidden()), true, 'the saved build is out of sight while asked');
console.log('prompt:', await page.textContent('#leave-title'), '|', await page.textContent('#leave-body'));
await page.screenshot({ path: `${SH}/fresh-prompt.png` });
const box = await page.locator('#leave-dialog [data-choice="fresh"]').boundingBox();
assert.ok(box.height >= 48, 'big buttons');
await page.tap('#leave-dialog [data-choice="fresh"]'); await page.waitForTimeout(800);
assert.equal(await mix(), '', 'Start fresh: empty');
assert.equal(await page.evaluate(() => window.__sceneHidden()), false, 'Start fresh: the world shown, empty');
await page.tap('#undo-btn'); await page.waitForTimeout(800);
assert.equal(await mix(), 'DI', '↶ brings it back');
await go(page, 'site=kaleidohedra&open=platonicMix&probe');
assert.equal(await asked(page), 1);
await page.tap('#leave-dialog [data-choice="continue"]'); await page.waitForTimeout(600);
assert.equal(await mix(), 'DI', 'Continue: the build');
assert.equal(await page.evaluate(() => window.__sceneHidden()), false, 'Continue: shown');
assert.equal(await page.locator('#leave-dialog').isHidden(), true);
// a link that opens a mix is not a saved build
await page.evaluate(() => localStorage.clear());
await go(page, 'site=kaleidohedra&open=platonicMix:DIC&probe');
assert.equal(await asked(page), 0, 'a mix by link: no question');
// view-only world: no question
await go(page, 'site=kaleidohedra&open=aristotle');
assert.equal(await asked(page), 0, 'view-only: no question');
// the RHOMBIS hint is Rhombiverse's
assert.equal(await page.locator('#rhombis-settings-link').count(), 0, 'no RHOMBIS hint on Kaleidohedra');

// ---- Kaleidohedra: the 3D lattices (one space) with a saved cell
console.log((Date.now() - T0) / 1000, '--', 'Kaleidohedra: the 3D lattices (one space');
await page.evaluate(() => { localStorage.clear(); });
await go(page, 'site=kaleidohedra');
const firstLattice = '.dicto-dim-content [data-action^="tool:pieceType:"]';
if (!(await page.locator(firstLattice).count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
await page.locator(firstLattice).first().tap(); await page.waitForTimeout(1500);
assert.equal(await asked(page), 0, 'empty lattice: no question');
await page.evaluate(() => {
  const m = document.getElementById('color-select').value;
  localStorage.setItem('kaleidohedra-world', JSON.stringify({ worldName: 'Kaleidohedra', version: 1, cells: { '0,0,0': { material: m }, '1,1,0': { material: m } }, meta: {} }));
});
await go(page, 'site=kaleidohedra');
if (!(await page.locator(firstLattice).count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
await page.locator(firstLattice).first().tap(); await page.waitForTimeout(1500);
assert.equal(await asked(page), 1, 'lattice with a saved build: asked');
await page.tap('#leave-dialog [data-choice="fresh"]'); await page.waitForTimeout(800);
const cells = await page.evaluate(() => Object.keys(JSON.parse(localStorage.getItem('kaleidohedra-world')).cells).length);
assert.equal(cells, 0, 'Start fresh: the lattice emptied');

// ---- every world by its link, twice, nothing changed in between: never asked (an untouched world is no saved build)
console.log((Date.now() - T0) / 1000, '--', 'every world by its link, twice, nothing ');
// (all of them with FULL=1; by default the build worlds most likely to open in a state of their own)
const ALL_WORLDS = ['octet', 'thirteens', 'chains', 'dodeca', 'theaetetus', 'up', 'upFilm', 'kpFilm', 'icosa', 'roofFold', 'stellaJewel', 'sunstar', 'octetBuild', 'breathing', 'bodhiPyro', 'doubleVision', 'vajrayana', 'ocdStella', 'octetTruss', 'reuleaux', 'aristotle', 'platonicMix', 'cycles', 'shells', 'golden', 'studies', 'targets'];
const WORLDS = process.env.FULL ? ALL_WORLDS : ['octetBuild', 'reuleaux', 'shells', 'golden', 'roofFold', 'cycles'];
await page.evaluate(() => localStorage.clear());
for (const w of WORLDS) for (const visit of [1, 2]) {
  await go(page, `site=kaleidohedra&open=${w}`);
  assert.equal(await asked(page), 0, `${w}, visit ${visit}: not asked`);
}

// ---- Rhombiverse: the hint, 3D+ toggles
console.log((Date.now() - T0) / 1000, '--', 'Rhombiverse: the hint, 3D+ toggles');
page = await door('rhombiverse');
await go(page, 'site=rhombiverse');
assert.equal(await page.locator('#rhombis-settings-link').count(), 1, 'RHOMBIS hint on Rhombiverse');
const d3 = page.locator('.dim-wizard-card-btn[data-dim="3D"]');
const exp1 = await d3.getAttribute('aria-expanded');
await d3.tap(); await page.waitForTimeout(500);
assert.equal(await page.locator('.dim-wizard-overlay.open').count(), 1, '3D+ tap stays in the menu');
const exp2 = await page.locator('.dim-wizard-card-btn[data-dim="3D"]').getAttribute('aria-expanded');
assert.notEqual(exp1, exp2, '3D+ toggles');
await page.locator('.dim-wizard-card-btn[data-dim="3D"]').tap(); await page.waitForTimeout(500);
assert.equal(await page.locator('.dim-wizard-card-btn[data-dim="3D"]').getAttribute('aria-expanded'), exp1, 'and back');

// ---- Polyhedraverse: its space opens behind the menu; closing the menu over a saved build asks
console.log((Date.now() - T0) / 1000, '--', 'Polyhedraverse: its space opens behind t');
page = await door('polyhedraverse');
await page.goto(`${BASE}/index.html?site=polyhedraverse`); await page.waitForTimeout(1500);
await page.evaluate(() => localStorage.setItem('polyhedraverse-poly-world', JSON.stringify({ version: 1, nodes: [{ id: 'a', shape: 'CUBE', transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } }], connections: [], view: {} })));
await page.reload(); await page.waitForTimeout(1500);
if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open'); await page.tap('.dim-wizard-close'); await page.waitForTimeout(800);
assert.equal(await asked(page), 1, 'Polyhedraverse door: asked');
await page.tap('#leave-dialog [data-choice="fresh"]'); await page.waitForTimeout(800);
assert.equal(JSON.parse(await page.evaluate(() => localStorage.getItem('polyhedraverse-poly-world'))).nodes.length, 0, 'Start fresh: empty');

// ---- ?from=dicto is ?dicto
console.log((Date.now() - T0) / 1000, '--', '?from=dicto is ?dicto');
await page.goto(`${BASE}/index.html?site=rhombiverse&from=dicto`); await page.waitForTimeout(2000);
assert.equal(await page.locator('#welcome-overlay').isVisible(), false, '?from=dicto: no welcome');
assert.ok(!page.url().includes('from=dicto'), 'dropped from the address');

console.log(errors.length ? 'ERRORS ' + errors.join(' | ') : 'no errors'); assert.equal(errors.length, 0);
await b.close(); console.log('fresh-start OK');
