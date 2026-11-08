# proof_check.py -- exact check of every step of the proof of the octahedral covering lemma
#   for all unit u, w:  max_{g in O} (g u).w >= 1/sqrt3,
# and so (with #43 Theorem 1) of S inside 3 P(S) for every convex polytope with octahedral rotational symmetry.
# Exact parts: sympy / Fraction.  Float parts (marked) only test that the reduction was set up correctly.
import itertools
from fractions import Fraction as Fr
import numpy as np
import sympy as sp

checks = {}

# --- the groups: O = 24 signed permutation matrices of det +1; O_h = all 48
def signed_perms():
    out = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product([1, -1], repeat=3):
            M = sp.zeros(3, 3)
            for i, j in enumerate(perm):
                M[j, i] = sg[i]
            out.append(M)
    return out
ALL = signed_perms()
O = [M for M in ALL if M.det() == 1]
checks['|O| = 24, |O_h| = 48'] = len(O) == 24 and len(ALL) == 48
# closure of O
key = lambda M: tuple(M)
Oset = {key(M) for M in O}
checks['O closed under products'] = all(key(A * B) in Oset for A in O for B in O)

# --- the three rotations of case B
s0 = sp.diag(1, 1, -1)                                   # mirror in the side e1-m of T (plane x3 = 0)
P12 = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])       # mirror in the side m-c3 (plane x1 = x2)
P23 = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])       # mirror in the side e1-c3 (plane x2 = x3)
g1, g2, g3 = sp.eye(3), s0 * P12, s0 * P23
checks['g1, g2, g3 are rotations in O'] = all(key(g) in Oset for g in (g1, g2, g3))
# g2 = half-turn about (1,1,0); g3 = quarter-turn about the x1 axis
checks['g2 half-turn about (1,1,0)'] = g2 * sp.Matrix([1, 1, 0]) == sp.Matrix([1, 1, 0]) and g2 * g2 == sp.eye(3)
checks['g3 quarter-turn about x1'] = g3 * sp.Matrix([1, 0, 0]) == sp.Matrix([1, 0, 0]) and g3**4 == sp.eye(3) and g3**2 != sp.eye(3)

a1, a2, a3, b1, b2, b3 = sp.symbols('a1 a2 a3 b1 b2 b3')
a, b = sp.Matrix([a1, a2, a3]), sp.Matrix([b1, b2, b3])
E = [sp.expand(((g * a).T * (s0 * b))[0]) for g in (g1, g2, g3)]
E0, E12, E23 = a1*b1 + a2*b2 - a3*b3, a1*b2 + a2*b1 + a3*b3, a1*b1 + a2*b3 + a3*b2
checks['(g_i a).(s0 b) = E0, E12, E23'] = [sp.expand(e - f) for e, f in zip(E, (E0, E12, E23))] == [0, 0, 0]
Lsum = sp.expand(E0 + E12 + E23)
checks['E0+E12+E23 has nonnegative coefficients'] = all(c >= 0 for c in sp.Poly(Lsum, a1, a2, a3, b1, b2, b3).coeffs())

# --- vertex lemma inputs: chamber T = cone(e1, e1+e2, e1+e2+e3) = {x1 >= x2 >= x3 >= 0}
V = [sp.Matrix([1, 0, 0]), sp.Matrix([1, 1, 0]), sp.Matrix([1, 1, 1])]
def ev(expr, v, w):
    return expr.subs({a1: v[0], a2: v[1], a3: v[2], b1: w[0], b2: w[1], b3: w[2]})
