// Every Mix of the Platonic Solids (DICTO 2026-10-22; paper #47, DICTO DOI 10.5281/zenodo.23551326): the geometry of the world,
// ported from the paper's checked study (2026-10-22-platonic-mix-step1: mixes3.py, mixes2.py, pieces_figure.py). No three.js here,
// so the unit tests can run it. All solids edge 1; φ the golden ratio; s = 1/√2; L = φ²/√2.
// Space is cut by horizontal planes into slabs, one per "world" in the mix, stacked bottom to top (z up here):
//   D  dodecahedra (Euclid: cube of edge φ + 6 roofs) on alternate cubes of a cubic lattice of edge φ, Dogstars S in the others; a
//      boundary layer each side, X = cube minus the roof poking in from a dodecahedron, Y = cube plus the roof a Dogstar is missing;
//   C  cubes (edge 1);
//   TO the octet (edge 1), its octahedra at both faces cut into half octahedra P; an octahedron not in the mix is 2 P, a tetrahedron
//      not in the mix 4 Q (its face pyramids);
//   I  icosahedra in Pacioli's position in octahedra of edge L, the rest of each octahedron six Admiral Caps A; a large octet between
//      two of its (111) layer planes, its tetrahedra as 4 Q′ each.
// A block of about 3 × 3 cells across: pieces whose cell (or parent solid) centre lies in the square |x|, |y| < FOOTPRINT.
// A piece is { kind, slab, faces: [[x, y, z][]] } (each face a convex polygon, corners in order; closed surface).
export const PHI = (1 + Math.sqrt(5)) / 2;
const s = Math.SQRT1_2, L = PHI * PHI / Math.SQRT2, h = PHI / 2;
export const WORLDS = ['D', 'I', 'C', 'T', 'O'];      // the letter toggles, in the name's order
export const SOLID_KINDS = ['D', 'I', 'C', 'T', 'O'];
export const HELPER_KINDS = ['P', 'Q', 'Q′', 'A', 'S', 'X', 'Y'];
export const FOOTPRINT = 1.5 * PHI;                    // half-width: the D slab's 3 × 3 cubes of edge φ

const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
const mul = (a, k) => [a[0] * k, a[1] * k, a[2] * k];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const mean = (P) => mul(P.reduce(add, [0, 0, 0]), 1 / P.length);
const EPS = 1e-9;

/** The faces of the convex hull of a few points: every plane through three of them with all on one side, corners in order. */
export function hullFaces(V) {
  const c = mean(V), planes = [];
  for (let a = 0; a < V.length; a++) for (let b = a + 1; b < V.length; b++) for (let d = b + 1; d < V.length; d++) {
    let n = cross(sub(V[b], V[a]), sub(V[d], V[a])); const l = Math.hypot(...n);
    if (l < 1e-9) continue;
    n = mul(n, 1 / l); let o = dot(n, V[a]);
    if (dot(n, c) > o) { n = mul(n, -1); o = -o; }
    if (V.some((v) => dot(n, v) > o + 1e-7)) continue;
    if (planes.some(([m, p]) => Math.abs(p - o) < 1e-7 && Math.hypot(...sub(m, n)) < 1e-7)) continue;
    planes.push([n, o]);
  }
  return planes.map(([n, o]) => {
    const F = V.filter((v) => Math.abs(dot(n, v) - o) < 1e-7), fc = mean(F), u = sub(F[0], fc), w = cross(n, u);
    return F.sort((p, q) => Math.atan2(dot(sub(p, fc), w), dot(sub(p, fc), u)) - Math.atan2(dot(sub(q, fc), w), dot(sub(q, fc), u)));
  });
}
const key = (v) => v.map((x) => x.toFixed(6)).join(',');
const signedVolume = (faces) => { let v = 0; for (const F of faces) for (let i = 1; i + 1 < F.length; i++) v += dot(F[0], cross(F[i], F[i + 1])); return v / 6; };
/** A closed surface's polygons turned so that neighbours run along a shared edge in opposite directions, outward (positive volume). */
function orient(faces) {
  const F = faces.map((f) => [...f]), edges = new Map(), done = F.map(() => false);
  const ek = (a, b) => [key(a), key(b)].sort().join('|');
  F.forEach((f, i) => f.forEach((v, a) => { const k = ek(v, f[(a + 1) % f.length]); if (!edges.has(k)) edges.set(k, []); edges.get(k).push(i); }));
  for (let st = 0; st < F.length; st++) {
    if (done[st]) continue;
    done[st] = true; const stack = [st];
    while (stack.length) {
      const i = stack.pop(), f = F[i];
      f.forEach((v, a) => {
        const w = f[(a + 1) % f.length];
        for (const j of edges.get(ek(v, w))) {
          if (j === i || done[j]) continue;
          const g = F[j], same = g.some((u, b) => key(u) === key(v) && key(g[(b + 1) % g.length]) === key(w));
          if (same) F[j] = g.reverse();
          done[j] = true; stack.push(j);
        }
      });
    }
  }
  return signedVolume(F) > 0 ? F : F.map((f) => [...f].reverse());
}
const moved = (faces, f) => faces.map((F) => F.map(f));
const shift = (faces, t) => moved(faces, (v) => add(v, t));
const flipZ = (faces) => faces.map((F) => F.map(([x, y, z]) => [x, y, -z]).reverse());

