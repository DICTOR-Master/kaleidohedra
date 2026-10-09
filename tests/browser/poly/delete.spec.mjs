// From delete.spec.ts: long-press removes a piece (a real held touch). The joined app removes just
// the piece pressed (its joins go with it), and removing the last leaves the outline to tap.
import { open, at, assert } from './lib.mjs';
export default [
  { name: 'long-press removes the piece pressed; removing the last leaves the outline', async run(b) {
    const h = await open(b, { build: { nodes: [at('CUBE', [0, 0, 0], [0, 0, 0, 1], 'a'), at('CUBE', [1, 0, 0], [0, 0, 0, 1], 'b')], connections: [{ nodeA: 'a', vertexA: 0, nodeB: 'b', vertexB: 1, kind: 'face' }] } });
    await h.longPressFace(1, await h.frontFace(1));
    let s = await h.state();
    assert.equal(s.nodes.length, 1); assert.equal(s.connections.length, 0);
    await h.longPressFace(0, await h.frontFace(0));
    assert.equal((await h.state()).nodes.length, 0);
    h.noErrors(); await h.close();
  } },
];
