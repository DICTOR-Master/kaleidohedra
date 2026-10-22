# Builds src/app/reuleaux-data.js (the film) and src/krp-core/src/polyhedra/reuleaux-bodies.js (the five bodies, shared with Polyhedraverse) (DICTO 2026-10-21): The Reuleaux Platonic Solids, DICTO's #45 (DICTO DOI 10.5281/zenodo.23529499).
# For each Platonic solid (edge 1) the body is the common part of balls centred on its corners, radius D = the solid's diameter (its
# widest span). Named by look: balls on the tetrahedron -> Reuleaux tetrahedron, cube -> Reuleaux octahedron, octahedron -> Reuleaux
# cube, dodecahedron -> Reuleaux icosahedron, icosahedron -> Reuleaux dodecahedron.
#   - the film: the common part of the balls at 16 radii, from just past the circumradius R (where it first exists, as one point) up to
#     D, where it is the Reuleaux body (the last frame is the build body itself);
#   - the build: the body, each triangle tagged with its ball patch (face), the seams between patches (the only lines drawn), and each
#     face's corners: the points where three or more patches meet, found exactly (points at distance D from three centres, inside every
#     ball), listed counter-clockwise seen from outside.
# Meshes: manifold3d sphere intersection (as the study, studies/2026-10-21-reuleaux-platonic/reuleaux_platonic.py), then each patch
# simplified on its own with its border kept (pyfqmr), so the seams stay exact and the data stays small. Coordinates as integers x 1e4.
# Needs manifold3d, pyfqmr, numpy (run on dicto-node). Usage: python3 scripts/build-reuleaux-data.py [repo root]
import itertools, json, os, sys
import numpy as np, manifold3d as m3, pyfqmr
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
phi = (1 + 5 ** .5) / 2; Q = 10000
def cyc(v): return [np.roll(v, k) for k in range(3)]
SOURCES = {'Tetrahedron': [p for p in itertools.product((1, -1), repeat=3) if np.prod(p) > 0],
           'Cube': list(itertools.product((1, -1), repeat=3)),
           'Octahedron': [s * e for e in np.eye(3) for s in (1, -1)],
           'Dodecahedron': list(itertools.product((1, -1), repeat=3)) + [w for a, b in itertools.product((1, -1), repeat=2) for w in cyc(np.array([0, a / phi, b * phi]))],
           'Icosahedron': [w for a, b in itertools.product((1, -1), repeat=2) for w in cyc(np.array([0, a, b * phi]))]}
# key (by look), source solid, look name; the order the app shows them in
BODIES = [('tetrahedron', 'Tetrahedron', 'Reuleaux tetrahedron'), ('octahedron', 'Cube', 'Reuleaux octahedron'),
          ('cube', 'Octahedron', 'Reuleaux cube'), ('icosahedron', 'Dodecahedron', 'Reuleaux icosahedron'),
          ('dodecahedron', 'Icosahedron', 'Reuleaux dodecahedron')]
FRAMES = 16
SEG_FILM, SEG_BODY = 64, 128                          # sphere segments: film frames, the build body
TRIS_FILM, TRIS_BODY = 700, 2400                      # triangles kept per mesh

def intersect(V, r, seg):
    body = None
    for v in V:
        b = m3.Manifold.sphere(r, seg).translate(list(v)); body = b if body is None else body ^ b
    return body

def simplify_by_patch(P, T, own, target):
    """Simplify each ball patch on its own, its border kept, then weld the patches back along the seams."""
    outV, outT, outL, index = [], [], [], {}
    def vid(p):
        k = tuple(np.round(p, 7))
        if k not in index: index[k] = len(outV); outV.append(p)
        return index[k]
    for lab in np.unique(own):
        sub = T[own == lab]; used = np.unique(sub); remap = {int(u): i for i, u in enumerate(used)}
        Vs = P[used]; Ts = np.vectorize(remap.get)(sub)
        n = max(8, int(round(target * len(sub) / len(T))))
        if len(sub) > n:
            s = pyfqmr.Simplify(); s.setMesh(Vs, Ts); s.simplify_mesh(target_count=n, aggressiveness=4, preserve_border=True, verbose=False)
            Vs, Ts, _ = s.getMesh()
        for tri in Ts:
            ids = [vid(Vs[i]) for i in tri]
            if len(set(ids)) == 3: outT.append(ids); outL.append(int(lab))
    return np.array(outV), np.array(outT), np.array(outL)

