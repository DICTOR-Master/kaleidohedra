// The Reuleaux Platonic Solids family (DICTO 2026-10-23; DICTO's idea, paper #45) and the Soft view on Polyhedraverse builds, through the
// real UI on every door, on a phone (390 px) and an iPad, with touch:
//  - DICTO → 3D+ → Reuleaux Platonic Solids (#45) lists the five bodies by the world's names; a body's details carry the #45 credit and
//    DICTO DOI, curved faces, no 4D buttons; Build places it; a tap on its face with the strip's body attaches a second, corner to corner;
//    search "Reuleaux" finds the five;
//  - a mixed build (cube, square pyramid, tetrahedron, two Reuleaux bodies, M-S t1 and t5) seen through the Soft button: Soft on → the
//    Softness slider appears; off → it goes; each finish switches; it renders with no errors;
//  - a large build (343 pieces) with Soft Metallic on: frame time on the phone profile.
// SHOTS: where screenshots go (soft-reuleaux-*.png, the Polyhedraverse door only). DOORS, VPS pick doors and viewports.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import { POLYHEDRA } from '../../src/krp-core/src/polyhedra/index.js';
import { facesCongruent } from '../../src/krp-core/src/polyhedra/core.js';
import { faceAttachOptions } from '../../src/krp-core/src/assembly/faceAttach.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SHOTS = process.env.SHOTS ?? '/tmp';
const DOORS = (process.env.DOORS ?? 'polyhedraverse,kaleidohedra,rhombiverse').split(',');
const ALL_VPS = { phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } };
const VPS = (process.env.VPS ?? 'phone,ipad').split(',');
const NAMES = ['Reuleaux tetrahedron', 'Reuleaux octahedron', 'Reuleaux icosahedron', 'Reuleaux cube', 'Reuleaux dodecahedron'];

// ---- builds, placed exactly as the app places them (krp-core faceAttach) ----
function attach(nodes, i, fi, id) {
  const n = nodes[i], T = POLYHEDRA[n.shape], S = POLYHEDRA[id];
  const M = new THREE.Matrix4().compose(new THREE.Vector3(...n.transform.position), new THREE.Quaternion(...n.transform.quaternion), new THREE.Vector3(1, 1, 1));
  const inc = S.faces.map((_, k) => k).filter((k) => S.faces[k].length === T.faces[fi].length && facesCongruent(T.vertices, T.faces[fi], S.vertices, S.faces[k]));
  const o = faceAttachOptions(T, fi, M, S, inc)[0];
  assert.ok(o, `${id} on ${n.shape} face ${fi}`);
  nodes.push({ id: `n${nodes.length}`, shape: id, transform: { position: o.position.toArray(), quaternion: o.quaternion.toArray() } });
  return nodes.length - 1;
}
const root = (shape, p = [0, 0, 0]) => ({ id: 'n0', shape, transform: { position: p, quaternion: [0, 0, 0, 1] } });
const MIXED = (() => {
  const b = [root('CUBE')];
  attach(b, 0, 0, 'REULEAUX_CUBE');
  const py = attach(b, 0, 2, 'J1_SQUARE_PYRAMID');
  const tri = POLYHEDRA.J1_SQUARE_PYRAMID.faces.map((f, k) => (f.length === 3 ? k : -1)).filter((k) => k >= 0);
  attach(b, py, tri[0], 'REULEAUX_TETRAHEDRON');
  attach(b, py, tri[2], 'D4');
  attach(b, 0, 4, 'REULEAUX_CUBE');
  // the two new Mosseri–Sadoc tiles, face to face, beside the rest
  const t1 = b.push({ id: `n${b.length}`, shape: 'MS_T1', transform: { position: [-1.4, -0.2, 0.6], quaternion: [0, 0, 0, 1] } }) - 1;
  const T1 = POLYHEDRA.MS_T1, T5 = POLYHEDRA.MS_T5;
  const fi = T1.faces.findIndex((f) => T5.faces.some((g) => facesCongruent(T1.vertices, f, T5.vertices, g)));
  if (fi >= 0) attach(b, t1, fi, 'MS_T5');
  return b;
})();
const LARGE = (() => {
  const b = [];
  for (let x = 0; x < 7; x++) for (let y = 0; y < 7; y++) for (let z = 0; z < 7; z++) b.push({ id: `n${b.length}`, shape: (x + y + z) % 2 ? 'REULEAUX_CUBE' : 'CUBE', transform: { position: [x - 3, y - 3, z - 3], quaternion: [0, 0, 0, 1] } });
  return b;
})();

