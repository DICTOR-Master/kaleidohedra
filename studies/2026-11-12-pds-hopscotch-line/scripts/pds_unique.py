"""Aim 2 paper, closing item (12 Nov 2026): EXACT count of the 19-design stations on the whole family of 1440-point W(H4) orbits.
Every 1440-point orbit of W(H4) has a point stabiliser of order 10, a parabolic subgroup of type I2(5) (Steinberg: stabilisers of
points are parabolic; the only parabolic of order 10 is I2(5)); its fixed points in one closed chamber form the cone between a 600-cell
vertex v and the midpoint of an edge vw at v. So the 1440-point orbits are exactly the orbits of x(mu) = v + s(w - v), s in (0, 1/2),
and these are the corners of the Queens' line S(mu) in the truncated-600-cell hop: the plane v.x = mu cuts the edge at
s = (1 - mu)/(1 - v.w), v.w = phi/2, for mu in ((5+sqrt5)/8, 1) (600-cell of circumradius 1).
The orbit of x is a spherical 19-design iff P12(x) = 0, P12(y) = sum_v (v.y)^12 - 120 E[y1^12] |y|^12 the degree-12 W(H4)-invariant
harmonic (W(H4) has no invariant harmonic of degree 1..11 or 13..19: basic degrees 2, 12, 20, 30; Sobolev's theorem as stated by
Sloane, Hardin and Cara 2003). P12(x(mu)) is a polynomial in mu over Q(sqrt5); its zeros in the open hop are counted EXACTLY with the
counter of canon_unique.py (norm over Q, exact real-root isolation, sign of gcd(A, F) over Q(sqrt5) at rational endpoints).
Controls: (P1) the root equals mu* = 0.924138673238867458601238076667 of pds_line.py and its factor is pds_line's degree-20 minimal
polynomial; (P2) P12 is harmonic (Laplacian 0, exact) and W(H4)-invariant under one icosian left multiplication (exact); (P3) at mu = 1
(the 600-cell, an 11-design that sounds at degree 12) P12 != 0; (N1) without the sphere-mean term the sum has no zero in the hop."""
import os, time, itertools, sympy as sp
from sympy.combinatorics import Permutation
T0 = time.time()
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, '..', '..', '2026-11-10-canonical-sweep', 'scripts', 'canon_unique.py')).read()
s5 = sp.sqrt(5)
ns = {'sp': sp, 's5': s5}
exec(src[src.index('# ---------- exact arithmetic in Q(sqrt5) ----------'):src.index('ok_all = True')], ns)
count_roots, sgn5 = ns['count_roots'], ns['sgn5']
ok = True
def check(name, cond):
    global ok; ok &= bool(cond); print(('ok   ' if cond else 'FAIL ') + name, flush=True)
phi = (1 + s5) / 2; h = sp.Rational(1, 2)
V = set()
for i in range(4):
    for sg in (1, -1):
        e = [0] * 4; e[i] = sg; V.add(tuple(sp.Integer(c) for c in e))
for sg in itertools.product((1, -1), repeat=4): V.add(tuple(h * c for c in sg))
base = (phi, sp.Integer(1), 1 / phi, sp.Integer(0))
even = [p for p in itertools.permutations(range(4)) if Permutation(list(p)).is_even]
for p in even:
    for sg in itertools.product((1, -1), repeat=3):
        c = [base[0] * sg[0], base[1] * sg[1], base[2] * sg[2], sp.Integer(0)]
        V.add(tuple(sp.radsimp(h * c[p[k]]) for k in range(4)))
