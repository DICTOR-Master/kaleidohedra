# design_proof.py -- second proof of the octahedral covering lemma, by moments (every O-orbit is a spherical 3-design).
# Exact (sympy): for symbolic u, w the 24 rotations g of O give
#     sum_g (g u . w)   = 0,   sum_g (g u . w)^2 = 8 |u|^2 |w|^2,   sum_g (g u . w)^3 = 0,
# i.e. for unit u, w the 24 numbers t_g = (g u).w have mean 0, mean square 1/3, mean cube 0.
# If every t_g <= m (m > 0), the cubic p(t) = (t - m)(t + 1/(3m))^2 is <= 0 at every t_g, so its mean
# 1/(9m) - m/3 is <= 0, i.e. m >= 1/sqrt3.  Equality forces every t_g in {m, -1/(3m)} = {1/sqrt3, -1/sqrt3}.
# Float part (marked): the same moment bound for 5-designs (icosahedral orbits), as a LEAD -- is it as strong as #43's c?
import itertools
import numpy as np
import sympy as sp
from scipy.optimize import linprog

checks = {}
O = []
for perm in itertools.permutations(range(3)):
    for sg in itertools.product([1, -1], repeat=3):
        M = sp.zeros(3, 3)
        for i, j in enumerate(perm): M[j, i] = sg[i]
        if M.det() == 1: O.append(M)
u = sp.Matrix(sp.symbols('u1 u2 u3')); w = sp.Matrix(sp.symbols('w1 w2 w3'))
uu, ww = u.dot(u), w.dot(w)
S = [sp.expand(sum(((g * u).dot(w))**k for g in O)) for k in (1, 2, 3, 4)]
checks['sum_g t = 0'] = S[0] == 0
checks['sum_g t^2 = 8 |u|^2 |w|^2'] = sp.expand(S[1] - 8 * uu * ww) == 0
checks['sum_g t^3 = 0'] = S[2] == 0
# degree 4 is NOT the uniform moment (O-orbits are not 4-designs): mean t^4 differs from 1/5 in general
checks['sum_g t^4 != 24/5 |u|^4|w|^4 (not a 4-design)'] = sp.expand(S[3] - sp.Rational(24, 5) * uu**2 * ww**2) != 0
m, t = sp.symbols('m t', positive=True)
p = sp.expand((t - m) * (t + 1 / (3 * m))**2)
mom = {0: 1, 1: 0, 2: sp.Rational(1, 3), 3: 0}
Ep = sp.simplify(sum(p.coeff(t, k) * mom[k] for k in range(4)))
print('mean of p =', Ep, ' (= (1 - 3 m^2)/(9 m))')
checks['mean p = (1 - 3m^2)/(9m)'] = sp.simplify(Ep - (1 - 3 * m**2) / (9 * m)) == 0
checks['p <= 0 for t <= m (factor form)'] = sp.factor(p) == sp.factor((t - m) * (3 * m * t + 1)**2 / (9 * m**2))
print('=> max_g (g u).w >= 1/sqrt3 for all unit u, w; equality only if all 24 values are +-1/sqrt3')
# known equality cases: u on a 4-fold axis, w on a 3-fold axis (and the reverse)
e1, c3 = sp.Matrix([1, 0, 0]), sp.Matrix([1, 1, 1]) / sp.sqrt(3)
vals = sorted({sp.nsimplify((g * e1).dot(c3)) for g in O})
print('values (g e1).c3 over O:', vals)
checks['equality case e1, c3'] = vals == [-1 / sp.sqrt(3), 1 / sp.sqrt(3)]

# Other groups (exact): which finite groups have all orbits 3-designs (constant 3) or only 2-designs (constant 9)?
# T = rotations of the tetrahedron, T_d = full tetrahedral, T_h = pyritohedral, I = icosahedral rotations.
def sp_signed(cond):
    out = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product([1, -1], repeat=3):
            M = sp.zeros(3, 3)
            for i, j in enumerate(perm): M[j, i] = sg[i]
            if cond(M, perm, sg): out.append(M)
    return out
