# Buildable great icosahedron (DICTO, 2026-10-14, option 2): Polyhedraverse's icosahedron (D20, edge 1) as the core, plus 20 congruent face
# units: each the part of the great icosahedron (the stellation whose core is D20) inside the cone from the centre over one face, minus
# the core. Units are built from the 413 stellation cells clipped by the cone, merged into one solid per face (boundary = facets covered
# from one side only, per plane). Writes src/krp-core/src/polyhedra/great-icosahedron.js. DICTO · dictospheres.com
import itertools, json, math, os, sys, collections
import numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
import shapely
from shapely.geometry import Polygon
from shapely.ops import unary_union
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); K = os.path.expanduser('~/kaleidohedra')
phi = (1 + 5 ** .5) / 2
V = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float) / 2   # edge 1 = D20's size
D = np.linalg.norm(V[:, None] - V[None], axis=2)
ICO = [list(t) for t in itertools.combinations(range(12), 3) if all(abs(D[a, b] - 1) < 1e-9 for a, b in itertools.combinations(t, 2))]
for f in ICO:                                                     # orient outward
    a, b, c = V[f]
    if np.cross(b - a, c - a) @ a < 0: f[1], f[2] = f[2], f[1]
N = np.array([V[f].mean(0) for f in ICO]); h = np.linalg.norm(N[0]); N /= np.linalg.norm(N, axis=1)[:, None]   # planes n.x = h
# great icosahedron with these planes: its corners are V scaled so that its faces (edge phi triangles of V) lie at distance h
GI = [t for t in itertools.combinations(range(12), 3) if all(abs(D[a, b] - phi) < 1e-9 for a, b in itertools.combinations(t, 2))]
dg = float(np.mean([abs(np.cross(V[b] - V[a], V[c] - V[a]) @ V[a]) / np.linalg.norm(np.cross(V[b] - V[a], V[c] - V[a])) for a, b, c in GI]))
P = V * h / dg
def winding(X):
    w = np.zeros(len(X))
    for a, b, c in GI:
        A, B, C = P[a] - X, P[b] - X, P[c] - X; la, lb, lc = [np.linalg.norm(Y, axis=1) for Y in (A, B, C)]
        num = np.einsum('ij,ij->i', A, np.cross(B, C)); den = la * lb * lc + np.einsum('ij,ij->i', A, B) * lc + np.einsum('ij,ij->i', A, C) * lb + np.einsum('ij,ij->i', B, C) * la
        w += np.sign(P[[a, b, c]].mean(0) @ np.cross(P[b] - P[a], P[c] - P[a])) * 2 * np.arctan2(num, den)
    return np.round(w / (4 * np.pi)).astype(int)
def cell(hs):
    r = linprog(c=[0, 0, 0, -1], A_ub=np.c_[hs[:, :3], np.linalg.norm(hs[:, :3], axis=1)], b_ub=-hs[:, 3], bounds=[(None, None)] * 3 + [(0, None)])
    if r.status != 0 or r.x[3] < 1e-7: return None
    Y = HalfspaceIntersection(hs, r.x[:3]).intersections; Y = Y[ConvexHull(Y).vertices]; Z = []
    for y in Y:
        if all(np.linalg.norm(y - z) > 1e-7 * h for z in Z): Z.append(y)
    return np.array(Z)
R = np.linalg.norm(P[0]); rng = np.random.default_rng(7)
X = rng.uniform(-R, R, (1_500_000, 3)); X = X[np.linalg.norm(X, axis=1) < R]; X = X[winding(X) != 0]
keys = np.unique((X @ N.T > h).astype(np.int8), axis=0)
cells = [c for k in keys if (c := cell(np.c_[N * np.where(k == 1, -1.0, 1.0)[:, None], -h * np.where(k == 1, -1.0, 1.0)])) is not None]
assert len(cells) == 413, len(cells)
core = [c for c in cells if len(c) == 12 and np.linalg.norm(c.mean(0)) < 1e-9][0]
# face 0's cone: x = a A + b B + c C with a, b, c >= 0  <=>  (B x C).x >= 0 etc.
f0 = ICO[0]; A, B, C = V[f0]
cone = np.array([np.r_[-np.cross(B, C), 0], np.r_[-np.cross(C, A), 0], np.r_[-np.cross(A, B), 0]])
pieces = []
for c in cells:
    if c is core: continue
    hc = ConvexHull(c); hs = np.r_[np.unique(np.round(hc.equations, 12), axis=0), cone]
    q = cell(hs)
    if q is not None and ConvexHull(q).volume > 1e-10: pieces.append(q)
# merge into one solid: per plane, facets covered from one side only
def facets(Q):
    hq = ConvexHull(Q); out = []
    for e in np.unique(np.round(hq.equations, 10), axis=0):
        on = np.where(np.abs(Q @ e[:3] + e[3]) < 1e-8)[0]; out.append((e, Q[on]))
    return out
