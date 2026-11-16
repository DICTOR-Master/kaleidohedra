// DICTO Vacuus, Fins apart and the three kinds (DICTO 2026-11-16), through the real UI on the Polyhedraverse door, phone (touch) and
// desktop (mouse): a one-piece octahedron (heart: 3 full square sheets) and a one-piece tetrahedron (non-heart: 6 single fins); the lens
// button, the Fins view, the kind label, the Apart slider in Fins, the Sheet kinds colouring and its key. No console errors.
// Screenshots ($SHOTS): the octahedron and the tetrahedron in Fins, apart, coloured by kind.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { mkdirSync } from 'node:fs';

const SH = process.env.SHOTS ?? '/tmp/vacuus-fins-shots', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
mkdirSync(SH, { recursive: true });
const DEVICES = { phone: { viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true }, desktop: { viewport: { width: 1280, height: 900 } } };
const CASES = [
  { id: 'D8', name: 'octahedron', kind: 'heart', label: 'heart', plates: 3, counts: { full: 3, shared: 0, single: 0 }, key: /full sheet ×3/ },
  { id: 'D4', name: 'tetrahedron', kind: 'nonheart', label: 'non-heart', plates: 6, counts: { full: 0, shared: 0, single: 6 }, key: /single fin ×6/ },
];
const b = await chromium.launch();
let checks = 0;
for (const [dev, opts] of Object.entries(DEVICES)) {
  const page = await b.newPage(opts), touch = !!opts.hasTouch;
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('dialog', (d) => d.accept());
  const press = (sel) => (touch ? page.tap(sel) : page.click(sel));
  const probe = () => page.evaluate(() => window.__vacuusProbe());
  for (const c of CASES) {
    const tag = `${dev} ${c.name}`;
    await page.goto(`${BASE}/index.html?site=polyhedraverse&probe`);
    await page.evaluate((s) => localStorage.setItem('polyhedraverse-poly-world', JSON.stringify({ version: 1, connections: [], view: { shape: s },
      nodes: [{ id: 'n1', shape: s, transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } }] })), c.id);
    await page.goto(`${BASE}/index.html?site=polyhedraverse&probe`); await page.waitForTimeout(1500);
    if (await page.locator('#welcome-overlay').isVisible()) await page.keyboard.press('Enter');
    await page.waitForTimeout(1500);
    if (await page.locator('.dim-wizard-overlay.open').count()) { await press('.dim-wizard-close'); await page.waitForTimeout(500); }
    if (await page.locator('#leave-dialog:not([hidden]) [data-choice="continue"]').count()) { await press('#leave-dialog [data-choice="continue"]'); await page.waitForTimeout(400); }
    await press('[data-vac]'); await page.waitForTimeout(600);
    // the kind label and the Sheet kinds button only in Fins (nothing unnecessary shown)
    assert.equal(await page.locator('[data-vac-kind]').count(), 0, `${tag}: no kind label in Pyramids`);
    await press('[data-vac-view="sheets"]'); await page.waitForTimeout(800);
    let st = await probe();
    assert.equal(st.view, 'sheets'); assert.equal(st.kind, c.kind); assert.equal(st.plates, c.plates); assert.deepEqual(st.sheetCounts, c.counts, `${tag}: sheets`);
    assert.equal(await page.getAttribute('[data-vac-kind]', 'data-vac-kind'), c.kind);
    assert.equal((await page.textContent('[data-vac-kind]')).trim(), `Kind: ${c.label}`, `${tag}: kind label`); checks++;
    const kb = await page.locator('[data-vac-kinds]').boundingBox(); assert.ok(kb.height >= 30 && kb.width >= 44, `${tag}: Sheet kinds touchable`);
    // Apart in Fins: the slider is there and moves the sheets
    const slider = page.locator('[data-vac-apart]');
    assert.equal(await slider.count(), 1, `${tag}: Apart in Fins`);
    await slider.fill('0'); await page.waitForTimeout(500); assert.equal((await probe()).apart, 0);
    await slider.fill('70'); await page.waitForTimeout(800); st = await probe(); assert.equal(st.apart, 70, `${tag}: apart`); checks++;
    // the sheets by kind, with their key
    await press('[data-vac-kinds]'); await page.waitForTimeout(800); st = await probe();
    assert.equal(st.kinds, true); assert.equal(await page.getAttribute('[data-vac-kinds]', 'aria-pressed'), 'true');
    assert.match(await page.textContent('.vac-legend'), c.key, `${tag}: key`); checks++;
    await page.waitForTimeout(800);
    await page.screenshot({ path: `${SH}/${dev}-${c.name}-fins-apart.png` });
    await press('[data-vac-kinds]'); await page.waitForTimeout(400); assert.equal((await probe()).kinds, false);
    // the other views: no kind label, no Sheet kinds
    await press('[data-vac-view="struts"]'); await page.waitForTimeout(500);
    assert.equal(await page.locator('[data-vac-kind]').count(), 0); assert.equal(await page.locator('[data-vac-apart]').count(), 0, `${tag}: no Apart in Struts`); checks++;
    await press('[data-vac-off]'); await page.waitForTimeout(400);
  }
  assert.deepEqual(errors, [], `${dev}: console`); await page.close();
}
await b.close(); console.log(`vacuus-fins: ${checks} checks ok`);