// ---- the dodecahedron of edge 1 = the cube [-h, h]³ + 6 roofs (Euclid's orientation, as in the study)
const CUBE_V = []; for (const x of [-h, h]) for (const y of [-h, h]) for (const z of [-h, h]) CUBE_V.push([x, y, z]);
function roof(axis, sg) {
  const face = CUBE_V.filter((c) => Math.abs(c[axis] - sg * h) < EPS), ridge = [];
  for (const t of [0.5, -0.5]) { const p = [0, 0, 0]; p[axis] = sg * PHI * PHI / 2; p[(axis + 2) % 3] = t; ridge.push(p); }
  return face.concat(ridge);
}
const DOD_V = CUBE_V.concat(...[0, 1, 2].flatMap((a) => [1, -1].map((sg) => roof(a, sg).slice(4))));
const CUBE_F = hullFaces(CUBE_V);
const UNIT_V = []; for (const x of [0, 1]) for (const y of [0, 1]) for (const z of [0, 1]) UNIT_V.push([x, y, z]);
const UNIT_F = hullFaces(UNIT_V);
const DOD_F = hullFaces(DOD_V);
/** A roof's faces other than its base on the cube face axis = sg·h. */
const roofSides = (R, axis, sg) => hullFaces(R).filter((F) => !F.every((v) => Math.abs(v[axis] - sg * h) < EPS));
const cubeWithout = (axis, sg) => CUBE_F.filter((F) => !F.every((v) => Math.abs(v[axis] - sg * h) < EPS));
const inward = (axis, sg) => roof(axis, sg).map((v) => { const w = [...v]; w[axis] = 2 * sg * h - w[axis]; return w; });
// S Dogstar: the cube of edge φ minus the six roofs poking in (its surface: the six inward roofs' sides)
const S_F = orient([0, 1, 2].flatMap((a) => [1, -1].flatMap((sg) => roofSides(inward(a, sg), a, sg))));
// X cube minus a roof (on its top face); Y cube plus a roof (on its top face)
const X_F = orient(cubeWithout(2, 1).concat(roofSides(inward(2, 1), 2, 1)));
const Y_F = orient(cubeWithout(2, 1).concat(roofSides(roof(2, 1), 2, 1)));

// ---- the octahedron (edge L) with the Pacioli icosahedron (edge 1) inside, and its six Admiral Caps
const ICO_V = [];
for (const a of [1, -1]) for (const b of [PHI, -PHI]) ICO_V.push([0, a / 2, b / 2], [a / 2, b / 2, 0], [b / 2, 0, a / 2]);
const ICO_F = hullFaces(ICO_V);
const R_OCT = PHI * PHI / 2;
const OCT_SIGNS = []; for (const x of [1, -1]) for (const y of [1, -1]) for (const z of [1, -1]) OCT_SIGNS.push([x, y, z]);
const FREE_ICO_F = ICO_F.filter((F) => !OCT_SIGNS.some((n) => Math.abs(dot(mean(F), n) - R_OCT) < 1e-6));
const unit = (v) => mul(v, 1 / Math.hypot(...v));
/** The Admiral Cap round the octahedron corner c: the 4 corner triangles of the octahedron faces there + the 2 free icosahedron faces nearest it. */
function capFaces(c) {
  const out = [];
  for (const n of OCT_SIGNS.filter((n) => dot(n, c) > 0)) {
    const on = ICO_V.filter((v) => Math.abs(dot(v, n) - R_OCT) < 1e-9).sort((p, q) => Math.hypot(...sub(p, c)) - Math.hypot(...sub(q, c)));
    out.push([c, on[0], on[1]]);
  }
  const near = [...FREE_ICO_F].sort((F, G) => Math.hypot(...sub(unit(mean(F)), unit(c))) - Math.hypot(...sub(unit(mean(G)), unit(c))));
  return out.concat(near.slice(0, 2));
}
const OCT_CORNERS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]].map((v) => mul(v, R_OCT));
const CAPS_F = OCT_CORNERS.map((c) => orient(capFaces(c)));