def label(P, T, V, r):
    X = P[T].mean(1); return np.argmin(np.abs(np.linalg.norm(X[:, None] - V[None], axis=2) - r), axis=1)

def seams(T, own):
    by = {}
    for f, tri in enumerate(T):
        for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])): by.setdefault((min(a, b), max(a, b)), []).append(f)
    return [[int(a), int(b)] for (a, b), fs in by.items() if len(fs) == 2 and own[fs[0]] != own[fs[1]]]

def mesh_ok(P, T):
    mf = m3.Manifold(m3.Mesh(vert_properties=np.array(P, np.float32), tri_verts=np.array(T, np.uint32)))
    return mf.status() == m3.Error.NoError, mf.volume()

def corners(V, D):
    """Points at distance D from three or more centres and inside every ball: where three or more patches meet."""
    out = []
    for i, j, k in itertools.combinations(range(len(V)), 3):
        a, b, c = V[i], V[j], V[k]
        # |x-a|=|x-b|=|x-c|=D: x on the line through the circumcentre of abc, normal to its plane
        n = np.cross(b - a, c - a)
        if np.linalg.norm(n) < 1e-12: continue
        A = np.array([b - a, c - a, n]); rhs = np.array([(b @ b - a @ a) / 2, (c @ c - a @ a) / 2, n @ a])
        o = np.linalg.solve(A, rhs); h2 = D * D - (o - a) @ (o - a)
        if h2 < 0: continue
        u = n / np.linalg.norm(n)
        for x in (o + u * h2 ** .5, o - u * h2 ** .5):
            if (np.linalg.norm(V - x, axis=1) <= D + 1e-9).all() and not any(np.linalg.norm(x - y) < 1e-7 for y in out): out.append(x)
    return np.array(out)

def q(a): return [int(round(x * Q)) for x in np.asarray(a, float).ravel()]

