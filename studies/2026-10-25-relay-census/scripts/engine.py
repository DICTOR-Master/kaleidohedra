# Relay census engine (2026-10-25). Generalises the Bond Relay study's power_cell (../../2026-10-25-web-of-bonds/scripts/lib.py):
#  * any dimension d = 2, 3; sites in rational coordinates x with a rational metric G (|v|^2 = v^T G v), so hexagonal lattices stay
#    rational (power diagrams in the metric G are the affine images of the Euclidean ones: same combinatorics, same weights);
#  * the weights are affine in a parameter lam (m = 1, or m = 2 for three kinds): w_k = c_k0 + c_k1 lam1 (+ c_k2 lam2).
# Power cell of site i: { p : |p - c_i|^2 - w_i <= |p - c_j|^2 - w_j  for all j }  <=>  n_ij . p <= b_ij(lam),
#   n_ij = 2 G (c_j - c_i) (rational),  b_ij = c_j G c_j - c_i G c_i + w_i - w_j   (affine in lam, rational coefficients).
# Every corner is the solution of d of these planes: p(lam) = A^{-1} b(lam), affine in lam with rational coefficients, and every
# slack b_k(lam) - n_k . p(lam) is affine in lam. So, at a sample lam0, the face lattice is provably constant on the open interval
# where no slack that is positive at lam0 reaches 0 (rational end points); this is how the weight line is walked exactly.
# Floats (scipy HalfspaceIntersection / linprog) only choose candidate corners; every corner is solved and tested exactly. That no
# corner was missed is checked exactly afterwards: the cell volumes (polynomials in lam) add up to the lattice cell identically,
# and every face is matched face to face by the neighbour's own cell.
from fractions import Fraction as Fr
from itertools import combinations, product
import numpy as np
import sympy as sp
from scipy.optimize import linprog
from scipy.spatial import HalfspaceIntersection

LAM = sp.Symbol("lam"); MU = sp.Symbol("mu"); SYMS = (LAM, MU)


def matvec(G, v): return tuple(sum(G[r][c] * v[c] for c in range(len(v))) for r in range(len(G)))
def gdot(G, a, b): return sum(a[r] * G[r][c] * b[c] for r in range(len(a)) for c in range(len(b)))
def vsub(a, b): return tuple(x - y for x, y in zip(a, b))
def vadd(a, b): return tuple(x + y for x, y in zip(a, b))


def solve(A, B):
    """Exact Gauss: A (d x d Fractions), B (d x k Fractions) -> X with A X = B, or None if singular."""
    d = len(A); M = [list(A[r]) + list(B[r]) for r in range(d)]
    for c in range(d):
        piv = next((r for r in range(c, d) if M[r][c] != 0), None)
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]; M[c] = [x / pv for x in M[c]]
        for r in range(d):
            if r != c and M[r][c] != 0:
                f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [row[d:] for row in M]


def rank(vecs):
    """Exact rank of a list of Fraction vectors."""
    M = [list(v) for v in vecs]; r = 0
    if not M:
        return 0
    n = len(M[0])
    for c in range(n):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
    return r


