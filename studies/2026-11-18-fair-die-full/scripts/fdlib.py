"""Shared definitions for the fair 14-face die study (2026-11-18-fair-die-full).
The line S(mu) = [-1,1]^3 ∩ {|x|+|y|+|z| <= mu} (cube-octahedron sweep; #90, #94, the Turn Law draft), chamber I (1 < mu < 2):
corners perms(±1, ±b, 0), b = mu - 1. The fair die (studies/2026-11-18-gods-dice): mu_f = 1 + sqrt(2T), T = tan(pi/14) tan(2pi/7).
Exact work: b_f is the root of m_b(y) = y^6 - 18 y^4 - 4 y^2 + 8 near 0.7566 (from T's cubic x^3 - 9x^2 - x + 1 with x = y^2/2, times 8);
minpoly_of(R(b)) takes the resultant with m_b and keeps the factor that vanishes at the 60-digit value (checked)."""
import itertools, math
import numpy as np, sympy as sp, mpmath as mp

mp.mp.dps = 60
y, z, m = sp.symbols('y z m')
M_B = y**6 - 18*y**4 - 4*y**2 + 8
T_HP = mp.tan(mp.pi/14)*mp.tan(2*mp.pi/7)
B_HP = mp.sqrt(2*T_HP)          # b_f to 60 digits
MU_HP = 1 + B_HP
MUF = float(MU_HP); BF = float(B_HP)
KELVIN = 1.5

def minpoly_of(expr, var=y):
    """exact minimal polynomial (in z) of expr(b_f), expr a rational function of the symbol y"""
    expr = sp.sympify(expr)
    num, den = sp.fraction(sp.together(expr))
    res = sp.resultant(sp.Poly(z*den - num, var), sp.Poly(M_B, var))
    val = mp.mpf(str(sp.N(expr.subs(var, sp.Float(mp.nstr(B_HP, 70), 70)), 60)))
    rs = []
    for f, _ in sp.factor_list(sp.Poly(res, z))[1]:
        cs = [mp.mpf(sp.Rational(c).p)/sp.Rational(c).q for c in sp.Poly(f, z).all_coeffs()]
        r = abs(mp.polyval(cs, val))/max(abs(c) for c in cs)
        rs.append((r, f))
    rs.sort(key=lambda t: t[0]); best = rs[0]
    assert best[0] < mp.mpf(10)**-25 and (len(rs) == 1 or rs[1][0] > mp.mpf(10)**-8), ('minpoly factor not identified', [t[0] for t in rs])
    p = sp.Poly(best[1], z).primitive()[1]
    if p.LC() < 0: p = -p
    return p, val

def perms(v):
    return np.array(sorted({tuple(a*s for a, s in zip(p, sg)) for p in itertools.permutations(v) for sg in itertools.product((1, -1), repeat=3)}), float)

def corners(mu):
    return perms((1, mu - 1, 0)) if mu <= 2 else perms((1, 1, mu - 2))

def faces(V):
    """ordered faces of the hull (list of index lists) and their outward unit normals"""
    from scipy.spatial import ConvexHull
    H = ConvexHull(V); fs = {}
    for eq, s in zip(H.equations, H.simplices): fs.setdefault(tuple(np.round(eq, 8)), set()).update(s)
    F, N = [], []
    for k, idx in fs.items():
        idx = list(idx); n = np.array(k[:3]); c = V[idx].mean(0); u = V[idx[0]] - c; w = np.cross(n, u)
        F.append(sorted(idx, key=lambda i: math.atan2(np.dot(V[i] - c, w), np.dot(V[i] - c, u)))); N.append(n)
    return F, N, H

def solid_angle_face(V, f):
    """solid angle of a convex face seen from the origin (fan of Van Oosterom–Strackee triangles)"""
    tot = 0.0; a = V[f[0]]
    for i in range(1, len(f) - 1):
        b, c = V[f[i]], V[f[i + 1]]; la, lb, lc = map(np.linalg.norm, (a, b, c))
        tot += 2*math.atan2(abs(np.dot(a, np.cross(b, c))), la*lb*lc + np.dot(a, b)*lc + np.dot(a, c)*lb + np.dot(b, c)*la)
    return tot

class Checks:
    def __init__(self): self.n = 0; self.bad = []
    def __call__(self, label, cond, detail=''):
        self.n += 1; print(f"  [{'PASS' if cond else 'FAIL'}] {label}" + (f"  ({detail})" if detail else ''))
        if not cond: self.bad.append(label)
    def final(self):
        print(f"\nchecks {self.n - len(self.bad)}/{self.n}")
        print("FINAL ok" if not self.bad else f"FINAL FAIL {self.bad}")
