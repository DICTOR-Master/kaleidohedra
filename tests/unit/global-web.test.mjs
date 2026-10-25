// The Global Web of Bonds (DICTO 2026-10-25; src/app/world-global-web.js): the cells the world computes equal the exact study
// (k-research studies/2026-10-25-relay-census, data/raw/tables.md and the README's closed forms) for square + centres, honeycomb +
// centres and rock salt: at every stop and inside every interval, each kind's cell (corners or face vector), its bonds by neighbour
// kind, the cell areas / volumes and the bond sizes; the flips are exactly where the tables change; the named stops (4.8.8, 3.12.12,
// 3.6.3.6, regular hexagons, the rock salt pieces with all edges equal) hold; the near-neighbour list is enough; the 3D faces are the
// convex hull's; the web of bonds (webOf over the drawn pieces) has exactly the study's bond types and sizes. And the shared theorem
// sheet still draws DICTONIC's switch exactly as before.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { NETS, GLOBAL_WEB_NETWORKS, GLOBAL_WEB_STOPS, GLOBAL_WEB_VIEWS, STUDY_TABLES, BOND_SIZES, CELL_MEASURES, SWITCH, powerCell, globalWeb, globalWebFamily, tableRow } from '../../src/app/world-global-web.js';
import { convexPolygons } from '../../src/krp-core/src/polyhedra/golden-split.js';
import { switchPicture } from '../../src/app/theorem-sheet.js';

const S3 = Math.sqrt(3);
const close = (a, b, msg, tol = 1e-9) => assert.ok(Math.abs(a - b) < tol, `${msg}: ${a} vs ${b}`);
// a cell in the tables' words: 'point', 'n-gon' (2D) or the face vector '6×4+12×6' (3D, by face size)
function describe(name, c) {
  if (!c) return 'point';
  if (NETS[name].dim === 2) return `${c.points.length}-gon`;
  const by = new Map(); for (const f of c.points.faces) by.set(f.length, (by.get(f.length) ?? 0) + 1);
  return [...by].sort((a, b) => a[0] - b[0]).map(([n, k]) => `${k}×${n}`).join('+');
}
const bondsOf = (c) => (c ? c.facets.filter((f) => f.size > 1e-9).reduce((o, f) => ({ ...o, [f.kind]: (o[f.kind] ?? 0) + 1 }), {}) : {});
// the cell of each kind (the honeycomb's two classes are mirror images: both checked, they must agree)
function kindCells(name, l) {
  const net = NETS[name], out = {};
  net.motif.forEach(([kind], m) => {
    const c = powerCell(name, m, l), d = [describe(name, c), bondsOf(c), c?.measure ?? 0];
    if (out[kind]) assert.deepEqual(out[kind].slice(0, 2), d.slice(0, 2), `${name} λ=${l}: the ${kind} classes agree`); else out[kind] = d;
  });
  return net.kinds.map((k) => out[k]);
}
// sample points: every stop of the tables, and five points inside every open interval
const samples = (name) => STUDY_TABLES[name].flatMap(([w]) => (Array.isArray(w) ? [0.03, 0.2, 0.5, 0.8, 0.97].map((f) => w[0] + f * (w[1] - w[0])) : [w]));

