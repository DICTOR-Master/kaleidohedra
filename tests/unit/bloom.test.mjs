// The Icosaxes Bloom (DICTO 2026-10-27; src/app/bloom-geometry.js) against paper #59 (DICTO DOI 10.5281/zenodo.23677485): the 60
// rotations and 20 corners, the exact volumes of the pieces (Icosaxes 1 + 2√5/3, Unborn Axes 1 + √5/3, Lotus Jewel Axes √5, Dodecaxes 2),
// the first touch φ²√3/2 (neighbours just apart above it, the stops' fractions), the Hexa (9 pieces, together 9 + 17√5/3) and the Keyaxes (volume φ²).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { rotations, cornerTurns, ICOSAXES, LOTUS_JEWEL_AXES, UNBORN_AXES, DODECAXES, volume, twenty, hexa, kagome, TOUCH, STOP_FRACTIONS } from '../../src/app/bloom-geometry.js';
const S5 = Math.sqrt(5), PHI = (1 + S5) / 2, close = (a, b, m) => assert.ok(Math.abs(a - b) < 1e-9, `${m}: ${a} vs ${b}`);
test('icosahedral rotations and the twenty corners', () => {
  assert.equal(rotations().length, 60); assert.equal(cornerTurns().length, 20);
  const C = twenty(false, 1).map((p) => p.centre), r = C.map((c) => Math.hypot(...c));
  r.forEach((x) => close(x, TOUCH, 'centre distance'));
  const near = Math.min(...C.slice(1).map((c) => Math.hypot(...c.map((x, i) => x - C[0][i]))));
  close(near, TOUCH * (2 / PHI) / Math.sqrt(3), 'neighbours on a dodecahedron edge');
});
test('exact volumes (#59 §3)', () => {
  close(volume(ICOSAXES), 1 + 2 * S5 / 3, 'Icosaxes'); close(volume(UNBORN_AXES), 1 + S5 / 3, 'Unborn Axes');
  close(volume(LOTUS_JEWEL_AXES), S5, 'Lotus Jewel Axes'); close(volume(DODECAXES), 2, 'Dodecaxes');
});
test('stops', () => {
  close(TOUCH, PHI * PHI * Math.sqrt(3) / 2, 'first touch'); close(STOP_FRACTIONS.bud, 1 / PHI, 'bud'); close(STOP_FRACTIONS.seed, 1 / 3, 'seed');
  close(STOP_FRACTIONS.lotusSeed, 1 / PHI ** 3, 'lotus seed');
});
test('Icosaxes Hexa, Lotus Hexa and the Keyaxes', () => {
  const H = hexa(false), K = hexa(true);
  assert.equal(H.length, 9); assert.equal(K.length, 9);
  close(H.reduce((s, p) => s + volume(p), 0), 9 + 17 * S5 / 3, 'Icosaxes Hexa = 8 Icosaxes + Unborn Axes = 9 + 17√5/3');
  const net = kagome(), inner = net.filter((p) => p.role === 'big' && Math.abs(volume(p) - PHI * PHI) < 1e-9);
  assert.ok(inner.length >= 8, `Keyaxes (volume φ²) in the patch: ${inner.length}`);
});
