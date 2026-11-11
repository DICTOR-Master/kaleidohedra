// Copy build (DICTO 2026-11-11) through the real UI, on every door, on a phone (390 px) and an iPad, with touch:
//  - one RD-Hemi (bare), opened by its Build in DICTO's search: no Copy build button (nothing attached yet);
//  - two taps on its faces attach two more (the chosen shape goes straight on); the button shows, a full touch target;
//  - a tap copies the build: the clipboard's JSON parses, has as many pieces as the caption counts (and as the build), every
//    child's parent and faces in range, the caption the one on screen; the note says "Build copied";
//  - with no clipboard at all (Clipboard API refused, execCommand failing), the record opens in a dialog, selected, to copy by hand.
// No console errors. DOORS, VPS pick doors and viewports.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const DOORS = (process.env.DOORS ?? 'polyhedraverse,kaleidohedra,rhombiverse').split(',');
const ALL_VPS = { phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } };
const VPS = (process.env.VPS ?? 'phone,ipad').split(',');
const HEMI = 'RVCMG_RD_HEMI';
const captionCount = (cap) => cap.split(' + ').reduce((n, part) => n + (Number(part.match(/^(\d+)×/)?.[1]) || 1), 0);

const b = await chromium.launch();
let failures = 0;
for (const door of DOORS) for (const vp of VPS) {
  const ctx = await b.newContext({ viewport: ALL_VPS[vp], hasTouch: true, isMobile: true, deviceScaleFactor: 2 });
  await ctx.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: new URL(BASE).origin });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon|Failed to load resource|Ignored attempt to cancel a touch/.test(m.text())) errors.push(m.text()); });
  page.on('dialog', (d) => d.accept());
  const state = () => page.evaluate(() => window.__polyProbe.state());
  const keep = async () => { for (let k = 0; k < 8; k++) { if (await page.locator('#leave-dialog:not([hidden])').count()) { await page.tap('#leave-dialog [data-choice="continue"], #leave-dialog [data-choice="keep"]'); await page.waitForTimeout(700); return; } await page.waitForTimeout(400); } };
  try {
    // ---- a stored build of one RD-Hemi, opened by its Build ----
    await page.goto(`${BASE}/index.html?site=${door}&probe`);
    await page.evaluate((hemi) => {
      for (const s of ['polyhedraverse', 'kaleidohedra', 'rhombiverse']) localStorage.setItem(`${s}-poly-world`, JSON.stringify({ version: 1, connections: [], view: { shape: hemi },
        nodes: [{ id: 'n1', shape: hemi, transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } }] }));
    }, HEMI);
    await page.goto(`${BASE}/index.html?site=${door}&probe`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await page.keyboard.press('Enter');
    await page.waitForSelector('.dim-wizard-overlay.open', { timeout: 15000 });
    if (!(await page.locator('.poly-search-input').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
    const inp = page.locator('.poly-search-input').first(); await inp.scrollIntoViewIfNeeded(); await inp.tap(); await inp.fill('rd-hemi'); await page.waitForTimeout(900);
    await page.locator(`.poly-search-results [data-shape="${HEMI}"]`).first().tap(); await page.waitForTimeout(700);
    await page.tap('.poly-detail-build'); await page.waitForTimeout(2500); await keep();
    let st = await state();
    assert.deepEqual(st.nodes.map((n) => n.shape), [HEMI], `${door}/${vp}: the one stored piece`);
    assert.equal(await page.locator('[data-copy-build]').count(), 0, `${door}/${vp}: no Copy build with nothing attached`);
    assert.equal((await page.evaluate(() => window.__polyBuild())).pieces.length, 1);

    // ---- two taps attach two pieces (each tap on a face of the newest piece first) on faces whose middle is beyond a finger's reach of every corner (0.22 of an edge; nearer
    // picks the corner), as the app decides ----
    const roomy = (await page.evaluate(() => window.__polyBuild())).pieces[0];
    const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
    const edge = roomy.faces.flatMap((f) => f.map((v, k) => dist(roomy.vertices[v], roomy.vertices[f[(k + 1) % f.length]])));
    const reach = 0.22 * edge.reduce((s, x) => s + x, 0) / edge.length;
    const away = roomy.faces.map((f) => { const c = [0, 1, 2].map((j) => f.reduce((s, v) => s + roomy.vertices[v][j], 0) / f.length); return Math.min(...f.map((v) => dist(c, roomy.vertices[v]))) > 1.3 * reach; });
    for (let want = 2; want <= 3; want++) {
      for (let i = st.nodes.length - 1; i >= 0 && st.nodes.length < want; i--) {   // the newest first: nothing in front of it
        for (const f of (await page.evaluate((k) => window.__polyProbe.faces(k), i)).filter((k) => away[k]).slice(0, 4)) {
          const at = await page.evaluate(([k, ff]) => window.__polyProbe.face(k, ff), [i, f]);
          await page.touchscreen.tap(at.x, at.y); await page.waitForTimeout(900);
          st = await state();
          if (st.nodes.length === want) break;   // once chosen, the RD-Hemi goes straight on
          const s = page.locator(`.poly-shape[data-shape="${HEMI}"]`).first();   // the face waits for a shape: the strip's RD-Hemi
          if (await page.locator('.poly-strip [data-more]').count() && await s.count()) { await s.tap(); await page.waitForTimeout(1200); st = await state(); if (st.nodes.length === want) break; }
        }
      }
      assert.equal(st.nodes.length, want, `${door}/${vp}: piece ${want} attached by a tap`);
    }
    assert.equal(st.connections.filter((c) => c.kind === 'face').length, 2, `${door}/${vp}: two face joins ${JSON.stringify(st.connections)}`);

    // ---- Copy build ----
    const btn = page.locator('[data-copy-build]');
    assert.equal(await btn.isVisible(), true, `${door}/${vp}: Copy build shown`);
    assert.equal((await btn.textContent()).trim(), 'Copy build');
    const box = await btn.boundingBox();
    assert.ok(box.height >= 44 && box.width >= 44, `${door}/${vp}: a full touch target (${box.width} × ${box.height})`);
    await page.evaluate(() => navigator.clipboard.writeText(''));
    await btn.tap(); await page.waitForTimeout(600);
    const rec = JSON.parse(await page.evaluate(() => navigator.clipboard.readText()));
    assert.equal(rec.app, 'Polyhedraverse'); assert.equal(rec.version, 1);
    assert.equal(rec.pieces.length, 3, `${door}/${vp}: three pieces`);
    assert.equal(rec.pieces.length, captionCount(rec.caption), `${door}/${vp}: as many pieces as the caption counts (${rec.caption})`);
    assert.equal(rec.caption, (await page.textContent('#poly-build-name')).trim(), `${door}/${vp}: the caption on screen`);
    assert.deepEqual(rec, await page.evaluate(() => window.__polyBuild()), `${door}/${vp}: the copy is window.__polyBuild()`);
    assert.equal(rec.pieces[0].parent, null);
    for (const p of rec.pieces.slice(1)) {
      assert.ok(p.parent >= 0 && p.parent < p.i && p.join === 'face', `${door}/${vp}: piece ${p.i} parent ${p.parent}`);
      assert.ok(p.face >= 0 && p.face < p.faces.length && p.parentFace >= 0 && p.parentFace < rec.pieces[p.parent].faces.length);
      assert.equal(p.solid, HEMI);
      assert.ok(p.vertices.every((v) => v.length === 3 && v.every(Number.isFinite)));
    }
    assert.match(await page.textContent('#hud-prompt'), /Build copied/, `${door}/${vp}: the note`);

    // ---- no clipboard: the dialog, text selected ----
    await page.evaluate(() => {
      Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText: () => Promise.reject(new Error('denied')) } });
      document.execCommand = () => false;
    });
    await btn.tap(); await page.waitForTimeout(600);
    assert.equal(await page.locator('#poly-copy-dialog').isVisible(), true, `${door}/${vp}: the copy-by-hand dialog`);
    const sel = await page.evaluate(() => { const ta = document.querySelector('#poly-copy-dialog textarea'); return { all: ta.selectionStart === 0 && ta.selectionEnd === ta.value.length, text: ta.value }; });
    assert.ok(sel.all, `${door}/${vp}: the text is selected`);
    assert.equal(JSON.parse(sel.text).pieces.length, 3);
    await page.tap('#poly-copy-dialog [data-close]'); await page.waitForTimeout(300);
    assert.equal(await page.locator('#poly-copy-dialog').count(), 0, `${door}/${vp}: the dialog closes`);

    // ---- back to one piece (Undo twice): hidden again ----
    await page.tap('#undo-btn'); await page.waitForTimeout(700); await page.tap('#undo-btn'); await page.waitForTimeout(900);
    assert.equal((await state()).nodes.length, 1, `${door}/${vp}: undone to one piece`);
    assert.equal(await page.locator('[data-copy-build]').count(), 0, `${door}/${vp}: Copy build hidden again`);

    assert.deepEqual(errors, [], `${door}/${vp}: page errors: ${errors.join(' | ')}`);
    console.log(`ok   ${door}/${vp}: ${rec.caption}`);
  } catch (e) {
    failures++;
    console.log(`FAIL ${door}/${vp}: ${String(e.message ?? e).split('\n').slice(0, 4).join(' | ')}`);
  }
  await ctx.close();
}
await b.close();
console.log(failures ? `${failures} failed` : 'all passed');
process.exit(failures ? 1 : 0);
