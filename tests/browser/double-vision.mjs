// The Double Vision world (DICTO 2026-10-16) through the real UI on an iPad: opened from the DICTO wizard (first of DICTO's worlds),
// the paper's preset (Interlock, ends shared, 536 pieces), the toggle to middle (502), the three views, a tapped piece named, the
// slider, the film (unwrap, pause, wrap, scrub), Reset back to the paper, X-ray offered, the leave dialog on going to another world (Keep / Put back), and the ?open= link;
// no errors. Screenshots.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const b = await chromium.launch(); const page = await b.newPage({ viewport: { width: 1024, height: 1366 }, hasTouch: true, isMobile: true });
const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
const SH = process.env.SHOTS ?? '/tmp', BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const panel = '#worlddoublevision-panel';
const note = () => page.locator(`${panel} .dv-note`).textContent();
await page.goto(`${BASE}/index.html?site=kaleidohedra`);
await page.waitForSelector('#welcome-overlay', { state: 'visible' }); await page.keyboard.press('Enter');
await page.waitForSelector('.dim-wizard-overlay.open');
if (!(await page.locator('[data-action="tool:doubleVisionWorld"]').count())) await page.tap('.dim-wizard-card-btn[data-dim="3D"]');
await page.waitForTimeout(500);
const worlds = await page.evaluate(() => [...document.querySelectorAll('[data-action]')].map((e) => e.dataset.action).filter((a) => /World/.test(a)));
console.log('first DICTO worlds:', worlds.slice(0, 3).join(', '));
assert.equal(worlds.filter((a) => a === 'tool:doubleVisionWorld').length, 1, 'listed once');
const btn = page.locator('[data-action="tool:doubleVisionWorld"]').first(); await btn.scrollIntoViewIfNeeded(); await btn.tap();
await page.waitForTimeout(500);
if (await page.locator('#leave-dialog:not([hidden])').count()) await page.tap('#leave-dialog [data-choice="keep"]');
await page.waitForFunction(() => /536/.test(document.querySelector('#worlddoublevision-panel .dv-note')?.textContent ?? ''), null, { timeout: 15000 });
console.log('preset:', (await note()).slice(0, 120));
assert.match(await note(), /536 exact pieces of 12 kinds/); assert.match(await note(), /Dharma-Ends/);
await page.screenshot({ path: `${SH}/dv-interlock-ends.png` });