// ---- the rotation taking (1, 1, 1) to z (as in the study)
const RZ = (() => {
  const n = unit([1, 1, 1]), z = [0, 0, 1], ax0 = cross(n, z), S = Math.hypot(...ax0), c = dot(n, z), ax = mul(ax0, 1 / S);
  const K = [[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]];
  const KK = K.map((r) => [0, 1, 2].map((j) => r[0] * K[0][j] + r[1] * K[1][j] + r[2] * K[2][j]));
  return [0, 1, 2].map((i) => [0, 1, 2].map((j) => (i === j ? 1 : 0) + S * K[i][j] + (1 - c) * KK[i][j]));
})();
const rot = (v) => RZ.map((r) => dot(r, v));

const inFoot = (c) => Math.abs(c[0]) < FOOTPRINT && Math.abs(c[1]) < FOOTPRINT;
/** The 4 face pyramids of a tetrahedron (corners V): each face + the centre. */
const quarters = (V) => { const g = mean(V); return [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]].map((f) => hullFaces(f.map((i) => V[i]).concat([g]))); };

function dWorld(z0, slab) {
  const P = [], layers = 3, R = 1, mid = (k) => k > 0 && k < layers - 1, isD = (i, j, k) => mid(k) && (((i + j + k) % 2) + 2) % 2 === 0;
  const cell = (i, j, k) => [i * PHI, j * PHI, z0 + k * PHI + h];
  for (let i = -R; i <= R; i++) for (let j = -R; j <= R; j++) for (let k = 0; k < layers; k++) {
    const c = cell(i, j, k);
    if (isD(i, j, k)) { P.push({ kind: 'D', slab, faces: shift(DOD_F, c) }); continue; }
    if (mid(k)) { P.push({ kind: 'S', slab, faces: shift(S_F, c) }); continue; }
    const sg = k === 0 ? 1 : -1, n = [i, j, k + sg];         // the middle neighbour, above the bottom layer or below the top one
    const F = isD(...n) ? X_F : Y_F;
    P.push({ kind: isD(...n) ? 'X' : 'Y', slab, faces: shift(sg === 1 ? F : flipZ(F), c) });
  }
  return { pieces: P, top: z0 + layers * PHI };
}
function cWorld(z0, slab) {
  const P = [];
  for (let i = -3; i <= 2; i++) for (let j = -3; j <= 2; j++) if (inFoot([i + 0.5, j + 0.5])) P.push({ kind: 'C', slab, faces: shift(UNIT_F, [i, j, z0]) });
  return { pieces: P, top: z0 + 1 };
}
function toWorld(z0, mix, slab) {
  const P = [], K = 2, R = 4, O6 = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]];
  for (let x = -R; x <= R; x++) for (let y = -R; y <= R; y++) for (let z = 0; z <= K; z++) {
    const c = [x * s, y * s, z * s + z0];
    if (((x + y + z) % 2 + 2) % 2 === 1 && inFoot(c)) {
      const V = O6.map((d) => add(c, mul(d, s))), eq = V.filter((v) => Math.abs(v[2] - c[2]) < EPS);
      const up = hullFaces(eq.concat([add(c, [0, 0, s])])), dn = hullFaces(eq.concat([sub(c, [0, 0, s])]));
      if (z === 0) P.push({ kind: 'P', slab, faces: up });
      else if (z === K) P.push({ kind: 'P', slab, faces: dn });
      else if (mix.has('O')) P.push({ kind: 'O', slab, faces: hullFaces(V) });
      else P.push({ kind: 'P', slab, faces: up }, { kind: 'P', slab, faces: dn });
    }
    if (z === K) continue;
    const ev = [];
    for (const i of [0, 1]) for (const j of [0, 1]) for (const k of [0, 1]) if ((x + i + y + j + z + k) % 2 === 0) ev.push([(x + i) * s, (y + j) * s, (z + k) * s + z0]);
    if (!inFoot(mean(ev))) continue;
    if (mix.has('T')) P.push({ kind: 'T', slab, faces: hullFaces(ev) });
    else for (const q of quarters(ev)) P.push({ kind: 'Q', slab, faces: q });
  }
  return { pieces: P, top: z0 + K * s };
}
function iWorld(z0, slab) {
  const P = [], R = 4, top = z0 + L * Math.sqrt(2 / 3), O6 = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]];
  const place = (v) => add(rot(v), [0, 0, z0]);
  for (let x = -R; x <= R; x++) for (let y = -R; y <= R; y++) for (let z = -R; z <= R; z++) {
    if (((x + y + z) % 2 + 2) % 2 === 1) {
      const c = mul([x, y, z], s * L), m = place(c);
      if (m[2] > z0 + EPS && m[2] < top - EPS && inFoot(m)) {
        const at = (v) => place(add(c, v));
        P.push({ kind: 'I', slab, faces: moved(ICO_F, at) });
        for (const F of CAPS_F) P.push({ kind: 'A', slab, faces: moved(F, at) });
      }
    }
    const ev = [];
    for (const i of [0, 1]) for (const j of [0, 1]) for (const k of [0, 1]) if ((x + i + y + j + z + k) % 2 === 0) ev.push(place(mul([x + i, y + j, z + k], s * L)));
    const m = mean(ev);
    if (m[2] > z0 + EPS && m[2] < top - EPS && inFoot(m)) for (const q of quarters(ev)) P.push({ kind: 'Q′', slab, faces: q });
  }
  return { pieces: P, top };
}

