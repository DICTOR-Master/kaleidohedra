// DICTO 2026-10-28: build with the golden-split pieces. Icosaxes, Unborn Axes and Lotus Jewel Axes are
// picked from DICTO's pieces (Build, then tap the outline); a tapped face then takes the next piece face to face.
import { open, at, assert } from './lib.mjs';
const morePick = async (h, family, id) => {
  await h.page.tap('.poly-strip [data-more]'); await h.wait(600);
  await h.page.tap(`.dim-wizard-body [data-family="${family}"]`); await h.wait(500);
  await h.page.tap(`.dim-wizard-body [data-action="tool:polyShape:${id}"]`); await h.wait(1200);
};
const PIECES = ['DICTO_ICOSAXES', 'DICTO_UNBORN_AXES', 'DICTO_LOTUS_JEWEL_AXES'];
export default [
  { name: 'each axes piece builds from its card in DICTO\'s pieces', async run(b) {
    for (const id of PIECES) {
      const h = await open(b, { wizard: true });
      const fam = h.page.locator('.dicto-dim-content [data-family="DICTO_PIECES"]').first(); await fam.scrollIntoViewIfNeeded(); await fam.tap(); await h.wait(800);
      const card = h.page.locator(`[data-action="tool:polyShape:${id}"]`).first(); await card.scrollIntoViewIfNeeded(); await card.tap(); await h.wait(800);
      await h.page.tap('.poly-detail-build'); await h.wait(1500);
      const c = await (await h.page.$('canvas')).boundingBox();
      await h.tap({ x: c.x + c.width / 2, y: c.y + c.height / 2 });   // the outline: tap it to place the piece
      assert.deepEqual(await h.shapes(), [id], `${id}: placed`);
      h.noErrors(); await h.close();
    }
  } },
  { name: 'a tapped face takes the next axes piece face to face', async run(b) {
    for (const [a, c] of [['DICTO_ICOSAXES', 'DICTO_ICOSAXES'], ['DICTO_ICOSAXES', 'DICTO_UNBORN_AXES'], ['DICTO_LOTUS_JEWEL_AXES', 'DICTO_LOTUS_JEWEL_AXES']]) {
      const h = await open(b, { build: { nodes: [at(a, [0, 0, 0], [0, 0, 0, 1], 'a')] } });
      await h.tapFace(0, await h.frontFace(0));
      await morePick(h, 'DICTO_PIECES', c);
      const s = await h.state();
      assert.deepEqual(s.nodes.map((n) => n.shape), [a, c], `${a} + ${c}`);
      assert.equal(s.connections.filter((x) => x.kind === 'face').length, 1, `${a} + ${c}: one face join`);
      h.noErrors(); await h.close();
    }
  } },
];
