"""DICTO 11-06: "a lattice of five shapes, the Platonic solids" (after "get them all in octet and make the adaptors out of the pieces
themselves"). Kepler's nest in every octahedron of the octet (edge 1): octahedron O > icosahedron I (Pacioli: corners on O's edges in
golden ratio) > dodecahedron D (corners at I's face centres) > cube C (8 of D's corners) > tetrahedron T (4 of C's corners); the octet's
tetrahedra between. Checks: each solid regular (edges), each inside the next (all corners inside), volumes and the gap pieces between
neighbours; the whole is periodic in three directions (fcc)."""
import itertools, numpy as np
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = set()
    for s in itertools.product((1, -1), repeat=3): S.update(cyc(tuple(a * b for a, b in zip(s, v))))
    return np.array(sorted(S), float)
O = orbit((1, 0, 0)) / np.sqrt(2)                       # edge 1, corners on the axes
# Pacioli: icosahedron corners on O's 12 edges, dividing each in the golden ratio (cyclic, consistent): (0, a, b) type points
I = orbit((0, 1 / phi, 1)) ; I = I / (np.linalg.norm(I[0]))  # direction set (0, 1, phi) up to scale
def edges(V):
    D = np.linalg.norm(V[:, None] - V[None], axis=2); m = D[D > 1e-9].min(); return m, np.isclose(D, m).sum() // 2
# scale I so its corners lie on O's edges: point t*(0,1,phi)/|..| must satisfy |y|+|z| = 1/sqrt2 (O: |x|+|y|+|z| = 1/sqrt2)
I = orbit((0, 1, phi)); I = I * (1 / np.sqrt(2)) / (1 + phi)
hO = ConvexHull(O); hI = ConvexHull(I)
# D: corners at I's face centres
FI = {}
for eq, sp in zip(hI.equations, hI.simplices): FI.setdefault(tuple(np.round(eq, 8)), set()).update(sp)
D = np.array([I[list(s)].mean(0) for s in FI.values()])
# C: the 8 corners of D of the form (±t, ±t, ±t)
C = np.array([p for p in D if np.allclose(np.abs(p), np.abs(p[0]))])
# T: alternate corners of C
T = np.array([p for p in C if np.prod(np.sign(p)) > 0])
def inside(inner, outer):
    h = ConvexHull(outer); return bool(((inner @ h.equations[:, :3].T + h.equations[:, 3]) <= 1e-9).all())
for name, V, nv, ne in (('O', O, 6, 12), ('I', I, 12, 30), ('D', D, 20, 30), ('C', C, 8, 12), ('T', T, 4, 6)):
    m, k = edges(V); print(f"{name}: {len(V)} corners, edge {m:.6f}, {k} edges (expect {ne}), volume {ConvexHull(V).volume:.6f}")
print("nest:", [inside(a, b) for a, b in ((I, O), (D, I), (C, D), (T, C))])
vO, vI, vD, vC, vT = (ConvexHull(V).volume for V in (O, I, D, C, T))
print(f"gaps per octahedron: O-I {vO-vI:.6f} ({(vO-vI)/vO:.3f} of O), I-D {vI-vD:.6f}, D-C {vD-vC:.6f}, C-T {vC-vT:.6f}; T core {vT:.6f}")
# octet per fcc cell (cube side sqrt2): 4 octahedra, 8 tetrahedra of edge 1
A = np.sqrt(2); vtet = np.sqrt(2) / 12
print(f"per cell (volume {A**3:.6f}): 4 nests + 8 tetrahedra = {4*vO + 8*vtet:.6f}")
print(f"space shares: octet tetrahedra {8*vtet/A**3:.4f}; in the octahedra: I {4*vI/A**3:.4f} of which D {4*vD/A**3:.4f} > C {4*vC/A**3:.4f} > T {4*vT/A**3:.4f}")
print(f"ratios: I/O edge {edges(I)[0]/edges(O)[0]:.6f} (sqrt2/phi^2 = {np.sqrt(2)/phi**2:.6f}); D/I {edges(D)[0]/edges(I)[0]:.6f}; C/D {edges(C)[0]/edges(D)[0]:.6f} (phi {phi:.6f}); T/C {edges(T)[0]/edges(C)[0]:.6f} (sqrt2)")
print("FINAL ok")
