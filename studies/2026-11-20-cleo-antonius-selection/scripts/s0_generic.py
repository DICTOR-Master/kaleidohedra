"""Step 0 (exact, Sage/Singular over Q): the generic system of the (b), (c), (d) family with BOTH great slopes free.
Construction copied line by line from studies/2026-11-15-dicto-yantra-uniqueness/scripts/s1_system.py (#103 Theorem 15's
census): u = w7/b7, v = w3/(1 - b3), t = b1/w1 ((b) by construction), S = b9; every other quantity is a meeting point.
G = 0 is (c), H1 = 0 the closing marma (1,4,6), D = 0 (d) squared; numerators stripped of the divisor-lemma factors (over Q,
generic u, v), exactly as in s1.  Also the crossing C = det3(t4 right leg, t5 base, t6 right leg) (#103 Proposition 13, Figure 12).
Writes data/system-uv.json (exponents (u, v, t, S) -> integer coefficient).  FINAL ok iff the lemma closes."""
import sys, time, os, json
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
D = lambda *p: os.path.join(ROOT, *p)
from sage.all__sagemath_singular import QQ, ZZ, PolynomialRing
Rg = PolynomialRing(QQ, 'u,v,t,S'); Fr = Rg.fraction_field()
u, v, t, S = (Fr(x) for x in Rg.gens()); one = Fr(1)
print('PROGRESS 0.05 construction (generic great slopes u, v)')
P = v**2 / (1 + v**2); R = one / (1 + u**2)             # t3, t7 inscribed
w3 = v / (1 + v**2); w7 = u / (1 + u**2)
b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2)             # (b)
steps = []
def step(name, q, why): steps.append((name, q, why)); return q
step('R', R, 'b7 > 0')
xW = w7 * P / R                                         # t7's leg at depth P (marma (2,3,7))
step('S - P', S - P, 'b9 > b3')
xX = xW * (S - R) / (S - P)                             # t2's leg (apex S = a2 = b9) at depth R
step('R - P', R - P, 'b7 > b3')
k9 = xX / (R - P)                                       # t9's leg (apex P = a9 = b3) through (xX, R): marma (2,7,9)
w9 = k9 * (S - P)
Gx = w9**2 + S**2 - S                                   # (c)
step('1 - P', 1 - P, 'b3 < 1 = a3')
k3 = w3 / (1 - P)                                       # t3's leg x = k3 (1 - d)
xZ = k3 * (1 - R)                                       # t3's leg at depth R (marma (3,7,8))
step('R - b1', R - b1, 'b1 < b7')
c138 = w1 * (R - b1) - xZ * (P - b1)                    # marma (1,3,8), linear in Q
step('c138', c138, 'if 0, the marma equation reduces to w1 (R - b1)(b1 - P) = 0, impossible (w1 > 0, b1 < b3 < b7)')
Q = (w1 * P * (R - b1) - xZ * b1 * (P - b1)) / c138
step('Q - b1', Q - b1, 'b6 > b1')
m1 = w1 / (Q - b1)
step('k3 + k9', k3 + k9, 'both slopes positive (S > R > P)')
b8 = (k3 + k9 * P) / (k3 + k9)                          # marma (3,8,9)
xF = k9 * (Q - P)                                       # marma (4,6,9)
w6 = xW * (S - Q) / (S - P)                             # corner touch (2,6,6)
k7 = w7 / R
step('m1 + k7', m1 + k7, 'both slopes positive')
b2 = m1 * Q / (m1 + k7)                                 # marma (1,2,7)
step('b8 - Q', b8 - Q, 'b8 > b6')
c4 = xF / (b8 - Q)
c8 = xZ / (R - b1)
step('c4 + c8', c4 + c8, 'both slopes positive (xF > 0 since Q > P)')
b4 = (c4 * b8 + c8 * b1) / (c4 + c8)                    # corner touch (4,4,8)
step('Q - b2', Q - b2, 'b6 > b2')
E146 = m1 * (Q - b4) * (Q - b2) - w6 * (b4 - b2)        # marma (1,4,6), times (Q - b2)
step('m1 + k9', m1 + k9, 'both slopes positive')
b5 = (m1 * Q + k9 * P) / (m1 + k9)                      # marma (1,5,9)
h = Q - b5; hw = m1 * h; cc = one / 2 - b5
Dd = (hw**2 + h**2) * cc**2 - (hw * (Q - one / 2))**2   # (d), squared
extra = [('P - b1', P - b1, 'b1 < b3'), ('Q - P', Q - P, 'b6 > b3'), ('S - R', S - R, 'b9 > b7'), ('S - Q', S - Q, 'b9 > b6'),
         ('1 - S', 1 - S, 'b9 < 1'), ('b8 - b1', b8 - b1, 'b8 > b1'), ('b8 - R', b8 - R, 'b8 > b7'),
         ('b5 - b4', b5 - b4, 'b5 > b4'), ('b2 - b1', b2 - b1, 'b2 > b1')]
