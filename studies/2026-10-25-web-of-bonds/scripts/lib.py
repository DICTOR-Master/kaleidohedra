# Exact tools for the Bond Relay study (2026-10-25).
#  * Field / E: exact numbers in Q(alpha), alpha a real root of a monic minimal polynomial (Q itself, Q(sqrt5), Q(sqrt2), Q(sqrt6),
#    Q(cbrt2), Q(cbrt6)); +, -, *, exact zero test (coefficients), sign of a nonzero element from an 80-digit evaluation (an element
#    is zero only when all its coefficients are; nonzero elements here have small height, far above 1e-80).
#  * power_cell: the power (Laguerre) cell of one site among fixed sites with weights, |p - c_i|^2 - w_i <= |p - c_j|^2 - w_j.
#    Normals c_j - c_i are rational, so every corner is (rational 3x3 inverse) x (field vector): exact. Floats only pick the candidate
#    triples of planes; every corner is then solved and tested against every plane exactly.
#  * faces, exact area^2 and exact volume of a cell; the distance bound that makes the finite site list enough.
from fractions import Fraction as Fr
from itertools import combinations
import numpy as np
import mpmath as mp

mp.mp.dps = 80


class Field:
    def __init__(self, name, minpoly, root):
        # minpoly: monic, coefficients low -> high, e.g. x^2 - 5 -> [-5, 0, 1]; root: mp approximation of the chosen real root
        self.name, self.m, self.d, self.root = name, [Fr(c) for c in minpoly], len(minpoly) - 1, mp.mpf(root)
        self.pw = [self.root ** k for k in range(self.d)]

    def __call__(self, *coeffs):
        c = [Fr(x) for x in coeffs] + [Fr(0)] * (self.d - len(coeffs))
        return E(self, tuple(c[: self.d]))

    def gen(self):
        return self(0, 1) if self.d > 1 else self(0)


class E:
    __slots__ = ("F", "c")

    def __init__(self, F, c):
        self.F, self.c = F, c

    def _co(self, o):
        return o if isinstance(o, E) else self.F(o)

    def __add__(self, o):
        o = self._co(o); return E(self.F, tuple(a + b for a, b in zip(self.c, o.c)))
    __radd__ = __add__

    def __neg__(self):
        return E(self.F, tuple(-a for a in self.c))

    def __sub__(self, o):
        return self + (-self._co(o))

    def __rsub__(self, o):
        return self._co(o) - self

    def __mul__(self, o):
        if not isinstance(o, E):
            o = Fr(o); return E(self.F, tuple(a * o for a in self.c))
        d, m = self.F.d, self.F.m
        p = [Fr(0)] * (2 * d - 1)
        for i, a in enumerate(self.c):
            if a:
                for j, b in enumerate(o.c):
                    p[i + j] += a * b
        for k in range(2 * d - 2, d - 1, -1):  # reduce x^k with x^d = -(m_0 + ... + m_{d-1} x^{d-1})
            if p[k]:
                q = p[k]; p[k] = Fr(0)
                for i in range(d):
                    p[k - d + i] -= q * m[i]
        return E(self.F, tuple(p[:d]))
    __rmul__ = __mul__

    def __truediv__(self, o):  # only by rationals (all divisions in this study are)
        return self * (Fr(1) / Fr(o))

    def iszero(self):
        return all(a == 0 for a in self.c)

    def __eq__(self, o):
        return (self - o).iszero()

    def __hash__(self):
        return hash(self.c)

    def mpf(self):
        return sum(mp.mpf(a.numerator) / a.denominator * w for a, w in zip(self.c, self.F.pw))

    def __float__(self):
        return float(self.mpf())

    def sign(self):
        if self.iszero():
            return 0
        v = self.mpf()
        assert abs(v) > mp.mpf(10) ** -60, "sign undecided"
        return 1 if v > 0 else -1

    def __repr__(self):
        return f"E({self.F.name}:{[str(a) for a in self.c]}~{float(self):.12g})"


QQ = Field("Q", [0, 1], 0)
Q5 = Field("Q(sqrt5)", [-5, 0, 1], mp.sqrt(5))
Q2 = Field("Q(sqrt2)", [-2, 0, 1], mp.sqrt(2))
Q6 = Field("Q(sqrt6)", [-6, 0, 1], mp.sqrt(6))
C2 = Field("Q(cbrt2)", [-2, 0, 0, 1], mp.cbrt(2))
C6 = Field("Q(cbrt6)", [-6, 0, 0, 1], mp.cbrt(6))


