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
