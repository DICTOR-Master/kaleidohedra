// Verifies the target cells (geometry-extensions/targets.js, data/geometry-targets.json, TARGETS.md):
//
//   - all 160 rebuild from their Gram matrices: unit directions with exactly that Gram matrix;
//   - each zonohedron is closed and outward, every edge has length 1, and its
//     faces by kind and its volume are the ones recorded;
//   - each tiles space by translation: three face translations form a basis of
//     determinant = volume, and no translate in the lattice overlaps it
//     (separating axis on the face normals, which include every edge-pair cross);
//   - TARGETS.md lists the same cells in the same order (per type: faces, volume,
//     built status), and the type counts agree;
//   - the emblem (#5) is also the truncated octahedron with one zone removed;
//   - names: "Type #n · angles" is unique for every cell.
import { readFileSync } from 'node:fs';
import { TARGET_TYPES, buildTarget, faceCounts, numberTargets, targetAngles, det3, zonohedron, volumeOf, EMBLEM_DIRECTIONS } from '../src/geometry-extensions/targets.js';

let failures = 0;
function check(label, condition) {
  console.log(`${condition ? 'OK  ' : 'FAIL'} ${label}`);
  if (!condition) failures++;
}
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const sub = (a, b) => a.map((c, i) => c - b[i]);
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const norm = (a) => Math.hypot(...a);
const sameCounts = (a, b) => Object.keys({ ...a, ...b }).every((k) => a[k] === b[k]);

const data = JSON.parse(readFileSync(new URL('../data/geometry-targets.json', import.meta.url)));
const targets = numberTargets(data.targets);
const built = targets.map(buildTarget);
check(`${targets.length} targets, all of the five Fedorov types`, targets.length === 160 && targets.every((t) => TARGET_TYPES.includes(t.type)));

check('directions: unit vectors whose Gram matrix is the recorded one (to 1e-8)',
  built.every((b) => b.directions.every((u, i) => b.directions.every((v, j) => Math.abs(dot(u, v) - targets[built.indexOf(b)].gram[i][j]) < 1e-8))));

// Closed and outward: every directed edge appears once each way; the normal agrees with the winding and points away from the centre.
const rk = (v) => v.map((c) => (Math.round(c * 1e6) / 1e6 + 0).toFixed(6)).join();
const closed = (faces) => {
  const seen = new Map();
  for (const { polygon: P } of faces) for (let i = 0; i < P.length; i++) { const k = `${rk(P[i])}>${rk(P[(i + 1) % P.length])}`; seen.set(k, (seen.get(k) ?? 0) + 1); }
  return [...seen.keys()].every((k) => { const [a, b] = k.split('>'); return seen.get(k) === 1 && seen.get(`${b}>${a}`) === 1; });
};
const outward = (faces) => faces.every(({ polygon: P, normal, centre }) => dot(cross(sub(P[1], P[0]), sub(P[2], P[1])), normal) > 0 && dot(centre, normal) > 0);
check('every cell is closed and outward', built.every((b) => closed(b.faces) && outward(b.faces)));
check('every edge has length 1', built.every((b) => b.faces.every(({ polygon: P }) => P.every((p, i) => Math.abs(norm(sub(P[(i + 1) % P.length], p)) - 1) < 1e-9))));
check('faces by kind match the recorded ones for all 160', built.every((b, i) => sameCounts(faceCounts(b.faces), targets[i].faces)));
check('volumes match the recorded ones (to 1e-6)', built.every((b, i) => Math.abs(b.volume - targets[i].volume) < 1e-6));

// Tiling: a basis of determinant = volume, and no overlapping translate.
check('each has three face translations forming a basis of determinant = volume', built.every((b) => b.basis && Math.abs(Math.abs(det3(...b.basis)) - b.volume) < 1e-6));
function overlapsSomeTranslate(b) {
  const verts = b.faces.flatMap((f) => f.polygon);
  const R = Math.max(...verts.map(norm));
  const normals = b.faces.map((f) => f.normal);
  const h = normals.map((m) => Math.max(...verts.map((v) => dot(v, m))));
  const N = 4;
  for (let i = -N; i <= N; i++) for (let j = -N; j <= N; j++) for (let k = -N; k <= N; k++) {
    if (!i && !j && !k) continue;
    const t = [0, 1, 2].map((a) => i * b.basis[0][a] + j * b.basis[1][a] + k * b.basis[2][a]);
    if (norm(t) >= 2 * R) continue;
    if (normals.every((m, n) => Math.abs(dot(t, m)) < 2 * h[n] - 1e-9)) return true;
  }
  return false;
}
check('no lattice translate overlaps its cell (so, with the volume, each tiles space)', built.every((b) => b.basis && !overlapsSomeTranslate(b)));

