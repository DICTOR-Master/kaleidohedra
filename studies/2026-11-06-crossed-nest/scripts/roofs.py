"""Roofs (DICTO 11-06: "continue with the roofs and dodecahedra"). In the octet (edge 1) every octahedral site carries a grown solid
(icosahedron or dodecahedron of the nest, scaled by s about its centre; all cells have the same orientation). A face of one cell and the
parallel face of a neighbour lie in ONE plane exactly when the neighbour's offset is perpendicular to the face normal (for every s). Those
coplanar faces meet edge to edge and join into a continuous sheet through the lattice at a definite s: the octet's version of EKP's roofs.
For each solid: the coplanar face families, the s at which neighbouring coplanar faces first meet, and whether they then close up into a
gap-free sheet; also the solid's touching and space-covering thresholds."""
import itertools, numpy as np
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon
from shapely.ops import unary_union
phi = (1 + 5 ** .5) / 2; A = np.sqrt(2)
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = set()
    for s in itertools.product((1, -1), repeat=3): S.update(cyc(tuple(a * b for a, b in zip(s, v))))
    return np.array(sorted(S), float)
I = orbit((0, 1, phi)) * (1 / np.sqrt(2)) / (1 + phi)
hI = ConvexHull(I); FI = {}
for eq, sp in zip(hI.equations, hI.simplices): FI.setdefault(tuple(np.round(eq, 8)), set()).update(sp)
D = np.array([I[list(s)].mean(0) for s in FI.values()])
octc = np.array([[.5, .5, .5], [.5, 0, 0], [0, .5, 0], [0, 0, .5]]) * A
sites = np.array([c + A * np.array(t) for c in octc for t in itertools.product(range(-2, 3), repeat=3)])
nbr = [v for v in sites - octc[0] if 1e-9 < np.linalg.norm(v) < 2.2]
def faces(V):
    h = ConvexHull(V); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 7)), set()).update(sp)
    out = []
    for k, idx in F.items():
        idx = list(idx); n = np.array(k[:3]); c = V[idx].mean(0); u = V[idx[0]] - c; w = np.cross(n, u)
        out.append((n, -k[3], V[sorted(idx, key=lambda i: np.arctan2((V[i] - c) @ w, (V[i] - c) @ u))]))
    return out
def study(name, V):
    F = faces(V); print(f"== {name}: {len(F)} faces")
    fam = {}
    for n, h, P in F:
        cop = [v for v in nbr if abs(n @ v) < 1e-9]
        if cop: fam.setdefault(tuple(np.round(np.abs(n), 4)), []).append((n, h, P, cop))
    for key, items in fam.items():
        n, h, P, cop = items[0]
        u = P[0] - P.mean(0); u /= np.linalg.norm(u); w = np.cross(n, u)
        def poly(s, shift): Q = (P * s + shift); return Polygon(np.c_[Q @ u, Q @ w])
        lo, hi = 0.5, 3.0
        for _ in range(50):
            m = (lo + hi) / 2
            if any(poly(m, 0).intersects(poly(m, v)) for v in cop): hi = m
            else: lo = m
        smeet = hi
        # gap-free sheet? union of this face over all coplanar sites (a patch) vs the patch's square: area share at s = smeet and at phi
        def share(s):
            pats = [poly(s, v) for v in [np.zeros(3)] + [v for v in sites - octc[0] if abs(n @ v) < 1e-9 and np.linalg.norm(v) < 4.5]]
            U = unary_union(pats); box = Polygon([(-1, -1), (1, -1), (1, 1), (-1, 1)])
            return U.intersection(box).area / box.area
        print(f"   faces with |normal| {key}: {len(items)} per cell, coplanar with {len(cop)} neighbours; neighbours' faces meet at s = {smeet:.6f}; "
              f"plane covered {share(smeet):.3f} there, {share(phi):.3f} at s = phi")
    # touch threshold
    def disjoint(P_, Q_):
        for X, Y in ((P_, Q_), (Q_, P_)):
            for eq in ConvexHull(X).equations:
                if ((Y @ eq[:3] + eq[3]) >= -1e-9).all(): return True
        return False
    lo, hi = 0.5, 4.0
    for _ in range(50):
        m = (lo + hi) / 2
        if all(disjoint(V * m, V * m + v) for v in nbr if np.linalg.norm(v) < 1.5): lo = m
        else: hi = m
    print(f"   neighbours first touch at s = {lo:.6f}")
study('icosahedron (Pacioli)', I); study('dodecahedron (the nest)', D)
print("FINAL ok")