def vadd(a, b): return tuple(x + y for x, y in zip(a, b))
def vsub(a, b): return tuple(x - y for x, y in zip(a, b))
def vmul(k, a): return tuple(k * x for x in a)
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def fl(v): return np.array([float(x) for x in v])


def inv3(A):  # rational 3x3 inverse (Fractions)
    a, b, c = A
    det = a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])
    if det == 0:
        return None
    cof = [[b[1] * c[2] - b[2] * c[1], -(a[1] * c[2] - a[2] * c[1]), a[1] * b[2] - a[2] * b[1]],
           [-(b[0] * c[2] - b[2] * c[0]), a[0] * c[2] - a[2] * c[0], -(a[0] * b[2] - a[2] * b[0])],
           [b[0] * c[1] - b[1] * c[0], -(a[0] * c[1] - a[1] * c[0]), a[0] * b[1] - a[1] * b[0]]]
    return [[Fr(x) / det for x in row] for row in cof]


def power_cell(i, sites, w, F):
    """Power cell of sites[i] = (kind, centre with Fraction coords); w: kind -> E (weights). Returns dict with exact corners, the
    planes (j, n, b) with n.p <= b, and for every corner the set of planes through it."""
    ki, ci = sites[i]
    H = []
    for j, (kj, cj) in enumerate(sites):
        if j == i:
            continue
        n = vsub(cj, ci)
        b = (F(dot(cj, cj) - dot(ci, ci)) + w[ki] - w[kj]) * Fr(1, 2)
        H.append((j, n, b))
    N = np.array([[float(x) for x in n] for _, n, _ in H]); B = np.array([float(b) for *_, b in H])
    idx = np.array(list(combinations(range(len(H)), 3)))
    M = N[idx]; det = np.linalg.det(M); ok = np.abs(det) > 1e-9
    idx, M = idx[ok], M[ok]
    P = np.linalg.solve(M, B[idx][..., None])[..., 0]
    feas = np.all(P @ N.T <= B[None, :] + 1e-7, axis=1)
    cand = {}
    for tri, p in zip(idx[feas], P[feas]):
        cand.setdefault(tuple(np.round(p, 6)), tuple(tri))
    corners = {}
    for tri in cand.values():
        A = [H[k][1] for k in tri]; Ai = inv3(A)
        bb = [H[k][2] for k in tri]
        p = tuple(sum((bb[c] * Ai[r][c] for c in range(3)), F(0)) for r in range(3))
        on = set()
        for k, (j, n, b) in enumerate(H):
            s = (b - dot(n, p)).sign()
            if s < 0:
                break
            if s == 0:
                on.add(j)
        else:
            corners[p] = on
    return {"site": i, "corners": corners, "planes": H}


def order_polygon(pts, normal):
    P = np.array([fl(p) for p in pts]); c = P.mean(0); nf = fl(normal); nf = nf / np.linalg.norm(nf)
    u = P[0] - c; u /= np.linalg.norm(u); v = np.cross(nf, u)
    ang = np.arctan2((P - c) @ v, (P - c) @ u)
    return [pts[k] for k in np.argsort(ang)]  # counter-clockwise seen from the outward normal


def cell_faces(cell, F):
    """Faces of positive area: {j: (ordered corners, area^2 exact, normal n)}; also exact volume (divergence theorem)."""
    out, vol = {}, F(0)
    for j, n, b in cell["planes"]:
        pts = [p for p, on in cell["corners"].items() if j in on]
        if len(pts) < 3:
            continue
        poly = order_polygon(pts, n)
        A = (F(0), F(0), F(0))
        for k in range(len(poly)):
            A = vadd(A, cross(poly[k], poly[(k + 1) % len(poly)]))
        A = vmul(Fr(1, 2), A)
        a2 = dot(A, A)
        if a2.iszero():
            continue  # a segment or a point: no bond
        out[j] = (poly, a2, n)
        for k in range(1, len(poly) - 1):
            vol = vol + dot(poly[0], cross(poly[k], poly[k + 1])) * Fr(1, 6)
    return out, vol


def enough_sites(cell, sites, w, D):
    """Sites farther than D from the centre cannot cut the cell: (D - rho)^2 >= rho^2 + max(w_j) - w_i (float, margin 1e-6)."""
    ki, ci = sites[cell["site"]]
    rho = max(np.linalg.norm(fl(vsub(p, ci))) for p in cell["corners"]) if cell["corners"] else 0.0
    dw = max(float(x) for x in w.values()) - float(w[ki])
    return (D - rho) ** 2 >= rho ** 2 + dw + 1e-6, rho