// a piece named by a tap at the centre of the view (the next turn in sits there)
const box = await page.locator('canvas').first().boundingBox();
await page.touchscreen.tap(box.x + box.width / 2, box.y + box.height * 0.4); await page.waitForTimeout(600);
const hud = await page.evaluate(() => [...document.querySelectorAll('body *')].map((e) => e.childElementCount ? '' : e.textContent).find((s) => /I1·\d+ \(/.test(s)) ?? '');
console.log('tapped:', hud); assert.match(hud, /I1·\d+ \((12f|11f|7f|6f|TBP|HPy|PPy|QPy|Tet)\): \d+ per turn/);
await page.screenshot({ path: `${SH}/dv-kind.png` });

// the toggle: middle shared
await page.tap(`${panel} [data-dv-setting="middle"]`); await page.waitForTimeout(900);
assert.match(await note(), /502 exact pieces of 11 kinds/); assert.match(await note(), /Dharma-Middle/);
await page.screenshot({ path: `${SH}/dv-interlock-middle.png` });
// views
await page.tap(`${panel} [data-dv-mode="cycles"]`); await page.waitForTimeout(900);
assert.match(await note(), /icosidodecahedron and the rhombic triacontahedron/);
assert.equal(await page.locator(`${panel} [data-dv="slice"]`).isHidden(), true, 'no slice button on the shells');
await page.screenshot({ path: `${SH}/dv-cycles-middle.png` });
await page.locator(`${panel} .dv-mix-row input`).fill('100'); await page.waitForTimeout(400);
await page.screenshot({ path: `${SH}/dv-cycles-flipped.png` });
await page.tap(`${panel} [data-dv-mode="layer"]`); await page.waitForTimeout(900);
await page.tap(`${panel} [data-dv-layer="4"]`); await page.waitForTimeout(700);
console.log('layer:', await note()); assert.match(await note(), /H → RT.*180 pieces/);
await page.screenshot({ path: `${SH}/dv-layer.png` });
// the film (the ∞ control: Wrap ◀ left ring, Unwrap ▶ right ring, VHS pause; a light runs round the ∞ while playing): Unwrap plays (no slider while playing), tapping it again pauses, Wrap runs backwards; screenshots along the way
await page.tap(`${panel} [data-dv-mode="interlock"]`); await page.waitForTimeout(800);
await page.tap(`${panel} [data-dv-film="unwrap"]`); await page.waitForTimeout(400);
assert.equal(await page.locator(`${panel} .dv-inf.run`).count(), 1, 'the ∞ lights up while playing'); assert.equal(await page.locator(`${panel} .dv-film-row`).isHidden(), true, 'no position while playing');
const f0 = Number(await page.locator(`${panel} .dv-film-row input`).inputValue());
for (const k of [1, 2, 3]) { await page.waitForTimeout(2600); await page.screenshot({ path: `${SH}/dv-film-${k}.png` }); }
const f1 = Number(await page.locator(`${panel} .dv-film-row input`).inputValue());
console.log('film position', f0, '->', f1); assert.ok(f1 > f0, 'the film moves forwards');
await page.tap(`${panel} [data-dv-film="unwrap"]`); await page.waitForTimeout(300);
const p1 = await page.locator(`${panel} .dv-film-row input`).inputValue(); await page.waitForTimeout(1500);
assert.equal(await page.locator(`${panel} .dv-film-row input`).inputValue(), p1, 'paused');
// the VHS pause: resumes the last direction (unwrap), then pauses again
await page.tap(`${panel} [data-dv-pause]`); await page.waitForTimeout(1500);
assert.notEqual(await page.locator(`${panel} .dv-film-row input`).inputValue(), p1, 'pause button resumes');
await page.tap(`${panel} [data-dv-pause]`); await page.waitForTimeout(300);
const p2 = await page.locator(`${panel} .dv-film-row input`).inputValue(); await page.waitForTimeout(1200);
assert.equal(await page.locator(`${panel} .dv-film-row input`).inputValue(), p2, 'pause button pauses');
await page.screenshot({ path: `${SH}/dv-inf-paused.png` });
await page.tap(`${panel} [data-dv-film="wrap"]`); await page.waitForTimeout(4500);
const f2 = Number(await page.locator(`${panel} .dv-film-row input`).inputValue());
console.log('after wrap', p2, '->', f2); assert.ok(f2 !== Number(p2), 'wrap moves');
assert.equal(await page.locator(`${panel} .dv-inf.run.rev`).count(), 1, 'the ∞ runs backwards for Wrap'); assert.equal(await page.locator(`${panel} .dv-film-row`).isHidden(), true, 'no position while playing');
await page.screenshot({ path: `${SH}/dv-chev-wrap.png` });
await page.tap(`${panel} [data-dv-pause]`); await page.waitForTimeout(300); assert.equal(await page.locator(`${panel} .dv-scrub`).isVisible(), true, 'slider when paused'); assert.equal(await page.locator(`${panel} .dv-inf.run`).count(), 0, 'the ∞ rests when paused');
await page.locator(`${panel} .dv-film-row input`).fill('300'); await page.waitForTimeout(500); await page.screenshot({ path: `${SH}/dv-film-scrub.png` });
// X-ray offered
assert.equal(await page.locator('#xray-toggle').isHidden(), false, 'X-ray offered');
// Reset back to the paper
await page.tap(`${panel} [data-dv="reset"]`); await page.waitForTimeout(900);
assert.match(await note(), /536 exact pieces/); assert.equal(await page.locator(`${panel} [data-dv="reset"]`).isHidden(), true);
// leave after a change: the dialog asks Keep / Put back
await page.tap(`${panel} [data-dv-setting="middle"]`); await page.waitForTimeout(1200);
await page.tap('#hud-world-back'); await page.waitForTimeout(700);
// leaving = picking another world (Back only opens the wizard over this one)
const other = page.locator('[data-action="tool:theaetetusWorld"]').first(); await other.scrollIntoViewIfNeeded(); await other.tap(); await page.waitForTimeout(700);
const asked = await page.locator('#leave-dialog:not([hidden])').count();
console.log('leave dialog shown:', !!asked); assert.ok(asked, 'leave dialog');
await page.tap('#leave-dialog [data-choice="discard"]'); await page.waitForTimeout(700);
const saved = await page.evaluate(() => Object.entries(localStorage).find(([k]) => /doublevision$/.test(k))?.[1] ?? '');
console.log('after Put back:', saved); assert.match(saved, /"setting":"ends"/);
// ?open= link
await page.goto(`${BASE}/index.html?site=kaleidohedra&open=doubleVision`);
await page.waitForFunction(() => /exact pieces/.test(document.querySelector('#worlddoublevision-panel .dv-note')?.textContent ?? ''), null, { timeout: 15000 });
assert.deepEqual(errors, []);
console.log('double vision ok'); await b.close();
