// Pacioli's golden rectangles on icosahedron kits (DICTO 2026-10-14).
import test from 'node:test';
import assert from 'node:assert/strict';
import { POLYHEDRA, KITS13 } from '../../src/krp-core/src/polyhedra/index.js';
import { kitIcosahedron, goldenRectangles } from '../../src/krp-core/src/assembly/kitHints.js';

const phi = (1 + Math.sqrt(5)) / 2;
const d = (a, b) => Math.hypot(...a.map((x, k) => x - b[k]));

test('the icosahedron kits are found, and only they', () => {
  const ico = Object.keys(KITS13).filter((id) => kitIcosahedron(KITS13[id], POLYHEDRA));
  assert.deepEqual(ico.sort(), ['cleoSphere.icosahedron', 'deshi.deshi', 'greatIcosahedron', 'icosa13.build', 'icosa13.pieces', 'icosa13.units']);
});

test('three golden rectangles on the 12 corners, short side an edge', () => {
  for (const id of ['cleoSphere.icosahedron', 'icosa13.build']) {
    const c = kitIcosahedron(KITS13[id], POLYHEDRA), R = goldenRectangles(c);
    const e = Math.min(...c.flatMap((v, i) => c.slice(i + 1).map((w) => d(v, w))));
    assert.equal(R.length, 3);
    assert.equal(new Set(R.flat().map((v) => v.map((x) => x.toFixed(6)).join())).size, 12);
    for (const r of R) {
      assert.ok(Math.abs(d(r[0], r[1]) - e) < 1e-5 * e);
      assert.ok(Math.abs(d(r[1], r[2]) / d(r[0], r[1]) - phi) < 1e-5);
      assert.ok(Math.abs(d(r[0], r[2]) - d(r[1], r[3])) < 1e-5 * e);
    }
  }
});