OUT = {'Q': Q, 'frames': FRAMES, 'bodies': []}
report = []
CORE = []   # the build bodies, to krp-core (Polyhedraverse shapes and this world share them)
for key, src, name in BODIES:
    V = np.array(SOURCES[src], float); E = min(np.linalg.norm(a - b) for a, b in itertools.combinations(V, 2)); V /= E
    D = max(np.linalg.norm(a - b) for a, b in itertools.combinations(V, 2)); R = float(np.linalg.norm(V[0]))
    edges = [[i, j] for i, j in itertools.combinations(range(len(V)), 2) if abs(np.linalg.norm(V[i] - V[j]) - 1) < 1e-9]
    # the bare solid: its hull triangles (for its glass faces)
    hull = m3.Manifold.hull_points(V.tolist()).to_mesh(); HP = np.asarray(hull.vert_properties[:, :3]); HT = np.asarray(hull.tri_verts)
    hmap = [int(np.argmin(np.linalg.norm(V - p, axis=1))) for p in HP]; HT = [[hmap[i] for i in t] for t in HT]
    radii = [R + (D - R) * (k + 1) / FRAMES for k in range(FRAMES)]
    frames = []
    for r in radii[:-1]:
        mf = intersect(V, r, SEG_FILM); vol = mf.volume(); me = mf.to_mesh()
        P = np.asarray(me.vert_properties[:, :3], float); T = np.asarray(me.tri_verts)
        own = label(P, T, V, r); P2, T2, L2 = simplify_by_patch(P, T, own, TRIS_FILM)
        ok, v2 = mesh_ok(P2, T2); assert ok and abs(v2 - vol) / vol < 0.03, (key, r, ok, v2, vol)
        frames.append({'r': round(r, 6), 'vol': round(vol, 6), 'v': q(P2), 't': T2.ravel().tolist(), 's': [x for e in seams(T2, L2) for x in e]})
    # the build body, finer, at radius D
    mf = intersect(V, D, SEG_BODY); vol = mf.volume(); me = mf.to_mesh()
    P = np.asarray(me.vert_properties[:, :3], float); T = np.asarray(me.tri_verts)
    own = label(P, T, V, D); P2, T2, L2 = simplify_by_patch(P, T, own, TRIS_BODY)
    ok, v2 = mesh_ok(P2, T2); assert ok and abs(v2 - vol) / vol < 0.02, (key, ok, v2, vol)
    body_mesh = {'v': q(P2), 't': T2.ravel().tolist(), 'patch': L2.tolist(), 's': [x for e in seams(T2, L2) for x in e]}
    frames.append({'r': round(D, 6), 'vol': round(vol, 6)})   # the last frame is the body itself (its mesh kept once, in krp-core)
    C = corners(V, D)
    faces = []
    for i in range(len(V)):
        on = [k for k in range(len(C)) if abs(np.linalg.norm(C[k] - V[i]) - D) < 1e-7]
        m = C[on].mean(0); n = m / np.linalg.norm(m)          # the face's outward direction (the patch lies away from its own centre)
        e1 = C[on[0]] - m; e1 -= n * (e1 @ n); e1 /= np.linalg.norm(e1); e2 = np.cross(n, e1)
        on.sort(key=lambda k: np.arctan2((C[k] - m) @ e2, (C[k] - m) @ e1))   # counter-clockwise seen from outside
        assert (L2 == i).any(), (key, i)
        faces.append(on)
    side = np.linalg.norm(C[faces[0][0]] - C[faces[0][1]])
    assert all(abs(np.linalg.norm(C[f[a]] - C[f[(a + 1) % len(f)]]) - side) < 1e-9 for f in faces for a in range(len(f))), key
    OUT['bodies'].append({'key': key, 'name': name, 'source': src.lower(), 'D': round(D, 9), 'R': round(R, 9), 'balls': np.round(V, 9).tolist(),
        'edges': edges, 'hull': HT, 'radii': [f['r'] for f in frames],
        'frames': frames, 'vol': round(vol, 6)})
    CORE.append({'key': key, 'name': name, 'source': src.lower(), 'body': body_mesh,
        'corners': np.round(C, 9).tolist(), 'faces': faces, 'side': round(float(side), 9)})
    report.append(f'{name:24s} balls {len(V):2d} D {D:.4f} R {R:.4f} faces {len(faces):2d} corners {len(C):2d} ({len(faces[0])}-gon, side {side:.4f}) '
                  f'vol {vol:.4f} body tris {len(T2)} film tris {sum(len(f["t"]) // 3 for f in frames)}')
DOI = 'DICTO DOI 10.5281/zenodo.23529499'
src = (f"// Generated by scripts/build-reuleaux-data.py (The Reuleaux Platonic Solids, DICTO 2026-10-21; paper #45, {DOI}). Do not edit.\n"
       "// Per body: the balls (the solid's corners, edge 1), D, the film's 16 radii with the common part at each (coordinates x Q, triangles, seams);\n"
       "// the last frame (radius D) is the body itself, kept once in krp-core (src/polyhedra/reuleaux-bodies.js) with its patches and corners.\n"
       f"export default {json.dumps(OUT, separators=(',', ':'))};\n")
open(os.path.join(ROOT, 'src/app/reuleaux-data.js'), 'w').write(src)
core = (f"// Generated by kaleidohedra scripts/build-reuleaux-data.py (The Reuleaux Platonic Solids, DICTO 2026-10-21; DICTO's idea, paper #45, {DOI}). Do not edit.\n"
        "// Per body (named by look): the body mesh at radius D (coordinates x Q, triangles, each triangle's ball patch = face, seams as vertex pairs),\n"
        "// the exact corners (where three or more patches meet), each face's corners counter-clockwise from outside, and the side (corner to corner).\n"
        f"export const REULEAUX_Q = {OUT['Q']};\nexport const REULEAUX_RAW = {json.dumps(CORE, separators=(',', ':'))};\n")
open(os.path.join(ROOT, 'src/krp-core/src/polyhedra/reuleaux-bodies.js'), 'w').write(core)
print('\n'.join(report)); print('bytes', len(src), len(core))
