// The Queens' walls, part 2 (DICTO 2026-11-16), through the real UI on both doors (DOORS), phone (390×844, touch) and desktop
// (1280×900, mouse): the modes A and B, Cats and Dual cats tapped in the panel. A and B: A 30 plates all on mirrors, B 80 (40 mirrors,
// 40 cross walls), together all 60 mirrors (10 shared); Apart 0 puts every fin back. Cats: the Red Queen, 5 of 10 inscribed 600-cells,
// 600 glowing corners each in exactly 2, the two states disjoint inside; a copy of A (30 faces) and of B (80), Next copy steps on. Dual
// cats: A* (10 corners, 4 faces on each of 10 mirror plates, inherited heart, 60 pentagons covered), C3* heart, B* 9 faces a plate.
// A direction keeps the mode; controls hidden where they do not apply; big touch targets, no arrows; ?open=queenswalls:cats opens Cats.
// No console errors. Screenshots ($SHOTS, default /tmp/queens-cats-shots): every new mode, phone and desktop.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', SH = process.env.SHOTS ?? '/tmp/queens-cats-shots';
mkdirSync(SH, { recursive: true });
const P = '#worldqueensWalls-panel';
const DEVICES = { phone: { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true }, desktop: { viewport: { width: 1280, height: 900 } } };
const b = await chromium.launch();
let checks = 0;
const probe = (page) => page.evaluate(() => window.__queensWallsProbe());
for (const door of (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',')) {
  for (const [dev, opts] of Object.entries(DEVICES)) {
    const page = await b.newPage(opts), tag = `${door}-${dev}`, touch = !!opts.hasTouch;
    const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    const tap = async (sel, wait = 900) => { await (touch ? page.tap(sel) : page.click(sel)); await page.waitForTimeout(wait); };
    const visible = (sel) => page.locator(`${P} ${sel}`).isVisible();
    const big = async (sel, h = 44) => { const bx = await page.locator(`${P} ${sel}`).boundingBox(); assert.ok(bx && bx.height >= h && bx.width >= 44, `${tag}: ${sel} big (${bx?.width}×${bx?.height})`); };
    const shot = (name) => page.screenshot({ path: `${SH}/${tag}-${name}.png` });
    await page.goto(`${BASE}/index.html?probe&site=${door}`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
    await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(400);
    if (!(await page.locator('[data-action="tool:queensWallsWorld"]').count())) await tap('.dim-wizard-card-btn[data-dim="3D"]', 500);
    await page.locator('[data-action="tool:queensWallsWorld"]').first()[touch ? 'tap' : 'click'](); await page.waitForTimeout(400);
    if (await page.locator('#leave-dialog:not([hidden])').count()) await tap('#leave-dialog [data-choice="keep"]', 300);
    await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(1200);
    for (const m of ['ab', 'cats', 'duals']) await big(`[data-qw-mode="${m}"]`, 30);
    const touchable = async (sel) => { for (const bx of await Promise.all((await page.locator(`${P} ${sel}`).all()).map((l) => l.boundingBox()))) assert.ok(bx.height >= 30 && bx.width >= 44, `${tag}: ${sel} touchable (${bx.width}×${bx.height})`); };
    const apart = async (v) => { await page.locator(`${P} .qw-apart-row input`).fill(String(v)); await page.waitForTimeout(400); };

    // ---- A and B ----
    await tap(`${P} [data-qw-mode="ab"]`, 1500);
    let st = await probe(page);
    assert.deepEqual([st.mode, st.queen, st.ab], ['ab', 'white', 'both'], `${tag}: A and B`);
    assert.deepEqual([st.stats.A.plates, st.stats.A.mirrors, st.stats.A.cross, st.stats.B.plates, st.stats.B.mirrors, st.stats.B.cross], [30, 30, 0, 80, 40, 40], `${tag}: plates`);
    assert.deepEqual([st.mirrorsUsed, st.mirrorsShared, st.crossUsed], [60, 10, 40], `${tag}: walls used`); checks++;
    await touchable('.qw-ab button');
    assert.ok(!(await visible('.qw-queens')) && (await visible('.qw-ab')) && !(await visible('.qw-states')) && !(await visible('.qw-duals')) && (await visible('.qw-apart-row')), `${tag}: only what applies`); checks++;
    assert.deepEqual(st.kinds, [['queen', 'heart'], ['A', 'nonheart'], ['B', 'nonheart']]);
    assert.match(await page.locator(`${P} .qw-kind`).textContent(), /White Queen: heart · A: non-heart · B: non-heart/); checks++;
    await apart(500); await shot('ab-both');
    await apart(0); st = await probe(page); assert.ok(st.moved < 1e-6, `${tag}: Apart 0`);
    await apart(800); st = await probe(page); assert.ok(st.moved > 0.01, `${tag}: Apart moves the fins`); checks++;
    await tap(`${P} [data-qw-ab="A"]`); st = await probe(page);
    assert.deepEqual([st.ab, Object.keys(st.stats), st.mirrorsUsed, st.crossUsed], ['A', ['A'], 30, 0], `${tag}: A alone`);
    assert.match(await page.locator(`${P} .ch-param-caption`).textContent(), /every plate of A lies on a wall of the 600-cell/); checks++;
    await apart(500); await shot('ab-A');
    await tap(`${P} [data-qw-ab="B"]`); st = await probe(page);
    assert.deepEqual([st.ab, st.stats.B.plates, st.mirrorsUsed, st.crossUsed], ['B', 80, 40, 40], `${tag}: B alone`); checks++;
    await shot('ab-B');
    await tap(`${P} [data-qw-dir="edge-first"]`); st = await probe(page);
    assert.deepEqual([st.mode, st.dir, st.ab], ['ab', 'edge-first', 'B'], `${tag}: a direction keeps the mode`); checks++;
    await tap(`${P} [data-qw-dir="vertex-first"]`);

    // ---- Cats ----
    await tap(`${P} [data-qw-mode="cats"]`, 2500); st = await probe(page);
    assert.deepEqual([st.mode, st.queen, st.state, st.cellsShown, st.inscribed, st.glow, st.membership, st.disjoint, st.copy], ['cats', 'red', 0, 5, 10, 600, [2], true, null], `${tag}: Cats state 1`);
    assert.equal(st.lines, 3600, `${tag}: 5 × 720 edges`); checks++;
    assert.ok(!(await visible('.qw-apart-row')) && !(await visible('.qw-ab')) && (await visible('.qw-states')) && !(await visible('[data-qw-next]')), `${tag}: only what applies in Cats`);
    await touchable('.qw-copies button:not([hidden])');
    await big('[data-qw-state="0"]', 46); await big('[data-qw-state="1"]', 46); checks++;
    assert.deepEqual(st.kinds, [['queen', 'heart'], ['inscribed', 'heart']]); checks++;
    await shot('cats-state1');
    await tap(`${P} [data-qw-state="1"]`, 1200); st = await probe(page);
    assert.deepEqual([st.state, st.cellsShown, st.disjoint, st.membership], [1, 5, true, [2]], `${tag}: state 2`); checks++;
    await shot('cats-state2');
    await tap(`${P} [data-qw-copy="A"]`, 2500); st = await probe(page);
    assert.deepEqual([st.copy.type, st.copy.n, st.copy.orbit, st.copy.corners, st.copy.faces, st.copy.plates, st.copy.kind], ['A', 0, 'A', 20, 30, 30, 'nonheart'], `${tag}: a copy of A`);
    assert.equal(st.lines, 720 + 40, `${tag}: its 600-cell and its 40 edges`);
    await big('[data-qw-next]', 46); checks++;
    await shot('cats-copyA');
    await tap(`${P} [data-qw-next]`, 1200); st = await probe(page);
    assert.deepEqual([st.copy.n, st.copy.orbit, st.copy.faces], [1, '-A', 30], `${tag}: Next copy`);
    assert.match(await page.locator(`${P} .ch-param-caption`).textContent(), /copy 2 of the 600 copies of A and −A in state 2 \(1200 in the 120-cell\)/); checks++;
    await tap(`${P} [data-qw-copy="B"]`, 2500); st = await probe(page);
    assert.deepEqual([st.copy.type, st.copy.corners, st.copy.faces, st.copy.plates, st.copy.kind], ['B', 30, 80, 80, 'nonheart'], `${tag}: a copy of B`); checks++;
    await shot('cats-copyB');
    await tap(`${P} [data-qw-copy="none"]`, 1200); st = await probe(page); assert.equal(st.copy, null);
    assert.ok(!(await visible('[data-qw-next]')), `${tag}: Next hidden without a copy`); checks++;

    // ---- Dual cats ----
    await tap(`${P} [data-qw-mode="duals"]`, 1500); st = await probe(page);
    assert.deepEqual([st.mode, st.queen, st.dual, st.corners, st.edges, st.faces, st.cells, st.plates, st.onMirrors, st.facesPerPlate, st.covered, st.pentagons], ['duals', 'red', 'A', 10, 30, 40, 20, 10, true, [4], 60, 120], `${tag}: A*`);
    assert.deepEqual(st.kinds, [['queen', 'heart'], ['A*', 'inherited']]);
    assert.match(await page.locator(`${P} .qw-kind`).textContent(), /A\*: inherited heart/); checks++;
    await touchable('.qw-duals button');
    assert.ok((await visible('.qw-duals')) && (await visible('.qw-apart-row')) && !(await visible('.qw-states')), `${tag}: only what applies in Dual cats`); checks++;
    await apart(300); await shot('duals-A');
    await tap(`${P} [data-qw-dual="C3"]`); st = await probe(page);
    assert.deepEqual([st.dual, st.corners, st.facesPerPlate, st.kinds[1][1], st.covered], ['C3', 30, [6], 'heart', 60], `${tag}: C3*`); checks++;
    await tap(`${P} [data-qw-dual="-B"]`); st = await probe(page);
    assert.deepEqual([st.dual, st.corners, st.faces, st.facesPerPlate, st.kinds[1][1]], ['-B', 20, 90, [9], 'inherited'], `${tag}: −B*`); checks++;
    await shot('duals-mB');
    await apart(0); st = await probe(page); assert.ok(st.moved < 1e-6, `${tag}: Apart 0 in Dual cats`); checks++;

    assert.ok(!/[◀▶]/.test(await page.locator(P).textContent()), `${tag}: no arrows`); checks++;
    // back to the part-1 modes: the Queen switch returns
    await tap(`${P} [data-qw-mode="sheets"]`, 1200); st = await probe(page);
    assert.deepEqual([st.mode, st.pieces], ['sheets', 60]); assert.ok(await visible('.qw-queens')); checks++;
    assert.deepEqual(errors, [], `${tag}: console`); await page.close();
  }
}
const page = await b.newPage({ viewport: { width: 820, height: 1180 }, hasTouch: true, isMobile: true });
await page.goto(`${BASE}/index.html?probe&site=kaleidohedra&open=queenswalls:cats`);
await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 25000 }); await page.keyboard.press('Enter');
await page.waitForSelector(`${P}.visible`); await page.waitForTimeout(2500);
const st = await probe(page);
assert.deepEqual([st.mode, st.queen], ['cats', 'red']); checks++;
await b.close(); console.log(`queens-cats: ${checks} checks ok`);
