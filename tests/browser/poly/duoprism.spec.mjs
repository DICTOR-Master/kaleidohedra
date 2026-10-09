// From duoprism.spec.ts: a dodecahedron face offers 4D Prism (no picker step): the same shape pushed
// out, joined by a prism cell; three faces share one far copy and survive a reload; a shape with no
// 4D prism never offers it.
import { open, at, assert } from './lib.mjs';
export default [
  { name: 'a dodecahedron face adds its 4D prism; three faces share one far copy, saved', async run(b) {
    const h = await open(b, { build: { nodes: [at('DODECAHEDRON', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    const faces = (await h.faces(0)).slice(0, 3);
    for (const f of faces) { await h.tapFace(0, f); await h.page.tap('.poly-strip [data-duoprism]'); await h.wait(900); }
    let s = await h.state();
    assert.equal(s.nodes.length, 2, 'one far copy');
    const c = s.connections.filter((x) => x.kind === 'duoprism');
    assert.equal(c.length, 1); assert.equal(1 + (c[0].duoprismExtraFaces?.length ?? 0), 3);
    await h.page.reload(); await h.page.waitForSelector('#welcome-overlay', { state: 'visible', timeout: 30000 }); await h.page.keyboard.press('Enter'); await h.wait(900);
    s = await h.state();
    assert.equal(1 + (s.connections.find((x) => x.kind === 'duoprism').duoprismExtraFaces?.length ?? 0), 3);
    h.noErrors(); await h.close();
  } },
  { name: 'a rhombic dodecahedron never offers 4D Prism on a face', async run(b) {
    const h = await open(b, { build: { nodes: [at('RHOMBIC_DODECAHEDRON', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    await h.tapFace(0, await h.frontFace(0));
    assert.equal(await h.page.$('.poly-strip [data-duoprism]'), null);
    h.noErrors(); await h.close();
  } },
];