for (const name of GLOBAL_WEB_NETWORKS) {
  test(`${name}: every stop and interval matches the study's tables (cells, bonds by kind), and the areas/volumes its closed forms`, () => {
    for (const l of samples(name)) {
      const row = tableRow(name, l), [a, b] = kindCells(name, l), [ma, mb] = CELL_MEASURES[name](l);
      assert.ok(row, `${name} λ=${l}: in the tables`);
      assert.deepEqual([a[0], a[1]], row[1], `${name} λ=${l}: ${NETS[name].kinds[0]} cell`);
      assert.deepEqual([b[0], b[1]], row[2], `${name} λ=${l}: ${NETS[name].kinds[1]} cell`);
      close(a[2], ma, `${name} λ=${l} A measure`); close(b[2], mb, `${name} λ=${l} B measure`);
      // the cells fill the plane / space: A and B measures in the motif's proportion add up to the translation cell
      const per = NETS[name].motif.reduce((s, [k]) => s + (k === NETS[name].kinds[0] ? a[2] : b[2]), 0);
      close(per, { square: 4, honeycomb: (3 * S3) / 2, nacl: 2 }[name], `${name} λ=${l} fills`);
    }
  });
  test(`${name}: the range, the one flip (the switch point) and the bond lives`, () => {
    const net = NETS[name], rows = STUDY_TABLES[name];
    assert.deepEqual([rows[0][0], rows[rows.length - 1][0]], [net.lo, net.hi], 'range ends');
    assert.deepEqual(rows.filter(([w]) => !Array.isArray(w)).map(([w]) => w), [net.lo, SWITCH[name], net.hi], 'stops of the tables: the ends and one flip');
    // just inside each end the small kind has a cell; at the end it is a point
    assert.equal(kindCells(name, net.lo)[0][0], 'point'); assert.equal(kindCells(name, net.hi)[1][0], 'point');
    assert.notEqual(kindCells(name, net.lo + 1e-4)[0][0], 'point'); assert.notEqual(kindCells(name, net.hi - 1e-4)[1][0], 'point');
    // the switch point: only unlike bonds; just before it the B–B bond, just after it the A–A bond
    const [A, B] = net.kinds, sw = SWITCH[name], d = 1e-4;
    const types = (l) => { const [ca, cb] = kindCells(name, l); return { aa: !!ca[1][A], bb: !!cb[1][B], ab: !!ca[1][B] }; };
    assert.deepEqual(types(sw), { aa: false, bb: false, ab: true }, 'only unlike bonds at the switch');
    assert.deepEqual(types(sw - d), { aa: false, bb: true, ab: true }, 'before');
    assert.deepEqual(types(sw + d), { aa: true, bb: false, ab: true }, 'after');
    for (const l of samples(name).filter((x) => x > net.lo && x < net.hi && x !== sw)) assert.ok(types(l).ab && (types(l).aa || types(l).bb) && !(types(l).aa && types(l).bb), `λ=${l}: one like bond`);
  });
  test(`${name}: every bond size is the study's closed form`, () => {
    for (const l of samples(name)) {
      const ex = BOND_SIZES[name](l), net = NETS[name];
      net.motif.forEach(([kind], m) => {
        const c = powerCell(name, m, l); if (!c) return;
        for (const f of c.facets) if (f.size > 1e-9) close(f.size, ex[f.kind !== kind ? 'ab' : kind === net.kinds[0] ? 'aa' : 'bb'], `${name} λ=${l} ${kind}–${f.kind}`);
      });
    }
  });
  test(`${name}: the near neighbours are enough (a list twice as far gives the same cells)`, () => {
    for (const l of samples(name)) NETS[name].motif.forEach((_, m) => {
      const c = powerCell(name, m, l), c2 = powerCell(name, m, l, 2.5 * NETS[name].reach2);
      assert.equal(describe(name, c), describe(name, c2)); close(c?.measure ?? 0, c2?.measure ?? 0, `${name} λ=${l} m=${m}`);
    });
  });
  test(`${name}: the web of bonds (webOf on the drawn pieces) has the study's bond types and sizes`, () => {
    for (const l of samples(name).filter((x) => x > NETS[name].lo && x < NETS[name].hi)) {
      const web = globalWeb(name, 2, l), ex = BOND_SIZES[name](l);
      const types = [...new Set(web.filter((w) => w[2] > 1e-9).map((w) => w[4]))].sort();
      assert.deepEqual(types, Object.keys(ex).filter((k) => ex[k] > 1e-9).sort(), `${name} λ=${l}: bond types`);
      for (const w of web) if (w[2] > 1e-9) close(w[2], ex[w[4]], `${name} λ=${l}: ${w[4]} size`, 1e-7);
    }
  });
  test(`${name}: the slider lands exactly on every stop; the world opens at the switch point`, () => {
    const pm = GLOBAL_WEB_VIEWS[name].param;
    for (const s of GLOBAL_WEB_STOPS[name]) assert.equal(pm.value(s.u), s.v);
    assert.equal(pm.value(pm.start), SWITCH[name]); assert.deepEqual(pm.pauseAt, [pm.start]);
    const us = GLOBAL_WEB_STOPS[name].map((s) => s.u); for (let i = 1; i < us.length; i++) assert.ok(us[i] - us[i - 1] > 40, 'stops further apart than the snap');
    assert.equal(pm.value(0), NETS[name].lo); assert.equal(pm.value(1000), NETS[name].hi);
  });
}

