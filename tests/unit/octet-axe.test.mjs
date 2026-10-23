// The AXE gap (DICTO 2026-10-23, study 2026-10-23-axe-gap): in the octet world's three simple cubic networks every cell is 1 Lotus
// Jewel + 1 void dodecahedron, 1 icosahedron + 1 Unborn, or 1 Lotus Jewel + 8 Tricaps + 1 Unborn, with 6 AXE; the pieces' volumes add
// up to phi^3 per cell; and the convex network (icosahedra, Unborns, AXE) covers every test point near the middle exactly once.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { OCTET_VIEWS, scSites, scPieces } from '../../src/app/world-octet.js';

const PHI = (1 + Math.sqrt(5)) / 2;
const sub = (a, b) => a.map((x, i) => x - b[i]);
const cross = (u, w) => [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]];
const dot = (u, w) => u[0] * w[0] + u[1] * w[1] + u[2] * w[2];
const volume = (V, F) => F.reduce((t, f) => { for (let m = 1; m + 1 < f.length; m++) t += dot(V[f[0]], cross(V[f[m]], V[f[m + 1]])) / 6; return t; }, 0);
const count = (list) => list.reduce((c, [r]) => ({ ...c, [r]: (c[r] ?? 0) + 1 }), {});
// A big block of whole cells: every site with -6 <= n <= 6 (icosahedra at even n, voids at odd n).
function block() {
  const ico = new Map(), voids = new Map();
  for (let x = -6; x <= 6; x++) for (let y = -6; y <= 6; y++) for (let z = -6; z <= 6; z++) {
    const n = [x, y, z], p = n.map((c) => Math.abs(c) % 2);
    if (p.every((c) => c === p[0])) (p[0] ? voids : ico).set(n.join(','), n);
  }
  return { ico, voids };
}

test('per cell: 6 AXE, 8 Tricaps, and volumes adding to phi^3', () => {
  const { ico, voids } = block(); // 7^3 icosahedra, 6^3 voids, 3 * 6^2 * 5 inner faces with 2 AXE each
  const want = { lotusJewel: { lotusJewel: 343, voidDodeca: 216 }, icoUnborn: { ico: 343, unborn: 216 }, axeNet: { lotusJewel: 343, tricap: 343 * 8, unborn: 216 } };
  for (const kind of ['lotusJewel', 'icoUnborn', 'axeNet']) {
    const list = scPieces(kind, ico, voids);
    assert.deepEqual(count(list), { ...want[kind], axe: 2 * 3 * 36 * 5 }, kind);
  }
  // one cell's pieces: the icosahedron's (and its Tricaps) at the origin, the void's at (1, 1, 1), and the 6 AXE on the faces x, y, z = 0 of
  // the cell (sites n = (0, 1, 1), (1, 0, 1), (1, 1, 0)) round that void
  for (const kind of ['lotusJewel', 'icoUnborn', 'axeNet']) {
    const list = scPieces(kind, new Map([['0,0,0', [0, 0, 0]]]), new Map([['1,1,1', [1, 1, 1]], ['-1,1,1', [-1, 1, 1]], ['1,-1,1', [1, -1, 1]], ['1,1,-1', [1, 1, -1]]]));
    const mine = list.filter(([r, V, , n]) => (r === 'axe' ? V.reduce((t, v) => t.map((c, i) => c + v[i] / 4), [0, 0, 0]).every((c) => c > -1e-9 && c < PHI - 1e-9) : n.join() === '0,0,0' || n.join() === '1,1,1'))
      .filter(([r, , , n]) => !(kind === 'axeNet' && r === 'tricap' && n.join() !== '0,0,0'));
    const v = mine.reduce((t, [, V, F]) => t + volume(V, F), 0);
    assert.equal(mine.filter(([r]) => r === 'axe').length, 6, `${kind}: 6 AXE in the cell`);
    assert.ok(Math.abs(v - PHI ** 3) < 1e-6, `${kind}: cell volume ${v} = phi^3`);
  }
});

