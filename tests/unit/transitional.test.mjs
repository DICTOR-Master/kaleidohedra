// DICTO Transitional Shells (DICTO 2026-10-13): each fused stage is a closed solid with a colour for every face, listed in its own
// Polyhedraverse family. (The volume and simple-face checks run when the shapes are generated: build_transitional.py.)
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { POLYHEDRA } from '../../src/krp-core/src/polyhedra/index.js';
import { familyIds } from '../../src/krp-core/src/polyhedra/families.js';
import { TRANSITIONAL_IDS } from '../../src/krp-core/src/polyhedra/transitional.js';

test('the DICTO Transitional Shells family lists every transitional shell', () => {
  assert.ok(TRANSITIONAL_IDS.length >= 6);
  assert.deepEqual([...familyIds('DICTO_TRANSITIONAL')].sort(), [...TRANSITIONAL_IDS].sort());
});
for (const id of TRANSITIONAL_IDS) {
  test(`${id}: one colour per face, outward faces, positive volume`, () => {
    const s = POLYHEDRA[id];
    assert.equal(s.faceColours.length, s.faces.length);
    const V = s.vertices;
    let vol = 0;
    for (const f of s.faces) for (let m = 1; m + 1 < f.length; m++) {
      const [a, b, c] = [V[f[0]], V[f[m]], V[f[m + 1]]];
      vol += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6;
    }
    assert.ok(vol > 0, `volume ${vol}`);
  });
}