class Net:
    def __init__(self, name, G, T, motif, wcoef, m=1):
        """G: metric (rational d x d). T: translation basis, list of d rational vectors. motif: list of (kind, coords).
        wcoef: kind -> tuple (c0, c1[, c2]) giving w_kind = c0 + c1 lam1 (+ c2 lam2)."""
        self.name, self.d, self.m = name, len(G), m
        self.G = [[Fr(x) for x in row] for row in G]
        self.T = [tuple(Fr(x) for x in v) for v in T]
        self.motif = [(k, tuple(Fr(x) for x in c)) for k, c in motif]
        self.wc = {k: tuple(Fr(x) for x in v) for k, v in wcoef.items()}
        self.detG = sp.Matrix(self.G).det()
        self.detT = abs(sp.Matrix([list(v) for v in self.T]).det())  # coordinate volume of the lattice cell
        self.kinds = sorted(set(k for k, _ in self.motif))

    def w(self, kind, lam):
        c = self.wc[kind]; return c[0] + sum(c[1 + q] * lam[q] for q in range(self.m))

    def sites_near(self, i, D2):
        """All sites (motif index, integer translation vector, coords) within G-distance^2 D2 of motif site i (excluding itself)."""
        ki, ci = self.motif[i]
        # translation range from the smallest eigenvalue of the coordinate Gram of T
        TG = np.array([[float(gdot(self.G, a, b)) for b in self.T] for a in self.T])
        K = int(np.ceil(np.sqrt(float(D2) / np.linalg.eigvalsh(TG).min()))) + 2
        out = []
        for kv in product(range(-K, K + 1), repeat=self.d):
            t = tuple(sum(kv[q] * self.T[q][r] for q in range(self.d)) for r in range(self.d))
            for j, (kj, cj) in enumerate(self.motif):
                c = vadd(cj, t)
                if j == i and all(x == 0 for x in kv):
                    continue
                dv = vsub(c, ci)
                if gdot(self.G, dv, dv) <= D2:
                    out.append((j, kv, c))
        return out

    def planes(self, i, D2):
        ki, ci = self.motif[i]; H = []
        for j, kv, c in self.sites_near(i, D2):
            kj = self.motif[j][0]
            n = tuple(2 * x for x in matvec(self.G, vsub(c, ci)))
            b0 = gdot(self.G, c, c) - gdot(self.G, ci, ci) + self.wc[ki][0] - self.wc[kj][0]
            b = (b0,) + tuple(self.wc[ki][1 + q] - self.wc[kj][1 + q] for q in range(self.m))
            H.append({"j": j, "kv": kv, "c": c, "kind": kj, "n": n, "b": b})
        return H


def aff_eval(coefs, lam):  # coefs (c0, c1, ...) affine in lam
    return coefs[0] + sum(coefs[1 + q] * lam[q] for q in range(len(lam)))


class Cell:
    """Power cell of motif site i at the exact parameter lam0 (tuple of Fractions)."""

    def __init__(self, net, i, lam0, D2):
        self.net, self.i, self.lam0, self.D2 = net, i, tuple(Fr(x) for x in lam0), Fr(D2)
        d = net.d; self.kind, self.c = net.motif[i]
        self.H = H = net.planes(i, D2)
        A = np.array([[float(x) for x in h["n"]] for h in H]); b = np.array([float(aff_eval(h["b"], self.lam0)) for h in H])
        # Chebyshev centre: max r with A x + r |A| <= b
        nr = np.linalg.norm(A, axis=1)
        res = linprog(np.r_[np.zeros(d), -1.0], A_ub=np.c_[A, nr], b_ub=b, bounds=[(None, None)] * d + [(0, None)], method="highs")
        self.empty = (res.status != 0) or res.x[-1] < 1e-9
        self.corners = []
        if self.empty:
            return
        x0 = res.x[:d]
        hs = HalfspaceIntersection(np.c_[A, -b], x0)
        V = np.unique(np.round(hs.intersections, 7), axis=0)
        seen = {}
        for v in V:
            r = A @ v - b
            tight = [k for k in np.argsort(np.abs(r)) if abs(r[k]) < 1e-6 * max(1, nr[k])]
            P = None
            for tri in combinations(tight, d):
                X = solve([list(H[k]["n"]) for k in tri], [list(H[k]["b"]) for k in tri])
                if X is not None:
                    P = X; break
            assert P is not None, "no independent tight planes"
            p0 = tuple(aff_eval(P[r_], self.lam0) for r_ in range(d))
            if p0 in seen:
                continue
            # exact slacks of every plane (affine in lam), exact feasibility and tight set at lam0
            sl, on = [], set()
            for k, h in enumerate(H):
                s = tuple(h["b"][q] - sum(h["n"][r_] * P[r_][q] for r_ in range(d)) for q in range(net.m + 1))
                v0 = aff_eval(s, self.lam0)
                assert v0 >= 0, "corner violates a plane exactly"
                if v0 == 0:
                    on.add(k)
                sl.append(s)
            seen[p0] = len(self.corners)
            self.corners.append({"P": P, "p0": p0, "on": on, "slack": sl})

    # ---- radius for the distance bound
    def rho2_at(self, lam):
        d = self.net.d
        return max(float(gdot(self.net.G, vsub(tuple(aff_eval(c["P"][r], lam) for r in range(d)), self.c),
                              vsub(tuple(aff_eval(c["P"][r], lam) for r in range(d)), self.c))) for c in self.corners)

    def bound_ok(self, lams):
        """Sites beyond D cannot cut the cell anywhere on the segment spanned by lams (rho is convex along a line, w affine)."""
        D = float(self.D2) ** 0.5; rho = max(self.rho2_at(l) for l in lams) ** 0.5
        ok = True
        for l in lams:
            dw = max(float(self.net.w(k, l)) for k in self.net.kinds) - float(self.net.w(self.kind, l))
            ok &= (D - rho) ** 2 >= rho ** 2 + dw + 1e-9 and D > rho
        return ok, rho

    # ---- interval (m = 1)
    def interval(self):
        lo, hi = None, None; l0 = self.lam0[0]
        for c in self.corners:
            for s in c["slack"]:
                v0 = s[0] + s[1] * l0
                if v0 == 0:
                    if s[1] != 0:
                        return ("breakpoint", l0)
                    continue
                if s[1] != 0:
                    r = -s[0] / s[1]
                    if r > l0 and (hi is None or r < hi):
                        hi = r
                    if r < l0 and (lo is None or r > lo):
                        lo = r
        return lo, hi

    # ---- faces (generic lam0)
    def faces(self):
        d = self.net.d; out = {}
        for k in range(len(self.H)):
            pts = [c for c in self.corners if k in c["on"]]
            if len(pts) < d:
                continue
            if rank([vsub(p["p0"], pts[0]["p0"]) for p in pts[1:]]) == d - 1:
                out[k] = pts
        return out


