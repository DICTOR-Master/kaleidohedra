// Star step (DICTO's Star Cores papers, #79 Sections 2–3): the star core treatment of a convex solid, one step at a time.
// Star: every face's pyramid from the centre O turned outwards as a spike, its tip by one of three rules:
//   polar     the pole of the face plane n·x = c (n unit) in the sphere of radius ρ about O, p = ρ² n / c, with ρ² = φR² (R the
//             circumradius about O): the main theorem of #79 — the halo is the polar solid, and the layer between star and halo is
//             tiled exactly by one pyramid over each corner (apex the corner, base the tips of its faces) and one tetrahedron over
//             each edge (the edge and the tips of its two faces);
//   doubling  tip = 2 × the foot of the face perpendicular (the pyramid mirrored in its face, #78's Double TI Star);
//   golden    tip = φ × the foot.
// Halo: the convex hull of the tips (white-queen-geometry.js's hull, coplanar triangles merged into real faces).
// Next: the halo, scaled back to the solid's circumradius, is the next solid of the star chain.
// Pure maths, no three.js.
import { hull } from './white-queen-geometry.js';

export const PHI = (1 + Math.sqrt(5)) / 2;
export const RULES = ['polar', 'doubling', 'golden'];

const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const scale = (a, s) => [a[0] * s, a[1] * s, a[2] * s];
const norm = (a) => Math.hypot(a[0], a[1], a[2]);

/** Newell normal of a face loop (not normalised; its length is twice the face's area). */
function newell(P, f) {
  const n = [0, 0, 0];
  for (let i = 0; i < f.length; i++) {
    const a = P[f[i]], b = P[f[(i + 1) % f.length]];
    n[0] += (a[1] - b[1]) * (a[2] + b[2]); n[1] += (a[2] - b[2]) * (a[0] + b[0]); n[2] += (a[0] - b[0]) * (a[1] + b[1]);
  }
  return n;
}

/** A solid in star-step form, centred on the mean of its corners: { vertices, faces (outward loops), edges, planes: [{ n, c, area }],
 *  R (circumradius about the centre) }; null when it is not convex or its centre is not inside every face. */
export function solidOf({ vertices, faces }) {
  const m = [0, 1, 2].map((k) => vertices.reduce((s, v) => s + v[k], 0) / vertices.length);
  const V = vertices.map((v) => sub(v, m));
  const R = Math.max(...V.map(norm));
  if (!(R > 0)) return null;
  const F = [], planes = [];
  for (const f0 of faces) {
    let f = [...f0], nn = newell(V, f);
    const area = norm(nn) / 2;
    if (area < 1e-12 * R * R) return null;
    let n = scale(nn, 1 / (2 * area)), c = dot(n, V[f[0]]);
    if (c < 0) { f = f.reverse(); n = scale(n, -1); c = -c; }
    if (c < 1e-9 * R) return null;                                                    // the centre must be inside every face's pyramid
    if (V.some((v) => dot(n, v) > c + 1e-7 * R)) return null;                         // convex: every corner on the inner side
    F.push(f); planes.push({ n, c, area });
  }
  const seen = new Set(), E = [];
  for (const f of F) f.forEach((a, i) => { const b = f[(i + 1) % f.length], k = a < b ? `${a},${b}` : `${b},${a}`; if (!seen.has(k)) { seen.add(k); E.push([a, b]); } });
  return { vertices: V, faces: F, edges: E, planes, R };
}

/** ρ² of the polar rule: φR². */
export const rho2Of = (solid) => PHI * solid.R * solid.R;

/** The spike tips, one per face, by the rule. */
export function tipsOf(solid, rule = 'polar') {
  const r2 = rho2Of(solid);
  return solid.planes.map(({ n, c }) => scale(n, rule === 'polar' ? r2 / c : (rule === 'doubling' ? 2 : PHI) * c));
}