even = lambda perm: perm in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]
groups = {
    'T':   sp_signed(lambda M, p, s: even(p) and M.det() == 1),
    'T_h': sp_signed(lambda M, p, s: even(p)),
    'T_d': sp_signed(lambda M, p, s: M.det() * sp.Matrix(3, 3, lambda i, j: 1 if p[j] == i else 0).det() == 1),
}
s5 = sp.sqrt(5); ph = (1 + s5) / 2
def red(M): return M.applyfunc(lambda x: sp.nsimplify(sp.radsimp(sp.expand(x))))
C5 = red(sp.Rational(1, 2) * sp.Matrix([[1, -ph, 1 / ph], [ph, 1 / ph, -1], [1 / ph, 1, ph]]))
gens = [sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]]), sp.diag(1, -1, -1), C5]
Iset = {tuple(sp.eye(3))}; Il = [sp.eye(3)]; fr = [sp.eye(3)]
while fr:
    nx = []
    for M_ in fr:
        for g_ in gens:
            P_ = red(g_ * M_)
            if tuple(P_) not in Iset: Iset.add(tuple(P_)); Il.append(P_); nx.append(P_)
    fr = nx
groups['I'] = Il
print('group orders:', {k: len(v) for k, v in groups.items()})
checks['orders T 12, T_h 24, T_d 24, I 60'] = [len(groups[k]) for k in ('T', 'T_h', 'T_d', 'I')] == [12, 24, 24, 60]
for name, G in groups.items():
    n = len(G)
    m1 = sp.expand(sum(((g * u).dot(w)) for g in G))
    m2 = sp.expand(sum(((g * u).dot(w))**2 for g in G) - sp.Rational(n, 3) * uu * ww)
    m3_ = sp.expand(sp.radsimp(sum(((g * u).dot(w))**3 for g in G)))
    design = 3 if (m1 == 0 and m2 == 0 and m3_ == 0) else (2 if (m1 == 0 and m2 == 0) else 0)
    print(f'  {name}: orbits are spherical {design}-designs -> constant {"3" if design == 3 else "9" if design == 2 else "?"}')
    checks[f'{name} design strength'] = design == {'T': 2, 'T_h': 3, 'T_d': 2, 'I': 3}[name]
# 2-design bound: t in [-1, m], mean 0, mean square 1/3  =>  mean of (m - t)(t + 1) = m - 1/3 >= 0  =>  m >= 1/3, (R/r)^2 <= 9
q = sp.expand((m - t) * (t + 1))
checks['2-design: mean (m-t)(t+1) = m - 1/3'] = sp.simplify(sum(q.coeff(t, k) * mom[k] for k in range(3)) - (m - sp.Rational(1, 3))) == 0

# LEAD (float LP): the same moment method for spherical 5-designs (every icosahedral orbit is one):
# least m such that some probability measure on [-1, m] has the uniform moments 0, 1/3, 0, 1/5, 0.
def least_m(deg):
    mom = [1, 0, 1 / 3, 0, 1 / 5, 0, 1 / 7, 0][:deg + 1]
    lo, hi = 0.0, 1.0
    for _ in range(50):
        mid = (lo + hi) / 2
        x = np.linspace(-1, mid, 4001)
        A = np.array([x**k for k in range(deg + 1)])
        r = linprog(np.zeros(len(x)), A_eq=A, b_eq=mom, bounds=[(0, None)] * len(x), method='highs')
        (hi, lo) = (mid, lo) if r.status == 0 else (hi, mid)
    return hi
m3, m5 = least_m(3), least_m(5)
cI = np.sqrt((5 + 2 * np.sqrt(5)) / 15)
print(f'float LP: moment bound for 3-designs m >= {m3:.6f} (1/sqrt3 = {1/np.sqrt(3):.6f}); '
      f'for 5-designs m >= {m5:.6f} (#43 icosahedral c = {cI:.6f})')
checks['float: 3-design LP bound = 1/sqrt3'] = abs(m3 - 1 / np.sqrt(3)) < 1e-3
for k, v in checks.items(): print(('  ok   ' if v else '  FAIL ') + k)
print('FINAL ok' if all(checks.values()) else 'FINAL FAIL: ' + ', '.join(k for k, v in checks.items() if not v))