// TARGETS.md: the same list, in the same order.
const md = readFileSync(new URL('../TARGETS.md', import.meta.url), 'utf8');
const sections = {};
let current = null;
for (const line of md.split('\n')) {
  const h = line.match(/^## (.+?) — .*\((\d+)\)$/);
  if (h) { current = TARGET_TYPES.find((t) => t === h[1].toLowerCase()) ?? null; if (current) sections[current] = { count: +h[2], rows: [] }; continue; }
  const r = current && line.match(/^\| (\d+) \| (.+?) \| (.+?) \| ([\d.]+) \| (.+?) \|$/);
  if (r) sections[current].rows.push({ n: +r[1], faces: Object.fromEntries(r[2].split(', ').map((s) => { const m = s.match(/^(\d+) (.+)$/); return [m[2], +m[1]]; })), volume: +r[4], status: r[5] });
}
const byType = (type) => targets.filter((t) => t.type === type);
check('TARGETS.md has a section per type with the right count', TARGET_TYPES.every((type) => sections[type]?.count === byType(type).length && sections[type].rows.length === byType(type).length));
check('TARGETS.md rows match the data in order: number, faces, volume',
  TARGET_TYPES.every((type) => byType(type).every((t, i) => { const r = sections[type].rows[i]; return r.n === t.number && sameCounts(r.faces, t.faces) && r.volume === Number(t.volume.toPrecision(6)); })));
check('TARGETS.md status: "built: ID" exactly where the data names a Polyhedraverse piece',
  TARGET_TYPES.every((type) => byType(type).every((t, i) => { const s = sections[type].rows[i].status; return t.in_polyhedraverse.length ? s.startsWith(`built: ${t.in_polyhedraverse[0]}`) : s === 'to find'; })));

// Each built hexagon's label names its corners; measure them on the polygon itself (not from the label).
// The six corners must sum to 720 and match the label, each corner value twice.
const interiorAngles = (P) => P.map((_, i) => {
  const a = P[(i - 1 + P.length) % P.length], c = P[(i + 1) % P.length], b0 = P[i];
  const u = sub(a, b0), v = sub(c, b0);
  return Math.acos(Math.max(-1, Math.min(1, dot(u, v) / norm(u) / norm(v)))) * 180 / Math.PI;
});
const labelCorners = (kind) => kind.slice('hexagon '.length).split('/').map(Number);
check('built hexagon corners measure 720 in total and match their labels (to 0.01)',
  built.every((b) => b.faces.every((f) => {
    if (!f.kind.startsWith('hexagon ')) return true;
    const measured = interiorAngles(f.polygon).map((x) => Math.round(x * 100) / 100).sort((x, y) => y - x);
    const sum = measured.reduce((x, y) => x + y, 0);
    const labelled = [...labelCorners(f.kind), ...labelCorners(f.kind)].sort((x, y) => y - x);
    return Math.abs(sum - 720) < 0.01 && measured.every((x, i) => Math.abs(x - labelled[i]) < 0.01);
  })));

const summary = Object.fromEntries([...md.matchAll(/^\| ([a-z ]+) \| sheared [^|]+\| (\d+) \| (\d+) \| (\d+) \|$/gm)].map((m) => [m[1], +m[4]]));
const total = md.match(/^\| \*\*total\*\* \|.*\*\*(\d+)\*\* \|$/m);
check('TARGETS.md summary: "In Polyhedraverse" per type and in total agree with the data',
  TARGET_TYPES.every((type) => summary[type] === byType(type).filter((t) => t.in_polyhedraverse.length).length) && +total?.[1] === targets.filter((t) => t.in_polyhedraverse.length).length);

const names = targets.map((t) => `${t.type} #${t.number} · ${targetAngles(t)}`);
check(`names "Type #n · angles" are unique (${new Set(names).size})`, new Set(names).size === targets.length);
const emblem = zonohedron(EMBLEM_DIRECTIONS);
check('emblem: the regular-hexagon ED, 4 regular hexagons + 4 squares + 4 60-degree rhombi, volume 4 sqrt2', sameCounts(faceCounts(emblem), { 'regular hexagon': 4, square: 4, 'rhombus 60': 4 }) && Math.abs(volumeOf(emblem) - 4 * Math.SQRT2) < 1e-9);
// DISCOVERIES.md #5: the same cell by Fedorov's route, the truncated octahedron with one zone removed.
const TO = [[1, 1, 0], [1, -1, 0], [1, 0, 1], [1, 0, -1], [0, 1, 1], [0, 1, -1]].map((v) => v.map((c) => c * Math.SQRT1_2));
const angleSet = (D) => D.flatMap((a, i) => D.slice(i + 1).map((b) => Math.abs(dot(a, b)).toFixed(9))).sort().join();
const contracted = zonohedron(TO.slice(1));
check('the truncated octahedron with one zone removed is the emblem: same edge-direction angles, faces and volume',
  angleSet(TO.slice(1)) === angleSet(EMBLEM_DIRECTIONS) && sameCounts(faceCounts(contracted), faceCounts(emblem)) && Math.abs(volumeOf(contracted) - volumeOf(emblem)) < 1e-9);
const builtCount = targets.filter((t) => t.in_polyhedraverse.length).length;
console.log(`(${builtCount} of ${targets.length} are in Polyhedraverse)`);

console.log(failures === 0 ? '\nAll checks passed (0 failures).' : `\n${failures} check(s) FAILED.`);
process.exit(failures === 0 ? 0 : 1);
