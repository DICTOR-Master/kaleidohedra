// Cleo Towers and the OG core of Aktis (DICTO 2026-10-20): the kits fill their solids, each piece is the shape it says.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { POLYHEDRA, KITS13, CLEO_TOWERS_VOLUMES as V } from '../../src/krp-core/src/polyhedra/index.js';

const volume = (s) => {
  const P = s.vertices, c = P.reduce((a, p) => a.map((x, i) => x + p[i] / P.length), [0, 0, 0]); let v = 0;
  for (const f of s.faces) for (let m = 1; m + 1 < f.length; m++) {
    const [a, b, d] = [P[f[0]], P[f[m]], P[f[m + 1]]].map((p) => p.map((x, i) => x - c[i]));
    v += (a[0] * (b[1] * d[2] - b[2] * d[1]) - a[1] * (b[0] * d[2] - b[2] * d[0]) + a[2] * (b[0] * d[1] - b[1] * d[0])) / 6;
  }
  return Math.abs(v);
};
const sum = (kit) => kit.entries.reduce((s, e) => { assert.ok(POLYHEDRA[e.shape], e.shape); return s + volume(POLYHEDRA[e.shape]); }, 0);
for (const [id, n, want] of [['cleoTowers.three', 126, 'three'], ['cleoTowers', 218, 'five'], ['ogAktis', 80, 'og']]) {
  test(`${id}: ${n} pieces filling their solid`, () => {
    const kit = KITS13[id]; assert.ok(kit, id); assert.equal(kit.group, 'cleo'); assert.equal(kit.entries.length, n);
    assert.ok(Math.abs(sum(kit) - V[want]) < 1e-6, `${sum(kit)} vs ${V[want]}`);
  });
}
test('the shells grow by 10/phi^4 a turn: the five-shell kit ends on the icosidodecahedron (10/phi^4)^3 the core', () => {
  const c = 10 / ((1 + Math.sqrt(5)) / 2) ** 4;
  assert.ok(Math.abs(V.five / V.core - c ** 9) < 1e-6, `${V.five / V.core}`);
});
test('Hex Aktis and Deltoid Aktis: 20 and 60, named', () => {
  const k = KITS13.ogAktis.entries;
  assert.equal(k.filter((e) => e.shape === 'HEX_AKTIS').length, 20); assert.equal(k.filter((e) => e.shape === 'DELTOID_AKTIS').length, 60);
  assert.equal(POLYHEDRA.HEX_AKTIS.name, 'DICTO Hex Aktis'); assert.equal(POLYHEDRA.DELTOID_AKTIS.name, 'DICTO Deltoid Aktis');
  assert.equal(POLYHEDRA.HEX_AKTIS.faces.length, 7); assert.equal(POLYHEDRA.DELTOID_AKTIS.faces.length, 5);
});
