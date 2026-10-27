# Swap Rule proof, shared geometry (DICTO 2026-10-27). Exact rationals throughout; floats (scipy HiGHS) only propose LP bases.
#
# Frame. Lateral coordinates (x, y) in the hexagonal layer basis, Q(a) = a1^2 + a1 a2 + a2^2 (ball spacing 1); height zeta in layer
# spacings; layer spacing^2 = q = s * 2/3 (s = 1 is #57). Positions A = (0,0), B = (1/3,1/3), C = (2/3,2/3) mod the integer lattice.
# The gap under study lies between layer 0 (A, zeta = 0) and layer 1 (B, zeta = 1); the third position is C. Its sites:
#   tetY = tetrahedral hole under the upper layer, (B, 1/4), weight lam;  oct = (C, 1/2), weight 0;  tetX = over the lower layer, (A, 3/4), lam.
# Layer -1 is W = C (layer 0 is then c: layers -1, 0, 1 all different) or W = B (layer 0 is h).
# Gap between layer m (position P) and m+1 (position R): tet (R, m+1/4) lam; oct (third(P,R), m+1/2) 0; tet (P, m+3/4) lam.
#
# LINEARISATION. With u = q * zeta, the power-bisector condition pow_i(p) <= pow_j(p) reads
#   (2 d1 + d2) x + (d1 + 2 d2) y + 2 dz u - q (zj^2 - zi^2) - lam (ti - tj)  <=  Q(cj) - Q(ci)       (d = cj - ci laterally, dz = zj - zi)
# i.e. a FIXED normal in z = (q, lam, x, y, u) and a constant right side: every cell, half-cell and domain is one convex polyhedron in
# the 5-space of (parameters, point). A Farkas certificate y >= 0 with y^T M = c, y^T m <= beta proves c.z <= beta on all of it, i.e.
# for EVERY (s, lam) of the domain at once, the unbounded range s -> infinity included.
from fractions import Fraction as Fr
from itertools import combinations, product
import numpy as np
from scipy.optimize import linprog

POS = {'A': (Fr(0), Fr(0)), 'B': (Fr(1, 3), Fr(1, 3)), 'C': (Fr(2, 3), Fr(2, 3))}
def third(P, R): return ({'A', 'B', 'C'} - {P, R}).pop()
def Qf(a): return a[0] * a[0] + a[0] * a[1] + a[1] * a[1]
ROLE = {'tetY': ('B', Fr(1, 4), 1), 'oct': ('C', Fr(1, 2), 0), 'tetX': ('A', Fr(3, 4), 1)}
MIRROR = {'tetY': 'tetX', 'oct': 'oct', 'tetX': 'tetY'}
RLAT2 = Fr(2)          # lateral list radius^2 (>= 4/3 = (2 x covering radius of the unit triangular lattice)^2 is what the proof needs)

def gap_levels(m, P, R):
    """levels of the gap between layer m (position P) and m+1 (position R): (height, position, tet?)"""
    return [(m + Fr(1, 4), R, 1), (m + Fr(1, 2), third(P, R), 0), (m + Fr(3, 4), P, 1)]

def levels(t):
    """t = type of layer 0 ('c' or 'h'). Returns {group: [(height, position, tet?)]}; group 'K' = gaps -1, 0 (define the half-piece),
    'up1' = gap 1 (both choices of layer 2), 'dn2' = gap -2 (both choices of layer -2), 'up2'/'dn3' = all three positions (supersets)."""
    W = 'C' if t == 'c' else 'B'
    L = {'K': gap_levels(-1, W, 'A') + gap_levels(0, 'A', 'B')}
    L['up1'] = sorted({lv for R in ('A', 'C') for lv in gap_levels(1, 'B', R)})
    L['dn2'] = sorted({lv for V in 'ABC' if V != W for lv in gap_levels(-2, V, W)})
    L['up2'] = [(Fr(2) + f, P, tt) for f, tt in ((Fr(1, 4), 1), (Fr(1, 2), 0), (Fr(3, 4), 1)) for P in 'ABC']
    L['dn3'] = [(Fr(-3) + f, P, tt) for f, tt in ((Fr(1, 4), 1), (Fr(1, 2), 0), (Fr(3, 4), 1)) for P in 'ABC']
    return L

