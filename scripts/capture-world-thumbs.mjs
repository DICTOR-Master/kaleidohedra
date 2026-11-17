// The world menu's pictures (DICTO 2026-11-17): each world opened through the real menu (its book, then its row), its scene alone
// photographed (the panels hidden for the picture), cropped to the shape and saved small: assets/worlds/<key>.webp, 96 px.
// Then src/app/world-thumbs.js lists the worlds that have one. A world whose picture comes out blank (or that fails to open) is
// listed at the end and keeps its turning wireframe in the menu. A world that opens on an empty scene, a bare outline or a choice
// that hides its main shape is first set going through its own controls, as a visitor would (PREP below): nothing in the world
// changes for the picture. PROBE=dir also saves each world's whole screen there.
// Needs the app served (BASE_URL, default http://localhost:8000) and Playwright; run on a compute host, not the Pi:
//   python3 -m http.server 8000 &  node scripts/capture-world-thumbs.mjs   [KEYS=dodeca,up …] [DOOR=kaleidohedra]
import { chromium } from 'playwright';
import { writeFileSync, mkdirSync, readdirSync } from 'node:fs';
import { BOOKS, OTHERS_SHELF, TOOLS_SHELF } from '../src/app/book-menu-data.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000', DOOR = process.env.DOOR ?? 'kaleidohedra';
const OUT = new URL('../assets/worlds/', import.meta.url), LIST = new URL('../src/app/world-thumbs.js', import.meta.url);
mkdirSync(OUT, { recursive: true });
// [section, item key, file key]: the books' worlds, and the worlds on the shelves (Golden Rhombohedra, Generalized Permutohedra,
// Studies, Targets, Shells, Golamandalas)
const ALL = [
  ...BOOKS.flatMap((b) => b.worlds.map(([k]) => [b.id, k, k])),
  ...OTHERS_SHELF.filter((s) => s.world).map((s) => ['others', s.id, s.world]),
  ...TOOLS_SHELF.filter((s) => s.world).map((s) => ['tools', s.id, s.world]),
];
const only = process.env.KEYS?.split(',');
const todo = only ? ALL.filter(([, , k]) => only.includes(k)) : ALL;