test('the named stops: 4.8.8 and 3.12.12 with all edges equal, 3.6.3.6 with edge √3/2, regular hexagons at 0, rock salt all edges equal at ±(4 − 2√3)', () => {
  const edgesOf = (name, l) => NETS[name].motif.flatMap((_, m) => { const c = powerCell(name, m, l); if (!c) return [];
    if (NETS[name].dim === 2) return c.facets.map((f) => f.size);
    return c.points.faces.flatMap((f) => f.map((k, i) => Math.hypot(...c.points.vertices[k].map((x, j) => x - c.points.vertices[f[(i + 1) % f.length]][j])))); });
  const allEqual = (name, l, e) => { const E = edgesOf(name, l); for (const x of E) close(x, e ?? E[0], `${name} λ=${l}`); };
  for (const l of [-(2 * Math.SQRT2 - 2), 2 * Math.SQRT2 - 2]) allEqual('square', l, 2 * Math.SQRT2 - 2);
  allEqual('honeycomb', 1 - S3, 2 * S3 - 3); allEqual('honeycomb', -0.5, S3 / 2); allEqual('honeycomb', 0, 1 / S3);
  for (const l of [-(4 - 2 * S3), 4 - 2 * S3]) { allEqual('nacl', l); assert.deepEqual(kindCells('nacl', l).map((c) => c[0]).sort(), ['6×4', '6×4+12×6']); }
  assert.deepEqual(kindCells('nacl', 1)[0][0], '12×4', 'rhombic dodecahedra at the ends');
});

test('3D faces = the convex hull of the corners (convexPolygons)', () => {
  for (const l of samples('nacl')) [0, 1].forEach((m) => { const c = powerCell('nacl', m, l); if (!c) return;
    const h = convexPolygons(c.points.vertices); assert.equal(h.faces.length, c.points.faces.length, `λ=${l}`); assert.equal(h.vertices.length, c.points.vertices.length); });
});

test('the pieces drawn: one per site of the ball, the shrunk kind left out at the ends', () => {
  for (const name of GLOBAL_WEB_NETWORKS) {
    const n = (l) => globalWebFamily(name, 2, l).reduce((o, [r]) => ({ ...o, [r]: (o[r] ?? 0) + 1 }), {});
    assert.ok(n(SWITCH[name]).gwA > 0 && n(SWITCH[name]).gwB > 0);
    assert.equal(n(NETS[name].lo).gwA, undefined); assert.equal(n(NETS[name].hi).gwB, undefined);
  }
});

test("the shared theorem sheet draws DICTONIC's switch exactly as before", () => {
  // the markup dictonic-theorem.js drew before the sheet was shared (cx 60, cy 40, a 38, b = a/√2)
  const old = (before, after) => { const cx = 60, cy = 40, a = 38, b = a / Math.SQRT2;
    return `<polygon points="${cx - a},${cy} ${cx},${cy - b} ${cx + a},${cy} ${cx},${cy + b}" fill="none" stroke="#9fa8c0" stroke-width="1.5"/>
        <line x1="${cx - a}" y1="${cy}" x2="${cx + a}" y2="${cy}" stroke="#9d8cff" stroke-width="${before ? 5 : 1.2}" ${before ? '' : 'stroke-dasharray="3 3"'}/>
        <line x1="${cx}" y1="${cy - b}" x2="${cx}" y2="${cy + b}" stroke="#ffc857" stroke-width="${after ? 5 : 1.2}" ${after ? '' : 'stroke-dasharray="3 3"'}/>
        ${[[cx - a, cy, '#9d8cff'], [cx + a, cy, '#9d8cff'], [cx, cy - b, '#ffc857'], [cx, cy + b, '#ffc857']].map(([px, py, c]) => `<circle cx="${px}" cy="${py}" r="5" fill="${c}"/>`).join('')}`; };
  for (const [bf, af] of [[true, false], [false, true], [false, false]]) assert.equal(switchPicture({ a: 38, b: 38 / Math.SQRT2, cols: ['#9d8cff', '#ffc857'], before: bf, after: af }), old(bf, af));
});
