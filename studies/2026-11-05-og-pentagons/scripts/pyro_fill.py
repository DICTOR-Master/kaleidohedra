# DICTO 5 Nov 2026: where does the pyrochlore network go? Leftover space split into the truncated octahedra of the bcc lattice
# formed by the diamond nodes (cut OGs) + the empty diamond (void sites). Hexagon faces of each cell bisect the bonds = pyrochlore sites.
import numpy as np, itertools, math, manifold3d as m3
from scipy.spatial import ConvexHull
V = np.load("equilateral.npy"); V = V - V.mean(0)
def hull(P): return m3.Manifold.hull_points(np.asarray(P, float).tolist())
h = ConvexHull(V); pl = {}
for eq, s in zip(h.equations, h.simplices): pl.setdefault(tuple(np.round(eq, 5)), set()).update(s)
HEX = [sorted(f) for f in pl.values() if len(f) == 6]; cen = [V[f].mean(0) for f in HEX]; u = [c/np.linalg.norm(c) for c in cen]
tet = next(q for q in itertools.combinations(range(len(HEX)), 4) if all(abs(u[a] @ u[b] + 1/3) < 1e-5 for a, b in itertools.combinations(q, 2)))
H = [V[HEX[i]] for i in tet]; tu = [u[i] for i in tet]; d = np.linalg.norm(cen[tet[0]])
SQ = [ (tu[i] + tu[j])/np.linalg.norm(tu[i] + tu[j]) for i, j in ((0, 1), (0, 2), (0, 3)) ]
def TO(c, M):
    X = m3.Manifold.cube([8*M]*3, True).translate(list(c))
    for n, off in [(s*t, M) for t in tu for s in (1, -1)] + [(s*q, 2*M/math.sqrt(3)) for q in SQ for s in (1, -1)]:
        X = X.trim_by_plane(list(-n), float(-(off + n @ c)))
    return X
for g in (0.0, 0.1, 0.3):
    M = d + g/2; m = [M*t for t in tu]
    a1 = [2*m[i] - 2*m[j] for i, j in ((0, 1), (0, 2), (0, 3))]
    Ls = [n1*a1[0] + n2*a1[1] + n3*a1[2] for n1, n2, n3 in itertools.product(range(-2, 3), repeat=3)]
    nodes = [(c, 1) for c in Ls if np.linalg.norm(c) < 5*M] + [(c + 2*m[0], -1) for c in Ls if np.linalg.norm(c + 2*m[0]) < 5*M]
    sol = [hull(c + s*V) for c, s in nodes]; nc = 0
    if g > 0:
        for c, s in nodes:
            if s == 1:
                for i in range(4): sol.append(hull(np.vstack([c + H[i], c + 2*m[i] - H[i]]))); nc += 1
    U = m3.Manifold.batch_boolean(sol, m3.OpType.Add)
    conn = hull(np.vstack([H[0], 2*m[0] - H[0]])).volume() if g > 0 else 0
    print(f"gap {g}: cut OG vol {hull(V).volume():.4f}, connector vol {conn:.4f}, overlap {sum(x.volume() for x in sol) - U.volume():.1e}", flush=True)
    for name, c in (("cut-OG cell", np.zeros(3)), ("void cell A", -2*m[0]), ("void cell B", 4*m[0])):
        C = TO(c, M); rest = C - U; parts = sorted((round(p.volume(), 4) for p in rest.decompose() if p.volume() > 1e-6), reverse=True)
        print(f"   {name}: cell {C.volume():.4f}, filled {1 - rest.volume()/C.volume():.4f}, leftover pieces {len(parts)}: {parts[:8]}", flush=True)
print("FINAL ok")
