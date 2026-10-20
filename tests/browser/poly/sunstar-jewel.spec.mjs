// DICTO 2026-10-20: the Sunstar and Jewel helpers. A Sunstar piece's details say it is the Sunstar family (whole dodecahedra and
// Dogstars) and how it differs from the Jewel family, and the other way round; a lone cluster of either family shows ghosts of what
// comes next (its next copies and the loose Dogstars or stellas of its tiling), and tapping one places that piece.
import { open, at, assert } from './lib.mjs';
export default [
  { name: 'Sunstar and Jewel pieces explain their family', async run(b) {
    const h = await open(b, { wizard: true });
    const fam = h.page.locator('.dicto-dim-content [data-family="DICTO_PIECES"]').first(); await fam.scrollIntoViewIfNeeded(); await fam.tap(); await h.wait(800);
    for (const [id, credit, text] of [['DODECA_OCTAHEDRAL_CLUSTER', 'sunstar-family', /Sunstar family/], ['DJ_TETRAHEDRAL_CLUSTER', 'jewel-family', /Jewel family/]]) {
      const card = h.page.locator(`[data-action="tool:polyShape:${id}"]`).first(); await card.scrollIntoViewIfNeeded(); await card.tap(); await h.wait(800);
      assert.match(await h.page.textContent(`[data-credit="${credit}"]`), text, `${id}: ${credit} line`);
      await h.page.tap('.dim-wizard-back'); await h.wait(500);
    }
    h.noErrors(); await h.close();
  } },
  { name: 'a lone cluster shows ghosts of its tiling, and a tap places one', async run(b) {
    for (const [cluster, loose] of [['DODECA_OCTAHEDRAL_CLUSTER', 'DOGSTAR'], ['DJ_TETRAHEDRAL_CLUSTER', 'STELLA_OCTANGULA']]) {
      const h = await open(b, { build: { nodes: [at(cluster, [0, 0, 0], [0, 0, 0, 1], 'a')], view: { hints: true } } });
      await h.wait(1200);
      const ghosts = await h.page.evaluate(() => window.__polyProbe.ghosts());
      assert.ok(ghosts.length >= 6, `${cluster}: ${ghosts.length} ghosts`);
      for (const g of ghosts) { await h.tap(g); if ((await h.shapes()).length > 1) break; }
      const shapes = await h.shapes();
      assert.equal(shapes.length, 2, `${cluster}: a ghost tap placed a piece`);
      assert.ok([cluster, loose].includes(shapes[1]), `${cluster}: placed ${shapes[1]}`);
      h.noErrors(); await h.close();
    }
  } },
];
