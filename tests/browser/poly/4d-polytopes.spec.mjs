// From 4d-polytopes.spec.ts: DICTO -> 4D -> 4D Polytopes shows the six by symmetry; Build starts the
// 24-cell from an octahedron; the 600-cell also builds from a vertex.
import { open, assert } from './lib.mjs';
export default [
  { name: 'the six by symmetry; Build starts the 24-cell from an octahedron', async run(b) {
    const h = await open(b, { wizard: true });
    await h.page.tap('[data-dim="4D"]'); await h.wait(500);
    await h.page.tap('.dicto-dim-content [data-family="POLYTOPES_4D"]'); await h.wait(700);
    const secs = await h.page.evaluate(() => [...document.querySelectorAll('.poly-section')].map((s) => `${s.dataset.section}:${s.querySelectorAll('[data-action]').length}`));
    assert.deepEqual(secs, ['A4:1', 'B4:2', 'F4:1', 'H4:2']);
    await h.page.tap('[data-action="tool:polyShape:POLYTOPE_24_CELL"]'); await h.wait(700);
    await h.page.tap('.poly-detail-build'); await h.wait(1500);
    const s = await h.saved();
    assert.deepEqual(s.nodes.map((n) => n.shape), ['D8']); assert.equal(s.view.rcp.target, '24-cell');
    h.noErrors(); await h.close();
  } },
  { name: 'the 600-cell offers a vertex-first build too', async run(b) {
    const h = await open(b, { wizard: true });
    await h.page.tap('[data-dim="4D"]'); await h.wait(500);
    await h.page.tap('.dicto-dim-content [data-family="POLYTOPES_4D"]'); await h.wait(700);
    await h.page.tap('[data-action="tool:polyShape:POLYTOPE_600_CELL"]'); await h.wait(700);
    const targets = await h.page.evaluate(() => [...document.querySelectorAll('.poly-detail-build')].map((x) => x.dataset.target));
    assert.deepEqual(targets, ['600-cell', '600-cell (vertex-first)']);
    await h.page.tap('.poly-detail-build[data-target="600-cell (vertex-first)"]'); await h.wait(1500);
    assert.equal((await h.saved()).view.rcp.target, '600-cell (vertex-first)');
    h.noErrors(); await h.close();
  } },
];