def canon(e):
    n, d = e[:3], e[3]; i = int(np.argmax(np.abs(n)));  s = 1 if n[i] > 0 else -1
    return tuple(np.round(np.r_[n * s, d * s], 7)), s
def merge(pieces):
    verts, faces = [], []
    def vid(p):
        for i, q in enumerate(verts):
            if np.linalg.norm(q - p) < 1e-7: return i
        verts.append(p); return len(verts) - 1
    plane = {}
    for Q in pieces:
        for e, F in facets(Q):
            key, s = canon(e); plane.setdefault(key, {1: [], -1: []})[s].append(F)
    for key, sides in plane.items():
        n = np.array(key[:3]); d = key[3]; o = -d * n; u = np.cross(n, [1, 0, 0] if abs(n[0]) < .9 else [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(n, u)
        to2 = lambda F: Polygon([((p - o) @ u, (p - o) @ w) for p in F[np.argsort(np.arctan2((F - F.mean(0)) @ w, (F - F.mean(0)) @ u))]])
        U = {s: unary_union([to2(F) for F in L]).buffer(0) if L else Polygon() for s, L in sides.items()}
        for s, region in ((1, U[1].difference(U[-1])), (-1, U[-1].difference(U[1]))):    # facets of pieces with outward normal s*n
            region = region.buffer(0)
            geoms = getattr(region, 'geoms', [region])
            for g in geoms:
                if g.is_empty or g.area < 1e-10: continue
                g = shapely.simplify(g, 1e-9)
                tris = [g] if not g.interiors else list(shapely.constrained_delaunay_triangles(g).geoms)
                for t in tris:
                    pts = [o + x * u + y * w for x, y in list(t.exterior.coords)[:-1]]
                    idx = [vid(p) for p in pts]
                    # orient outward (normal s*n)
                    P3 = np.array(pts); nn = sum(np.cross(P3[k], P3[(k + 1) % len(P3)]) for k in range(len(P3)))   # Newell normal (robust to collinear corners)
                    if nn @ (s * n) < 0: idx = idx[::-1]
                    faces.append(idx)
    V3 = np.array(verts)
    # no T-junctions: put every corner lying on a face's edge into that face
    for fi, f in enumerate(faces):
        g = []
        for k in range(len(f)):
            a, b = V3[f[k]], V3[f[(k + 1) % len(f)]]; g.append(f[k]); L = np.linalg.norm(b - a)
            if L < 1e-9: continue
            on = [(np.dot(V3[j] - a, b - a) / L ** 2, j) for j in range(len(V3)) if j not in (f[k], f[(k + 1) % len(f)])
                  and np.linalg.norm(np.cross(V3[j] - a, b - a)) / L < 1e-7 and 1e-7 < np.dot(V3[j] - a, b - a) / L ** 2 < 1 - 1e-7]
            g += [j for _, j in sorted(on)]
        faces[fi] = [x for i, x in enumerate(g) if x != g[i - 1]]
    return V3, faces
verts, faces = merge(pieces)
def mesh_volume(Vt, F):
    return sum(np.dot(Vt[f[0]], np.cross(Vt[f[k]], Vt[f[k + 1]])) for f in F for k in range(1, len(f) - 1)) / 6
vol_unit = mesh_volume(verts, faces); vol_pieces = sum(ConvexHull(Q).volume for Q in pieces)
vol_gi = sum(ConvexHull(c).volume for c in cells)
checks = dict(cells=len(cells), unit_pieces=len(pieces), unit_volume_mesh=vol_unit, unit_volume_pieces=vol_pieces,
              core_plus_20_units=ConvexHull(core).volume + 20 * vol_unit, great_icosahedron=vol_gi, unit_corners=len(verts), unit_faces=len(faces),
              great_ico_edge=float(np.linalg.norm(P[GI[0][0]] - P[GI[0][1]])), great_ico_radius=float(np.linalg.norm(P[0])))
print(json.dumps(checks, indent=1))
assert abs(vol_unit - vol_pieces) < 1e-5 and abs(checks['core_plus_20_units'] - vol_gi) < 1e-4
json.dump(checks, open(os.path.join(ROOT, 'great-ico-kit-checks.json'), 'w'), indent=1)
json.dump(dict(unit=dict(v=verts.tolist(), f=faces), V=V.tolist(), ICO=ICO), open(os.path.join(ROOT, 'great-ico-unit.json'), 'w'))

# the unit's placements, and the module, in D20's own frame
checks.update(unit_edges_once=sum(v == 1 for v in collections.Counter(tuple(sorted((f[k], f[(k + 1) % len(f)]))) for f in faces for k in range(len(f))).values()))
D20 = np.array(json.load(open(sys.argv[1])), float)
def kabsch(S, T):
    U, _, Wt = np.linalg.svd(T.T @ S); Rm = U @ np.diag([1, 1, np.sign(np.linalg.det(U @ Wt))]) @ Wt; return Rm
Rw = None
for perm in itertools.permutations(range(12), 3):
    if not all(abs(np.linalg.norm(D20[perm[i]] - D20[perm[j]]) - 1) < 1e-6 for i, j in ((0, 1), (1, 2), (0, 2))): continue
    Rm = kabsch(V[ICO[0]], D20[list(perm)])
    if np.abs(V @ Rm.T)[:, None].shape and all(np.min(np.linalg.norm(D20 - x, axis=1)) < 1e-6 for x in V @ Rm.T): Rw = Rm; break
assert Rw is not None
sys.path.insert(0, os.path.join(K, 'studies/2026-10-14-fuji-family/scripts'))
def quat(Rm):
    tr = np.trace(Rm); m = max(range(4), key=lambda i: [tr, Rm[0, 0], Rm[1, 1], Rm[2, 2]][i])
    if m == 0: w = math.sqrt(1 + tr) / 2; x, y, z = (Rm[2, 1] - Rm[1, 2]) / (4 * w), (Rm[0, 2] - Rm[2, 0]) / (4 * w), (Rm[1, 0] - Rm[0, 1]) / (4 * w)
    elif m == 1: x = math.sqrt(1 + 2 * Rm[0, 0] - tr) / 2; w, y, z = (Rm[2, 1] - Rm[1, 2]) / (4 * x), (Rm[0, 1] + Rm[1, 0]) / (4 * x), (Rm[0, 2] + Rm[2, 0]) / (4 * x)
    elif m == 2: y = math.sqrt(1 + 2 * Rm[1, 1] - tr) / 2; w, x, z = (Rm[0, 2] - Rm[2, 0]) / (4 * y), (Rm[0, 1] + Rm[1, 0]) / (4 * y), (Rm[1, 2] + Rm[2, 1]) / (4 * y)
    else: z = math.sqrt(1 + 2 * Rm[2, 2] - tr) / 2; w, x, y = (Rm[1, 0] - Rm[0, 1]) / (4 * z), (Rm[0, 2] + Rm[2, 0]) / (4 * z), (Rm[1, 2] + Rm[2, 1]) / (4 * z)
    q = np.array([x, y, z, w]); return (q / np.linalg.norm(q)).round(12).tolist()
UV = verts @ Rw.T; cU = UV.mean(0); UNIT = UV - cU          # unit in D20's frame, centred
entries = [dict(shape='D20', position=[0, 0, 0], quaternion=[0, 0, 0, 1])]
F0 = V[ICO[0]] @ Rw.T
for f in ICO:
    T = V[f] @ Rw.T; Rm = None
    for r in range(3):
        cand = kabsch(F0, np.roll(T, r, axis=0))
        if np.allclose(F0 @ cand.T, np.roll(T, r, axis=0), atol=1e-9) and np.linalg.det(cand) > 0: Rm = cand; break
    assert Rm is not None
    entries.append(dict(shape='GREAT_ICO_UNIT', position=[round(float(x), 12) for x in Rm @ cU], quaternion=quat(Rm)))
RAW = {'GREAT_ICO_UNIT': dict(name='Great icosahedron face unit (one of 20 round the icosahedron)', vertices=UNIT.round(12).tolist(), faces=faces)}
KITS = {'greatIcosahedron': dict(label='Great icosahedron · icosahedron + 20 face units', group='stars', entries=entries)}
js = ('// Generated by studies/2026-10-14-cycles/scripts/great_ico_kit.py (DICTO 2026-10-14). Do not edit.\n'
      '// The great icosahedron made buildable: Polyhedraverse\'s icosahedron (D20) + 20 congruent face units.\n'
      "import { specOf } from './stellaJewel.js';\n"
      f'const RAW = {json.dumps(RAW, separators=(",", ":"))};\n'
      'export const GREAT_ICO_ADDITIONS = Object.fromEntries(Object.entries(RAW).map(([id, p]) => [id, specOf(id, p.name, p.vertices, p.faces, true, 1)]));\n'
      'export const GREAT_ICO_ADDITION_IDS = Object.keys(GREAT_ICO_ADDITIONS);\n'
      f'export const GREAT_ICO_KITS = {json.dumps(KITS, separators=(",", ":"))};\n')
open(os.path.join(K, 'src/krp-core/src/polyhedra/great-icosahedron.js'), 'w').write(js)
json.dump(checks, open(os.path.join(ROOT, 'great-ico-kit-checks.json'), 'w'), indent=1); print(json.dumps(checks, indent=1))
