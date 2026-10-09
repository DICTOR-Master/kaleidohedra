// From render.spec.ts: the canvas renders; every shape of every family has its card in DICTO; a cube,
// truncated tetrahedron, truncated dodecahedron, square pyramid (its apex) and gyroelongated square
// pyramid each take a corner tap (any shape fits a corner).
import { open, at, assert } from './lib.mjs';
export default [
  { name: 'every shape of every family has its card', async run(b) {
    const h = await open(b, { wizard: true });
    assert.ok(await h.page.$('canvas'));
    const fams = await h.page.evaluate(() => [...document.querySelectorAll('.dicto-dim-content [data-family]')].map((x) => x.dataset.family));
    const { familyIds } = await import('../../../src/krp-core/src/polyhedra/families.js');
    let checked = 0;
    for (const f of fams.filter((x) => !['FAVOURITES', 'RECENT', 'STARS', 'DICTO_PIECES'].includes(x))) {
      await h.page.tap(`.dicto-dim-content [data-family="${f}"]`); await h.wait(500);
      const ids = new Set(await h.page.evaluate(() => [...document.querySelectorAll('[data-action^="tool:polyShape:"]')].map((x) => x.dataset.action.split(':').pop())));
      const want = familyIds(f);
      assert.deepEqual(want.filter((id) => !ids.has(id)), [], `${f}: every shape has a card`);
      checked += want.length;
      await h.page.tap('.dim-wizard-back'); await h.wait(500);
    }
    assert.ok(checked > 250, `checked ${checked}`);
    h.noErrors(); await h.close();
  } },
  { name: 'corners take a tap on five kinds of shape', async run(b) {
    for (const id of ['CUBE', 'TRUNCATED_TETRAHEDRON', 'TRUNCATED_DODECAHEDRON', 'J1_SQUARE_PYRAMID', 'J10_GYROELONGATED_SQUARE_PYRAMID']) {
      // Hints off: a piece with a pattern (the truncated tetrahedron) has ghosts in front of it.
      const h = await open(b, { build: { nodes: [at(id, [0, 0, 0], [0, 0, 0, 1], 'a')], view: { hints: false } } });
      const f = await h.frontFace(0), v = await h.faceVertex(0, f);
      await h.tapCorner(0, f, v);
      const pt = await h.page.evaluate(([f, v]) => window.__polyProbe.corner(0, f, v), [f, v]);
      if (!(await h.page.$('.poly-strip [data-more]'))) throw new Error(`${id}: no strip after a corner tap at ${JSON.stringify(pt)}, face ${f}, corner ${v}`);
      await h.page.tap('.poly-strip [data-more]'); await h.wait(600);
      const fams = await h.page.evaluate(() => [...document.querySelectorAll('.dim-wizard-body [data-family]')].map((x) => x.dataset.family));
      assert.ok(fams.includes('PLATONIC') && fams.includes('JOHNSON'), `${id}: a corner takes any shape (${fams})`);
      h.noErrors(); await h.close();
    }
  } },
];
