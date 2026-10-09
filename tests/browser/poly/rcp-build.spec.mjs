// From rcp-build.spec.ts (RCP-C2B): a lone 4D seed grows into its polytope, shell 1 a cell at a time
// then a shell per tap; Open / Closed is saved and locks from shell 2; the 600-cell has a vertex-first
// target; non-4D shapes never offer it; old saves with the earlier spellings still load; RCP-
// Coordinates toggles and survives every stage; the row shows only for a lone seed.
import { open, at, assert } from './lib.mjs';
const row = (h) => h.page.evaluate(() => ({ next: document.querySelector('[data-rcp-next]')?.textContent, nextOff: document.querySelector('[data-rcp-next]')?.disabled, open: document.querySelector('[data-rcp-open]')?.textContent, openOff: document.querySelector('[data-rcp-open]')?.disabled, start: !!document.querySelector('[data-rcp-start]') }));
const tapIt = async (h, sel) => { await h.page.tap(sel); await h.wait(600); };
export default [
  { name: 'a cube grows into the tesseract: 6 cells one at a time, then the last shell', async run(b) {
    const h = await open(b, { build: { nodes: [at('CUBE', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    assert.ok((await row(h)).start, 'Grow into 4D offered');
    await tapIt(h, '[data-rcp-start]');
    for (let i = 0; i < 6; i++) await tapIt(h, '[data-rcp-next]');
    assert.match((await row(h)).next, /2\/2/);
    await tapIt(h, '[data-rcp-next]');
    assert.ok((await row(h)).nextOff, 'complete');
    assert.equal((await h.saved()).view.rcp.n, 8);
    h.noErrors(); await h.close();
  } },
  { name: 'Open / Closed is saved; building shell 2 closes it and locks it until shell 2 goes', async run(b) {
    const h = await open(b, { build: { nodes: [at('DODECAHEDRON', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    await tapIt(h, '[data-rcp-start]');
    for (let i = 0; i < 12; i++) await tapIt(h, '[data-rcp-next]');
    assert.equal((await h.saved()).view.rcp.open, true);
    await tapIt(h, '[data-rcp-open]');
    assert.equal((await h.saved()).view.rcp.open, false);
    await tapIt(h, '[data-rcp-open]');
    await tapIt(h, '[data-rcp-next]'); // shell 2
    const r = await row(h);
    assert.ok(r.openOff, 'locked from shell 2'); assert.equal((await h.saved()).view.rcp.open, false);
    await tapIt(h, '[data-rcp-back]');
    assert.ok(!(await row(h)).openOff, 'unlocked again');
    h.noErrors(); await h.close();
  } },
  { name: 'a tetrahedron offers the 16-, 5- and 600-cell, and the 600-cell from a vertex', async run(b) {
    const h = await open(b, { build: { nodes: [at('D4', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    await tapIt(h, '[data-rcp-start]');
    const targets = await h.page.evaluate(() => [...document.querySelectorAll('[data-rcp-target] option')].map((o) => o.value));
    assert.deepEqual(targets, ['16-cell', '5-cell', '600-cell', '600-cell (vertex-first)']);
    for (const t of ['600-cell', '600-cell (vertex-first)']) {
      await h.page.selectOption('[data-rcp-target]', t); await h.wait(800);
      await tapIt(h, '[data-rcp-next]'); await tapIt(h, '[data-rcp-next]');
      assert.equal((await h.saved()).view.rcp.target, t); assert.equal((await h.saved()).view.rcp.n, 3);
      await tapIt(h, '[data-rcp-open]');
    }
    h.noErrors(); await h.close();
  } },
  { name: 'a shape that is no 4D seed never offers Grow into 4D; a second piece hides the row', async run(b) {
    let h = await open(b, { build: { nodes: [at('RHOMBIC_DODECAHEDRON', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    assert.ok(!(await row(h)).start); await h.close();
    h = await open(b, { build: { nodes: [at('CUBE', [0, 0, 0], [0, 0, 0, 1], 'a'), at('CUBE', [1, 0, 0], [0, 0, 0, 1], 'b')] } });
    assert.ok(!(await row(h)).start && !(await row(h)).next, 'no 4D row with two pieces');
    h.noErrors(); await h.close();
  } },
  { name: "an old site's save with the earlier rpcPolytope / rpc4d spellings loads as a grown polytope", async run(b) {
    const old = { nodes: [{ id: 'r', shape: 'CUBE', transform: { position: [0, 0, 0], quaternion: [0, 0, 0, 1] }, rpcPolytope: { seedSpecId: 'CUBE', target: 'tesseract', view3D: false } }, { id: 'c', shape: 'CUBE', transform: { position: [1, 0, 0], quaternion: [0, 0, 0, 1] } }], connections: [{ nodeA: 'r', vertexA: 0, nodeB: 'c', vertexB: 0, kind: 'rpc4d' }] };
    const h = await open(b, { old });
    const s = await h.saved();
    assert.deepEqual(s.nodes.map((n) => n.shape), ['CUBE']);
    assert.deepEqual(s.view.rcp, { target: 'tesseract', n: 2, open: false, coords: false });
    h.noErrors(); await h.close();
  } },
  { name: 'RCP-Coordinates toggles, and survives every build and remove stage', async run(b) {
    const h = await open(b, { build: { nodes: [at('D8', [0, 0, 0], [0, 0, 0, 1], 'a')] } });
    await tapIt(h, '[data-rcp-start]');
    await tapIt(h, '[data-rcp-coords]');
    assert.equal((await h.saved()).view.rcp.coords, true);
    for (let i = 0; i < 10; i++) { if ((await row(h)).nextOff) break; await tapIt(h, '[data-rcp-next]'); }
    for (let i = 0; i < 10; i++) { if (await h.page.evaluate(() => document.querySelector('[data-rcp-back]').disabled)) break; await tapIt(h, '[data-rcp-back]'); }
    await tapIt(h, '[data-rcp-coords]');
    assert.equal((await h.saved()).view.rcp.coords, false);
    h.noErrors(); await h.close();
  } },
];