const b = await chromium.launch();
let failures = 0;
for (const door of DOORS) for (const vp of VPS) {
  const ctx = await b.newContext({ viewport: ALL_VPS[vp], hasTouch: true, isMobile: true, deviceScaleFactor: vp === 'phone' ? 2 : 1 });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon|Failed to load resource|Ignored attempt to cancel a touch/.test(m.text())) errors.push(m.text()); });
  page.on('dialog', (d) => d.accept());
  const shot = (name) => (door === 'polyhedraverse' ? page.screenshot({ path: `${SHOTS}/soft-reuleaux-${name}-${vp}.png` }) : null);
  // "Continue where you left off": the stored build is kept (the dialog can take a moment to come)
  const keep = async () => { for (let k = 0; k < 8; k++) { if (await page.locator('#leave-dialog:not([hidden])').count()) { await page.tap('#leave-dialog [data-choice="continue"], #leave-dialog [data-choice="keep"]'); await page.waitForTimeout(700); return; } await page.waitForTimeout(400); } };
  const openWizard = async (url) => {
    await page.goto(url);
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await page.keyboard.press('Enter');
    await page.waitForSelector('.dim-wizard-overlay.open', { timeout: 15000 });
    if (!(await page.locator('[data-family="REULEAUX_PLATONIC"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
  };
  try {
    // ---- the family, a body's details, Build ----
    await openWizard(`${BASE}/index.html?site=${door}&probe`);
    const fam = page.locator('[data-family="REULEAUX_PLATONIC"]').first(); await fam.scrollIntoViewIfNeeded();
    assert.match(await fam.textContent(), /Reuleaux Platonic Solids \(#45\)/, 'family row');
    await fam.tap(); await page.waitForTimeout(900);
    const labels = await page.$$eval('.dim-wizard-body [data-action^="tool:polyShape:"] .dim-wizard-label', (els) => els.map((e) => e.textContent.trim()));
    assert.deepEqual(labels, NAMES, 'family list');
    assert.equal(await page.locator('.dim-wizard-body [data-action^="tool:polyShape:REULEAUX_"].dicto-gold').count(), 5, 'in DICTO\'s livery');
    await shot('family');
    const card = page.locator('[data-action="tool:polyShape:REULEAUX_CUBE"]').first(); await card.scrollIntoViewIfNeeded(); await card.tap(); await page.waitForTimeout(900);
    assert.equal((await page.textContent('.poly-detail-name')).trim(), 'Reuleaux cube');
    const credit = await page.textContent('[data-credit="reuleaux"]');
    assert.ok(credit.includes("DICTO's idea") && credit.includes('#45') && credit.includes('10.5281/zenodo.23529499') && credit.includes('octahedron'), `credit: ${credit}`);
    assert.match(await page.textContent('.poly-detail-stats'), /6: curved \(ball patches\), 4 corners each/);
    assert.equal(await page.locator('.poly-detail-4d').count(), 0, 'no 4D buttons for a curved body');
    await shot('detail');
    await page.tap('.poly-detail-build'); await page.waitForTimeout(2500);
    assert.equal(await page.locator('.dim-wizard-overlay.open').count(), 0, 'wizard closed on Build');
    await keep();
    let st = await page.evaluate(() => window.__polyProbe.state());
    if (!st.nodes.length) { // an empty world shows the body's outline: tap it to place it
      await page.touchscreen.tap(ALL_VPS[vp].width / 2, ALL_VPS[vp].height / 2); await page.waitForTimeout(1200);
      st = await page.evaluate(() => window.__polyProbe.state());
    }
    assert.ok(st.nodes.length >= 1 && st.nodes.at(-1).shape === 'REULEAUX_CUBE', `built: ${JSON.stringify(st.nodes.map((n) => n.shape))}`);
    // attach a second body: tap its most camera-facing face (a ball patch), then the body in the strip if it waits for a shape
    const before = st.nodes.length, i = before - 1;
    const f = (await page.evaluate((k) => window.__polyProbe.faces(k), i))[0];
    const at = await page.evaluate(([k, ff]) => window.__polyProbe.face(k, ff), [i, f]);
    await page.touchscreen.tap(at.x, at.y); await page.waitForTimeout(900);
    st = await page.evaluate(() => window.__polyProbe.state());
    if (st.nodes.length === before) {
      const s = page.locator('.poly-shape[data-shape="REULEAUX_CUBE"]').first();
      if (await s.count()) { await s.tap(); await page.waitForTimeout(1200); }
      st = await page.evaluate(() => window.__polyProbe.state());
    }
    assert.equal(st.nodes.length, before + 1, 'a second Reuleaux cube attached face to face');
    const [A, B] = st.nodes.slice(-2).map((n) => n.transform.position);
    assert.ok(Math.abs(Math.hypot(A[0] - B[0], A[1] - B[1], A[2] - B[2]) - 1) < 1e-6, 'corner to corner: centres 1 apart');
    await page.waitForTimeout(400);
    if (door === 'polyhedraverse') await page.screenshot({ path: `${SHOTS}/soft-reuleaux-built-${vp}.png` });

    // ---- search ----
    await openWizard(`${BASE}/index.html?site=${door}&probe`);
    const input = page.locator('.poly-search-input').first(); await input.scrollIntoViewIfNeeded(); await input.tap(); await input.fill('reuleaux'); await page.waitForTimeout(900);
    const found = await page.$$eval('.poly-search-results [data-shape]', (els) => els.map((e) => e.dataset.shape));
    assert.deepEqual(found.sort(), ['REULEAUX_CUBE', 'REULEAUX_DODECAHEDRON', 'REULEAUX_ICOSAHEDRON', 'REULEAUX_OCTAHEDRON', 'REULEAUX_TETRAHEDRON'], 'search');

    // ---- Soft on a mixed build, through the Soft button ----
    await page.evaluate((build) => {
      for (const k of Object.keys(localStorage)) if (k.endsWith('poly-world')) localStorage.setItem(k, JSON.stringify({ version: 1, nodes: build, connections: [], view: {} }));
      localStorage.setItem('rv-soft-finish', JSON.stringify({ soft: false, finish: 'plain', amount: 0.25 }));
    }, MIXED);
    // open Polyhedraverse's space on the stored build: a shape's Build from search (the build is kept)
    await page.goto(`${BASE}/index.html?site=${door}&probe`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await page.keyboard.press('Enter');
    await page.waitForSelector('.dim-wizard-overlay.open', { timeout: 15000 });
    if (!(await page.locator('.poly-search-input').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    { const inp = page.locator('.poly-search-input').first(); await inp.scrollIntoViewIfNeeded(); await inp.tap(); await inp.fill('reuleaux tetrahedron'); await page.waitForTimeout(900);
      await page.locator('.poly-search-results [data-shape="REULEAUX_TETRAHEDRON"]').first().tap(); await page.waitForTimeout(700);
      await page.tap('.poly-detail-build'); await page.waitForTimeout(2500); await keep(); }
    st = await page.evaluate(() => window.__polyProbe.state());
    assert.ok(st.nodes.length >= MIXED.length, `the mixed build is there (${st.nodes.length})`);
    await page.waitForSelector('#soft-toggle:not([hidden])', { timeout: 15000 });
    await page.mouse.move(ALL_VPS[vp].width / 2, ALL_VPS[vp].height / 2); await page.mouse.wheel(0, 500); await page.waitForTimeout(900); // a step back, the whole build in view
    assert.ok(await page.$eval('#soft-toggle', (x) => !!x.querySelector('svg path') && x.textContent.trim() === ''), 'puffed-square icon');
    await page.tap('#soft-toggle'); await page.waitForTimeout(500);
    const sliderShown = () => page.$eval('#soft-panel .soft-amount', (r) => !r.hidden && r.getBoundingClientRect().height > 0);
    assert.equal(await sliderShown(), false, 'Flat: no Softness slider');
    await shot('controls-off');
    await page.tap('#soft-panel [data-mode=soft]'); await page.waitForTimeout(900);
    assert.equal(await sliderShown(), true, 'Soft: the Softness slider');
    // a big slider, low on the screen: right above the bottom buttons or above the other bottom panel there, never over it
    const geo = await page.$eval('#soft-amount', (s) => { const r = s.getBoundingClientRect(), o = [...document.querySelectorAll('.qc-panel.visible:not(#soft-panel), #world4d-panel.visible, #kaleido-body:not([hidden])')].map((e) => e.getBoundingClientRect()).filter((q) => q.height > 0);
      return { w: r.width, h: r.height, bottom: r.bottom, vh: innerHeight, over: o.some((q) => q.top < r.bottom - 1 && q.bottom > r.top + 1), above: o.length ? Math.min(...o.map((q) => q.top)) - r.bottom : null }; });
    assert.ok(geo.w >= 300 && geo.h >= 44 && !geo.over && (geo.vh - geo.bottom < 200 || (geo.above !== null && geo.above < 60)), `a big low slider, clear of other panels ${JSON.stringify(geo)}`);
    await shot('controls-on');
    for (const fin of ['plain', 'metallic', 'ceramic']) {
      await page.tap(`#soft-panel [data-finish=${fin}]`); await page.waitForTimeout(700);
      assert.ok(await page.$eval(`#soft-panel [data-finish=${fin}]`, (x) => x.classList.contains('active')), `${fin} chosen`);
      const fin2 = await page.evaluate(() => JSON.parse(localStorage.getItem('rv-soft-finish')).finish);
      assert.equal(fin2, fin);
      await page.tap('#soft-toggle'); await page.waitForTimeout(700); // the panel away for a clear view
      await shot(`mixed-${fin}`);
      await page.tap('#soft-toggle'); await page.waitForTimeout(400);
    }
    // Soft off again: the slider goes
    await page.tap('#soft-panel [data-mode=flat]'); await page.waitForTimeout(500);
    assert.equal(await sliderShown(), false, 'Flat again: slider gone');
    await page.tap('#soft-panel [data-finish=plain]'); await page.waitForTimeout(300);

    // ---- a large build: frame time (phone profile) with Soft off, Soft Plain and Soft Metallic, switched through the panel ----
    if (vp === 'phone' && door === 'polyhedraverse') {
      await page.evaluate((build) => { for (const k of Object.keys(localStorage)) if (k.endsWith('poly-world')) localStorage.setItem(k, JSON.stringify({ version: 1, nodes: build, connections: [], view: {} })); localStorage.setItem('rv-soft-finish', JSON.stringify({ soft: false, finish: 'plain', amount: 0.25 })); }, LARGE);
      await page.reload();
      await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await page.keyboard.press('Enter');
      await page.waitForSelector('.dim-wizard-overlay.open', { timeout: 15000 });
      if (!(await page.locator('.poly-search-input').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
      { const inp = page.locator('.poly-search-input').first(); await inp.scrollIntoViewIfNeeded(); await inp.tap(); await inp.fill('reuleaux cube'); await page.waitForTimeout(900);
        await page.locator('.poly-search-results [data-shape="REULEAUX_CUBE"]').first().tap(); await page.waitForTimeout(700);
        await page.tap('.poly-detail-build'); await keep(); }
      await page.waitForFunction((n) => window.__polyProbe?.state().nodes.length >= n, LARGE.length, { timeout: 60000 });
      await page.waitForTimeout(1500);
      const frameMs = () => page.evaluate(() => new Promise((res) => { const ts = []; const tick = (t) => { ts.push(t); if (ts.length < 13) requestAnimationFrame(tick); else { const d = ts.slice(1).map((x, k) => x - ts[k]).sort((p, q) => p - q); res(d[6]); } }; requestAnimationFrame(tick); }));
      // the time from a tap to the next drawn frame (the Soft copies made and drawn)
      const tapToFrame = async (sel) => { const t0 = Date.now(); await page.tap(sel); await page.evaluate(() => new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))); return Date.now() - t0; };
      const off = await frameMs();
      await page.tap('#soft-toggle'); await page.waitForTimeout(500);
      const switchSoft = await tapToFrame('#soft-panel [data-mode=soft]');
      await page.tap('#soft-toggle'); await page.waitForTimeout(500);
      const plain = await frameMs();
      await page.tap('#soft-toggle'); await page.waitForTimeout(500);
      const switchMetal = await tapToFrame('#soft-panel [data-finish=metallic]');
      await page.tap('#soft-toggle'); await page.waitForTimeout(500);
      const metal = await frameMs();
      console.log(`PERF ${door} ${vp} (headless software GL, 780×1688 px): ${LARGE.length} pieces (half Reuleaux cubes) · frame median: Soft off ${off.toFixed(0)} ms, Soft Plain ${plain.toFixed(0)} ms, Soft Metallic ${metal.toFixed(0)} ms · tap to Soft drawn ${switchSoft} ms, tap to Metallic drawn ${switchMetal} ms`);
      await page.screenshot({ path: `${SHOTS}/soft-reuleaux-large-metallic-${vp}.png` });
      await page.evaluate(() => localStorage.setItem('rv-soft-finish', JSON.stringify({ soft: false, finish: 'plain', amount: 0.25 })));
    }
    assert.deepEqual(errors, [], `console errors: ${errors.join(' | ')}`);
    console.log(`ok ${door} ${vp}`);
  } catch (e) {
    failures++;
    console.log(`FAIL ${door} ${vp}: ${e.message.split("\n")[0]} @ ${(e.stack.match(/soft-reuleaux.mjs:\d+/g) ?? []).join(" ")}`);
    await page.screenshot({ path: `${SHOTS}/soft-reuleaux-fail-${door}-${vp}.png` }).catch(() => {});
  }
  await ctx.close().catch(() => {});
}
await b.close();
process.exit(failures ? 1 : 0);
