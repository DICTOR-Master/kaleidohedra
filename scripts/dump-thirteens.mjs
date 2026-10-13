// Gathers every 13's kits from their checked sources into one JSON (DICTO 2026-10-13, docs/PLAN-13.md stage 1).
// Usage: node scripts/dump-thirteens.mjs <rd13 rounded json (0.15, exact RD centre)> <fattest json (0.35, exact RD centre)> <free-centre json (0.15)> > thirteens-raw.json
import fs from 'fs';
import { ICOSA_PARTS } from '../src/krp-core/src/geometry-extensions/icosa.js';
import { DODECA13_PARTS } from '../src/krp-core/src/polyhedra/dodeca13.js';
import SEEDS from '../src/app/seeds-data.js';
import STAR from '../src/app/dodeca-data.js';
const conv = (list) => list.map((p) => [p.role, p.vertices, p.faces]);
const d13 = DODECA13_PARTS.DICTO_DODECA13;
// RD 13: plain (13 RDs of the FCC lattice, neighbours sqrt2 apart) and the rounded keyed block (studies/2026-10-13-rd13-block)
const NB = []; for (const x of [-1, 0, 1]) for (const y of [-1, 0, 1]) for (const z of [-1, 0, 1]) { const a = [x, y, z].map(Math.abs).sort(); if (a[0] === 0 && a[1] === 1 && a[2] === 1) NB.push([x, y, z]); }
const rdCell = (p) => {
  const V = [], key = (v) => v.map((c) => c.toFixed(6)).join(','), at = (v) => { let i = V.findIndex((w) => key(w) === key(v)); if (i < 0) { V.push(v); i = V.length - 1; } return i; };
  const F = NB.map((n) => { const [i, j] = [0, 1, 2].filter((k) => n[k]); const k = 3 - i - j; const e = (m, s) => [0, 1, 2].map((q) => (q === m ? s : 0));
    const add = (...vs) => [0, 1, 2].map((q) => p[q] + vs.reduce((t, v) => t + v[q], 0));
    return [add(e(i, n[i])), add(e(i, n[i] / 2), e(j, n[j] / 2), e(k, 0.5)), add(e(j, n[j])), add(e(i, n[i] / 2), e(j, n[j] / 2), e(k, -0.5))].map(at); });
  return [V, F];
};
// Every face wound outward (normal away from the cell's middle).
const outward = ([V, F]) => {
  const c = [0, 1, 2].map((q) => V.reduce((t, v) => t + v[q], 0) / V.length);
  return [V, F.map((f) => {
    const [a, b, d] = f.map((i) => V[i]); const u = [0, 1, 2].map((q) => b[q] - a[q]), w = [0, 1, 2].map((q) => d[q] - a[q]);
    const n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]];
    const m = [0, 1, 2].map((q) => f.reduce((t, i) => t + V[i][q], 0) / f.length - c[q]);
    return n[0] * m[0] + n[1] * m[1] + n[2] * m[2] < 0 ? [...f].reverse() : f;
  })];
};
const plain = [[0, 0, 0], ...NB].map((p, i) => { const [V, F] = outward(rdCell(p)); return [i ? 'rd' : 'rdCentre', V, F]; });
const R = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const blockOf = (R) => R.cells.map((faces, ci) => {
  const V = [], key = (v) => v.map((c) => c.toFixed(6)).join(','), at = (v) => { let i = V.findIndex((w) => key(w) === key(v)); if (i < 0) { V.push(v); i = V.length - 1; } return i; };
  const [, F] = outward([V, faces.map((f) => f.map(at))]);
  return [ci === 0 ? 'rdCentre' : Math.abs(R.volumes[ci] - R.volumes[1]) < 1e-3 ? 'rdA' : 'rdB', V, F];
});
const rounded = blockOf(R);
// The fattest outer pieces (DICTO 2026-10-13: "I like the fattest RDs"), minimum thickness 0.35, as a second rounded view.
const fattest = process.argv[3] ? blockOf(JSON.parse(fs.readFileSync(process.argv[3], 'utf8'))) : null;
// The free-centre block (DICTO 2026-10-13: exact RD centre as main, free as variant).
const roundedFree = process.argv[4] ? blockOf(JSON.parse(fs.readFileSync(process.argv[4], 'utf8'))) : null;
const out = {
  dodeca13: { pieces: conv(d13.pieces), units: conv(d13.units), stars: conv(d13.stars) },
  icosa13: { pieces: conv(ICOSA_PARTS.LOTUS_SEED.pieces), build: conv(ICOSA_PARTS.LOTUS_SEED.build), units: conv(ICOSA_PARTS.LOTUS_SEED.units) },
  unity: { open: conv(ICOSA_PARTS.UNITY.pieces), venus: conv(ICOSA_PARTS.VENUS.pieces) },
  deshi: { deshi: conv(ICOSA_PARTS.DESHI.pieces) },
  bodhi: { seed: SEEDS.bodhi.views.seed.filter((p) => p[0] !== 'outer'), kitA: SEEDS.bodhi.views.kitA, kitB: SEEDS.bodhi.views.kitB },
  dictoStar: { star: STAR.star.views.star },
  // Seven rounded blocks: one and its six nearest neighbours (plus and minus the block lattice's three short vectors), keyed.
  rd13: { plain, rounded, ...(fattest ? { fattest } : {}), ...(roundedFree ? { roundedFree } : {}), blocks: [[0, 0, 0], ...R.L.flatMap((t) => [t, t.map((x) => -x)])].flatMap((t, b) => rounded.map(([role, V, F]) => [b ? `${role}N` : role, V.map((v) => v.map((x, q) => x + t[q])), F])) },
};
process.stdout.write(JSON.stringify(out));
