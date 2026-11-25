// DICTO's Vacuus and Resonus (DICTO 2026-11-25), through the real UI at desktop (mouse), phone and iPad (touch) sizes.
// Polyhedraverse door: search finds the truncated octahedron; its details show Vacuus and Resonus buttons; Vacuus alone shows the view
// (canvas drawn, preview hidden), a key with Vacuus only and the card's Vacuus counts from the catalogue; adding Resonus adds its key,
// the "in both" key and its card; Pull apart changes the picture; both off brings the preview back. An Archimedean polyhedron has no
// centre switch; J66 opens on the corner centroid and the volume centroid changes the card to the catalogue's volume counts. A
// polyhedron outside the catalogue (the elongated dodecahedron) shows no buttons. Kaleidohedra door: DICTO → Studies and tools
// lists Vacuus and Resonus first; tapping it opens the page with DICTO's four builds (images loaded) and the five qualities; the page
// links to Polyhedraverse and the Aequi picker, and the Aequi picker links back. No sideways scrolling; no console errors.
// PREVIEW_DIR, if set: two screenshots (desktop truncated octahedron with both on; phone J66 on its volume centroid).
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const CAT = JSON.parse(readFileSync(new URL('../../data/vacuus-resonus-catalogue.json', import.meta.url), 'utf8'));
const SIZES = { desktop: { width: 1280, height: 900 }, phone: { width: 390, height: 844 }, ipad: { width: 820, height: 1180 } };
const b = await chromium.launch();
let checks = 0;

