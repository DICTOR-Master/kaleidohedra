// The Stackings World's geometry (DICTO 2026-10-26): the pieces of paper #57, "The Rule of Halves: the Holes of Every Close-Packed
// Stacking" (DICTO DOI 10.5281/zenodo.23647898), computed for any stacking word. Units and weights are the study's
// (k-research studies/2026-10-25-stackings/scripts/stackings.py): ball spacing 1, layers √(2/3) apart, in-plane positions
// A = 0, B = (a1 + a2)/3, C = 2(a1 + a2)/3; in the gap between layers k and k+1 (letters X, Y) one octahedral hole over the third
// letter Z at mid-height and two tetrahedral holes, over X at 3/4 (nearest layer k+1) and over Y at 1/4 (nearest layer k).
// Each piece is the power cell of its hole with w_tet = λ, w_oct = 0, λ ∈ [−11/24, 3/8]. An octahedral piece is cut at its mid-plane
// into a bottom half (decided by layer k) and a top half (layer k+1). A layer is h when its two neighbours share a letter, else c.
const S3 = Math.sqrt(3);
export const LAYER_H = Math.sqrt(2 / 3);
export const LAM_LO = -11 / 24, LAM_HI = 3 / 8;
const A1 = [1, 0, 0], A2 = [0.5, S3 / 2, 0];
const POS = { A: [0, 0], B: [1 / 3, 1 / 3], C: [2 / 3, 2 / 3] };
const EPS = 1e-9;
const sub = (a, b) => a.map((x, i) => x - b[i]);
const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const inPlane = ([f, g]) => [f * A1[0] + g * A2[0], f * A1[1] + g * A2[1]];

/** The standard polytypes as ABC words (Ramsdell names). */
export const PRESETS = { '3C': 'ABC', '2H': 'AB', '4H': 'ABAC', '6H': 'ABCACB', '9R': 'ABACACBCB', '15R': 'ABCACBCABACABCB' };

export function validWord(word) {
  const n = word.length;
  return n >= 2 && /^[ABC]+$/.test(word) && [...word].every((x, i) => x !== word[(i + 1) % n]);
}
/** h or c for every layer of a periodic word (Jagodzinski). */
export const layerTypes = (word) => [...word].map((x, k, w) => (w[(k - 1 + w.length) % w.length] === w[(k + 1) % w.length] ? 'h' : 'c'));

/** One period of holes: [{ kind: 'tet' | 'oct', p: [x, y, z], layer (tets: nearest layer; octs: the layer below), gap }]. */
export function holes(word) {
  const n = word.length, out = [];
  for (let k = 0; k < n; k++) {
    const X = word[k], Y = word[(k + 1) % n], Z = 'ABC'.replace(X, '').replace(Y, '');
    const at = (L, f) => [...inPlane(POS[L]), (k + f) * LAYER_H];
    out.push({ kind: 'oct', p: at(Z, 0.5), layer: k, gap: k });
    out.push({ kind: 'tet', p: at(X, 0.75), layer: (k + 1) % n, gap: k });
    out.push({ kind: 'tet', p: at(Y, 0.25), layer: k, gap: k });
  }
  return out;
}
const weight = (kind, lam) => (kind === 'tet' ? lam : 0);

// every hole within reach of p, over the lattice translations (period n layers)
function neighbours(word, hs, p, reach) {
  const n = word.length, H = n * LAYER_H, out = [], m = Math.ceil(reach) + 2, mz = Math.ceil(reach / H) + 1;
  for (const h of hs) for (let i = -m; i <= m; i++) for (let j = -m; j <= m; j++) for (let l = -mz; l <= mz; l++) {
    const q = [h.p[0] + i * A1[0] + j * A2[0], h.p[1] + i * A1[1] + j * A2[1], h.p[2] + l * H], d = sub(q, p), d2 = dot(d, d);
    if (d2 > EPS && d2 <= reach * reach) out.push({ kind: h.kind, d });
  }
  return out;
}