export const SLAB_ORDER = ['D', 'C', 'TO', 'I'];
/** The slab worlds a mix uses, bottom to top (T and O share the octet slab 'TO'). */
export const slabsOf = (mixIn) => { const m = new Set(mixIn); return SLAB_ORDER.filter((w) => [...w].some((c) => m.has(c))); };
/** One slab on its own, from z = 0: its pieces (for the world, which stacks the slabs itself) and its height. */
export function slabPieces(world, mixIn, slab = 0) {
  const mix = new Set(mixIn);
  return world === 'D' ? dWorld(0, slab) : world === 'C' ? cWorld(0, slab) : world === 'TO' ? toWorld(0, mix, slab) : iWorld(0, slab);
}
/** A piece's name within its slab: its kind and centre, so it survives a change of mix in the octet slab. */
export function pieceKey(p) {
  const c = mean(p.faces.flat());
  return `${p.kind}@${c.map((x) => (Math.round(x * 1000) / 1000).toFixed(3)).join(',')}`;
}
/** The centre of a piece (the mean of its face corners). */
export const pieceCentre = (p) => mean(p.faces.flat());

/** The slabs of a mix (a Set or string of the letters D I C T O), bottom to top: [{ world, z0, top }] and every piece. */
export function buildMix(mixIn) {
  const mix = new Set(mixIn), slabs = [], pieces = [];
  let z = 0;
  const put = (world, made) => { slabs.push({ world, z0: z, top: made.top }); pieces.push(...made.pieces); z = made.top; };
  if (mix.has('D')) put('D', dWorld(z, slabs.length));
  if (mix.has('C')) put('C', cWorld(z, slabs.length));
  if (mix.has('T') || mix.has('O')) put('TO', toWorld(z, mix, slabs.length));
  if (mix.has('I')) put('I', iWorld(z, slabs.length));
  return { slabs, pieces, top: z };
}
export const isSolid = (kind) => SOLID_KINDS.includes(kind);
/** The helper kinds a mix uses, in the panel's order. */
export function helpersOf(pieces) { const k = new Set(pieces.map((p) => p.kind)); return HELPER_KINDS.filter((x) => k.has(x)); }

/** A closed piece's volume (faces fanned into triangles; the divergence theorem, orientation-free by abs). */
export const pieceVolume = (p) => Math.abs(signedVolume(p.faces));
/** The templates, for the unit tests. */
export const TEMPLATES = { D: DOD_F, S: S_F, X: X_F, Y: Y_F, I: ICO_F, A: CAPS_F[0], C: UNIT_F };
