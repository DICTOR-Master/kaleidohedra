"""Footballs and scutoids (DICTO 11-06: "could make an interesting spacefill with footballs and scutoids"; "A please first",
reading A: footballs (truncated icosahedra) joined face to face by bridge pieces; a pentagon facing a hexagon gives a scutoid).
Geometry of the football (edge 1) and of a pentagon-hexagon link: two footballs on one axis, one showing a pentagon, the other a hexagon.
Also: the axis angles that decide which networks of such links exist."""
import numpy as np, itertools
from scipy.spatial import ConvexHull
phi = (1 + 5 ** .5) / 2
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def orbit(v):
    S = set()
    for s in itertools.product((1, -1), repeat=3):
        w = tuple(a * b for a, b in zip(s, v)); S.update(cyc(w))
    return S
V = np.array(sorted(orbit((0, 1, 3 * phi)) | orbit((1, 2 + phi, 2 * phi)) | orbit((phi, 2, phi ** 3)))) / 2
assert len(V) == 60
def faces(P):
    h = ConvexHull(P); F = {}
    for eq, sp in zip(h.equations, h.simplices): F.setdefault(tuple(np.round(eq, 7)), set()).update(sp)
    out = []
    for eq, idx in F.items():
        idx = list(idx); n = np.array(eq[:3]); c = P[idx].mean(0); u = P[idx[0]] - c; w = np.cross(n, u)
        idx.sort(key=lambda i: np.arctan2((P[i] - c) @ w, (P[i] - c) @ u)); out.append((n, -eq[3], idx))
    return out
F = faces(V)
pent = [f for f in F if len(f[2]) == 5]; hexa = [f for f in F if len(f[2]) == 6]
assert len(pent) == 12 and len(hexa) == 20
h5, h6 = pent[0][1], hexa[0][1]
ax5 = np.array([f[0] for f in pent]); ax3 = np.array([f[0] for f in hexa])
def angles(A, B=None):
    B = A if B is None else B; c = np.clip(np.abs(A @ B.T), 0, 1); a = np.degrees(np.arccos(c))
    return sorted({round(x, 2) for x in a.ravel() if x > 1e-6})
if __name__ == '__main__':
    print(f"football edge 1: centre to pentagon {h5:.6f}, to hexagon {h6:.6f}; pentagon circumradius {1/(2*np.sin(np.pi/5)):.6f}, hexagon 1")
    print("angles between 5-fold axes (lines):", angles(ax5))
    print("angles between 3-fold axes (lines):", angles(ax3))
    print("angles between a 5-fold and a 3-fold axis:", angles(ax5, ax3))
    print("common to 5-5 and 3-3:", set(angles(ax5)) & set(angles(ax3)))
