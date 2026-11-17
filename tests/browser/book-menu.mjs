// The world menu by the books (DICTO 2026-11-17, "build it"), through the real menu by touch on a phone (400×844) and with a mouse on
// a desktop (1280×900), through both doors (DOORS, default Kaleidohedra and Rhombiverse): DICTO → 3D+ shows a search box, then each
// book with a world of its own in series order (One … Eight, Ten), folded, each heading neutral (no ring or app colour) with its cover,
// "Book N", title and count, then the others' lattices and tilings and the studies and tools. Every world is listed once. Tapping a book
// opens it; tapping a world opens it (its title in the HUD). Searching "Golden Rhombohedra" leaves only the 3D Penrose tiling's entry,
// which opens Golden Rhombohedra; a name that matches nothing says so. The same entries in the same order through both doors. Big
// touch targets; no sideways scrolling on the phone. No console errors. PREVIEW_PHONE / PREVIEW_DESKTOP, if set: screenshots of the
// Kaleidohedra door with Book One open.
import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import { BOOKS } from '../../src/app/book-menu-data.js';

const BASE = process.env.BASE_URL ?? 'http://localhost:8000';
const DOORS = (process.env.DOORS ?? 'kaleidohedra,rhombiverse').split(',');
const SECTIONS = [...BOOKS.filter((b) => b.worlds.length).map((b) => b.id), 'others', 'tools'];
const b = await chromium.launch();
let checks = 0;
const orders = {};
const grey = (rgb) => { const [r, g, bl] = rgb.match(/\d+/g).map(Number); return Math.max(r, g, bl) - Math.min(r, g, bl) <= 24; };

