// DICTO Shadow Form (DICTO 2026-10-24; src/app/shadow-form-engine.js): the three grids, snapping to a grid point, the shared turn and
// its 15°/36° snap, every form a closed solid in manifold-3d with its registry volume, and the negative's volume in exact cases:
// two cubes on neighbouring cubic points (hull = union, 0); a cube and an octahedron side by side (by hand); every example's check,
// against its exact or published value. Lattice examples are checked on a whole cell well inside the cluster (volumeInBox), never by
// counting pockets: pieces that meet along edges or at corners, and cavities, make manifold's component count unreliable.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import * as E from '../../src/app/shadow-form-engine.js';

const wasm = await E.loadManifold(() => import('manifold-3d'));
await E.loadFormData();
const PHI = (1 + Math.sqrt(5)) / 2;
const near = (a, b, tol = 1e-9) => assert.ok(Math.abs(a - b) <= tol * Math.max(1, Math.abs(b)), `${a} ≈ ${b}`);
const run = (arr) => { const r = E.shadowForm(E.normaliseArrangement(arr), wasm); const out = { ...r }; r.negative?.delete(); return out; };

test('grids: cubic, face-centred (even sum), body-centred (one parity); their neighbour distances', () => {
  assert.equal(E.gridIndices('cubic', 1).length, 27);
  assert.equal(E.gridIndices('fcc', 1).length, 13); // the centre and its 12 neighbours
  assert.equal(E.gridIndices('bcc', 1).length, 9);  // the centre and the 8 cube corners
  assert.ok(E.onGrid('fcc', [1, 1, 0]) && !E.onGrid('fcc', [1, 0, 0]));
  assert.ok(E.onGrid('bcc', [1, 1, 1]) && E.onGrid('bcc', [2, 0, 0]) && !E.onGrid('bcc', [1, 1, 0]));
  near(E.neighbourDistance('fcc', 1), Math.SQRT2); near(E.neighbourDistance('bcc', 1), Math.sqrt(3));
});

test('snapping to the nearest grid point', () => {
  assert.deepEqual(E.snapToGrid('cubic', 1, [0.4, 1.6, -0.2]), [0, 2, 0]);
  assert.deepEqual(E.snapToGrid('fcc', 1, [0.9, 0.3, 0]), [1, 1, 0]); // (1, 0, 0) is no fcc point
  assert.deepEqual(E.snapToGrid('bcc', 2, [1.1, 0.9, 1.2]), [1, 1, 1]);
  assert.deepEqual(E.snapToGrid('bcc', 1, [0.2, -0.1, 0.1]), [0, 0, 0]);
});

test('the shared turn: every form turns about its own grid point; snapping to multiples of 15° or 36°', () => {
  const q = E.qAxisAngle([0, 0, 1], Math.PI / 2);
  const arr = E.normaliseArrangement({ grid: 'cubic', spacing: 2, turn: q, forms: [{ form: 'cube', at: [1, 0, 0] }, { form: 'tetrahedron', at: [0, 1, 0] }] });
  const at = E.placer(arr, arr.forms[0]);
  const p = at([0.5, 0, 0]);
  near(p[0], 2); near(p[1], 0.5); near(p[2], 0); // turned 90° about z, about its own point (2, 0, 0)
  const ang = (s) => 2 * Math.acos(Math.min(1, Math.abs(s[3])));
  near(ang(E.snapTurn(E.qAxisAngle([1, 0, 0], (44 * Math.PI) / 180))), (45 * Math.PI) / 180, 1e-9);
  near(ang(E.snapTurn(E.qAxisAngle([0, 1, 0], (70 * Math.PI) / 180))), (72 * Math.PI) / 180, 1e-9);
  near(ang(E.snapTurn(E.qAxisAngle([0, 0, 1], (37 * Math.PI) / 180))), (36 * Math.PI) / 180, 1e-9);
});

test('every form is a closed solid in manifold-3d with its registry volume', () => {
  for (const k of E.FORM_KEYS) {
    const g = E.formGeometry(k), r = run({ forms: [{ form: k, at: [0, 0, 0] }] });
    near(r.formsVolume, g.volume, 1e-5);
    assert.ok(r.negativeVolume >= -1e-9 && (g.convex ? r.negativeVolume < 1e-6 : true), k);
  }
});

test('exact: two unit cubes on neighbouring cubic points, hull = their union, negative 0', () => {
  const r = run({ grid: 'cubic', spacing: 1, forms: [{ form: 'cube', at: [0, 0, 0] }, { form: 'cube', at: [1, 0, 0] }] });
  near(r.hullVolume, 2); near(r.formsVolume, 2); near(r.negativeVolume, 0, 1e-9);
});

