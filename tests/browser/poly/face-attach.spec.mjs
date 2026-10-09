// From face-attach.spec.ts: tap a face, the shapes that fit it are offered (More... lists them by
// family, partners first), picking one attaches it flush; a face can be left again; pointed faces
// that fit nothing say so.
import { open, at, assert } from './lib.mjs';
const morePick = async (h, family, id) => {
  await h.page.tap('.poly-strip [data-more]'); await h.wait(600);
  await h.page.tap(`.dim-wizard-body [data-family="${family}"]`); await h.wait(500);
  await h.page.tap(`.dim-wizard-body [data-action="tool:polyShape:${id}"]`); await h.wait(1200);
};
export default [
  { name: 'tapping a cube face offers a cube by More..., and picking it attaches it face to face', async run(b) {
    const h = await open(b, { build: { nodes: [at('CUBE', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    await h.tapFace(0, await h.frontFace(0));
    await morePick(h, 'PLATONIC', 'CUBE');
    const s = await h.state();
    assert.deepEqual(s.nodes.map((n) => n.shape), ['CUBE', 'CUBE']);
    assert.equal(s.connections.filter((c) => c.kind === 'face').length, 1);
    h.noErrors(); await h.close();
  } },
  { name: 'leaving a picked face (closing More...) adds nothing, and the face still takes a shape', async run(b) {
    const h = await open(b, { build: { nodes: [at('CUBE', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    const f = await h.frontFace(0);
    await h.tapFace(0, f);
    await h.page.tap('.poly-strip [data-more]'); await h.wait(500);
    await h.page.tap('.dim-wizard-close'); await h.wait(400);
    assert.equal((await h.state()).nodes.length, 1);
    await h.tapFace(0, f);
    await morePick(h, 'PLATONIC', 'CUBE');
    assert.equal((await h.state()).nodes.length, 2);
    h.noErrors(); await h.close();
  } },
  { name: 'a rhombic dodecahedron face filters More... to shapes with a matching rhombus', async run(b) {
    const h = await open(b, { build: { nodes: [at('RHOMBIC_DODECAHEDRON', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    await h.tapFace(0, await h.frontFace(0));
    await h.page.tap('.poly-strip [data-more]'); await h.wait(800);
    const fams = await h.page.evaluate(() => [...document.querySelectorAll('.dim-wizard-body [data-family]')].map((x) => x.dataset.family));
    assert.ok(!fams.includes('PLATONIC') && !fams.includes('ARCHIMEDEAN'), `no square/triangle families: ${fams}`);
    assert.ok(fams.includes('CATALAN') || fams.includes('PARALLELOHEDRA'), `rhombus families listed: ${fams}`);
    h.noErrors(); await h.close();
  } },
  { name: 'a pointed graded-pyramid side fits nothing; its base takes a cube', async run(b) {
    // Two pyramids, one upright and one flipped, so one base faces the camera.
    const h = await open(b, { build: { nodes: [at('PYRAMID_SQUARE_G4', [-1.2, 0, 0], [0, 0, 0, 1], 'a'), at('PYRAMID_SQUARE_G4', [1.2, 0, 0], [1, 0, 0, 0], 'b')] } });
    const sizes = await h.page.evaluate(async () => { const { POLYHEDRA } = await import('./src/krp-core/src/polyhedra/index.js'); return POLYHEDRA.PYRAMID_SQUARE_G4.faces.map((f) => f.length); });
    const base = sizes.indexOf(4);
    const i = (await h.page.evaluate((f) => window.__polyProbe.facing(0, f), base)) > 0.2 ? 0 : 1;
    const side = (await h.faces(i)).find((f) => sizes[f] === 3);
    await h.tapFace(i, side);
    await h.page.tap('.poly-strip [data-more]').catch(() => {}); await h.wait(700);
    const fams = await h.page.evaluate(() => [...document.querySelectorAll('.dim-wizard-overlay.open .dim-wizard-body [data-family]')].map((x) => x.dataset.family));
    assert.deepEqual(fams, [], `a pointed side should fit nothing: ${fams}`);
    await h.page.tap('.dim-wizard-close').catch(() => {}); await h.wait(300);
    await h.tapFace(i, base);
    await morePick(h, 'PLATONIC', 'CUBE');
    assert.equal((await h.state()).nodes.length, 3);
    h.noErrors(); await h.close();
  } },
  { name: "More... lists the tapped shape's space-filling partners first", async run(b) {
    const h = await open(b, { build: { nodes: [at('D4', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    await h.tapFace(0, await h.frontFace(0));
    await h.page.tap('.poly-strip [data-more]'); await h.wait(800);
    const first = await h.page.evaluate(() => document.querySelector('.dim-wizard-body [data-family]')?.dataset.family);
    assert.equal(first, 'PARTNERS');
    await h.page.tap('.dim-wizard-body [data-family="PARTNERS"]'); await h.wait(500);
    const ids = await h.page.evaluate(() => [...document.querySelectorAll('.dim-wizard-body [data-action]')].map((x) => x.dataset.action.split(':').pop()));
    assert.deepEqual(ids.sort(), ['D8', 'TRUNCATED_TETRAHEDRON']);
    h.noErrors(); await h.close();
  } },
];