def coset_points(P, centre, r2=RLAT2):
    base = POS[P]; out = []
    for a, b in product(range(-4, 5), repeat=2):
        c = (base[0] + a, base[1] + b)
        if Qf((c[0] - centre[0], c[1] - centre[1])) <= r2: out.append(c)
    return out

def sites(role, t):
    """site i and the finite site lists per group: each j = (cxy, zeta, tet?)"""
    P, zi, ti = ROLE[role]; ci = POS[P]
    out = {}
    for g, lvs in levels(t).items():
        S = []
        for z, Pj, tj in lvs:
            for c in coset_points(Pj, ci):
                if z == zi and c == ci: continue
                S.append((c, z, tj))
        out[g] = S
    return (ci, zi, ti), out

def row(i, j):
    """bisector row (coefficients on z = (q, lam, x, y, u), right side) for pow_i <= pow_j"""
    (ci, zi, ti), (cj, zj, tj) = i, j
    d1, d2 = cj[0] - ci[0], cj[1] - ci[1]; dz = zj - zi
    return ([-(zj * zj - zi * zi), -Fr(ti - tj), 2 * d1 + d2, d1 + 2 * d2, 2 * dz], Qf(cj) - Qf(ci))

def domain_rows(t, q0, cut=True, qmax=None):
    """q >= q0; lam <= U(q) = min(1/3 + q/16, 9q/16) (the upper end of the cubic walk: octahedral pieces exist; beyond 9q/16 the
    tetrahedral hole of the next gap straight over an octahedral hole takes the hole's own point); lam >= -1/3 - 3q/16 (h) or
    -1/4 - 3q/16 (c) (tetrahedral pieces next to a layer of that type exist); cut: zeta <= 1/2 (u <= q/2)."""
    R = [([-1, 0, 0, 0, 0], -Fr(q0)), ([-Fr(1, 16), 1, 0, 0, 0], Fr(1, 3)), ([-Fr(9, 16), 1, 0, 0, 0], Fr(0)),
         ([-Fr(3, 16), -1, 0, 0, 0], Fr(1, 3) if t == 'h' else Fr(1, 4))]
    if cut: R.append(([-Fr(1, 2), 0, 0, 0, 1], Fr(0)))
    if qmax is not None: R.append(([1, 0, 0, 0, 0], Fr(qmax)))
    return [([Fr(x) for x in a], Fr(b)) for a, b in R]