test('exact: a unit cube and a small octahedron touching its face; the negative by hand', () => {
  // Cube [-1/2, 1/2]³; octahedron of edge √2/2 (corners 1/2 from its centre) at (1, 0, 0), its near corner on the cube's face centre.
  // Beyond the cube the hull is a prismatoid from the face x = 1/2 (square, area 1) to the octahedron's middle square at x = 1 (turned
  // 45°, area 1/2): its middle section is (square + turned square)/2, area (2² − 4 · 1/8)/4 = 7/8, so V = (1/2)/6 · (1 + 7/2 + 1/2) = 5/12;
  // then the octahedron's far half, 1/12 (its faces lie in the prismatoid's planes x + y + z = 3/2 ...). Hull = 1 + 5/12 + 1/12 = 3/2,
  // forms = 1 + 1/6, negative = 1/3.
  const r = run({ grid: 'cubic', spacing: 1, forms: [{ form: 'cube', at: [0, 0, 0] }, { form: 'octahedron', at: [1, 0, 0], scale: Math.SQRT1_2 }] });
  near(r.hullVolume, 3 / 2, 1e-6);
  near(r.formsVolume, 7 / 6, 1e-6);
  near(r.negativeVolume, 1 / 3, 1e-6);
});

test('containers: the inside of a container counts as space', () => {
  const A = E.exampleArrangement('cubeOcta');
  near(run(A).negativeVolume, 5 / 6, 1e-6);
  A.forms[0].container = false; // the cube solid: no space left
  near(run(A).negativeVolume, 0, 1e-6);
});

for (const key of E.EXAMPLE_KEYS) {
  const ex = E.EXAMPLES[key];
  test(`example ${key} (${ex.paper || 'classical'})${ex.check ? `: ${ex.check.what}` : ''}`, () => {
    const arr = E.exampleArrangement(key);
    assert.ok(arr.forms.length > 0 && arr.forms.every((f) => E.FORM_KEYS.includes(f.form)), 'forms placed');
    const r = E.shadowForm(arr, wasm);
    assert.ok(r.negativeVolume > 0 && r.negativeVolume < r.hullVolume);
    if (ex.check) {
      const got = ex.check.whole ? r.negativeVolume : E.volumeInBox(wasm, r.negative, ex.check.min, ex.check.max);
      near(got, ex.check.expected, key === 'lotusBuild' ? 1e-5 : 1e-6); // the AXE and FUJI volumes are stored to 6 places
    }
    r.negative.delete();
  });
}

test('exact values behind the checks', () => {
  near(E.EXAMPLES.dogstar.check.expected, PHI / 2);                                     // one Dogstar = 2φ³ − dodecahedron
  near(E.EXAMPLES.goldenSplit.check.expected, (3 + 7 * Math.sqrt(5)) / 12 + 6 / 12);    // Unborn + 6 AXE
  near(E.EXAMPLES.longHexagon.check.expected, PHI ** 3 - (2 / 3) * ((15 + 7 * Math.sqrt(5)) / 4 - PHI ** 3), 1e-9); // the cube − 4 roofs
  near(E.EXAMPLES.euclidRoofs.check.expected, (15 + 7 * Math.sqrt(5)) / 4 - PHI ** 3);  // dodecahedron − its cube
  near(E.EXAMPLES.bullHorns.check.expected / (8 * E.exampleArrangement('bullHorns').spacing ** 3), 0.22566665, 1e-6);
});

test('the shared turn keeps the negative: an example turned and snapped has the same volumes', () => {
  const A = E.exampleArrangement('euclidRoofs'), r0 = run(A);
  A.turn = E.qAxisAngle([1, 2, 3], 0.7);
  const r1 = run(A);
  near(r1.negativeVolume, r0.negativeVolume, 1e-6); near(r1.hullVolume, r0.hullVolume, 1e-6);
  // two cubes side by side, turned 45°: each turns about its own point, so they now overlap less and the hull grows
  const B = E.normaliseArrangement({ grid: 'cubic', spacing: 1, turn: E.qAxisAngle([0, 0, 1], Math.PI / 4), forms: [{ form: 'cube', at: [0, 0, 0] }, { form: 'cube', at: [1, 0, 0] }] });
  assert.ok(run(B).negativeVolume > 0.01);
});

test('arrangements are plain JSON and round-trip', () => {
  const A = E.exampleArrangement('stellaJewel'), J = JSON.parse(JSON.stringify(A));
  assert.deepEqual(J, A);
  const B = E.normaliseArrangement(J);
  assert.equal(B.forms.length, A.forms.length);
  near(run(B).negativeVolume, run(A).negativeVolume, 1e-9);
});