test('icosahedra + Unborns + AXE: every point near the middle in exactly one piece', () => {
  const list = OCTET_VIEWS.icoUnborn.views.network(2);
  const planes = list.map(([, V, F]) => F.map((f) => { const n = cross(sub(V[f[1]], V[f[0]]), sub(V[f[2]], V[f[0]])); return [n, dot(n, V[f[0]])]; }));
  let seed = 7; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  for (let k = 0; k < 4000; k++) {
    const p = [0, 1, 2].map(() => (rnd() * 2 - 1) * PHI);
    const inside = planes.filter((pl) => pl.every(([n, d]) => dot(n, p) <= d + 1e-9)).length;
    assert.equal(inside, 1, `point ${p} in ${inside} pieces`);
  }
});

test('the growing networks', () => {
  for (const size of [1, 2, 3]) {
    const { ico, voids } = scSites(size);
    assert.ok(ico.has('0,0,0') && voids.size > 0);
    for (const kind of ['lotusJewel', 'icoUnborn', 'axeNet']) assert.ok(count(OCTET_VIEWS[kind].views.network(size)).axe > 0, `${kind} size ${size} has AXE`);
  }
});

// Mixed blocks (DICTO 2026-10-23): every pattern, block size and swap: the pieces are closed meshes with the volumes of their kind, and
// every test point near the middle lies in exactly one piece (winding numbers, the transition pieces being non-convex).
import { mixedPieces, MIXED_PATTERNS } from '../../src/app/world-octet.js';
const S5 = Math.sqrt(5), VOL = { mxIco: 5 * (3 + S5) / 12, mxJewel: (1 + 3 * S5) / 4, mxDodeca: (5 + S5) / 4, mxUnborn: (3 + 7 * S5) / 12, axe: 1 / 12 };
const TRICAP = (3 - S5) / 24;
function winding(V, F, p) {
  let w = 0;
  for (const f of F) for (let m = 1; m + 1 < f.length; m++) {
    const [a, b, c] = [f[0], f[m], f[m + 1]].map((i) => sub(V[i], p)), [la, lb, lc] = [a, b, c].map((x) => Math.hypot(...x));
    w += 2 * Math.atan2(dot(a, cross(b, c)), la * lb * lc + dot(a, b) * lc + dot(b, c) * la + dot(c, a) * lb);
  }
  return w / (4 * Math.PI);
}
for (const pattern of Object.keys(MIXED_PATTERNS)) {
  test(`mixed blocks, ${pattern}: closed pieces of the right volumes, space filled near the middle`, () => {
    for (const block of [1, 2, 3]) for (const swap of [false, true]) {
      const list = mixedPieces(1, { pattern, block, swap }), tag = `${pattern} ${block} ${swap}`;
      for (const [r, V, F] of list) {
        const E = new Map();
        for (const f of F) f.forEach((a, i) => E.set(`${a}>${f[(i + 1) % f.length]}`, 1));
        for (const k of E.keys()) { const [a, b] = k.split('>'); assert.ok(E.has(`${b}>${a}`), `${tag} ${r}: closed`); }
        const v = volume(V, F);
        if (VOL[r]) assert.ok(Math.abs(v - VOL[r]) < 1e-6, `${tag} ${r}: volume ${v}`);
        else { // a transition piece: an Unborn or a Lotus Jewel with 1 to 7 Tricaps
          const k = [VOL.mxUnborn, VOL.mxJewel].map((b) => (v - b) / TRICAP).find((x) => Math.abs(x - Math.round(x)) < 1e-5 && x > 0.5 && x < 7.5);
          assert.ok(k !== undefined, `${tag} ${r}: volume ${v} is a Jewel or an Unborn and 1-7 Tricaps`);
        }
      }
      const near = list.filter(([, V]) => Math.hypot(...V.reduce((t, x) => t.map((c, i) => c + x[i] / V.length), [0, 0, 0])) < 3);
      let seed = 11; const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
      for (let k = 0; k < 150; k++) {
        const p = [0, 1, 2].map(() => (rnd() * 2 - 1) * 1.25);
        if (Math.hypot(...p) > 1.25) continue; // inside every piece shown round the middle (the ball of size 1 + 1)
        const inside = near.filter(([, V, F]) => Math.abs(winding(V, F, p) - 1) < 1e-6).length;
        assert.equal(inside, 1, `${tag}: point ${p} in ${inside} pieces`);
      }
    }
  });
}
