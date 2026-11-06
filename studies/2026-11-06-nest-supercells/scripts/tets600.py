"""Route (c), the 600-cell side (DICTO 11-06 "then do the 600 side"): the 600-cell's 20 tetrahedra round one corner, built in 3D with
REGULAR tetrahedra (edge 1): each has a corner at the centre and its far face square-on to an icosahedron face direction, turned so its
edges run toward the icosahedron's corners. In 4D they close exactly; in 3D they leave thin gaps (the angular defect), as the Dodeca-13
does for the 120-cell. Every tetrahedron carries the six-solid nest T > TT (1/3) > O (1/2) > I (Pacioli) > D > C. Checks: tetrahedra
pairwise disjoint, nests regular and nested; gap = hull - tetrahedra."""
import itertools, json, numpy as np
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = set()
    for s in itertools.product((1, -1), repeat=3): S.update(cyc(tuple(a * b for a, b in zip(s, v))))
    return np.array(sorted(S), float)
ICO = orbit((0, 1, phi)); ICO /= np.linalg.norm(ICO[0])
hI = ConvexHull(ICO); FI = {}
for eq, sp in zip(hI.equations, hI.simplices): FI.setdefault(tuple(np.round(eq, 8)), set()).update(sp)
def faces(V, r=5):
    h = ConvexHull(V); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, r)), set()).update(sp)
    return [V[list(s)] for s in F.values()]
def edges(V):
    D_ = np.linalg.norm(V[:, None] - V[None], axis=2); e = D_[D_ > 1e-9].min()
    return [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if abs(D_[i, j] - e) < 1e-6]
def inside(a, b):
    h = ConvexHull(b); return bool(((a @ h.equations[:, :3].T + h.equations[:, 3]) <= 1e-7).all())
# reference tetrahedron: corner at origin, axis along f, far corners toward the face's icosahedron corners (projected), edge 1
def tet(face_idx):
    tri = ICO[list(face_idx)]; f = tri.mean(0); f /= np.linalg.norm(f)
    h = np.sqrt(2 / 3); r = 1 / np.sqrt(3); out = [np.zeros(3)]
    for v in tri:
        u = v - (v @ f) * f; u /= np.linalg.norm(u); out.append(h * f + r * u)
    return np.array(out)
tets = [tet(s) for s in FI.values()]
def disjoint(A, B):
    for P, Q in ((A, B), (B, A)):
        for eq in ConvexHull(P).equations:
            if ((Q @ eq[:3] + eq[3]) >= -1e-9).all(): return True
    return False
print("20 tetrahedra, edges all 1:", all(np.allclose(sorted(np.linalg.norm(t[:, None] - t[None], axis=2)[np.triu_indices(4, 1)]), 1) for t in tets))
print("pairwise disjoint:", all(disjoint(a, b) for a, b in itertools.combinations(tets, 2)))
hull = ConvexHull(np.vstack(tets)); vt = sum(ConvexHull(t).volume for t in tets)
print(f"hull volume {hull.volume:.6f}, tetrahedra {vt:.6f}, gap {hull.volume - vt:.6f} ({(hull.volume - vt)/hull.volume:.4f} of the hull)")
# gap angle between neighbouring tetrahedra along a shared corner direction
a, b = tets[0], None
# nest in a tetrahedron: T > TT (corner thirds) > O (edge midpoints) > I (Pacioli in O) > D (face centres of I) > C (8 corners of D)
def nest(Tv):
    E = [(i, j) for i, j in itertools.combinations(range(4), 2)]
    U = np.array([Tv[i] + t * (Tv[j] - Tv[i]) for i, j in E for t in (1 / 3, 2 / 3)])
    O = np.array([(Tv[i] + Tv[j]) / 2 for i, j in E]); c = O.mean(0)
    # Pacioli: on each O edge, the point at 1/phi^2 or 1/phi, chosen so the 12 points make an icosahedron
    EO = edges(O); best = None
    for choice in itertools.product((0, 1), repeat=len(EO)):
        P = np.array([O[i] + (1 / phi ** 2 if ch == 0 else 1 / phi) * (O[j] - O[i]) for (i, j), ch in zip(EO, choice)])
        if len(edges(P)) == 30: best = P; break
    I = best
    D = np.array([f.mean(0) for f in faces(I)])
    Dc = D - c; ax = O - c
    # the cube on 8 of D's corners: corners whose coordinates in the octahedron's axis frame are (±t,±t,±t)
    Bm = np.array([ax[0], ax[1], ax[2]]) if False else None
    frame = []
    for p in ax:
        if not any(abs(abs(p @ q) / np.linalg.norm(p) / np.linalg.norm(q) - 1) < 1e-6 for q in frame): frame.append(p)
    Fm = np.array([p / np.linalg.norm(p) for p in frame[:3]])
    co = Dc @ Fm.T; C = D[np.all(np.isclose(np.abs(co), np.abs(co[:, :1]), atol=1e-6), axis=1)]
    return {'U': U, 'O': O, 'I': I, 'D': D, 'C': C}
nests = [nest(t) for t in tets]
REGN = {'U': 12, 'O': 6, 'I': 12, 'D': 20, 'C': 8}
ok = True
for t, n in zip(tets, nests):
    ok &= len(n['C']) == 8 and inside(n['U'], t) and inside(n['O'], n['U']) and inside(n['I'], n['O']) and inside(n['D'], n['I']) and inside(n['C'], n['D'])
    ok &= len(edges(n['I'])) == 30 and len(edges(n['D'])) == 30 and len(edges(n['C'])) == 12
print("every tetrahedron holds T > TT > O > I > D > C, all regular (TT Archimedean), each inside the next:", ok)
json.dump({'tets': [t.tolist() for t in tets], 'nests': [{k: v.tolist() for k, v in n.items()} for n in nests]}, open('../nest600.json', 'w'))
print("FINAL", "ok" if ok else "FAIL")
