"""Overlap version (DICTO 11-06: "the interesting part of EKP was overlap of cells, which made the roofs work throughout and the
rectangles"). Octet of edge 1 (fcc cube side sqrt2): octahedra centred on the octahedral sites, each with Pacioli's icosahedron (and D, C, T).
(1) Planes that continue through the lattice at the nest's own size: which icosahedron faces lie in the octet's (111) layer planes, and
    which golden rectangles (the icosahedron's three) lie in planes shared by many cells.
(2) Grow every icosahedron about its centre by s >= 1 (and the dodecahedra likewise): where neighbours first touch, overlap volume per cell,
    and the share of space covered by the octet's tetrahedra + the grown icosahedra (EKP-like: overlaps make the surfaces run on)."""
import itertools, numpy as np
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2; A = np.sqrt(2)
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = set()
    for s in itertools.product((1, -1), repeat=3): S.update(cyc(tuple(a * b for a, b in zip(s, v))))
    return np.array(sorted(S), float)
O = orbit((1, 0, 0)) / np.sqrt(2); I = orbit((0, 1, phi)) * (1 / np.sqrt(2)) / (1 + phi)
octc = np.array([[.5, .5, .5], [.5, 0, 0], [0, .5, 0], [0, 0, .5]]) * A          # octahedral sites per cubic cell
hI = ConvexHull(I); fI = {}
for eq, sp in zip(hI.equations, hI.simplices): fI.setdefault(tuple(np.round(eq, 8)), set()).update(sp)
n111 = [k for k in fI if np.allclose(np.abs(k[:3]), 1 / np.sqrt(3), atol=1e-6)]
print(f"(1) icosahedron faces square-on to the octet's (111) layers: {len(n111)} of 20 (they lie in the octahedron's faces, i.e. in the layer planes)")
rect = [p for p in I if abs(p[0]) < 1e-9]; print(f"    golden rectangle in the plane x = 0 (through the centre): corners {np.round(rect, 4).tolist()}, sides {2*abs(rect[0][1]):.4f} x {2*abs(rect[0][2]):.4f} (ratio {abs(rect[0][2]/rect[0][1]):.4f})")
# which other octahedral sites lie in the plane x = 0 through a site? (fcc: a square lattice of sites, spacing sqrt2/2 along the diagonals)
pts = np.array([c + A * np.array(t) for c in octc for t in itertools.product(range(-2, 3), repeat=3)])
inplane = pts[np.abs(pts[:, 0] - octc[1][0]) < 1e-9]; d = np.sort(np.linalg.norm(inplane - octc[1], axis=1))[1:5]
print(f"    sites in the same x-plane: nearest at {np.round(d, 4).tolist()}: every icosahedron there has a golden rectangle in that plane")
# (2) grow icosahedra
def disjoint(P, Q):
    for X, Y in ((P, Q), (Q, P)):
        for eq in ConvexHull(X).equations:
            if ((Y @ eq[:3] + eq[3]) >= -1e-9).all(): return True
    return False
nb = sorted({tuple(np.round(p - octc[0], 6)) for p in pts if 1e-6 < np.linalg.norm(p - octc[0]) < 1.5})
nb = [np.array(v) for v in nb]
lo, hi = 1.0, 3.0
for _ in range(50):
    m = (lo + hi) / 2
    if all(disjoint(I * m, I * m + v) for v in nb): lo = m
    else: hi = m
print(f"(2) grown icosahedra first touch their neighbours at s = {lo:.6f} (edge {np.sqrt(2)/phi**2*lo:.6f}); 1/(phi^2 sqrt2)... compare phi = {phi:.6f}")
rng = np.random.default_rng(0); X = rng.uniform(0, A, (300000, 3))
def wrap(dv): return dv - A * np.round(dv / A)
eO = ConvexHull(O).equations
inO = np.zeros(len(X), bool)
for c in octc: inO |= ((wrap(X - c) @ eO[:, :3].T + eO[:, 3]) <= 0).all(1)
eIc = ConvexHull(I).equations
for s in (1.0, lo, 1.2, 1.3, 1.4, 1.5, 1.6):
    cnt = np.zeros(len(X), int)
    for c in octc:
        dv = wrap(X - c); cnt += ((dv @ eIc[:, :3].T + eIc[:, 3] * s) <= 0).all(1)
    cov = ((cnt > 0) | ~inO).mean()
    print(f"    s = {s:.4f}: icosahedra cover {(cnt > 0).mean():.4f} of space, overlap (counted twice) {(cnt > 1).mean():.4f}; with the tetrahedra the cover is {cov:.4f}")
print("FINAL ok")
