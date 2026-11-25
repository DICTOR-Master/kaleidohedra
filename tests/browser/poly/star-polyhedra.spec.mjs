// From star-polyhedra.spec.ts: the Kepler–Poinsot group has the four star solids; the great
// icosahedron is reference only (not an icosahedron stellation piece); details show Schläfli and
// density and no Build; the viewer turns by drag and has Solid / Translucent / Wireframe.
import { open, assert } from './lib.mjs';
const toStars = async (h) => { await h.page.tap('.dicto-dim-content [data-family="STARS"]'); await h.wait(700); };
export default [
  { name: 'Kepler–Poinsot lists all four; none of the icosahedron stellation pieces is the great icosahedron', async run(b) {
    const h = await open(b, { wizard: true });
    await toStars(h);
    const ids = await h.page.evaluate(() => [...document.querySelectorAll('[data-action^="tool:polyShape:"]')].map((x) => x.dataset.action.split(':').pop()));
    assert.equal(ids.length, 4);
    const names = await h.page.evaluate(async () => { const { STELLATION_IDS, stellationInfo } = await import('./src/krp-core/src/polyhedra/stellations/index.js'); const { POLYHEDRA } = await import('./src/krp-core/src/polyhedra/index.js'); return STELLATION_IDS.filter((id) => stellationInfo(id).solid === 'D20').map((id) => POLYHEDRA[id].name); });
    assert.ok(!names.some((n) => /great icosahedron/i.test(n)), names.join(', '));
    h.noErrors(); await h.close();
  } },
  { name: 'star details: Schläfli and density, no Build; the viewer turns by drag and changes mode', async run(b) {
    const h = await open(b, { wizard: true });
    await toStars(h);
    await h.page.tap('[data-action^="tool:polyShape:"]'); await h.wait(900);
    const text = await h.page.evaluate(() => document.querySelector('.poly-detail-stats')?.textContent ?? '');
    assert.match(text, /Schläfli/); assert.ok(text.includes('/2') || text.includes('5/'), `a star Schläfli symbol: ${text}`);
    assert.equal(await h.page.$('.poly-detail-build'), null, 'no Build for a star solid');
    const cv = await h.page.$('.poly-detail-stage canvas');
    const shot1 = await cv.screenshot();
    const bx = await cv.boundingBox();
    await h.page.mouse.move(bx.x + bx.width / 2, bx.y + bx.height / 2); await h.page.mouse.down(); await h.page.mouse.move(bx.x + bx.width / 2 + 80, bx.y + bx.height / 2 + 10, { steps: 8 }); await h.page.mouse.up(); await h.wait(400);
    assert.notDeepEqual(await cv.screenshot(), shot1, 'dragging turns it');
    for (const m of ['translucent', 'wireframe', 'solid']) { await h.page.tap(`[data-star-mode="${m}"]`); await h.wait(250); assert.equal(await h.page.getAttribute(`[data-star-mode="${m}"]`, 'aria-pressed'), 'true'); }
    h.noErrors(); await h.close();
  } },
];
