// From radial-projection.spec.ts: a shape's details show its 4D prism (any shape) or, for a 4D seed,
// Extend into 4D: the whole polytope in perspective, with its real cell count.
import { open, assert } from './lib.mjs';
const details = async (h, fam, id) => { await h.page.tap(`.dicto-dim-content [data-family="${fam}"]`); await h.wait(600); await h.page.tap(`[data-action="tool:polyShape:${id}"]`); await h.wait(800); };
export default [
  { name: 'a shape with no 4D polytope shows its 4D prism', async run(b) {
    const h = await open(b, { wizard: true });
    await details(h, 'ARCHIMEDEAN', 'CUBOCTAHEDRON');
    await h.page.tap('.poly-detail-4d'); await h.wait(900);
    assert.ok(await h.page.$('.poly-detail-4dbox:not([hidden]) canvas'), 'a 4D prism view');
    assert.equal(await h.page.$('.poly-detail-4dbox [data-cells]'), null);
    h.noErrors(); await h.close();
  } },
  { name: 'every 4D seed shows its own polytope and real cell count', async run(b) {
    for (const [id, cells] of [['D4', 16], ['CUBE', 8], ['D8', 24], ['DODECAHEDRON', 120]]) {
      const h = await open(b, { wizard: true });
      await details(h, 'PLATONIC', id);
      await h.page.tap('.poly-detail-4d'); await h.wait(1200);
      assert.ok(await h.page.$('.poly-detail-4dbox:not([hidden]) canvas'), `${id}: a view`);
      assert.equal(await h.page.getAttribute('.poly-detail-4dbox [data-cells]', 'data-cells'), String(cells), id);
      h.noErrors(); await h.close();
    }
  } },
];