// Worlds set going before the picture, through their own controls only.
// tapBuild: the first tap on the outline places the first piece, each further tap adds the piece across the face it lands on. Each
// tap aims at what the scene shows then (the outline need not sit at the screen's middle): its middle moved by a fraction of its
// half-width and half-height, so later taps land on the outer pieces' sides and the cluster spreads. If the cluster grows past half
// the screen, the wheel steps back, as a visitor would.
async function shapeBox() {
  const png = await page.screenshot();
  return page.evaluate(async (b64) => {
    const img = new Image(); img.src = `data:image/png;base64,${b64}`; await img.decode();
    const c = document.createElement('canvas'); c.width = img.width; c.height = img.height; const g = c.getContext('2d'); g.drawImage(img, 0, 0);
    const cv = document.getElementById('scene-canvas').getBoundingClientRect(), W = img.width, px = g.getImageData(0, 0, W, img.height).data;
    const o = (Math.round(cv.top + 4) * W + Math.round(cv.left + 4)) * 4, bg = [px[o], px[o + 1], px[o + 2]];
    let x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1;
    for (let y = Math.round(cv.top); y < cv.bottom; y++) for (let x = Math.round(cv.left); x < cv.right; x++) {
      const i = (y * W + x) * 4;
      if (Math.abs(px[i] - bg[0]) + Math.abs(px[i + 1] - bg[1]) + Math.abs(px[i + 2] - bg[2]) > 30) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
    }
    const mid = [cv.left + cv.width / 2, cv.top + cv.height / 2];
    return x1 < 0 ? { c: mid, w: 0, h: 0, cw: cv.width, ch: cv.height } : { c: [(x0 + x1) / 2, (y0 + y1) / 2], w: x1 - x0, h: y1 - y0, cw: cv.width, ch: cv.height };
  }, png.toString('base64'));
}
async function tapBuild(taps) {
  const hide = (on) => page.evaluate((v) => {
    let s = document.getElementById('thumb-hide');
    if (!s) { s = document.createElement('style'); s.id = 'thumb-hide'; s.textContent = 'body > *:not(#app), #app > *:not(#scene-canvas) { visibility: hidden !important; }'; document.head.appendChild(s); }
    s.disabled = !v;
  }, on);
  for (const [fx, fy] of taps) {
    await hide(true); let box = await shapeBox();
    for (let n = 0; n < 6 && Math.max(box.w / box.cw, box.h / box.ch) > 0.5; n++) {
      await page.mouse.move(box.cw / 2, box.ch / 2); await page.mouse.wheel(0, 400); await page.waitForTimeout(500); box = await shapeBox();
    }
    await hide(false);
    await page.mouse.click(box.c[0] + (fx * box.w) / 2, box.c[1] + (fy * box.h) / 2); await page.waitForTimeout(450);
  }
  await page.evaluate(() => document.getElementById('thumb-hide')?.remove());
  await page.waitForTimeout(1200);
}
// fractions of the shape's half-size: the first piece, one more on its front, then round its sides
const CLUSTER = [[0, 0], [0, 0], [0.6, 0], [-0.6, 0], [0, -0.6], [0, 0.6], [0.5, 0.5], [-0.5, -0.5]];
const PREP = {
  // the Star Cores' own shape, the Cube Pearl (as the menu's drawing), at its first step: the solid
  starCores: async () => { await page.selectOption('[data-sc-shape]', 'D106'); await page.waitForTimeout(2500); },
  // a full-bodied target: the first rhombic dodecahedron cell, with its face neighbours
  targets: async () => { await page.selectOption('[data-select="type"]', 'rhombic dodecahedron'); await page.selectOption('[data-select="show"]', 'neighbours'); await page.waitForTimeout(2000); },
  // every letter tapped, so all five solids' layers are in the mix
  platonicMix: async () => { for (const w of ['D', 'C', 'T', 'O', 'I']) { await page.click(`[data-pm-world="${w}"]`); await page.waitForTimeout(1500); } await page.waitForTimeout(2500); },
  // the cover's picture: the Shells view cut open (Whole), the gold Cleo core inside its shells in their colours
  whiteQueen: async () => { await page.click('#worldwhiteQueen-panel [data-wq-mode="shells"]'); await page.waitForTimeout(600); await page.click('#worldwhiteQueen-panel [data-wq-whole]'); await page.waitForTimeout(3000); },
  dictofcc: () => tapBuild(CLUSTER),
  dictohex: () => tapBuild(CLUSTER),
  // both pieces in their own colours (prolate gold, oblate blue): a few of each, then the Penrose check off
  golden: async () => {
    await tapBuild(CLUSTER.slice(0, 4));
    await page.selectOption('#worldgolden-panel [data-select="piece"]', 'oblate'); await page.waitForTimeout(400);
    await tapBuild(CLUSTER.slice(4));
    await page.click('#worldgolden-panel [data-opt="check"]'); await page.waitForTimeout(1200);
  },
  shells: () => tapBuild(CLUSTER),
  roofFold: () => tapBuild(CLUSTER),
};
const PROBE = process.env.PROBE;
if (PROBE) mkdirSync(PROBE, { recursive: true });

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 640, height: 640 }, deviceScaleFactor: 1 });
const failed = [];
let page = null;
async function fresh() {
  page?.close().catch(() => {});
  page = await ctx.newPage();
  page.on('dialog', (d) => d.accept());
  await page.goto(`${BASE}/index.html?site=${DOOR}`);
  await page.evaluate(() => localStorage.clear()); await page.reload(); // no build left from a world set going before
  await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 });
  await page.keyboard.press('Enter');
  await page.waitForSelector('.dim-wizard-overlay.open .bm', { timeout: 20000 });
}
async function openWorld(section, key) {
  if (!(await page.evaluate(() => document.querySelector('.dim-wizard-overlay')?.classList.contains('open')))) {
    await page.keyboard.press('Tab'); await page.waitForTimeout(600);
  }
  await page.waitForSelector('.dim-wizard-overlay.open .bm', { timeout: 10000 });
  const head = page.locator(`.bm-book[data-book="${section}"] > .bm-head`);
  if ((await head.getAttribute('aria-expanded')) !== 'true') await head.click();
  const row = page.locator(`.bm-book[data-book="${section}"] .bm-item[data-item="${key}"] > .bm-row`);
  await row.scrollIntoViewIfNeeded();
  if (await row.getAttribute('data-item-toggle')) {
    if ((await row.getAttribute('aria-expanded')) !== 'true') await row.click();
    await page.locator(`.bm-book[data-book="${section}"] .bm-item[data-item="${key}"] .bm-piece`).first().click();
  } else await row.click();
  await page.waitForFunction(() => !document.querySelector('.dim-wizard-overlay')?.classList.contains('open'), null, { timeout: 10000 });
  // a saved build's question (none on a fresh page), then the world drawing itself
  await page.waitForTimeout(4500);
}
// The scene alone: everything but the canvas hidden for the shot; then cropped to the shape (the square around every pixel that
// differs from the background, with a margin) and shrunk to 96 px in the page itself (webp). sd: how much the picture varies.
async function shoot() {
  await page.evaluate(() => { const s = document.createElement('style'); s.id = 'thumb-hide'; s.textContent = 'body > *:not(#app), #app > *:not(#scene-canvas) { visibility: hidden !important; }'; document.head.appendChild(s); });
  await page.waitForTimeout(400);
  const png = await page.screenshot();
  await page.evaluate(() => document.getElementById('thumb-hide')?.remove());
  return page.evaluate(async (b64) => {
    const img = new Image(); img.src = `data:image/png;base64,${b64}`; await img.decode();
    const W = img.width, H = img.height, full = document.createElement('canvas'); full.width = W; full.height = H;
    const f = full.getContext('2d'); f.drawImage(img, 0, 0);
    const px = f.getImageData(0, 0, W, H).data, bg = [px[0], px[1], px[2]];
    let x0 = W, y0 = H, x1 = -1, y1 = -1;
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
      const i = (y * W + x) * 4;
      if (Math.abs(px[i] - bg[0]) + Math.abs(px[i + 1] - bg[1]) + Math.abs(px[i + 2] - bg[2]) > 30) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
    }
    if (x1 < 0) return { url: null, sd: 0 };
    const side = Math.min(Math.max(W, H), Math.max(64, Math.round(Math.max(x1 - x0, y1 - y0) * 1.12)));
    const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    const sx = Math.max(0, Math.min(W - side, Math.round(cx - side / 2))), sy = Math.max(0, Math.min(H - side, Math.round(cy - side / 2)));
    const c = document.createElement('canvas'); c.width = c.height = 96;
    const g = c.getContext('2d'); g.fillStyle = `rgb(${bg})`; g.fillRect(0, 0, 96, 96); g.imageSmoothingQuality = 'high';
    g.drawImage(full, sx, sy, side, side, 0, 0, 96, 96);
    const d = g.getImageData(0, 0, 96, 96).data;
    let m = 0, m2 = 0; const n = d.length / 4;
    for (let i = 0; i < d.length; i += 4) { const v = (d[i] + d[i + 1] + d[i + 2]) / 3; m += v; m2 += v * v; }
    return { url: c.toDataURL('image/webp', 0.85), sd: Math.sqrt(Math.max(0, m2 / n - (m / n) ** 2)) };
  }, png.toString('base64'));
}

