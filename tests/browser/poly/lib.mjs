// Helpers for Polyhedraverse's browser tests (step D6: the old site's 23 Playwright specs, ported to
// the joined app). Each test opens the Polyhedraverse door on a phone-sized touch screen, with the
// read-only ?probe (render.js) that says where a piece's faces and corners are on screen, so taps
// land on the real canvas. Long-press is a real held touch (Chrome DevTools touch events).
import assert from 'node:assert/strict';

export const BASE_URL = process.env.BASE_URL ?? 'http://localhost:8000';
export const SAVE_KEY = 'polyhedraverse-poly-world';
export { assert };
export const at = (shape, position = [0, 0, 0], quaternion = [0, 0, 0, 1], id = `n${Math.random().toString(36).slice(2, 8)}`) => ({ id, shape, transform: { position, quaternion } });

/** Open the Polyhedraverse door. build: { nodes, connections, view } saved before load; old: an old-site save. */
export async function open(browser, { build, old, wizard = false, lang } = {}) {
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true, acceptDownloads: true });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', (e) => errors.push(String(e)));
  page.on('console', (m) => { if (m.type() === 'error' && !/favicon|Failed to load resource/.test(m.text())) errors.push(m.text()); });
  page.on('dialog', (d) => d.accept());
  await ctx.addInitScript(({ key, build, old, lang }) => {
    if (sessionStorage.getItem('seeded')) return; // seed once; reloads keep what the app saved
    sessionStorage.setItem('seeded', '1');
    if (build) localStorage.setItem(key, JSON.stringify({ version: 1, connections: [], view: {}, ...build }));
    if (old) localStorage.setItem('polyhedraverse:assembly', JSON.stringify(old));
    if (lang) localStorage.setItem('polyhedraverse-settings', JSON.stringify({ language: lang }));
  }, { key: SAVE_KEY, build, old, lang });
  await page.goto(`${BASE_URL}/index.html?site=polyhedraverse&probe`);
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 });
  await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open', { timeout: 10000 });
  if (!wizard) await closeDicto(page);
  const cdp = await ctx.newCDPSession(page);
  return helpers(page, ctx, cdp, errors);
}
export async function closeDicto(page) {
  if (await page.evaluate(() => document.querySelector('.dim-wizard-overlay')?.classList.contains('open'))) {
    await page.tap('.dim-wizard-close');
    await page.waitForTimeout(400);
  }
}

function helpers(page, ctx, cdp, errors) {
  const h = {
    page, ctx, errors,
    wait: (ms = 500) => page.waitForTimeout(ms),
    saved: () => page.evaluate((k) => JSON.parse(localStorage.getItem(k) ?? 'null'), SAVE_KEY),
    state: () => page.evaluate(() => window.__polyProbe.state()),
    shapes: async () => (await h.state()).nodes.map((n) => n.shape),
    /** Face indices of node i, most camera-facing first. */
    faces: (i) => page.evaluate((i) => window.__polyProbe.faces(i), i),
    async tap(p) { await page.touchscreen.tap(p.x, p.y); await page.waitForTimeout(700); },
    async tapFace(i, f) { await h.tap(await page.evaluate(([i, f]) => window.__polyProbe.face(i, f), [i, f])); },
    async tapCorner(i, f, v) { await h.tap(await page.evaluate(([i, f, v]) => window.__polyProbe.corner(i, f, v), [i, f, v])); },
    /** The most camera-facing face of node i with n sides (any if n is omitted). */
    async frontFace(i, n) {
      const spec = await page.evaluate(async ([i]) => { const { POLYHEDRA } = await import('./src/krp-core/src/polyhedra/index.js'); return POLYHEDRA[window.__polyProbe.state().nodes[i].shape].faces.map((f) => f.length); }, [i]);
      return (await h.faces(i)).find((f) => n == null || spec[f] === n);
    },
    async faceVertex(i, f) { return page.evaluate(async ([i, f]) => { const { POLYHEDRA } = await import('./src/krp-core/src/polyhedra/index.js'); return POLYHEDRA[window.__polyProbe.state().nodes[i].shape].faces[f][0]; }, [i, f]); },
    async longPress(p) {
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: p.x, y: p.y }] });
      await page.waitForTimeout(700);
      await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
      await page.waitForTimeout(600);
    },
    async longPressFace(i, f) { await h.longPress(await page.evaluate(([i, f]) => window.__polyProbe.face(i, f), [i, f])); },
    offers: () => page.evaluate(() => [...document.querySelectorAll('.poly-strip .poly-shape')].map((b) => b.dataset.shape)),
    async pick(id) { await page.tap(`.poly-strip .poly-shape[data-shape="${id}"]`); await page.waitForTimeout(900); },
    prompt: () => page.evaluate(() => document.getElementById('hud-prompt')?.textContent ?? ''),
    async dicto() { await page.keyboard.press('Tab'); await page.waitForSelector('.dim-wizard-overlay.open'); await page.waitForTimeout(300); },
    async family(key) { if (!(await page.evaluate(() => document.querySelector('.dim-wizard-overlay')?.classList.contains('open')))) await h.dicto(); await page.tap(`.dicto-dim-content [data-family="${key}"]`); await page.waitForTimeout(600); },
    async details(id) { await page.tap(`[data-action="tool:polyShape:${id}"]`); await page.waitForTimeout(700); },
    async undo() { await page.tap('#undo-btn'); await page.waitForTimeout(700); },
    async settings() { await page.tap('#lab-toggle'); await page.waitForTimeout(500); },
    async close() { await ctx.close(); },
    noErrors() { assert.deepEqual(errors, [], `page errors: ${errors.join(' | ')}`); },
  };
  return h;
}
