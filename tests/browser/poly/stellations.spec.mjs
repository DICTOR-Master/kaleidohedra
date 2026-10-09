// From stellations.spec.ts: Stellations in one section per stellated solid; a third-stellation piece
// attaches onto a rhombic dodecahedron's face.
import { open, at, assert } from './lib.mjs';
export default [
  { name: 'one section per stellated solid', async run(b) {
    const h = await open(b, { wizard: true });
    await h.page.tap('.dicto-dim-content [data-family="STELLATIONS"]'); await h.wait(900);
    const { STELLATION_IDS, stellationInfo } = await import('../../../src/krp-core/src/polyhedra/stellations/index.js');
    const solids = new Set(STELLATION_IDS.map((id) => stellationInfo(id).solid));
    assert.equal(await h.page.evaluate(() => document.querySelectorAll('.poly-section').length), solids.size);
    h.noErrors(); await h.close();
  } },
  { name: 'a third-stellation piece attaches onto a rhombic dodecahedron', async run(b) {
    const h = await open(b, { build: { nodes: [at('RHOMBIC_DODECAHEDRON', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    await h.tapFace(0, await h.frontFace(0));
    await h.page.tap('.poly-strip [data-more]'); await h.wait(700);
    await h.page.tap('.dim-wizard-body [data-family="STELLATIONS"]'); await h.wait(700);
    await h.page.tap('[data-action="tool:polyShape:STELLATION_RHOMBIC_DODECAHEDRON_3"]'); await h.wait(1300);
    assert.deepEqual(await h.shapes(), ['RHOMBIC_DODECAHEDRON', 'STELLATION_RHOMBIC_DODECAHEDRON_3']);
    h.noErrors(); await h.close();
  } },
];
