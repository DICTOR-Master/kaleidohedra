// The Mandala World's geometry (mandala-geometry.js), checked against the DICTO Yantra study's own counts and conditions
// (k-research studies/2026-11-08-tetra-yantra: render3d.py, cleo_sphere.py, sphere81.py).
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { YANTRA_B, YANTRA_W, YANTRA_APEX } from '../../src/app/mandala-data.js';
import { N_TRI, isUp, flatSegments, marmas, tetra, cone, narrowed, STILL_STOPS, stopAt, icosahedron, cleoSphere, sphere81, sphereYantra, mandalaPreviewEdges } from '../../src/app/mandala-geometry.js';

const close = (a, b, e = 1e-9) => Math.abs(a - b) <= e;
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];

test('the DICTO Yantra data: nine triangles, t1–t5 point down, t6–t9 up, the great pair spans the circle', () => {
  for (const L of [YANTRA_B, YANTRA_W, YANTRA_APEX]) assert.equal(L.length, 9);
  assert.deepEqual([...Array(N_TRI).keys()].map(isUp), [false, false, false, false, false, true, true, true, true]);
  assert.equal(YANTRA_APEX[2], 1); assert.equal(YANTRA_APEX[6], 0);   // triangle 3 touches the bottom, triangle 7 the top
  // the base corners of triangles 1, 3, 7 and 9 lie on the circle
  for (const i of [0, 2, 6, 8]) assert.ok(close(YANTRA_W[i] ** 2 + (YANTRA_B[i] - 0.5) ** 2, 0.25, 1e-12), `t${i + 1} on the circle`);
});

test('the flat yantra has the 9 marmas (mirror pairs folded) of render3d.py', () => {
  assert.equal(flatSegments().length, 27);
  const m = marmas();
  assert.equal(m.length, 9);
  assert.deepEqual(m.map(([r, d]) => [r.toFixed(9), d.toFixed(9)]).slice(0, 3), [['0.040044872', '0.472508077'], ['0.068415791', '0.576510322'], ['0.069102659', '0.397040858']]);
});

test('each tetrahedron: apex on the axis, base level and inscribed in its cone; turning keeps it on the cone', () => {
  for (let i = 0; i < N_TRI; i++) {
    const c = cone(i);
    for (const deg of [0, 17, 60, 133]) {
      const { base, apex } = tetra(i, deg);
      assert.deepEqual([apex[0], apex[2]], [0, 0]); assert.ok(close(apex[1], c.apex));
      for (const p of base) { assert.ok(close(p[1], c.base)); assert.ok(close(Math.hypot(p[0], p[2]), c.r)); }
    }
  }
});

test('the three still positions: seen along z the tetrahedra are the yantra narrowed to cos 30° with 18 meetings', () => {
  assert.deepEqual(STILL_STOPS, [0, 60, 120]);
  assert.equal(stopAt(60), 1); assert.equal(stopAt(61), -1);
  const { segs, meet } = narrowed();
  assert.equal(meet.length, 18);
  // every meeting lies on three or more of the narrowed segments
  const onSeg = (p, [a, b]) => { const d = [b[0] - a[0], b[1] - a[1]], q = [p[0] - a[0], p[1] - a[1]], l = d[0] ** 2 + d[1] ** 2, s = (q[0] * d[0] + q[1] * d[1]) / l; return s > -1e-9 && s < 1 + 1e-9 && Math.abs(q[0] * d[1] - q[1] * d[0]) / Math.sqrt(l) < 1e-8; };
  for (const p of meet) assert.ok(segs.filter(([a, b]) => onSeg(p, [a, b])).length >= 3, `meeting ${p}`);
  // the tetrahedra's edges projected along z at each still position cover exactly the narrowed segments' x-extent
  for (const deg of STILL_STOPS) for (let i = 0; i < N_TRI; i++) {
    const xs = tetra(i, deg).base.map((p) => p[0]).sort((a, b) => a - b), w = (Math.sqrt(3) / 2) * cone(i).r;
    assert.ok(close(xs[0], -w) && close(xs[1], 0) && close(xs[2], w), `t${i + 1} at ${deg}°`);
  }
});

test('the Cleo sphere: 20 faces, inscribed caps of 20.9052°, every yantra line a great circle', () => {
  const { V, F } = icosahedron();
  assert.equal(V.length, 12); assert.equal(F.length, 20);
  const { caps, rho } = cleoSphere();
  assert.ok(close((rho * 180) / Math.PI, 20.9051574, 1e-6));
  for (const { cen, point } of caps.slice(0, 4)) for (const [pts] of sphereYantra(cen, point, rho, 8)) {
    const n = cross(pts[0], pts[8]);
    for (const p of pts) assert.ok(Math.abs(dot(p, n)) < 1e-12);
  }
});

test('the 81 sphere: 80 triangles, 42 corners, 120 sides (Euler 2), plus the bindu: 81', () => {
  const s = sphere81();
  assert.equal(s.tris.length, 80); assert.equal(s.corners, 42); assert.equal(s.edges, 120);
  assert.equal(s.corners - s.edges + s.tris.length, 2);
  assert.equal(s.tris.length + 1, 81);
  for (const tr of s.tris) assert.ok(tr.rho > 0.15 && tr.rho < 0.2);
});

test('the wizard preview: 9 tetrahedra × 6 edges', () => assert.equal(mandalaPreviewEdges().length, 54));

// Every world card in the DICTO list has its one-line description (HexOct and Star Cores showed their raw keys until 2026-11-08).
test('every K_WORLDS entry has its wiz.3d description in all seven languages', async () => {
  const { readFileSync } = await import('node:fs');
  const { __I18N_FOR_VERIFY_ONLY__: I, LANG_ORDER } = await import('../../src/app/i18n.js');
  const src = readFileSync(new URL('../../src/app/dimension-wizard.js', import.meta.url), 'utf8');
  const a = src.indexOf('const K_WORLDS = ['), keys = [...src.slice(a, src.indexOf('\n];', a)).matchAll(/\{ key: '(\w+)'/g)].map((m) => m[1]);
  assert.ok(keys.includes('mandala'));
  for (const L of LANG_ORDER) assert.deepEqual(keys.filter((k) => !I[L][`wiz.3d.${k}`]), [], `${L}: wiz.3d.* missing`);
});
