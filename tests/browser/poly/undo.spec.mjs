// From undo.spec.ts: Undo takes back the last attach (the face is free again), steps back through
// several, and reverses a remove too.
import { open, at, assert } from './lib.mjs';
const attachCube = async (h, i) => {
  await h.tapFace(i, await h.frontFace(i));
  await h.page.tap('.poly-strip [data-more]'); await h.wait(600);
  await h.page.tap('.dim-wizard-body [data-family="PLATONIC"]'); await h.wait(500);
  await h.page.tap('.dim-wizard-body [data-action="tool:polyShape:CUBE"]'); await h.wait(1200);
};
export default [
  { name: 'Undo takes back the last attach, then the one before', async run(b) {
    const h = await open(b, { build: { nodes: [at('CUBE', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    await attachCube(h, 0);
    // The chosen shape stays chosen: the next face takes it in one tap.
    await h.tapFace(1, await h.frontFace(1));
    const n = (await h.state()).nodes.length;
    assert.ok(n >= 3, `three cubes: ${n}`);
    await h.undo();
    assert.equal((await h.state()).nodes.length, n - 1);
    await h.undo();
    assert.equal((await h.state()).nodes.length, n - 2);
    h.noErrors(); await h.close();
  } },
  { name: 'Undo reverses a remove', async run(b) {
    const h = await open(b, { build: { nodes: [at('CUBE', [0, 0, 0], [0, 0, 0, 1], 'a'), at('CUBE', [1, 0, 0], [0, 0, 0, 1], 'b')] } });
    await h.longPressFace(1, await h.frontFace(1));
    assert.equal((await h.state()).nodes.length, 1);
    await h.undo();
    assert.equal((await h.state()).nodes.length, 2);
    h.noErrors(); await h.close();
  } },
];