/** Signed volume of a closed solid of outward loops. */
export function volumeOf(P, F) {
  let v = 0;
  for (const f of F) for (let i = 1; i + 1 < f.length; i++) v += dot(P[f[0]], cross(P[f[i]], P[f[i + 1]])) / 6;
  return v;
}
const tetVolume = (a, b, c, d) => Math.abs(dot(sub(b, a), cross(sub(c, a), sub(d, a)))) / 6;

/** The faces round each corner, in order round it: for corner v, the face indices in turn (outward loops: across the edge v→w
 *  out of one face lies the face with w→v). */
export function facesRound(solid) {
  const byEdge = new Map();
  solid.faces.forEach((f, fi) => f.forEach((a, i) => byEdge.set(`${a},${f[(i + 1) % f.length]}`, fi)));
  return solid.vertices.map((_, v) => {
    const start = solid.faces.findIndex((f) => f.includes(v));
    const ring = [];
    for (let fi = start, guard = 0; guard <= solid.faces.length; guard++) {
      ring.push(fi);
      const f = solid.faces[fi], w = f[(f.indexOf(v) + 1) % f.length];
      fi = byEdge.get(`${w},${v}`);
      if (fi === undefined || fi === start) break;
    }
    return ring;
  });
}

/** One star step's whole picture for a solid and a rule: { tips, spikes (one pyramid per face: { face, tip }), halo ({ vertices,
 *  faces }, outward), contains (the halo holds the star), layer (polar rule only, when the halo holds the star: { corners: [{ apex,
 *  base }], edges: [[a, b, p, q]] }), volumes { solid, star, halo, layer } }. */
export function starStep(solid, rule = 'polar') {
  const tips = tipsOf(solid, rule);
  const H = hull(tips);
  const hv = H.vertices, re = new Map(hv.map((k, i) => [k, i]));
  const halo = { vertices: hv.map((k) => H.points[k]), faces: H.faces.map((f) => f.map((k) => re.get(k))) };
  const scaleR = solid.R;
  const hPlanes = halo.faces.map((f) => { const nn = newell(halo.vertices, f), n = scale(nn, 1 / norm(nn)); return { n, d: dot(n, halo.vertices[f[0]]) }; });
  const contains = solid.vertices.every((v) => hPlanes.every(({ n, d }) => dot(n, v) <= d + 1e-9 * scaleR));
  const vSolid = volumeOf(solid.vertices, solid.faces);
  const vSpikes = solid.planes.reduce((s, { n, c, area }, i) => s + area * (dot(n, tips[i]) - c) / 3, 0);
  const out = { tips, halo, contains, layer: null, volumes: { solid: vSolid, star: vSolid + vSpikes, halo: volumeOf(halo.vertices, halo.faces), layer: null } };
  if (rule === 'polar' && contains) {
    const ring = facesRound(solid);
    const corners = solid.vertices.map((apex, v) => ({ apex, base: ring[v].map((fi) => tips[fi]) }));
    const faceOf = new Map();
    solid.faces.forEach((f, fi) => f.forEach((a, i) => faceOf.set(`${a},${f[(i + 1) % f.length]}`, fi)));
    const edges = solid.edges.map(([a, b]) => [solid.vertices[a], solid.vertices[b], tips[faceOf.get(`${a},${b}`)], tips[faceOf.get(`${b},${a}`)]]);
    let vLayer = 0;
    for (const { apex, base } of corners) for (let i = 1; i + 1 < base.length; i++) vLayer += tetVolume(apex, base[0], base[i], base[i + 1]);
    for (const e of edges) vLayer += tetVolume(...e);
    out.layer = { corners, edges };
    out.volumes.layer = vLayer;
  }
  return out;
}

/** The next solid of the chain: the halo, scaled back to circumradius R. */
export function nextSolid(step, R) {
  const r = Math.max(...step.halo.vertices.map(norm));
  return solidOf({ vertices: step.halo.vertices.map((v) => scale(v, R / r)), faces: step.halo.faces });
}
