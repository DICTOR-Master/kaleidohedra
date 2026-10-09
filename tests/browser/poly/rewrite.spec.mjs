// From rewrite.spec.ts: a 10-face deltahedron's face offers Transform to the 12-face one, in place.
import { open, at, assert } from './lib.mjs';
export default [
  { name: 'D10 offers Transform to D12, and it swaps in place', async run(b) {
    const h = await open(b, { build: { nodes: [at('D10', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    await h.tapFace(0, await h.frontFace(0));
    await h.page.tap('.poly-strip [data-transform]'); await h.wait(900);
    assert.deepEqual(await h.shapes(), ['D12']);
    h.noErrors(); await h.close();
  } },
];