/** The convex solid { vertices, faces, volume } cut out by half-spaces n·x ≤ b (coordinates about the site), or null if it is empty or flat. */
export function solidOf(H) {
  const pts = [], ok = (p) => H.every((h) => dot(h.n, p) <= h.b + 1e-9);
  for (let i = 0; i < H.length; i++) for (let j = i + 1; j < H.length; j++) {
    for (let k = j + 1; k < H.length; k++) {
      const A = H[i].n, B = H[j].n, C = H[k].n, bc = cross(B, C), det = dot(A, bc);
      if (Math.abs(det) < 1e-12) continue;
      const p = [0, 1, 2].map((c) => (H[i].b * bc[c] + H[j].b * cross(C, A)[c] + H[k].b * cross(A, B)[c]) / det);
      if (ok(p) && !pts.some((q) => Math.hypot(...sub(p, q)) < 1e-8)) pts.push(p);
    }
  }
  if (pts.length < 4) return null;
  const faces = [], seen = new Set();
  for (const h of H) {
    const on = pts.map((_, i) => i).filter((i) => Math.abs(dot(h.n, pts[i]) - h.b) < 1e-7), key = on.join(',');
    if (on.length < 3 || seen.has(key)) continue;
    const fc = on.reduce((a, i) => a.map((x, c) => x + pts[i][c] / on.length), [0, 0, 0]), u = sub(pts[on[0]], fc), w = cross(h.n, u);
    const f = on.sort((i, j) => Math.atan2(dot(sub(pts[i], fc), w), dot(sub(pts[i], fc), u)) - Math.atan2(dot(sub(pts[j], fc), w), dot(sub(pts[j], fc), u)));
    if (area(f.map((i) => pts[i])) < 1e-10) continue;
    seen.add(key); faces.push(f);
  }
  const volume = vol(pts, faces);
  return volume < 1e-10 ? null : { vertices: pts, faces, volume };
}
function area(P) {
  let x = 0, y = 0, z = 0;
  for (let i = 1; i + 1 < P.length; i++) { const c = cross(sub(P[i], P[0]), sub(P[i + 1], P[0])); x += c[0]; y += c[1]; z += c[2]; }
  return Math.hypot(x, y, z) / 2;
}
function vol(V, F) {
  const c = V.reduce((a, p) => a.map((x, i) => x + p[i] / V.length), [0, 0, 0]);
  return F.reduce((s, f) => {
    for (let m = 1; m + 1 < f.length; m++) s += Math.abs(dot(sub(V[f[0]], c), cross(sub(V[f[m]], c), sub(V[f[m + 1]], c))));
    return s;
  }, 0) / 6;
}

/** The pieces of one column (one period) at λ, about the origin of the column:
 *  [{ role: 'tet' | 'octBottom' | 'octTop', type: 'c' | 'h', layer, gap, site, vertices, faces, volume }]. Vanished pieces are left out. */
export function stackingPieces(word, lam, reach = 1.4) {
  const hs = holes(word), types = layerTypes(word), n = word.length, out = [];
  for (const h of hs) {
    const H = neighbours(word, hs, h.p, reach).map((q) => ({ n: q.d.map((x) => 2 * x), b: dot(q.d, q.d) - weight(q.kind, lam) + weight(h.kind, lam) }));
    const parts = h.kind === 'tet' ? [['tet', h.layer, H]]
      : [['octBottom', h.layer, [...H, { n: [0, 0, 1], b: 0 }]], ['octTop', (h.layer + 1) % n, [...H, { n: [0, 0, -1], b: 0 }]]];
    for (const [role, layer, planes] of parts) {
      const s = solidOf(planes);
      if (s) out.push({ role, type: types[layer], layer, gap: h.gap, site: h.p, vertices: s.vertices.map((v) => v.map((x, i) => x + h.p[i])), faces: s.faces, volume: s.volume });
    }
  }
  return out;
}

/** The census of a word: c/h layer counts, neighbour pairs (below→above), and the tetrahedral / octahedral share of space at λ. */
export function census(word, lam, pieces = stackingPieces(word, lam)) {
  const types = layerTypes(word), n = word.length, pairs = { cc: 0, ch: 0, hc: 0, hh: 0 };
  types.forEach((t, k) => { pairs[t + types[(k + 1) % n]]++; });
  const tet = pieces.filter((p) => p.role === 'tet').reduce((s, p) => s + p.volume, 0), oct = pieces.filter((p) => p.role !== 'tet').reduce((s, p) => s + p.volume, 0);
  return { c: types.filter((t) => t === 'c').length, h: types.filter((t) => t === 'h').length, pairs, tetShare: tet / (tet + oct), octShare: oct / (tet + oct), total: tet + oct };
}
