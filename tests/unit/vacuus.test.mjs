// DICTO Vacuus (vacuus-geometry.js): which solids the lens applies to, and the numbers behind its five views.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { POLYHEDRA } from '../../src/krp-core/src/polyhedra/index.js';
import { VACUUS_VIEWS, vacuusSolidOf, pyramidsOf, starTipsOf, finsOf, strutsOf, volumes, isCube } from '../../src/app/vacuus-geometry.js';

const close = (a, b, msg, eps = 1e-9) => assert.ok(Math.abs(a - b) <= eps, `${msg}: ${a} vs ${b}`);
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];

test('five views, in order', () => {
  assert.deepEqual(VACUUS_VIEWS, ['pyramids', 'exploded', 'star', 'sheets', 'struts']);
});

// The Platonic solids in DICTO's order (D·I·C·T·O), edge 1: faces, edges, corners, circumradius.
const PLATONIC = [
  ['DODECAHEDRON', 12, 30, 20, Math.sqrt(3) * (1 + Math.sqrt(5)) / 4],
  ['D20', 20, 30, 12, Math.sqrt(10 + 2 * Math.sqrt(5)) / 4],
  ['CUBE', 6, 12, 8, Math.sqrt(3) / 2],
  ['D4', 4, 6, 4, Math.sqrt(6) / 4],
  ['D8', 8, 12, 6, Math.SQRT1_2],
];
test('the Platonic solids (D·I·C·T·O): one fin shape, one strut length, the pyramids make up the solid', () => {
  for (const [id, f, e, v, R] of PLATONIC) {
    const s = vacuusSolidOf(POLYHEDRA[id]);
    assert.ok(s, `${id} qualifies`);
    assert.equal(pyramidsOf(s).length, f, `${id} pyramids`);
    const fins = finsOf(s), struts = strutsOf(s);
    assert.equal(fins.fins.length, e, `${id} fins`);
    assert.equal(fins.classes.length, 1, `${id} one fin shape`);
    assert.equal(struts.struts.length, v, `${id} struts`);
    assert.deepEqual(struts.classes.map((c) => c.count), [v], `${id} one strut length`);
    close(struts.classes[0].len, R, `${id} strut = circumradius`, 1e-6);
    [R, R, 1].sort((a, b) => a - b).forEach((x, i) => close(fins.classes[0].sides[i], x, `${id} fin: two circumradii and the edge`, 1e-6));
    const vol = volumes(s);
    close(vol.pyramids, vol.solid, `${id} pyramid volumes`, 1e-9);
  }
});

test('Star: each tip is the centre mirrored in its face plane', () => {
  for (const [id] of PLATONIC) {
    const s = vacuusSolidOf(POLYHEDRA[id]);
    starTipsOf(s).forEach((tip, i) => {
      const { n, c } = s.planes[i];
      close(dot(n, tip), 2 * c, `${id} face ${i}: tip at 2c`);
      close(Math.hypot(...tip), 2 * c, `${id} face ${i}: tip along the normal`);
    });
  }
});

test('classes: the rhombic dodecahedron has one fin shape and two strut lengths (8 and 6)', () => {
  const s = vacuusSolidOf(POLYHEDRA.RHOMBIC_DODECAHEDRON);
  assert.equal(finsOf(s).classes.length, 1);
  assert.deepEqual(strutsOf(s).classes.map((c) => c.count).sort(), [6, 8]);
  const ti = vacuusSolidOf(POLYHEDRA.TRUNCATED_ICOSAHEDRON);
  assert.deepEqual([finsOf(ti).fins.length, finsOf(ti).classes.length, strutsOf(ti).classes.length], [90, 1, 1]);
  const co = finsOf(vacuusSolidOf(POLYHEDRA.CUBOCTAHEDRON)).classes;
  assert.equal(co.length, 1);
  co[0].sides.forEach((x) => close(x, 1, 'cuboctahedron fins are equilateral', 1e-6));
});

test('applies beyond convex solids, but not where the centre is outside a face plane, nor to curved shapes', () => {
  assert.ok(vacuusSolidOf(POLYHEDRA.STELLA_OCTANGULA), 'the stella octangula (star-shaped about its centre)');
  assert.equal(vacuusSolidOf(POLYHEDRA.DICTO_HEXA), null, 'DICTO Hexa: its centre is outside some face planes');
  assert.equal(vacuusSolidOf(POLYHEDRA.REULEAUX_TETRAHEDRON), null, 'curved');
  const cube = POLYHEDRA.CUBE, bad = { vertices: cube.vertices, faces: cube.faces.map((f, i) => (i ? f : [...f].reverse())) };
  assert.equal(vacuusSolidOf(bad), null, 'faces not one consistently wound surface');
});

test('the cube, and only the cube, gets the rhombic dodecahedron line (DICTO 11-04; #87 Prop. 2)', () => {
  const cubes = Object.keys(POLYHEDRA).filter((id) => isCube(vacuusSolidOf(POLYHEDRA[id])));
  assert.ok(cubes.length >= 1, 'the cube is found');
  for (const id of cubes) {
    const s = vacuusSolidOf(POLYHEDRA[id]), tips = starTipsOf(s), P = [...s.vertices, ...tips];
    // the rhombic dodecahedron: the 6 tips at distance a from O and the 8 corners at a·√3/2, where a is the edge
    const a = Math.hypot(...s.vertices[s.edges[0][0]].map((x, k) => x - s.vertices[s.edges[0][1]][k]));
    tips.forEach((p) => close(Math.hypot(...p), a, `${id} tip at the edge length`, 1e-9));
    assert.equal(P.length, 14, `${id}: 14 corners`);
    // every old edge lies flat: the two tips across it and its two ends are coplanar (a rhombus)
    for (const [i, j] of s.edges) {
      const across = s.faces.map((f, fi) => [f, fi]).filter(([f]) => f.includes(i) && f.includes(j)).map(([, fi]) => tips[fi]);
      const [A, B] = [s.vertices[i], s.vertices[j]], [T, U] = across;
      const sub = (x, y) => x.map((v, k) => v - y[k]), cr = (u, v) => [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]];
      close(dot(cr(sub(B, A), sub(T, A)), sub(U, A)), 0, `${id}: edge ${i}-${j} flat`, 1e-9 * a ** 3);
    }
    const v = volumes(s).solid; close(v, a ** 3, `${id} cube volume`, 1e-9 * a ** 3);   // the Star adds the same again: 2a³
  }
  for (const id of ['tetrahedron', 'octahedron', 'dodecahedron', 'icosahedron', 'cuboctahedron']) {
    if (POLYHEDRA[id]) assert.equal(isCube(vacuusSolidOf(POLYHEDRA[id])), false, `${id} is not a cube`);
  }
});
