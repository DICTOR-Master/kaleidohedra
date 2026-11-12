# Laves locality certificates, shared geometry (DICTO 12 Nov 2026, LEAD 1 of this study; method of #61 step 2, splash-rules/proof).
#
# Frame. Lateral coordinates (x, y) in the hexagonal layer basis, Q(a) = a1^2 + a1 a2 + a2^2 (ball spacing 1); height zeta in layer
# spacings, layer spacing^2 = 2/3 (the ideal close packing of #64's Laves net, laves_net.py: G = diag-block [[1,1/2],[1/2,1]], 2/3).
# Positions A = (0,0), B = (1/3,1/3), C = (2/3,2/3) mod the integer lattice. Gap m lies between layer m (position X) and layer m+1
# (position Y), Z = the third position. Its six sites (laves_net.laves, motif order of #64):
#   M0 big over X at m;  M1 big over X at m + 3/4;  K1, K2, K3 small at X + (1/2,0), (0,1/2), (1/2,1/2) at m + 3/8;  T small over Z at m + 7/8.
# Power: pow_j(p) = |p - c_j|^2 - lam [j big]. The gap under study is gap 0; layer 0 is A.
#
# LINEARISATION. The layer spacing is fixed, so pow_i(p) <= pow_j(p) reads, in z = (lam, x, y, zeta),
#   (b_j - b_i) lam + (2 d1 + d2) x + (d1 + 2 d2) y + (4/3) dz zeta  <=  Q(c_j) - Q(c_i) + (2/3)(z_j^2 - z_i^2)
# (d = c_j - c_i laterally, dz = z_j - z_i, b = 1 for big): a fixed normal and a constant right side. Each cell, lifted over a closed
# lam-window, is ONE convex polyhedron in the 4-space (lam, point); one Farkas certificate y >= 0, y^T M = c, y^T m <= beta proves
# c.z <= beta on all of it, i.e. for every lam of the window at once.
from fractions import Fraction as Fr
from itertools import combinations, product
import numpy as np
from scipy.optimize import linprog

POS = {'A': (Fr(0), Fr(0)), 'B': (Fr(1, 3), Fr(1, 3)), 'C': (Fr(2, 3), Fr(2, 3))}
ORDER = 'ABC'
def third(P, R): return ({'A', 'B', 'C'} - {P, R}).pop()
def Qf(a): return a[0] * a[0] + a[0] * a[1] + a[1] * a[1]
ROLES = ['M0', 'M1', 'K1', 'K2', 'K3', 'T']
H2 = Fr(2, 3)
RLAT2 = Fr(4, 3)     # lateral list radius^2 = (2 x covering radius 1/sqrt3)^2: complete by lateral dominance (README, Locality proof)

def gap_sites(m, X, Y):
    """the six sites of gap m (layers m = X, m+1 = Y): {role: (lateral base point, height, big?)}"""
    x, y = POS[X]; Z = third(X, Y)
    return {'M0': ((x, y), Fr(m), 1), 'M1': ((x, y), m + Fr(3, 4), 1),
            'K1': ((x + Fr(1, 2), y), m + Fr(3, 8), 0), 'K2': ((x, y + Fr(1, 2)), m + Fr(3, 8), 0),
            'K3': ((x + Fr(1, 2), y + Fr(1, 2)), m + Fr(3, 8), 0), 'T': (POS[Z], m + Fr(7, 8), 0)}

def step_pos(P, s): return ORDER[(ORDER.index(P) + s) % 3]

def neighbourhoods():
    """all 32 six-layer neighbourhoods round gap 0: steps (s_-2, s_-1, s_0, s_1, s_2), layer m+1 = layer m + s_m; layer 0 = A.
    Returns {name: positions dict m -> letter for m = -2..3}"""
    out = {}
    for st in product((1, -1), repeat=5):
        P = {0: 'A'}
        P[-1] = step_pos('A', -st[1]); P[-2] = step_pos(P[-1], -st[0])
        P[1] = step_pos('A', st[2]); P[2] = step_pos(P[1], st[3]); P[3] = step_pos(P[2], st[4])
        out[''.join(P[m] for m in range(-2, 4))] = P
    return out

def ltype(P, m):
    """c/h type of layer m (needs layers m-1, m, m+1): c if the two steps agree"""
    s1 = (ORDER.index(P[m]) - ORDER.index(P[m - 1])) % 3; s2 = (ORDER.index(P[m + 1]) - ORDER.index(P[m])) % 3
    return 'c' if s1 == s2 else 'h'

def coset_points(base, centre, r2=RLAT2):
    out = []
    for a, b in product(range(-4, 5), repeat=2):
        c = (base[0] + a, base[1] + b)
        if Qf((c[0] - centre[0], c[1] - centre[1])) <= r2: out.append(c)
    return out

def expand(levels, ci, zi):
    """levels: iterable of (base, height, big) -> finite site list (lateral points within RLAT2 of ci), site i itself removed"""
    S = []
    for base, z, b in levels:
        for c in coset_points(base, ci):
            if z == zi and c == ci: continue
            S.append((c, z, b))
    return sorted(set(S))

OVER_X = ('M0', 'M1', 'K1', 'K2', 'K3')     # the sites of a gap fixed by its lower layer alone

def inside_levels(P, lo_gap, hi_gap):
    """every site fixed by the layers lo_gap .. hi_gap+1: all sites of gaps lo_gap .. hi_gap and the over-X sites of gap hi_gap+1"""
    S = [s for m in range(lo_gap, hi_gap + 1) for s in gap_sites(m, P[m], P[m + 1]).values()]
    up = hi_gap + 1; Y0 = next(Y for Y in ORDER if Y != P[up])
    return S + [gap_sites(up, P[up], Y0)[r] for r in OVER_X]

