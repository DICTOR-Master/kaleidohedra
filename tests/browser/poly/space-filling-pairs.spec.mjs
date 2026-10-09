// From space-filling-pairs.spec.ts: Space-Filling Pairs as nine named pair rows; a pair piece's
// details name its partners (the old gold partner minis).
import { open, assert } from './lib.mjs';
export default [
  { name: 'nine named pair rows; a tetrahedron pairs with the octahedron and truncated tetrahedron', async run(b) {
    const h = await open(b, { wizard: true });
    await h.page.tap('.dicto-dim-content [data-family="SPACE_FILLING_PAIRS"]'); await h.wait(800);
    const rows = await h.page.evaluate(() => [...document.querySelectorAll('.poly-section')].map((s) => [s.querySelector('.poly-section-title').textContent, s.querySelectorAll('[data-action]').length]));
    assert.equal(rows.length, 9); assert.ok(rows.every(([, n]) => n === 2)); assert.ok(rows.some(([t]) => /Octet/.test(t)));
    await h.page.tap('[data-action="tool:polyShape:D4"]'); await h.wait(800);
    const partners = await h.page.evaluate(() => [...document.querySelectorAll('.poly-detail-pair')].map((x) => x.dataset.shape).sort());
    assert.deepEqual(partners, ['D8', 'TRUNCATED_TETRAHEDRON']);
    h.noErrors(); await h.close();
  } },
];
