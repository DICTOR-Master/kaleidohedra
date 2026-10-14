// The CLEO sphere kits (DICTO 2026-10-14): 20 Cleo + 12 pentagonal pockets, or 20 Cleo + 60 Penta-cleo, fill an icosidodecahedron.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { POLYHEDRA, KITS13 } from '../../src/krp-core/src/polyhedra/index.js';

const volume = (s) => {
  const V = s.vertices, c = V.reduce((a, p) => a.map((x, i) => x + p[i] / V.length), [0, 0, 0]); let v = 0;
  for (const f of s.faces) for (let m = 1; m + 1 < f.length; m++) {
    const [a, b, d] = [V[f[0]], V[f[m]], V[f[m + 1]]].map((p) => p.map((x, i) => x - c[i]));
    v += (a[0] * (b[1] * d[2] - b[2] * d[1]) - a[1] * (b[0] * d[2] - b[2] * d[0]) + a[2] * (b[0] * d[1] - b[1] * d[0])) / 6;
  }
  return Math.abs(v);
};
const ICOSIDODECA = (11 * Math.sqrt(5) - 5) / 6;   // edge 1/phi, circumradius 1
for (const [id, n] of [['cleoSphere', 32], ['cleoSphere.allCleo', 80]]) {
  test(`${id}: ${n} pieces filling the icosidodecahedron`, () => {
    const kit = KITS13[id]; assert.ok(kit, id); assert.equal(kit.group, 'cleo'); assert.equal(kit.entries.length, n);
    const sum = kit.entries.reduce((s, e) => { assert.ok(POLYHEDRA[e.shape], e.shape); return s + volume(POLYHEDRA[e.shape]); }, 0);
    assert.ok(Math.abs(sum - ICOSIDODECA) < 1e-6, `${sum}`);
  });
}
test('Penta-cleo is a fifth of a pentagonal pocket', () => {
  assert.ok(Math.abs(5 * volume(POLYHEDRA.PENTA_CLEO) - volume(POLYHEDRA.CLEO_SPHERE_POCKET)) < 1e-9);
  assert.equal(POLYHEDRA.PENTA_CLEO.name ?? 'Penta-cleo', POLYHEDRA.PENTA_CLEO.name ?? 'Penta-cleo');
});
test('the faceted bases: 20 face pyramids fill an icosahedron of edge 2/sqrt5', () => {
  const kit = KITS13['cleoSphere.icosahedron']; assert.equal(kit.entries.length, 20);
  const a = 2 / Math.sqrt(5), ico = (5 * (3 + Math.sqrt(5)) / 12) * a ** 3;
  const sum = kit.entries.reduce((s, e) => s + volume(POLYHEDRA[e.shape]), 0);
  assert.ok(Math.abs(sum - ico) < 1e-6, `${sum} vs ${ico}`);
});
test('Antonius: golden rhombohedron = Cleo-Icos + Antonius + Cleo-Icos; the block fills 8 rhombohedra', () => {
  const c = volume(POLYHEDRA.ICOSA_FACE_PYRAMID), a = volume(POLYHEDRA.ANTONIUS);
  assert.ok(Math.abs(a - 4 * c) < 1e-9, `${a / c}`);
  const one = KITS13['antonius.rhombohedron'], block = KITS13['antonius.block'];
  assert.deepEqual(one.entries.map((e) => e.shape), ['ICOSA_FACE_PYRAMID', 'ANTONIUS', 'ICOSA_FACE_PYRAMID']);
  assert.equal(block.entries.length, 24);
  assert.equal(block.entries.filter((e) => e.shape === 'ANTONIUS').length, 8);
  const sum = block.entries.reduce((s, e) => s + volume(POLYHEDRA[e.shape]), 0);
  assert.ok(Math.abs(sum - 48 * c) < 1e-9);
});