# ---------------- divisor lemma (over Q, generic u, v) ----------------
print('PROGRESS 0.12 divisor lemma')
NZ = {}
def addnz(pol, why):
    for f, m in pol.factor():
        if f.degree() > 0: NZ.setdefault(f / f.lc(), why)
for base in (u, v, 1 + u**2, 1 + v**2, t, 1 + t**2): addnz(base.numerator(), 'coordinate (u, v, t > 0) or sum of squares')
def check_den(q): return [f for f, m in q.denominator().factor() if f.degree() > 0 and (f / f.lc()) not in NZ]
lemma_ok = True
for name, q, why in steps + extra:
    bad = check_den(q)
    if bad: lemma_ok = False; say('LEMMA GAP: denominator of', name, 'has factors outside NZ:', bad)
    addnz(q.numerator(), f'numerator of {name} ({why})')
for name, X in (('G', Gx), ('E146', E146), ('Dd', Dd)):
    bad = check_den(X)
    if bad: lemma_ok = False; say('LEMMA GAP: denominator of', name, bad)
say('divisor lemma (generic u, v) closes:', lemma_ok, '; NZ factors over Q:', len(NZ))
k7_ = w7 / R
w5 = w6 * (b5 - b2) / (Q - b2)                          # corner touch (5,5,6)
w4 = xF * (b8 - b4) / (b8 - Q)
def det3(p, q, r):
    def line(pp):
        (x1, y1), (x2, y2) = pp
        return (y1 - y2, x2 - x1, x1 * y2 - x2 * y1)
    A, B, C = line(p), line(q), line(r)
    return (A[0] * (B[1] * C[2] - B[2] * C[1]) - A[1] * (B[0] * C[2] - B[2] * C[0]) + A[2] * (B[0] * C[1] - B[1] * C[0]))
Cx = det3(((w4, b4), (0, b8)), ((-w5, b5), (w5, b5)), ((w6, Q), (0, b2)))   # t4 right leg (apex a4 = b8), t5 base, t6 right leg (apex a6 = b2)
def strip(X, label):
    keep = Rg(1); dropped = []
    for f, m in Rg(X.numerator()).factor():
        if f.degree() == 0: continue
        if (f / f.lc()) in NZ: dropped.append((str(f)[:30], m))
        else: keep *= f**m
    say(label, 'kept degrees (u, v, t, S) =', [keep.degree(g) for g in Rg.gens()], 'terms', len(keep.monomials()), '; dropped', dropped)
    return keep
out = {}
for name, X in (('G', Gx), ('H1', E146), ('D', Dd), ('C', Cx)):
    F = strip(X, name)
    out[name] = [[list(map(int, e)), str(ZZ(cf))] for e, cf in F.dict().items()]
json.dump(out, open(D('data', 'system-uv.json'), 'w'))
say('wrote data/system-uv.json')
print('FINAL ok' if lemma_ok else 'FINAL FAIL (divisor lemma gap)')
