#!/usr/bin/env python3
"""Integer Queens, part 0: controls and the containment theorem (18 Nov 2026).
(a) Golden control: the 600-cell in sum-zero R^5 as the closure of A = perms(phi^2,phi^2,phi^2,phi,0) under reflection in its
    own members, exact in Q(phi); its S5 split 20+30+20+20+30 and |G| = 14400 (sympy Schreier-Sims).
(b) Which irreducible finite reflection groups of rank n contain W(A_n)?  Lattice-index test (exact Cartan determinants),
    compared with the order-divisibility test of the heptagonal-queen study.  Reproduces the heptagonal result (n = 6: none).
Usage: s0_controls.py out.json"""
import sys, os, json, time, math, itertools; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from qlib import Checks
import sympy as sp
from sympy.combinatorics import Permutation, PermutationGroup
OUT = sys.argv[1]; C = Checks(); t0 = time.time(); out = {}

# ---------------- (a) exact Q(phi): a + b*phi, phi^2 = phi + 1 ----------------
class G:
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a = Fr(a); s.b = Fr(b)
    def __add__(s, o): return G(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return G(s.a - o.a, s.b - o.b)
    def __neg__(s): return G(-s.a, -s.b)
    def __mul__(s, o): return G(s.a*o.a + s.b*o.b, s.a*o.b + s.b*o.a + s.b*o.b)
    def inv(s):
        N = s.a*s.a + s.a*s.b - s.b*s.b; return G((s.a + s.b)/N, -s.b/N)
    def __eq__(s, o): return s.a == o.a and s.b == o.b
    def __hash__(s): return hash((s.a, s.b))
    def f(s): return float(s.a) + float(s.b)*(1 + 5**0.5)/2
Z, ONE, PHI = G(0), G(1), G(0, 1); PHI2 = PHI*PHI
def ip(x, y):
    s = Z
    for u, v in zip(x, y): s = s + u*v
    return s
def centre(x):
    s = Z
    for u in x: s = s + u
    return tuple(G(5)*u - s for u in x)
def perms(seed): return sorted({centre(p) for p in itertools.permutations(seed)}, key=lambda v: [u.f() for u in v])
def refl(x, r):
    k = G(2)*ip(x, r)*ip(r, r).inv(); return tuple(u - k*w for u, w in zip(x, r))

A = perms([PHI2, PHI2, PHI2, PHI, Z])
P = {x: 1 for x in A}; front = list(A)
while front:
    new = []
    for x in front:
        for r in list(P):
            y = refl(x, r)
            if y not in P: P[y] = 1; new.append(y)
    front = new
P = list(P)
C(len(P) == 120, f'control: closure of A under reflection in its own members has {len(P)} points (600-cell: 120)')
R2 = {ip(p, p) for p in P}; C(len(R2) == 1, 'control: all 120 on one sphere')
# S5 split: orbit = sorted coordinate multiset
orb = {}
for p in P: orb.setdefault(tuple(sorted(p, key=lambda u: u.f())), []).append(p)
sizes = sorted(len(v) for v in orb.values())
C(sizes == [20, 20, 20, 30, 30], f'control: S5 split of the 600-cell {sizes} = 20+20+20+30+30')
B = perms([PHI2, PHI2, ONE, ONE, Z])
negA = [tuple(-u for u in a) for a in A]; negB = [tuple(-u for u in b) for b in B]
C3 = perms([PHI, Z, Z, Z, -PHI])     # centre() of phi(e_i - e_j) is 5*phi(e_i - e_j)
Ps = set(P)
C(all(set(S) <= Ps for S in (A, B, negA, negB, C3)) and len(set(A) | set(B) | set(negA) | set(negB) | set(C3)) == 120,
  'control: the five orbits are A, B, -A, -B and C3 = phi x (A4 roots), together exactly the 600-cell')
idx = {p: i for i, p in enumerate(P)}
def as_perm(f): return Permutation([idx[f(p)] for p in P])
gens = [as_perm(lambda p: (p[1], p[0]) + p[2:]), as_perm(lambda p: p[1:] + p[:1])]
S5 = PermutationGroup(gens); C(S5.order() == 120, f'control: coordinate permutations act as S5 ({S5.order()})')
H = PermutationGroup(gens + [as_perm(lambda p: refl(p, A[0]))])
C(H.order() == 14400, f'control: S5 + one reflection in a corner of A generates order {H.order()} (W(H4) = 14400)')
# must fail: an ordinary seed is not closed under reflection in its own member
Ao = perms([PHI2, PHI2, PHI2, G(Fr(3, 2)), Z]); so = set(Ao)
C(not all(refl(x, Ao[0]) in so for x in Ao), 'control (must fail): ordinary orbit (phi^2,phi^2,phi^2,3/2,0) is not closed under reflection in its own corner')
out['golden'] = dict(n=len(P), split=sizes, H4=H.order())

# ---------------- (b) containment of W(A_n) ----------------
def cartan(t, n):
    M = sp.zeros(n, n)
    for i in range(n): M[i, i] = 2
    if t in 'ABCD' or t == 'E':
        for i in range(n - 1): M[i, i+1] = M[i+1, i] = -1
    if t == 'B': M[n-2, n-1] = -2
    if t == 'C': M[n-1, n-2] = -2
    if t == 'D':
        M[n-2, n-1] = M[n-1, n-2] = 0; M[n-3, n-1] = M[n-1, n-3] = -1
    if t == 'E':   # chain 0..n-2 plus node n-1 attached to node 2
        M[n-2, n-1] = M[n-1, n-2] = 0; M[2, n-1] = M[n-1, 2] = -1
    return M
dets = {('A', n): cartan('A', n).det() for n in range(1, 9)}
dets.update({('D', n): cartan('D', n).det() for n in range(4, 9)})
dets.update({('E', n): cartan('E', n).det() for n in (6, 7, 8)})
C(all(dets[('A', n)] == n + 1 for n in range(1, 9)) and all(dets[('D', n)] == 4 for n in range(4, 9))
  and [dets[('E', n)] for n in (6, 7, 8)] == [3, 2, 1], 'Cartan determinants: A_n n+1, D_n 4, E6 3, E7 2, E8 1 (exact)')
order = lambda t, n: {'A': math.factorial(n+1), 'B': 2**n*math.factorial(n), 'C': 2**n*math.factorial(n), 'D': 2**(n-1)*math.factorial(n),
                      'E': {6: 51840, 7: 2903040, 8: 696729600}.get(n), 'F': 1152, 'H': {3: 120, 4: 14400}.get(n)}[t]
table = []
for n in range(4, 9):
    rows = []
    # simply laced candidates (B_n, C_n and F4 reduce to their D-type one-length subsystems; A_n is connected, so it
    # cannot sit in the orthogonal A1^n part)
    cands = [('A', n, 'A', n), ('B', n, 'D', n), ('C', n, 'D', n), ('D', n, 'D', n)]
    if n in (6, 7, 8): cands.append(('E', n, 'E', n))
    if n == 4: cands += [('F', 4, 'D', 4)]
    for t, m, sub, _ in cands:
        ratio = sp.Rational(n + 1, dets[(sub, n)])
        index_ok = ratio.q == 1 and sp.sqrt(ratio).is_integer
        div_ok = order(t, m) % math.factorial(n + 1) == 0
        rows.append(dict(group=f'{t}{m}', via=f'{sub}{n}', det_ratio=str(ratio), index_test=bool(index_ok), divides=bool(div_ok)))
    if n == 4: rows.append(dict(group='H4', via='non-crystallographic', det_ratio='-', index_test=None, divides=order('H', 4) % 120 == 0))
    table.append(dict(n=n, rows=rows))
    print(f'n={n}: ' + '; '.join(f"{r['group']}(via {r['via']}): det ratio {r['det_ratio']}, index {r['index_test']}, divides {r['divides']}" for r in rows))
def allowed(n): return sorted(r['group'] for t in table if t['n'] == n for r in t['rows'] if r['index_test'])
C(allowed(4) == ['A4'] and allowed(5) == ['A5'] and allowed(6) == ['A6'],
  f'heptagonal control: crystallographic groups containing W(A_n) for n=4,5,6 are only A_n ({allowed(4)}, {allowed(5)}, {allowed(6)}); with H4 for n=4 (600-cell)')
C(allowed(7) == ['A7', 'E7'] and allowed(8) == ['A8', 'E8'], f'n=7: {allowed(7)}; n=8: {allowed(8)} (index test)')
div7 = sorted(r['group'] for t in table if t['n'] == 7 for r in t['rows'] if r['divides'])
C(div7 == ['A7', 'B7', 'C7', 'D7', 'E7'], f'order divisibility alone does not decide n=7 ({div7} pass); the index test is needed')
out['containment'] = table
json.dump(out, open(OUT, 'w'), indent=1)
print(f'time {time.time()-t0:.1f}s'); C.final()