def outside_levels(P, lo_gap, hi_gap):
    """every other site of gaps lo_gap-1 .. hi_gap+1, for every continuation of the stacking: gap hi_gap+1 its T site (layer hi_gap+2
    free), gap lo_gap-1 all six (layer lo_gap-1 free); supersets of gaps hi_gap+2 and lo_gap-2 (all ordered pairs of distinct positions)."""
    out = {}
    up = hi_gap + 1; X = P[up]
    out['near_up'] = sorted({gap_sites(up, X, Y)['T'] for Y in ORDER if Y != X})
    dn = lo_gap - 1; Y = P[dn + 1]
    out['near_dn'] = sorted({s for X2 in ORDER if X2 != Y for s in gap_sites(dn, X2, Y).values()})
    out['far_up'] = sorted({s for X2 in ORDER for Y2 in ORDER if X2 != Y2 for s in gap_sites(up + 1, X2, Y2).values()})
    out['far_dn'] = sorted({s for X2 in ORDER for Y2 in ORDER if X2 != Y2 for s in gap_sites(dn - 1, X2, Y2).values()})
    return out

def row(i, j):
    """bisector row (coefficients on z = (lam, x, y, zeta), right side) for pow_i <= pow_j"""
    (ci, zi, bi), (cj, zj, bj) = i, j
    d1, d2 = cj[0] - ci[0], cj[1] - ci[1]; dz = zj - zi
    return ([Fr(bj - bi), 2 * d1 + d2, d1 + 2 * d2, Fr(4, 3) * dz], Qf(cj) - Qf(ci) + H2 * (zj * zj - zi * zi))

def domain_rows(lo, hi):
    return [([Fr(-1), Fr(0), Fr(0), Fr(0)], -Fr(lo)), ([Fr(1), Fr(0), Fr(0), Fr(0)], Fr(hi))]

# ---------------- exact LP via a float-proposed basis (swapgeom.py of #61, generalised to n variables, float matrix cached)
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
    n = len(A); M = [list(A[r]) + [b[r]] for r in range(n)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None: return None
        M[c], M[piv] = M[piv], M[c]; pv = M[c][c]; M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]; M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[r][n] for r in range(n)]

def _solve_rect(A, b):
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

class Poly:
    """{z : a.z <= b} with exact rows and a cached float copy"""
    def __init__(self, rows):
        self.rows = rows; self.n = len(rows[0][0])
        self.A = np.array([[float(x) for x in a] for a, _ in rows]); self.b = np.array([float(x) for _, x in rows])

    def lp_max(self, c, tries=4000):
        """max c.z, EXACT: dict(status, value, z (exact optimal point, when found), y (dual certificate: rows -> multiplier))"""
        rows, n = self.rows, self.n
        res = linprog(-np.array([float(x) for x in c]), A_ub=self.A, b_ub=self.b, bounds=[(None, None)] * n, method='highs')
        if res.status == 3: return {'status': 'unbounded'}
        if res.status == 2: return {'status': 'infeasible'}
        if res.status != 0: return {'status': 'error ' + res.message}
        dual = -res.ineqlin.marginals; slack = self.b - self.A @ res.x
        act = [k for k in range(len(rows)) if abs(slack[k]) < 1e-7 * (1 + abs(self.b[k]))]
        act.sort(key=lambda k: -dual[k])
        for cnt, B in enumerate(combinations(act, n)):
            if cnt > tries: break
            MB = [rows[k][0] for k in B]
            if _rank(MB) < n: continue
            z = _solve(MB, [rows[k][1] for k in B])
            if any(sum(a[r] * z[r] for r in range(n)) > bb for a, bb in rows): continue
            yB = _solve([[MB[k][r] for k in range(n)] for r in range(n)], list(c))
            if yB is None or any(v < 0 for v in yB): continue
            val = sum(cc * zz for cc, zz in zip(c, z))
            assert val == sum(yB[k] * rows[B[k]][1] for k in range(n))
            return {'status': 'optimal', 'value': val, 'z': z, 'y': {B[k]: yB[k] for k in range(n) if yB[k] != 0}}
        if act:
            Ma = np.array([[float(x) for x in rows[k][0]] for k in act]).T
            dres = linprog(np.array([float(rows[k][1]) for k in act]), A_eq=Ma, b_eq=np.array([float(x) for x in c]),
                           bounds=[(0, None)] * len(act), method='highs-ds')
            if dres.status == 0:
                S = [act[k] for k in range(len(act)) if dres.x[k] > 1e-10]
                y = _solve_rect([[rows[k][0][r] for k in S] for r in range(len(c))], list(c))
                if y is not None and all(v >= 0 for v in y):
                    y = {S[k]: y[k] for k in range(len(S)) if y[k] != 0}
                    return {'status': 'optimal-dual', 'value': sum(v * rows[k][1] for k, v in y.items()), 'y': y, 'float': -res.fun}
        return {'status': 'no exact basis found (degenerate)', 'float': -res.fun}

def check_cert(c, rows, y, beta):
    """exact re-check: y >= 0, sum y_k a_k = c, sum y_k b_k <= beta"""
    if any(v < 0 for v in y.values()): return False
    s = [sum(y[k] * rows[k][0][r] for k in y) for r in range(len(c))]
    return s == list(c) and sum(y[k] * rows[k][1] for k in y) <= beta