V = [sp.Matrix(v) for v in V]
check(f'600-cell: {len(V)} vertices, all of norm 1', len(V) == 120 and all(sp.radsimp(sp.expand((v.T * v)[0])) == 1 for v in V))
y = sp.symbols('y1:5'); Y = sp.Matrix(y); m = sp.Symbol('m')
E12 = sp.Rational(10395, 4 * 6 * 8 * 10 * 12 * 14)          # E[y1^12] on S^3 = 11!!/(4.6...14)
S12 = sum(sp.expand(((v.T * Y)[0]) ** 12) for v in V)
P12 = sp.expand(sp.radsimp(S12 - 120 * E12 * sum(t ** 2 for t in y) ** 6))
lap = sp.expand(sp.radsimp(sum(sp.diff(P12, t, 2) for t in y)))
check('(P2) P12 is harmonic (exact)', lap == 0)
q = (h, h, h, h)                                              # unit icosian 1/2(1+i+j+k): left multiplication
def qmul(a, b):
    a1, b1, c1, d1 = a; a2, b2, c2, d2 = b
    return (a1*a2 - b1*b2 - c1*c2 - d1*d2, a1*b2 + b1*a2 + c1*d2 - d1*c2, a1*c2 - b1*d2 + c1*a2 + d1*b2, a1*d2 + b1*c2 - c1*b2 + d1*a2)
Yq = qmul(q, tuple(y))
check('(P2) P12 is invariant under left multiplication by the icosian (1+i+j+k)/2 (exact)',
      sp.expand(sp.radsimp(P12.subs(dict(zip(y, Yq)), simultaneous=True) - P12)) == 0)
v = sp.Matrix([1, 0, 0, 0]); w = sp.Matrix([phi / 2, h, 1 / (2 * phi), 0])
vw = sp.radsimp((v.T * w)[0]); check(f'v, w adjacent: v.w = phi/2 ({vw})', sp.expand(sp.radsimp(vw - phi / 2)) == 0 and sp.expand(sp.radsimp((w.T * w)[0])) == 1)
s = (1 - m) / (1 - vw); x = v + s * (w - v)
A = sp.expand(sp.radsimp(P12.subs(dict(zip(y, list(x))), simultaneous=True)))
A = sp.expand(sp.radsimp(A))
print(f'P12(x(mu)) = polynomial of degree {sp.Poly(A, m).degree()} in mu over Q(sqrt5) ({time.time() - T0:.0f} s)', flush=True)
lo, hi = (5 + s5) / 8, sp.Integer(1)
check('(P3) at mu = 1 (600-cell vertex) P12 != 0', sgn5(A.subs(m, 1)) != 0)
check('(P3) at mu = (5+sqrt5)/8 (edge midpoint, end of the hop) P12 != 0', sgn5(sp.expand(A.subs(m, lo))) != 0)
roots = count_roots(A, m, lo, hi, 'hop')
for F, (a, b), f in roots:
    print(f'   station mu = {sp.N(f, 30)} (isolating interval width {float(b - a):.1e}); factor of the norm: {sp.factor(F)}', flush=True)
MIN20 = sp.sympify('1048576*m**20 - 13107200*m**19 + 69468160*m**18 - 195952640*m**17 + 278528000*m**16 - 20480000*m**15 - 683458560*m**14 + 1317437440*m**13 - 1168629760*m**12 + 290048000*m**11 + 501350400*m**10 - 656972800*m**9 + 384408320*m**8 - 117126400*m**7 + 9318400*m**6 + 6118400*m**5 - 2304080*m**4 + 318600*m**3 - 12000*m**2 - 900*m + 45', locals={'m': m})
check(f'(P1) exactly one 19-design station in the hop, mu* = 0.924138673238867458601238076667, factor = the degree-20 minimal polynomial',
      len(roots) == 1 and abs(sp.N(roots[0][2], 30) - sp.Float('0.924138673238867458601238076667', 30)) < 1e-25
      and sp.expand(sp.Poly(roots[0][0], m).monic().as_expr() - sp.Poly(MIN20, m).monic().as_expr()) == 0)
S = sp.expand(sp.radsimp(S12.subs(dict(zip(y, list(x))), simultaneous=True)))
check('(N1) the sum without the sphere-mean term has no zero in the hop', len(count_roots(S, m, lo, hi, 'N1')) == 0)
print(f'THEOREM: among all 1440-point orbits of W(H4) exactly one is a spherical 19-design: the corners of S(mu*)' if ok else 'not proved', flush=True)
print(f'time {time.time() - T0:.0f} s', flush=True)
print('FINAL ok: all controls held' if ok else 'FINAL FAIL')
