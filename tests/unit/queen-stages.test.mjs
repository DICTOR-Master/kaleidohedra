// The five stages between the queens (DICTO 2026-10-30; src/app/queen-stages-geometry.js): each built from the White Queen's own
// corners has the classical counts of corners and edges (Coxeter's uniform polytopes), every edge one length, every corner on one
// sphere of radius 2, and a shadow in each of the four main directions.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { STAGE_KEYS, STAGE_FACTS, stage, stageShadowAt } from '../../src/app/queen-stages-geometry.js';
import { DIRECTIONS } from '../../src/app/white-queen-geometry.js';

test('seven stops: White, five stages, Red', () => assert.deepEqual(STAGE_KEYS, ['white', 't01', 't1', 't12', 't2', 't23', 'red']));
for (const [k, f] of Object.entries(STAGE_FACTS)) {
  test(`${k}: ${f.V} corners on one sphere, ${f.E} equal edges, degree 2E/V`, () => {
    const s = stage(k); assert.equal(s.vertices.length, f.V); assert.equal(s.edges.length, f.E);
    s.vertices.forEach((v) => assert.ok(Math.abs(Math.hypot(...v) - 2) < 1e-9));
    const L = s.edges.map(([a, b]) => Math.hypot(...s.vertices[a].map((x, i) => x - s.vertices[b][i])));
    assert.ok(Math.max(...L) - Math.min(...L) < 1e-9);
    const deg = new Array(f.V).fill(0); s.edges.flat().forEach((i) => deg[i]++); assert.ok(deg.every((d) => d === (2 * f.E) / f.V));
  });
}
test('a shadow in every main direction', () => {
  for (const k of Object.keys(STAGE_FACTS)) for (const d of DIRECTIONS) { const s = stageShadowAt(k, d, d, 0); assert.ok(s.faces.length > 0 && s.P.length === STAGE_FACTS[k].V); }
});
// The slider's Red end (DICTO 2026-11-16): the Red Queen drawn along the White Queen's turnings, so each named view keeps one 4D
// direction and frame from stage 1 to 6. The two sets of directions are swapped exactly, and her outlines there are her own atlas counts
// of the swapped direction (80, 160, 180, 158 along the White Queen's vertex-, edge-, face-, cell-first).
test('the Red end along the White Queen: one direction from stage 1 to 6, outlines 80 / 160 / 180 / 158', async () => {
  const W = await import('../../src/app/white-queen-geometry.js'), R = await import('../../src/app/red-queen-geometry.js');
  const RQ = (await import('../../src/app/red-queen-data.js')).default;
  const want = { 'vertex-first': 80, 'edge-first': 160, 'face-first': 180, 'cell-first': 158 };
  for (const d of DIRECTIONS) {
    const sw = R.WHITE_AS_RED[d], i = DIRECTIONS.indexOf(d), j = DIRECTIONS.indexOf(sw);
    assert.ok(Math.abs(W.UNIT_DIRECTIONS[i].reduce((s, x, k) => s + x * R.UNIT_DIRECTIONS[j][k], 0) - 1) < 1e-12, `${d} = Red ${sw}`);
    const red = R.shadowAlongWhite(d, d, 0), st1 = stageShadowAt('t01', d, d, 0);
    assert.deepEqual(red.u, st1.u); assert.deepEqual(red.frame, W.viewAt(d, d, 0).frame);
    assert.equal(red.vertices.length, want[d]); assert.equal(red.vertices.length, RQ.shadows[sw].V);
  }
  // part way along a turning too: the same 4D direction for a stage and for the Red end
  const a = R.shadowAlongWhite('vertex-first', 'cell-first', 0.37), c = stageShadowAt('t23', 'vertex-first', 'cell-first', 0.37);
  assert.deepEqual(a.u, c.u);
});
