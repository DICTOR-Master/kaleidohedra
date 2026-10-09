// From legacy-fold-migration.spec.ts: an old save with a 4D-fold join loads as a plain face join, and
// nothing anywhere offers the removed fold.
import { open, assert } from './lib.mjs';
export default [
  { name: 'an old fold join loads as a face join; no fold control exists', async run(b) {
    const old = { nodes: [{ id: 'a', shape: 'CUBE', transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] } }, { id: 'b', shape: 'CUBE', transform: { position: [1, 0, 0], quaternion: [0, 0, 0, 1] } }], connections: [{ nodeA: 'a', vertexA: 0, nodeB: 'b', vertexB: 1, kind: 'face', fold4: true }] };
    const h = await open(b, { old });
    const s = await h.saved();
    assert.equal(s.connections.length, 1); assert.equal(s.connections[0].kind, 'face'); assert.ok(!('fold4' in s.connections[0]));
    await h.tapFace(0, await h.frontFace(0));
    assert.ok(!(await h.page.evaluate(() => /fold/i.test(document.querySelector('.poly-strip')?.textContent ?? ''))));
    h.noErrors(); await h.close();
  } },
];
