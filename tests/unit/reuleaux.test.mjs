// The Reuleaux Platonic Solids (DICTO 2026-10-21; paper #45): the generated data (scripts/build-reuleaux-data.py) holds five bodies with
// the right face and corner counts, exact corners (each at distance D from its face's ball centres, inside every ball), film radii that
// increase from just past the circumradius to D, a last film frame that is the full body, and closed meshes; and a body placed on a face
// settles corner to corner, on the other side.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import DATA from '../../src/app/reuleaux-data.js';
import { REULEAUX_KEYS, placeOn } from '../../src/app/world-reuleaux.js';

// look -> [balls (the source solid's corners), faces, corners, corners per face]
const COUNTS = { tetrahedron: [4, 4, 4, 3], octahedron: [8, 8, 6, 3], cube: [6, 6, 8, 4], icosahedron: [20, 20, 12, 3], dodecahedron: [12, 12, 20, 5] };
const dist = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
const volume = (m) => {
  let v = 0; const P = m.v.map((x) => x / DATA.Q);
  for (let i = 0; i < m.t.length; i += 3) {
    const [a, b, c] = [m.t[i], m.t[i + 1], m.t[i + 2]].map((k) => P.slice(3 * k, 3 * k + 3));
    v += (a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])) / 6;
  }
  return v;
};
const closed = (t) => { const e = new Map(); for (let i = 0; i < t.length; i += 3) for (let j = 0; j < 3; j++) { const a = t[i + j], b = t[i + (j + 1) % 3], k = `${a},${b}`; e.set(k, (e.get(k) ?? 0) + 1); } return [...e.keys()].every((k) => { const [a, b] = k.split(','); return e.get(k) === 1 && e.get(`${b},${a}`) === 1; }); };

test('five bodies, in the app order, named by look', () => {
  assert.deepEqual(DATA.bodies.map((B) => B.key), REULEAUX_KEYS);
  assert.deepEqual(DATA.bodies.map((B) => B.source), ['tetrahedron', 'cube', 'octahedron', 'dodecahedron', 'icosahedron']);
});
for (const B of DATA.bodies) {
  test(`${B.name}: faces, corners, film and body`, () => {
    const [nb, nf, nc, k] = COUNTS[B.key];
    assert.equal(B.balls.length, nb); assert.equal(B.faces.length, nf); assert.equal(B.corners.length, nc);
    assert.ok(B.faces.every((f) => f.length === k), 'every face has as many corners');
    // D is the widest span; every corner lies on the balls of its faces and inside every ball
    let D = 0; for (const a of B.balls) for (const b of B.balls) D = Math.max(D, dist(a, b));
    assert.ok(Math.abs(D - B.D) < 1e-8);
    B.faces.forEach((f, i) => f.forEach((c) => assert.ok(Math.abs(dist(B.corners[c], B.balls[i]) - B.D) < 1e-8)));
    for (const c of B.corners) assert.ok(B.balls.every((v) => dist(c, v) <= B.D + 1e-8));
    // each corner is where three or more faces meet; the face polygons are regular with one side
    for (let c = 0; c < nc; c++) assert.ok(B.faces.filter((f) => f.includes(c)).length >= 3, `corner ${c} on 3+ faces`);
    for (const f of B.faces) for (let j = 0; j < k; j++) assert.ok(Math.abs(dist(B.corners[f[j]], B.corners[f[(j + 1) % k]]) - B.side) < 1e-8);
    // the film: 16 radii increasing from past R up to D; volumes growing; the last frame is the full body
    assert.equal(B.radii.length, DATA.frames); assert.equal(B.frames.length, DATA.frames);
    assert.ok(B.radii[0] > B.R && B.radii.every((r, i) => i === 0 || r > B.radii[i - 1]), 'radii increase');
    assert.ok(Math.abs(B.radii.at(-1) - B.D) < 1e-6, 'last radius is D');
    assert.ok(B.frames.every((f, i) => i === 0 || f.vol > B.frames[i - 1].vol), 'volumes grow');
    assert.equal(B.frames.at(-1).vol, B.vol); assert.deepEqual([B.frames.at(-1).v, B.frames.at(-1).t], [B.body.v, B.body.t], 'last frame = full body');
    for (const m of [...B.frames, B.body]) assert.ok(closed(m.t), 'closed, consistently wound mesh');
    assert.ok(Math.abs(volume(B.body) - B.vol) / B.vol < 0.02, 'body mesh volume');
    assert.ok(Math.abs(volume(B.frames.at(-1)) - B.vol) / B.vol < 0.03, 'last frame mesh volume');
    // the build body: every triangle on one patch, every patch present, seams drawn
    assert.equal(B.body.patch.length, B.body.t.length / 3);
    assert.deepEqual([...new Set(B.body.patch)].sort((a, b) => a - b), B.balls.map((_, i) => i));
    assert.ok(B.body.s.length > 0 && B.body.s.length % 2 === 0);
  });
}
test('a body placed on a face settles corner to corner, on the other side', () => {
  const byKey = Object.fromEntries(DATA.bodies.map((B) => [B.key, B]));
  for (const A of DATA.bodies) for (const B of DATA.bodies) {
    if (A.faces[0].length !== B.faces[0].length) { assert.equal(placeOn(B, A.faces[0].map((c) => new THREE.Vector3(...A.corners[c]).divideScalar(A.side))), null); continue; }
    A.faces.forEach((f, fi) => {
      const W = f.map((c) => new THREE.Vector3(...A.corners[c]).divideScalar(A.side));
      const put = placeOn(byKey[B.key], W);
      assert.ok(put, `${B.key} on ${A.key} face ${fi}`);
      const L = B.faces[0].map((c) => new THREE.Vector3(...B.corners[c]).divideScalar(B.side).applyQuaternion(put.quaternion).add(put.position));
      for (const p of L) assert.ok(W.some((w) => w.distanceTo(p) < 1e-6), 'corners coincide');
      const n = W[1].clone().sub(W[0]).cross(W[2].clone().sub(W[0])); // outward from A
      assert.ok(put.position.clone().sub(W[0]).dot(n) > 0, 'the new body lies on the other side');
    });
  }
});
