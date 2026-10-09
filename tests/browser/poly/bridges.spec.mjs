// From bridges.spec.ts: 3D+ Bridges in its four sections; the rhombic icosahedron's details say what
// it bridges to.
import { open, assert } from './lib.mjs';
export default [
  { name: '3D+ Bridges shows cells, shadows, slices, corners, and the rhombic icosahedron\'s bridge', async run(b) {
    const h = await open(b, { wizard: true });
    await h.page.tap('.dicto-dim-content [data-family="BRIDGES_3D"]'); await h.wait(700);
    assert.deepEqual(await h.page.evaluate(() => [...document.querySelectorAll('.poly-section')].map((s) => s.dataset.section)), ['cells', 'shadows', 'slices', 'corners']);
    await h.page.tap('[data-section="shadows"] [data-action="tool:polyShape:RHOMBIC_ICOSAHEDRON"]'); await h.wait(800);
    assert.match(await h.page.textContent('[data-credit="bridge"]'), /5-cube|five|6-cube|cube/i);
    h.noErrors(); await h.close();
  } },
];