def sym_point(P, d):
    return sp.Matrix([sp.Rational(P[r][0]) + sum(sp.Rational(P[r][1 + q]) * SYMS[q] for q in range(len(P[r]) - 1)) for r in range(d)])


def order(pts, normal):
    P = np.array([[float(x) for x in p["p0"]] for p in pts]); cen = P.mean(0)
    if len(normal) == 2:
        return pts
    nf = np.array([float(x) for x in normal]); nf /= np.linalg.norm(nf)
    u = P[0] - cen; u /= np.linalg.norm(u); v = np.cross(nf, u)
    ang = np.arctan2((P - cen) @ v, (P - cen) @ u)
    return [pts[k] for k in np.argsort(ang)]


def face_alpha(cell, k, pts):
    """Euclidean (d-1)-measure of face k as |alpha(lam)| * const, alpha polynomial; returns (alpha, const^2) with
    measure^2 = alpha^2 * const2. 3D: area vector A = alpha n (n the plane's coordinate normal), area^2 = alpha^2 detG n^T G^-1 n.
    2D: the segment p1 - p0 = alpha e, e the direction perpendicular (in coordinates) to n; length^2 = alpha^2 e^T G e."""
    d = cell.net.d; n = cell.H[k]["n"]; G = sp.Matrix(cell.net.G)
    if d == 3:
        pts = order(pts, n); S = [sym_point(p["P"], 3) for p in pts]
        A = sp.zeros(3, 1)
        for q in range(len(S)):
            A += S[q].cross(S[(q + 1) % len(S)])
        A = A / 2; nv = sp.Matrix(n)
        alpha = sp.expand((A.dot(nv)) / nv.dot(nv))
        const2 = cell.net.detG * (nv.T * G.inv() * nv)[0]
        return alpha, const2, pts
    a, b = (sym_point(p["P"], 2) for p in pts[:2]) if len(pts) == 2 else (None, None)
    assert len(pts) == 2
    e = sp.Matrix([-n[1], n[0]]); dv = b - a
    alpha = sp.expand(dv.dot(e) / e.dot(e))
    return alpha, (e.T * G * e)[0], pts


def cell_volume(cell, faces):
    """Coordinate volume (area in 2D) of the cell as a polynomial in lam (exact)."""
    d = cell.net.d
    if d == 2:
        pts = [c for c in cell.corners]
        P = np.array([[float(x) for x in p["p0"]] for p in pts]); cen = P.mean(0)
        ang = np.arctan2(P[:, 1] - cen[1], P[:, 0] - cen[0]); pts = [pts[k] for k in np.argsort(ang)]
        S = [sym_point(p["P"], 2) for p in pts]; V = 0
        for q in range(len(S)):
            a, b = S[q], S[(q + 1) % len(S)]; V += a[0] * b[1] - a[1] * b[0]
        return sp.expand(V / 2)
    V = 0
    for k, pts in faces.items():
        pts = order(pts, cell.H[k]["n"]); S = [sym_point(p["P"], 3) for p in pts]
        for q in range(1, len(S) - 1):
            V += S[0].dot(S[q].cross(S[q + 1])) / 6
    return sp.expand(V)