for (const [dev, viewport] of Object.entries(SIZES)) {
  const touch = dev !== 'desktop';
  const ctx = await b.newContext({ viewport, hasTouch: touch, isMobile: touch, deviceScaleFactor: touch ? 2 : 1 });
  const page = await ctx.newPage();
  const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) errors.push(m.text()); });
  page.on('dialog', (d) => d.accept());
  const press = async (sel) => { const l = page.locator(sel).first(); await l.scrollIntoViewIfNeeded(); await l[touch ? 'tap' : 'click'](); await page.waitForTimeout(450); };
  const card = () => page.locator('[data-vr-card]').innerText();
  const keys = () => page.evaluate(() => [...document.querySelectorAll('[data-vr-key] .vr-swatch')].map((s) => s.textContent.trim()));
  const sideways = () => page.evaluate(() => { const c = document.querySelector('.dim-wizard-card'); return c.scrollWidth - c.clientWidth; });
  const openShape = async (q, id) => {
    if (!(await page.evaluate(() => document.querySelector('.dim-wizard-overlay')?.classList.contains('open')))) { await page.keyboard.press('Tab'); await page.waitForTimeout(500); }
    await page.waitForSelector('.dim-wizard-overlay.open .bm');
    const input = page.locator('.bm-search input'); await input.scrollIntoViewIfNeeded(); await input[touch ? 'tap' : 'click'](); await input.fill(q); await page.waitForTimeout(900);
    await press(`.poly-search-results [data-shape="${id}"]`);
    await page.waitForSelector('.poly-detail-name');
  };
  const tag = (s) => `${dev}: ${s}`;

  await page.goto(`${BASE}/index.html?site=polyhedraverse`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open .bm');

  // the truncated octahedron: Vacuus, then Resonus too
  await openShape('truncated octahedron', 'TRUNCATED_OCTAHEDRON');
  await page.waitForSelector('[data-vr="vacuus"]:not([hidden])');
  assert.ok(await page.locator('.poly-detail-vrbox').isHidden(), tag('the view is closed at first'));
  await press('[data-vr="vacuus"]');
  await page.waitForSelector('.poly-detail-vrbox:not([hidden]) canvas.vr-canvas');
  await page.waitForTimeout(800);
  assert.ok(await page.locator('.poly-detail-preview').isHidden(), tag('the view stands in for the preview'));
  assert.equal(await page.getAttribute('[data-vr="vacuus"]', 'aria-pressed'), 'true', tag('Vacuus pressed'));
  assert.deepEqual(await keys(), ['Vacuus'], tag('key: Vacuus only'));
  const v = CAT.TRUNCATED_OCTAHEDRON.corner.vacuus, r = CAT.TRUNCATED_OCTAHEDRON.corner.resonus;
  let text = await card();
  assert.ok(text.includes(`${v.plates} plates: ${v.full} full sheets, ${v.shared} shared sheets, ${v.single} single fins`) && text.includes(`Kind: ${v.kind}`) && !(await page.locator('[data-vr-card-resonus]').count()), tag(`Vacuus card: ${text}`));
  assert.equal(await page.locator('[data-vr-centre]').count(), 0, tag('no centre switch on an Archimedean polyhedron'));
  const cv = page.locator('.poly-detail-vrbox canvas');
  const box = await cv.boundingBox();
  assert.ok(box.width >= Math.min(300, viewport.width - 60) && box.height >= 300, tag(`a big view (${box.width}×${box.height})`));
  await press('[data-vr="resonus"]');
  assert.deepEqual(await keys(), ['Vacuus', 'Resonus', 'in both'], tag('key: Vacuus, Resonus, in both'));
  text = await card();
  assert.ok(text.includes(`${r.planes} planes: ${r.twoFaces} carry two faces`) && text.includes(`R∩V: ${CAT.TRUNCATED_OCTAHEDRON.corner.both} planes are in both`), tag(`Resonus card: ${text}`));
  // pull apart: the picture changes (the slider dragged by its real control)
  const slider = page.locator('[data-vr-pull]');
  await slider.scrollIntoViewIfNeeded();
  const sb = await slider.boundingBox();
  if (touch) await page.touchscreen.tap(sb.x + sb.width * 0.9, sb.y + sb.height / 2);
  else { await page.mouse.click(sb.x + sb.width * 0.9, sb.y + sb.height / 2); }
  await page.waitForTimeout(400);
  assert.ok(Number(await slider.inputValue()) > 60, tag(`Pull apart moved (${await slider.inputValue()})`));
  assert.ok((await sideways()) <= 0, tag('no sideways scrolling'));
  if (process.env.PREVIEW_DIR && dev === 'desktop') {
    await page.evaluate(() => document.querySelector('[data-vr-pull]').scrollIntoView({ block: 'start' }));
    await page.locator('.poly-detail-vrbox').screenshot({ path: `${process.env.PREVIEW_DIR}/PREVIEW-kmix-vacuus-resonus-desktop-truncated-octahedron.png` });
  }
  await press('[data-vr="vacuus"]'); await press('[data-vr="resonus"]');
  assert.ok(await page.locator('.poly-detail-vrbox').isHidden() && await page.locator('.poly-detail-preview').isVisible(), tag('both off: the preview is back'));
  checks += 14;

  // J66: the centre switch opens on the corner centroid; the volume centroid changes the card
  await press('.dim-wizard-back');
  await openShape('augmented truncated cube', 'J66_AUGMENTED_TRUNCATED_CUBE');
  await page.waitForSelector('[data-vr="vacuus"]:not([hidden])');
  await press('[data-vr="vacuus"]');
  await page.waitForSelector('[data-vr-centre]');
  assert.equal(await page.getAttribute('[data-vr-centre-pick="corner"]', 'aria-pressed'), 'true', tag('J66 opens on the corner centroid'));
  const jc = CAT.J66_AUGMENTED_TRUNCATED_CUBE.corner.vacuus, jv = CAT.J66_AUGMENTED_TRUNCATED_CUBE.volume.vacuus;
  assert.ok((await card()).includes(`${jc.plates} plates: ${jc.full} full sheets, ${jc.shared} shared sheets, ${jc.single} single fins`), tag('J66 corner card'));
  await press('[data-vr-centre-pick="volume"]');
  assert.equal(await page.getAttribute('[data-vr-centre-pick="volume"]', 'aria-pressed'), 'true', tag('volume centroid pressed'));
  assert.ok((await card()).includes(`${jv.plates} plates: ${jv.full} full sheets, ${jv.shared} shared sheets, ${jv.single} single fins`), tag(`J66 volume card: ${await card()}`));
  assert.ok((await sideways()) <= 0, tag('no sideways scrolling (J66)'));
  if (process.env.PREVIEW_DIR && dev === 'phone') {
    await page.waitForTimeout(600);
    await page.evaluate(() => document.querySelector('.poly-detail-vrbox').scrollIntoView({ block: 'start' }));
    await page.screenshot({ path: `${process.env.PREVIEW_DIR}/PREVIEW-kmix-vacuus-resonus-phone-j66.png` });
  }
  checks += 5;

  // outside the catalogue (the elongated dodecahedron, a parallelohedron): no buttons
  await press('.dim-wizard-back');
  await openShape('elongated dodecahedron', 'ELONGATED_DODECAHEDRON');
  await page.waitForTimeout(800);
  assert.equal(await page.locator('[data-vr]:not([hidden])').count(), 0, tag('no Vacuus or Resonus outside the catalogue'));
  checks++;
  assert.deepEqual(errors, [], tag(`console errors: ${errors.join(' | ')}`));
  await ctx.close();

  // Kaleidohedra door: Studies and tools lists Vacuus and Resonus first; it opens the page
  const ctx2 = await b.newContext({ viewport, hasTouch: touch, isMobile: touch });
  const p2 = await ctx2.newPage();
  const errs2 = []; p2.on('pageerror', (e) => errs2.push(String(e))); p2.on('console', (m) => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) errs2.push(m.text()); });
  const press2 = async (sel) => { const l = p2.locator(sel).first(); await l.scrollIntoViewIfNeeded(); await l[touch ? 'tap' : 'click'](); await p2.waitForTimeout(450); };
  await p2.goto(`${BASE}/index.html?site=kaleidohedra`);
  await p2.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await p2.keyboard.press('Enter');
  await p2.waitForSelector('.dim-wizard-overlay.open .bm');
  await press2('.bm-book[data-book="tools"] > .bm-head');
  const first = await p2.evaluate(() => { const i = document.querySelector('.bm-book[data-book="tools"] .bm-item'); return { key: i.dataset.item, text: i.textContent.replace(/\s+/g, ' ').trim() }; });
  assert.equal(first.key, 'vacuus', tag('Vacuus and Resonus first among Studies and tools'));
  assert.ok(first.text.includes('Vacuus and Resonus') && first.text.includes("DICTO's original work"), tag(`marked as DICTO's original work: ${first.text}`));
  await press2('.bm-item[data-item="vacuus"] [data-href]');
  await p2.waitForURL(/\/vacuus-resonus\/$/);
  await p2.waitForFunction(() => [...document.images].length === 4 && [...document.images].every((i) => i.complete && i.naturalWidth > 0), null, { timeout: 15000 }).catch(async () => {
    for (const i of await p2.$$('img')) await i.scrollIntoViewIfNeeded();
    await p2.waitForFunction(() => [...document.images].every((i) => i.complete && i.naturalWidth > 0), null, { timeout: 15000 });
  });
  const pg = await p2.evaluate(() => ({ q: [...document.querySelectorAll('dl.q dt')].map((d) => d.textContent), own: document.querySelector('.own')?.textContent,
    links: [...document.querySelectorAll('a')].map((a) => a.getAttribute('href')), sideways: document.documentElement.scrollWidth - document.documentElement.clientWidth }));
  assert.deepEqual(pg.q, ['Vacuus', 'Resonus', 'Aequus', 'Tacitus', 'Sphericus'], tag('the five qualities'));
  assert.equal(pg.own, "DICTO's original work", tag('marked as DICTO\'s original work'));
  assert.ok(pg.links.includes('/aequi/') && pg.links.some((h) => h.includes('polyhedraverse')), tag('links to the Aequi picker and Polyhedraverse'));
  assert.ok(pg.sideways <= 0, tag(`page: no sideways scrolling (${pg.sideways})`));
  await p2.goto(`${BASE}/aequi/`);
  assert.ok(await p2.locator('a[href="/vacuus-resonus/"]').count() >= 1, tag('the Aequi picker links to the page'));
  assert.deepEqual(errs2, [], tag(`console errors (K door / page): ${errs2.join(' | ')}`));
  checks += 8;
  await ctx2.close();
  console.log(`ok ${dev}`);
}
await b.close();
console.log(`vacuus-resonus: ${checks} checks passed`);