for (const door of DOORS) {
  for (const [dev, viewport] of Object.entries({ phone: { width: 400, height: 844 }, desktop: { width: 1280, height: 900 } })) {
    const touch = dev === 'phone', tag = `${door}-${dev}`;
    const page = await b.newPage({ viewport, hasTouch: touch, isMobile: touch });
    const errors = []; page.on('pageerror', (e) => errors.push(String(e))); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('dialog', (d) => d.accept());
    const press = async (sel) => { const l = page.locator(sel).first(); await l.scrollIntoViewIfNeeded(); await l[touch ? 'tap' : 'click'](); await page.waitForTimeout(350); };
    const menu = async () => {
      if (!(await page.evaluate(() => document.querySelector('.dim-wizard-overlay')?.classList.contains('open')))) { await page.keyboard.press('Tab'); await page.waitForTimeout(500); }
      await page.waitForSelector('.dim-wizard-overlay.open .bm');
    };
    const title = () => page.evaluate(() => document.getElementById('hud-world-title')?.textContent.trim());
    await page.goto(`${BASE}/index.html?site=${door}`);
    await page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await page.keyboard.press('Enter');
    await menu();

    // the books, then the shelves; folded; neutral headings; touch-size; nothing sideways
    const read = await page.evaluate(() => ({
      sections: [...document.querySelectorAll('.bm-book')].map((s) => s.dataset.book),
      folded: [...document.querySelectorAll('.bm-list')].every((l) => l.hidden),
      heads: [...document.querySelectorAll('.bm-head')].map((h) => { const r = h.getBoundingClientRect(), cs = getComputedStyle(h); return { h: r.height, w: r.width, color: cs.color, bg: cs.backgroundColor, border: cs.borderLeftColor, num: h.querySelector('.bm-num')?.textContent, cover: !!h.querySelector('img.bm-cover') }; }),
      items: [...document.querySelectorAll('.bm-item')].map((i) => i.dataset.item),
      actions: [...document.querySelectorAll('.bm [data-action]')].map((e) => e.dataset.action),
      rings: document.querySelectorAll('.dicto-ring, .dicto-ring-jump').length,
      search: !!document.querySelector('.bm > .bm-search input[type=search]'),
      sideways: document.querySelector('.dim-wizard-card').scrollWidth - document.querySelector('.dim-wizard-card').clientWidth,
    }));
    assert.deepEqual(read.sections, SECTIONS, `${tag}: books in series order, then the two shelves`);
    assert.ok(read.search, `${tag}: a search box at the top`);
    assert.ok(read.folded, `${tag}: every book folded`);
    assert.equal(read.rings, 0, `${tag}: no ring labels or headings`);
    assert.ok(read.heads.every((h) => grey(h.color) && (h.bg === 'rgba(0, 0, 0, 0)' || grey(h.bg))), `${tag}: neutral headings ${JSON.stringify(read.heads.map((h) => [h.color, h.bg]))}`);
    assert.ok(read.heads.every((h) => h.h >= 48), `${tag}: big headings to touch`);
    assert.deepEqual(read.heads.slice(0, -2).map((h) => h.num), ['Book One', 'Book Two', 'Book Three', 'Book Four', 'Book Five', 'Book Six', 'Book Seven', 'Book Eight', 'Book Ten'], `${tag}: "Book N" on each book`);
    assert.ok(read.heads.slice(0, -2).every((h) => h.cover), `${tag}: a cover on each book`);
    assert.ok(read.sideways <= 0, `${tag}: no sideways scrolling (${read.sideways}px)`);
    // every entry once
    const dup = read.actions.filter((a, i) => read.actions.indexOf(a) !== i);
    assert.deepEqual(dup, [], `${tag}: every world and piece listed once`);
    const worlds = BOOKS.flatMap((bk) => bk.worlds.map(([k]) => k));
    assert.deepEqual(read.items.slice(0, worlds.length), worlds, `${tag}: each book's worlds in paper order`);
    orders[tag] = read.items;
    checks += 11;

    // a book opens on a tap; its rows are touch-size, each with a picture
    await press('.bm-book[data-book="Four"] > .bm-head');
    const four = await page.evaluate(() => { const s = document.querySelector('.bm-book[data-book="Four"]');
      return { open: !s.querySelector('.bm-list').hidden, rows: [...s.querySelectorAll('.bm-item > .bm-row')].map((r) => ({ h: r.getBoundingClientRect().height, pic: !!r.querySelector('.bm-thumb, canvas') })) }; });
    assert.ok(four.open, `${tag}: Book Four opens on a tap`);
    assert.equal(four.rows.length, 8, `${tag}: Book Four's eight worlds`);
    assert.ok(four.rows.every((r) => r.h >= 48 && r.pic), `${tag}: rows big enough to touch, each with a picture`);
    // a world opens from its row
    await press('.bm-book[data-book="Four"] [data-action="tool:theaetetusWorld"]');
    await page.waitForFunction(() => !document.querySelector('.dim-wizard-overlay')?.classList.contains('open'));
    await page.waitForTimeout(800);
    assert.equal(await title(), 'Theaetetus', `${tag}: Theaetetus opens from Book Four`);
    checks += 4;

    // the search: "Golden Rhombohedra" finds the 3D Penrose tiling's entry, which opens the world
    await menu();
    const input = page.locator('.bm-search input');
    await input.scrollIntoViewIfNeeded(); await input[touch ? 'tap' : 'click'](); await input.fill('Golden Rhombohedra'); await page.waitForTimeout(700);
    const hits = await page.evaluate(() => [...document.querySelectorAll('.bm-item')].filter((i) => !i.hidden && !i.closest('.bm-book').hidden).map((i) => i.dataset.item));
    assert.deepEqual(hits, ['golden'], `${tag}: the search finds Golden Rhombohedra only (${hits})`);
    await press('.bm-item[data-item="golden"] [data-action="tool:goldenWorld"]');
    await page.waitForFunction(() => !document.querySelector('.dim-wizard-overlay')?.classList.contains('open'));
    await page.waitForTimeout(800);
    assert.equal(await title(), 'Golden Rhombohedra', `${tag}: Golden Rhombohedra opens from the search`);
    await menu();
    const again = page.locator('.bm-search input'); await again.fill('zzqx'); await page.waitForTimeout(600);
    assert.ok(await page.locator('.bm-none').isVisible(), `${tag}: "no world by that name"`);
    await again.fill(''); await page.waitForTimeout(600);
    assert.ok(await page.evaluate(() => [...document.querySelectorAll('.bm-book')].every((s) => !s.hidden)), `${tag}: cleared, every book back`);
    checks += 4;

    // the preview pictures: the Kaleidohedra door, Book One open
    const shot = dev === 'phone' ? process.env.PREVIEW_PHONE : process.env.PREVIEW_DESKTOP;
    if (door === 'kaleidohedra' && shot) {
      await page.evaluate(() => { document.querySelectorAll('.bm-head[aria-expanded="true"]').forEach((h) => h.click()); });
      await press('.bm-book[data-book="One"] > .bm-head');
      await page.evaluate(() => document.querySelector('.bm-search').scrollIntoView({ block: 'start' }));
      await page.waitForTimeout(1500);
      await page.screenshot({ path: shot });
    }
    assert.deepEqual(errors, [], `${tag}: no console errors`);
    checks++;
    await page.close();
  }
}
// both doors, the same entries in the same order
const lists = Object.values(orders);
assert.ok(lists.every((l) => JSON.stringify(l) === JSON.stringify(lists[0])), 'the same menu through every door');
checks++;
await b.close();
console.log(`book-menu: ${checks} checks passed (${DOORS.join(', ')}; phone and desktop)`);