await fresh();
for (const [section, key, file] of todo) {
  try {
    await openWorld(section, key);
    if (PROBE) await page.screenshot({ path: `${PROBE}/${file}-open.png` });
    await PREP[file]?.();
    if (PROBE) await page.screenshot({ path: `${PROBE}/${file}.png` });
    const { url, sd } = await shoot();
    if (!url || sd < 4) { failed.push(`${file}: blank picture (sd ${sd.toFixed(1)})`); console.log(`BLANK ${file}`); }
    else { writeFileSync(new URL(`${file}.webp`, OUT), Buffer.from(url.split(',')[1], 'base64')); console.log(`ok    ${file} (sd ${sd.toFixed(1)})`); }
    if (PREP[file]) await fresh(); // a world set going leaves its state behind: start the next one clean
    else { await page.keyboard.press('Tab'); await page.waitForTimeout(500); }
  } catch (e) {
    failed.push(`${file}: ${String(e.message ?? e).split('\n')[0]}`); console.log(`FAIL  ${file}`);
    await fresh().catch(() => {});
  }
}
await browser.close();
const have = readdirSync(OUT).filter((f) => f.endsWith('.webp')).map((f) => f.slice(0, -5)).sort();
writeFileSync(LIST, `// The worlds with a picture taken in the world itself (assets/worlds/<key>.webp, 96 px), written by
// scripts/capture-world-thumbs.mjs; a world not listed shows its turning wireframe in the menu instead.
export const WORLD_THUMBS = new Set([${have.map((k) => `'${k}'`).join(', ')}]);
`);
console.log(`\n${have.length} pictures; failed: ${failed.length ? `\n  ${failed.join('\n  ')}` : 'none'}`);
