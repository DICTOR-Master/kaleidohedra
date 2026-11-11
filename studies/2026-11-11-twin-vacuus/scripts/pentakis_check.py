# pentakis_check.py, DICTO 11 Nov 2026 ("check if the hidden pentakis world is exactly Catalan"). Hop 7 twin sweep, slice at height 0.0857
# (32 corners, 60 triangles). Catalan test: (1) the 60 face planes lie at one distance from the centre (all tangent to one sphere: they
# form one symmetry orbit); (2) the dual (hull of the 60 face directions) is a truncated icosahedron with REGULAR hexagons (pentagons
# are regular by the five-fold symmetry) -> exactly the Catalan pentakis dodecahedron. Compared with the true Catalan pentakis
# (dual of the regular truncated icosahedron): edge long/short ratio and corner radii ratio.
# usage: python -u pentakis_check.py <five-fold-octet dir>
import sys, os, itertools, numpy as np
ARGS = list(sys.argv); here = os.path.expanduser("~/k-research/studies/2026-11-09-og-margin/scripts")
sys.argv = [ARGS[0], ARGS[1], "0", "0", "/dev/null"]; exec(open(os.path.join(here, "og_exchanges.py")).read().split("for k in range(KMAX + 1):")[0])
sys.argv = [ARGS[0], ARGS[1], "0", "/dev/null"]; exec(open(os.path.join(here, "exact_family.py")).read().split("t0 = time.time()")[0])
from collections import Counter
from scipy.spatial import ConvexHull, HalfspaceIntersection
def twinf(x):
    re = float(x.a) + float(x.b) * S5
    return float(x.a) - float(x.b) * S5 if abs(re) < 1e-6 or x.b == 0 else float(x.a * x.a - 5 * x.b * x.b) / re
def merged(P):
    h = ConvexHull(P); En = h.equations; n = len(En); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if np.abs(En[f] - En[g]).max() < 1e-9: par[find(f)] = find(g)
    grp = {}
    for f in range(n): grp.setdefault(find(f), set()).update(h.simplices[f].tolist())
    return h, list(grp.values())
def edge_ratio_and_radii(P):
    h = ConvexHull(P)
    el = sorted(set(round(float(np.linalg.norm(P[a] - P[c])), 11) for t in h.simplices for a, c in ((t[0], t[1]), (t[1], t[2]), (t[0], t[2]))))
    r = np.linalg.norm(P, axis=1); rs = sorted(set(np.round(r / r.max(), 11)))
    return max(el) / min(el), rs, len(el)
phi = (1 + 5 ** .5) / 2
TI = []
for base in ((0, 1, 3 * phi), (1, 2 + phi, 2 * phi), (phi, 2, 2 * phi + 1)):                # regular truncated icosahedron, edge 2
    for p in (base, (base[1], base[2], base[0]), (base[2], base[0], base[1])):
        for sg in itertools.product((1, -1), repeat=3): TI.append(tuple(s_ * c for s_, c in zip(sg, p)))
TI = np.unique(np.round(np.array(TI), 10), axis=0); assert len(TI) == 60, len(TI)
TU = TI / np.linalg.norm(TI, axis=1)[:, None]
Pc = HalfspaceIntersection(np.hstack([TU, -np.ones((60, 1))]), np.zeros(3)).intersections; Pc = np.unique(np.round(Pc, 10), axis=0)
cat_ratio, cat_r, _ = edge_ratio_and_radii(Pc)
W = [tuple(cv(x) for x in v) for v in OG]; ok = True
for k in range(8):
    idx = {v: i for i, v in enumerate(W)}; Wfx = np.array([fl(v) for v in W]); F, ne, _ = exact_faces(W, idx, Wfx)
    feet = list(dict.fromkeys(tuple((d_ / dot(n_, n_)) * x for x in n_) for n_, d_, _ in F.values()))
    if k == 7:
        Wt = np.array([[twinf(x) for x in v] for v in feet]); X = Wt / np.einsum("ij,ij->i", Wt, Wt)[:, None]; X /= np.linalg.norm(X, axis=1).max(); b = np.einsum("ij,ij->i", X, X)
        lam = 0.0857; s, V, E, Fc = slice_sides(X, b, lam); act = np.where(s > 0)[0]
        print(f"slice at {lam}: corners {V}, faces {Fc} ({dict(Counter(s[act].tolist()))})"); ok &= V == 32 and Fc == 60
        dist = (b[act] + lam) / np.linalg.norm(X[act], axis=1)
        one_sphere = np.ptp(dist) / dist.mean() < 1e-12
        print(f"(1) face distances from the centre: spread {np.ptp(dist) / dist.mean():.1e} -> all faces tangent to one sphere: {one_sphere}")
        U = X[act] / np.linalg.norm(X[act], axis=1)[:, None]; h, groups = merged(U)
        print(f"(2) dual = hull of the 60 face directions: corners {len(h.vertices)}, faces {dict(Counter(len(p) for p in groups))}")
        hexreg = None
        for pts in groups:
            if len(pts) == 6:
                ii = np.array(sorted(pts)); Q = U[ii]; c0 = Q.mean(0); B = np.linalg.svd(Q - c0)[2][:2]; q = (Q - c0) @ B.T; Q = Q[np.argsort(np.arctan2(q[:, 1], q[:, 0]))]
                L = np.linalg.norm(np.roll(Q, -1, 0) - Q, axis=1); hexreg = float(L.max() / L.min())
                print(f"    dual hexagon sides long/short {hexreg:.12f} -> regular: {abs(hexreg - 1) < 1e-12}"); break
        H = np.hstack([X[act], -(b[act] + lam)[:, None]]); P = HalfspaceIntersection(H, np.zeros(3)).intersections; P = np.unique(np.round(P, 11), axis=0)
        ratio, rs, nl = edge_ratio_and_radii(P)
        print(f"    hidden world: {nl} edge lengths, long/short {ratio:.12f}; corner radii {rs}")
        print(f"    CATALAN pentakis: long/short {cat_ratio:.12f}; corner radii {cat_r}")
        same = abs(ratio - cat_ratio) < 1e-9 and hexreg is not None and abs(hexreg - 1) < 1e-12
        print(f"VERDICT: the hidden world {'IS' if same else 'is NOT'} exactly the Catalan pentakis dodecahedron")
    W = feet
print("FINAL ok" if ok else "FINAL FAIL: the slice is not the 32-corner, 60-triangle world")
