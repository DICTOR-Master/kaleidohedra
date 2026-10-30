// ★ Star step (DICTO's Star Cores papers, #79 Sections 2–3; src/app/star-step-geometry.js): the spike tips by the three rules, the
// halo of the polar rule is the polar solid (one facet over each corner v, in the plane v·x = ρ², its corners the tips of v's faces),
// and the layer of V corner pyramids + E edge tetrahedra fills the halo minus the star exactly, for the cube, the icosahedron and the
// truncated icosahedron and along a star chain.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { POLYHEDRA } from '../../src/krp-core/src/polyhedra/index.js';
import { PHI, solidOf, tipsOf, starStep, nextSolid, facesRound } from '../../src/app/star-step-geometry.js';

const close = (a, b, msg, eps = 1e-9) => assert.ok(Math.abs(a - b) < eps, `${msg}: ${a} vs ${b}`);
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const SOLIDS = { CUBE: [8, 12, 6], D20: [12, 30, 20], TRUNCATED_ICOSAHEDRON: [60, 90, 32] };

test('the solids: centred, convex, counts', () => {
  for (const [id, [V, E, F]] of Object.entries(SOLIDS)) {
    const s = solidOf(POLYHEDRA[id]);
    assert.ok(s, id);
    assert.deepEqual([s.vertices.length, s.edges.length, s.faces.length], [V, E, F], id);
    for (const { n, c } of s.planes) { close(Math.hypot(...n), 1, `${id} unit normal`); assert.ok(c > 0, `${id} centre inside`); }
    facesRound(s).forEach((ring, v) => assert.equal(ring.length, s.faces.filter((f) => f.includes(v)).length, `${id} ring of corner ${v}`));
  }
});

test('a non-convex shape is refused', () => {
  const star = POLYHEDRA.STELLA_OCTANGULA;
  assert.ok(star);
  assert.equal(solidOf(star), null);
});

test('tips: polar p = ρ² n / c with ρ² = φR²; doubling 2 × foot; golden φ × foot', () => {
  for (const id of Object.keys(SOLIDS)) {
    const s = solidOf(POLYHEDRA[id]), r2 = PHI * s.R * s.R;
    const polar = tipsOf(s, 'polar'), dbl = tipsOf(s, 'doubling'), gold = tipsOf(s, 'golden');
    s.planes.forEach(({ n, c }, i) => {
      close(dot(polar[i], n) * c, r2, `${id} polar tip ${i}: |p| c = ρ²`);
      close(Math.hypot(...polar[i]), r2 / c, `${id} polar tip ${i} on the face's axis`);
      for (let k = 0; k < 3; k++) { close(dbl[i][k], 2 * c * n[k], `${id} doubling ${i}`); close(gold[i][k], PHI * c * n[k], `${id} golden ${i}`); }
      assert.ok(Math.hypot(...polar[i]) > c, `${id} polar tip beyond its face`);
    });
  }
});

test('polar rule: the halo is the polar solid, and the layer fills halo − star', () => {
  for (const [id, [V, E, F]] of Object.entries(SOLIDS)) {
    const s = solidOf(POLYHEDRA[id]), r2 = PHI * s.R * s.R, st = starStep(s, 'polar');
    assert.ok(st.contains, `${id}: the halo holds the star`);
    assert.equal(st.halo.vertices.length, F, `${id}: the halo's corners are the ${F} tips`);
    assert.equal(st.halo.faces.length, V, `${id}: one halo facet per corner`);
    // each corner v's plane v·x = ρ² carries a halo facet whose corners are exactly the tips of v's faces
    const ring = facesRound(s);
    s.vertices.forEach((v, vi) => {
      const on = st.halo.faces.find((f) => f.every((k) => Math.abs(dot(v, st.halo.vertices[k]) - r2) < 1e-9));
      assert.ok(on, `${id}: a facet in the plane of corner ${vi}`);
      assert.equal(on.length, ring[vi].length, `${id}: facet ${vi} has a corner per face round the corner`);
      for (const fi of ring[vi]) close(dot(v, st.tips[fi]), r2, `${id}: tip of face ${fi} on the plane of corner ${vi}`);
    });
    assert.equal(st.layer.corners.length, V, `${id}: ${V} corner pyramids`);
    assert.equal(st.layer.edges.length, E, `${id}: ${E} edge tetrahedra`);
    const { halo, star, layer } = st.volumes;
    assert.ok(star > st.volumes.solid && halo > star, `${id}: solid < star < halo`);
    close(layer, halo - star, `${id}: layer = halo − star`);
  }
});

test('the star chain: each halo, scaled back, fills again (polar)', () => {
  for (const id of Object.keys(SOLIDS)) {
    const s0 = solidOf(POLYHEDRA[id]);
    let s = s0;
    for (let k = 0; k < 3; k++) {
      const st = starStep(s, 'polar');
      close(st.volumes.layer, st.volumes.halo - st.volumes.star, `${id} chain ${k}`);
      s = nextSolid(st, s0.R);
      assert.ok(s, `${id} chain ${k}: the halo is a convex solid`);
      close(Math.max(...s.vertices.map((v) => Math.hypot(...v))), s0.R, `${id} chain ${k}: same size`, 1e-9);
    }
  }
});

test('doubling and golden: the cube star sticks out of its halo (no layer); the icosahedron star stays inside', () => {
  const cube = solidOf(POLYHEDRA.CUBE), ico = solidOf(POLYHEDRA.D20);
  for (const rule of ['doubling', 'golden']) {
    const c = starStep(cube, rule);
    assert.equal(c.contains, false, `cube ${rule}`);
    assert.equal(c.layer, null, `cube ${rule}: no layer`);
    const i = starStep(ico, rule);
    assert.equal(i.contains, true, `icosahedron ${rule}`);
    assert.equal(i.layer, null, `icosahedron ${rule}: layer pieces only for the polar rule`);
  }
});
