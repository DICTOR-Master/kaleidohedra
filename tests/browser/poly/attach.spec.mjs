// From attach.spec.ts (vertex attach): tap near a free corner and any shape goes on there, corner to
// corner, turned to its best fit by itself (no twist step: DICTO 2026-10-09, no arrows); leaving the
// corner adds nothing.
import { open, at, assert } from './lib.mjs';
export default [
  { name: 'a corner takes any shape, joined corner to corner', async run(b) {
    const h = await open(b, { build: { nodes: [at('CUBE', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    const f = await h.frontFace(0), v = await h.faceVertex(0, f);
    await h.tapCorner(0, f, v);
    await h.page.tap('.poly-strip [data-more]'); await h.wait(600);
    await h.page.tap('.dim-wizard-body [data-family="PLATONIC"]'); await h.wait(500);
    await h.page.tap('.dim-wizard-body [data-action="tool:polyShape:D8"]'); await h.wait(1500);
    const s = await h.state();
    assert.deepEqual(s.nodes.map((n) => n.shape), ['CUBE', 'D8']);
    const c = s.connections.find((x) => x.kind === 'vertex');
    assert.ok(c && c.vertexA === v, `a corner join at corner ${v}: ${JSON.stringify(s.connections)}`);
    h.noErrors(); await h.close();
  } },
  { name: 'leaving a picked corner adds nothing; the corner stays free', async run(b) {
    const h = await open(b, { build: { nodes: [at('CUBE', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    const f = await h.frontFace(0), v = await h.faceVertex(0, f);
    await h.tapCorner(0, f, v);
    await h.page.tap('.poly-strip [data-more]'); await h.wait(500);
    await h.page.tap('.dim-wizard-close'); await h.wait(400);
    assert.equal((await h.state()).connections.length, 0);
    await h.tapCorner(0, f, v);
    assert.ok(!(await h.prompt()).includes('taken'), 'the corner should still be free');
    h.noErrors(); await h.close();
  } },
];