rowsA, rowsB, eqA, eqB = [], [], [], []
for v in V:
    for w in V:
        n2 = (v.dot(v)) * (w.dot(w))
        A = v.dot(w)                                  # case A, g = identity
        B = sp.Rational(1, 3) * ev(Lsum, v, w)        # case B, average of the three
        okA = A >= 0 and 3 * A**2 >= n2
        okB = B >= 0 and 3 * B**2 >= n2
        rowsA.append(okA); rowsB.append(okB)
        if 3 * A**2 == n2: eqA.append((tuple(v), tuple(w)))
        if 3 * B**2 == n2: eqB.append((tuple(v), tuple(w)))
        print(f'  v={tuple(v)} w={tuple(w)}  |v|^2|w|^2={n2}  caseA L={A} (3L^2={3*A**2})  caseB L={B} (3L^2={3*B**2})')
checks['case A: 9 vertex pairs pass exactly'] = all(rowsA)
checks['case B: 9 vertex pairs pass exactly (weights 1/3)'] = all(rowsB)
print('equality pairs, case A:', eqA, ' case B:', eqB)
checks['equality only at (e1, c3) and (c3, e1)'] = sorted(eqA) == sorted(eqB) == sorted([((1, 0, 0), (1, 1, 1)), ((1, 1, 1), (1, 0, 0))])

# --- the sides of the Moebius triangle (exact cosines)
def cos2(v, w): return sp.nsimplify(v.dot(w)**2 / (v.dot(v) * w.dot(w)))
print('cos^2 of the sides e1-m, m-c3, e1-c3:', cos2(V[0], V[1]), cos2(V[1], V[2]), cos2(V[0], V[2]))
mp = P23 * V[1]                                            # m mirrored in the hypotenuse
print("kite diagonal m-m' cos =", sp.nsimplify(V[1].dot(mp) / V[1].dot(V[1])), '(60 deg; the kite proof needs <= 1/sqrt3)')
checks['hypotenuse cos^2 = 1/3, kite diagonal 60 deg'] = cos2(V[0], V[2]) == sp.Rational(1, 3) and V[1].dot(mp) / V[1].dot(V[1]) == sp.Rational(1, 2)

# --- FLOAT test of the reduction: F(u, w) computed directly over all 24 rotations, against the proof's
# case split (u moved into T by O_h, w into T or s0 T); the bound must hold in both.
On = np.array([np.array(M, float) for M in O]); Alln = np.array([np.array(M, float) for M in ALL])
rng = np.random.default_rng(7)
worst, mism = 9.0, 0
for _ in range(20000):
    u = rng.normal(size=3); u /= np.linalg.norm(u)
    w = rng.normal(size=3); w /= np.linalg.norm(w)
    F = max((M @ u) @ w for M in On)
    # reduction
    h = next(M for M in Alln if (lambda x: x[0] >= x[1] >= x[2] >= 0)(M @ u))
    ua, wa = h @ u, h @ w
    k = next(M for M in Alln if (lambda x: x[0] >= x[1] >= x[2] >= 0)(M @ wa))
    if round(np.linalg.det(k)) == 1:
        bound = ua @ (k @ wa)                                  # case A (g = k)
    else:
        bv = k @ wa                                            # wa = k^-1 bv, k^-1 improper: use s0 b
        g = k.T @ np.array(s0, float)                          # k^-1 s0 ... proper
        assert round(np.linalg.det(g)) == 1
        wb = np.array(s0, float) @ bv                          # = g^-1 wa  (same orbit position)
        bound = np.mean([(np.array(G, float) @ ua) @ wb for G in (g1, g2, g3)])
    worst = min(worst, F)
    if bound > F + 1e-12: mism += 1
print(f'float: min F over 20000 random pairs = {worst:.6f} (1/sqrt3 = {1/np.sqrt(3):.6f}); bound > F in {mism} cases')
checks['float: reduction bound never exceeds F, F >= 1/sqrt3'] = mism == 0 and worst >= 1 / np.sqrt(3) - 1e-12

for k_, v_ in checks.items(): print(('  ok   ' if v_ else '  FAIL ') + k_)
print('FINAL ok' if all(checks.values()) else 'FINAL FAIL: ' + ', '.join(k for k, v in checks.items() if not v))
