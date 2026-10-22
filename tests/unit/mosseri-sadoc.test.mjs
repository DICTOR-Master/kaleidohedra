// The Mosseri–Sadoc tiles t1 and t5 (DICTO 2026-10-23): exact edges and volumes at scale 1/tau, faces outward, and the
// family listing all six by M-S number, reusing the kit pieces and the DICTO Icosa world's solids, not copies.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { POLYHEDRA, MOSSERI_SADOC_TILES } from '../../src/krp-core/src/polyhedra/index.js';
import { familyIds, familiesFor } from '../../src/krp-core/src/polyhedra/families.js';
import { ICOSA_SOLIDS } from '../../src/krp-core/src/geometry-extensions/icosa.js';

const TAU = (1 + Math.sqrt(5)) / 2;
const d = (a, b) => Math.hypot(...a.map((x, i) => x - b[i]));
const volume = (s) => s.faces.reduce((t, [a, b, c]) => { const [p, q, r] = [a, b, c].map((i) => s.vertices[i]);
  return t + p[0] * (q[1] * r[2] - q[2] * r[1]) - p[1] * (q[0] * r[2] - q[2] * r[0]) + p[2] * (q[0] * r[1] - q[1] * r[0]); }, 0) / 6;
// Edge lengths at scale 1/tau for the pairs 01, 02, 03, 12, 13, 23 (Koca et al. 2020, Table 1: tau -> 1, 1 -> 1/tau).
const PAIRS = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]];
const WANT = { MS_T1: { edges: [1, 1 / TAU, 1 / TAU, 1 / TAU, 1 / TAU, 1 / TAU], volume: 1 / 12 / TAU ** 3 },
  MS_T5: { edges: [1, 1, 1 / TAU, 1, 1 / TAU, 1], volume: TAU ** 2 / 12 / TAU ** 3 } };

test('M-S t1 and t5: names, exact edges and volumes, faces outward', () => {
  for (const [id, w] of Object.entries(WANT)) {
    const s = POLYHEDRA[id];
    assert.equal(s.name, `M-S t${id.slice(-1)}`);
    PAIRS.forEach(([a, b], k) => assert.ok(Math.abs(d(s.vertices[a], s.vertices[b]) - w.edges[k]) < 1e-12, `${id} edge ${a}${b}`));
    assert.ok(Math.abs(volume(s) - w.volume) < 1e-12, `${id} volume`);
    // convex, so every face points away from the centroid (at the origin)
    for (const [a, b, c] of s.faces) {
      const [p, q, r] = [a, b, c].map((i) => s.vertices[i]), u = q.map((x, i) => x - p[i]), v = r.map((x, i) => x - p[i]);
      const n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
      assert.ok(n[0] * p[0] + n[1] * p[1] + n[2] * p[2] > 0, `${id} face outward`);
    }
  }
});

test('the Mosseri–Sadoc family: all six in M-S order, at one scale', () => {
  assert.deepEqual(familyIds('MOSSERI_SADOC'), ['MS_T1', 'HOUND_TOOTH', 'TRICAP', 'KIT13_ICOSA13_CLEO', 'MS_T5', 'KIT13_ICOSA13_AXE']);
  assert.deepEqual(MOSSERI_SADOC_TILES.map((x) => x.id), familyIds('MOSSERI_SADOC'));
  // Hound Tooth and Tricap: the Icosa world's own solids (names kept), volume tau/12 tau^-3 each (to its 6 decimals)
  for (const [id, name] of [['HOUND_TOOTH', 'Hound Tooth'], ['TRICAP', 'Tricap']]) {
    assert.equal(POLYHEDRA[id].name, name);
    assert.ok(Math.abs(volume(POLYHEDRA[id]) - TAU / 12 / TAU ** 3) < 1e-5, `${id} volume`);
    assert.equal(POLYHEDRA[id].faces.length, ICOSA_SOLIDS[id].faces.length);
  }
  assert.deepEqual(MOSSERI_SADOC_TILES.map((x) => x.n), [1, 2, 3, 4, 5, 6]);
  assert.deepEqual(familiesFor('KIT13_ICOSA13_AXE'), ['MOSSERI_SADOC']);
  // the existing pieces keep their names, and share the 1/tau scale: AXE's volume is tau^3/12 tau^-3, Cleo's tau^2/12 tau^-3
  assert.equal(POLYHEDRA.KIT13_ICOSA13_AXE.name, 'AXE');
  assert.equal(POLYHEDRA.KIT13_ICOSA13_CLEO.name, 'Cleo');
  assert.ok(Math.abs(Math.abs(volume(POLYHEDRA.KIT13_ICOSA13_AXE)) - 1 / 12) < 1e-6);
  assert.ok(Math.abs(Math.abs(volume(POLYHEDRA.KIT13_ICOSA13_CLEO)) - volume(POLYHEDRA.MS_T5)) < 1e-6);
  // Koca et al.: the icosahedron (edge 1/tau here) = 7 t1 + 6 t2 + 2 t5 + t6, by volume
  const ico = (5 * TAU ** 2 / 6) / TAU ** 3, t2 = volume(POLYHEDRA.HOUND_TOOTH);
  assert.ok(Math.abs(7 * volume(POLYHEDRA.MS_T1) + 6 * t2 + 2 * volume(POLYHEDRA.MS_T5) + Math.abs(volume(POLYHEDRA.KIT13_ICOSA13_AXE)) - ico) < 1e-6);
});