# ---------------- exact LP via a float-proposed basis
def _rank(rows):
    M = [list(r) for r in rows]; rk = 0; n = len(M[0]) if M else 0
    for c in range(n):
        piv = next((k for k in range(rk, len(M)) if M[k][c] != 0), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        for k in range(len(M)):
            if k != rk and M[k][c] != 0:
                f = M[k][c] / M[rk][c]; M[k] = [a - f * b for a, b in zip(M[k], M[rk])]
        rk += 1
    return rk

def _solve(A, b):
    """exact solve of square A x = b; None if singular"""
    n = len(A); M = [list(A[r]) + [b[r]] for r in range(n)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None: return None
        M[c], M[piv] = M[piv], M[c]; pv = M[c][c]; M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[r][n] for r in range(n)]

def lp_max(c, rows, tries=4000):
    """max c.z over {z : a.z <= b for (a, b) in rows}, z in R^5, EXACT. Returns dict(status, value, z, y) where y >= 0 is a Farkas/dual
    certificate on the rows (sum y_k a_k = c, sum y_k b_k = value) and z an exact feasible optimal point (sum c z = value)."""
    A = np.array([[float(x) for x in a] for a, _ in rows]); b = np.array([float(x) for _, x in rows])
    res = linprog(-np.array([float(x) for x in c]), A_ub=A, b_ub=b, bounds=[(None, None)] * 5, method='highs')
    if res.status == 3: return {'status': 'unbounded'}
    if res.status == 2: return {'status': 'infeasible'}
    if res.status != 0: return {'status': 'error ' + res.message}
    dual = -res.ineqlin.marginals; slack = b - A @ res.x
    act = [k for k in range(len(rows)) if abs(slack[k]) < 1e-7 * (1 + abs(b[k]))]
    act.sort(key=lambda k: -dual[k])
    n = len(c)
    for cnt, B in enumerate(combinations(act, n)):
        if cnt > tries: break
        MB = [rows[k][0] for k in B]
        if _rank(MB) < n: continue
        z = _solve(MB, [rows[k][1] for k in B])
        if any(sum(a[r] * z[r] for r in range(n)) > bb for a, bb in rows): continue          # exact primal feasibility
        yB = _solve([[MB[k][r] for k in range(n)] for r in range(n)], list(c))            # MB^T y = c
        if yB is None or any(v < 0 for v in yB): continue                                   # exact dual feasibility
        val = sum(cc * zz for cc, zz in zip(c, z))
        assert val == sum(yB[k] * rows[B[k]][1] for k in range(n))
        y = {B[k]: yB[k] for k in range(n) if yB[k] != 0}
        return {'status': 'optimal', 'value': val, 'z': z, 'y': y}
    # degenerate vertex: solve the dual LP on the active rows (a basic dual solution has small support) and solve it exactly
    if act:
        Ma = np.array([[float(x) for x in rows[k][0]] for k in act]).T
        dres = linprog(np.array([float(rows[k][1]) for k in act]), A_eq=Ma, b_eq=np.array([float(x) for x in c]), bounds=[(0, None)] * len(act), method='highs-ds')
        if dres.status == 0:
            S = [act[k] for k in range(len(act)) if dres.x[k] > 1e-10]
            y = _solve_rect([[rows[k][0][r] for k in S] for r in range(len(c))], list(c))
            if y is not None and all(v >= 0 for v in y):
                y = {S[k]: y[k] for k in range(len(S)) if y[k] != 0}
                val = sum(v * rows[k][1] for k, v in y.items())
                return {'status': 'optimal-dual', 'value': val, 'y': y, 'float': -res.fun}
    return {'status': 'no exact basis found (degenerate)', 'float': -res.fun}

def _solve_rect(A, b):
    """exact solution of a consistent (possibly over/under-determined) system A x = b, free unknowns set to 0; None if inconsistent"""
    m, n = len(A), len(A[0]); M = [list(A[r]) + [b[r]] for r in range(m)]; piv_cols = []; r0 = 0
    for c in range(n):
        piv = next((r for r in range(r0, m) if M[r][c] != 0), None)
        if piv is None: continue
        M[r0], M[piv] = M[piv], M[r0]; pv = M[r0][c]; M[r0] = [x / pv for x in M[r0]]
        for r in range(m):
            if r != r0 and M[r][c] != 0:
                f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[r0])]
        piv_cols.append(c); r0 += 1
    if any(M[r][n] != 0 for r in range(r0, m)): return None
    x = [Fr(0)] * n
    for r, c in enumerate(piv_cols): x[c] = M[r][n]
    return x

def check_cert(c, rows, y, beta):
    """independent exact re-check of a Farkas certificate: y >= 0, sum y_k a_k = c, sum y_k b_k <= beta"""
    if any(v < 0 for v in y.values()): return False
    s = [sum(y[k] * rows[k][0][r] for k in y) for r in range(len(c))]
    return s == list(c) and sum(y[k] * rows[k][1] for k in y) <= beta
