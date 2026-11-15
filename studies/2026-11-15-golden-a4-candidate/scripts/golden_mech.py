#!/usr/bin/env python3
"""Mechanism of the golden A4 double silence (exact, Q(sqrt5)).
A: the 20-set X = perms of (phi^2,phi^2,phi^2,phi,0) and the 30-set Y = perms of (phi^2,phi^2,1,1,0) (centred, R^5 coordinates of the census);
   P = reflection closure of X (the 600-cell); its five S5-orbits.
B: tones T_k (Gegenbauer = Chebyshev U_k on S^3) of every orbit, k <= KMAX.
C: block contents F_rho(O) = sum_{x,y in O} chi_rho(<x,y>) for the 9 irreducible characters of the binary icosahedral group 2I
   (the 600-cell is 2I; <x,y> = Re(x y^-1) names the conjugacy class); identity T_k = sum_rho m_{k,rho} F_rho checked exactly.
D: squared twisted character values |chi~_rho(O)|^2 = dim(rho) F_rho(O)/|O|^2 (must be integers, table of 2.S5 on odd classes, Schur 1911).
E: prediction of every zero from D, against the direct zeros.  F: Galois map Phi = phi^2 * sigma (Double Vision) on P and its orbits.
G: controls."""
import itertools, sys
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from q5 import Q5, PHI, dot, gegenbauer
KMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 30
FAILS = []
def check(ok, what):
    print(('  ok   ' if ok else '  FAIL ') + what, flush=True)
    if not ok: FAILS.append(what)
def centred(base):
    P = sorted(set(itertools.permutations(range(5))))
    pts = set()
    m = sum(base, Q5()) / 5
    for p in itertools.permutations(base):
        pts.add(tuple(x - m for x in p))
    return sorted(pts, key=lambda v: tuple(float(c) for c in v))
def closure(S0, cap=1000):
    n2 = dot(S0[0], S0[0]); S = set(S0); fr = list(S0)
    while fr:
        nf = []
        for x in fr:
            for r in list(S):
                c = dot(x, r) * 2 / n2
                y = tuple(a - c*b for a, b in zip(x, r))
                if y not in S:
                    S.add(y); nf.append(y)
                    if len(S) > cap: return S
        fr = nf
    return S
def s5orbit(x): return frozenset(tuple(x[g[i]] for i in range(5)) for g in itertools.permutations(range(5)))
def sqrtq5(q):
    """exact square root in Q(sqrt5) of q, or None"""
    A, B = q.a, q.b; N = A*A - 5*B*B
    def rsqrt(f):
        if f < 0: return None
        n, d = f.numerator, f.denominator
        import math
        rn, rd = math.isqrt(n), math.isqrt(d)
        return Fr(rn, rd) if rn*rn == n and rd*rd == d else None
    s = rsqrt(N)
    if s is None: return None
    for sg in (1, -1):
        a2 = (A + sg*s) / 2; a = rsqrt(a2)
        if a is None: continue
        for a_ in (a, -a):
            if a_ != 0: b = B / (2*a_)
            else:
                b2 = rsqrt(A / -5) if A <= 0 else None
                if b2 is None: continue
                b = b2
            r = Q5(a_, b)
            if r*r == q and r.sign() > 0: return r
    return None

print('A. point sets', flush=True)
phi2 = PHI*PHI
X = centred([phi2, phi2, phi2, PHI, Q5(0)])
Y = centred([phi2, phi2, Q5(1), Q5(1), Q5(0)])
P = closure(X)
print(f'  |X| = {len(X)}, |Y| = {len(Y)}, reflection closure of X: {len(P)} points', flush=True)
check(len(X) == 20 and len(Y) == 30 and len(P) == 120, 'X 20, Y 30, closure 120 (600-cell)')
n2 = dot(X[0], X[0])
orbs = []; rem = set(P)
while rem:
    o = s5orbit(next(iter(rem))); orbs.append(o); rem -= o
check(all(o <= set(P) for o in orbs) and sum(map(len, orbs)) == 120, 'P is a union of S5-orbits')
# name the orbits
neg = lambda S: frozenset(tuple(-c for c in v) for v in S)
C1 = frozenset(X); C2 = neg(C1)
s = sqrtq5(n2 / dot(Y[0], Y[0]))
print(f'  scale of Y onto the 600-cell radius: {s}', flush=True)
Ys = frozenset(tuple(s*c for c in v) for v in Y) if s is not None else frozenset()
check(s is not None and Ys in orbs, 'the 30-set Y (scaled exactly) is an S5-orbit of the same 600-cell')
C4 = Ys; C5 = neg(C4)
rest = [o for o in orbs if o not in (C1, C2, C4, C5)]
check(len(rest) == 1 and len(rest[0]) == 20 and neg(rest[0]) == rest[0], 'the remaining 20-orbit C3 is antipodal; C2 = -C1 and C5 = -C4 are distinct orbits')
C3 = rest[0]
ORB = [('C1 = X (20)', C1), ('C2 = -X (20)', C2), ('C3 antipodal (20)', C3), ('C4 = Y (30)', C4), ('C5 = -Y (30)', C5)]

print('B. cosine classes of the 600-cell = conjugacy classes of 2I', flush=True)
x0 = next(iter(P)); cls = {}
for y in P:
    c = dot(x0, y) / n2; cls[c] = cls.get(c, 0) + 1
CL = sorted(cls, key=float)
print('  ' + ', '.join(f'{c}: {cls[c]}' for c in CL), flush=True)
check(len(CL) == 9 and sorted(cls.values()) == [1, 1, 12, 12, 12, 12, 20, 20, 30], '9 classes with the sizes of 2I')
def U(k, c): return gegenbauer(k, 1, c)[k]
chars = {'1': lambda c: U(0, c), '2': lambda c: U(1, c), '3': lambda c: U(2, c), '4s': lambda c: U(3, c), '5': lambda c: U(4, c),
         '6': lambda c: U(5, c), "2'": lambda c: U(1, c.conj()), "3'": lambda c: U(2, c.conj()), '4': lambda c: U(6, c) - U(2, c.conj())}
IRR = list(chars)
tab = {r: {c: chars[r](c) for c in CL} for r in IRR}
inner = lambda f, g: sum((Q5(cls[c]) * f[c] * g[c] for c in CL), Q5()) / 120
check(all(inner(tab[r], tab[q]) == (1 if r == q else 0) for r in IRR for q in IRR), 'the 9 class functions are the orthonormal irreducible characters of 2I')
dim = {r: tab[r][Q5(1)] for r in IRR}
mult = {k: {r: inner({c: U(k, c) for c in CL}, tab[r]) for r in IRR} for k in range(KMAX + 1)}
for k in range(KMAX + 1):
    assert all(m.a.denominator == 1 and m.b == 0 and m.a >= 0 for m in mult[k].values())
print('  Sym^k content (McKay):', flush=True)
for k in range(min(KMAX, 20) + 1): print(f'    k={k:2d}: ' + ' + '.join(f'{int(mult[k][r].a) if mult[k][r].a > 1 else ""}{r}' for r in IRR if not mult[k][r].iszero()), flush=True)

print('C. tones and block contents of the five orbits', flush=True)
def paircounts(O):
    N = {}
    for x in O:
        for y in O:
            c = dot(x, y) / n2; N[c] = N.get(c, 0) + 1
    return N
RES = {}
for nm, O in ORB:
    N = paircounts(O)
    T = [sum((Q5(N[c]) * U(k, c) for c in N), Q5()) for k in range(KMAX + 1)]
    Fv = {r: sum((Q5(N[c]) * tab[r][c] for c in N), Q5()) for r in IRR}
    ident = all(T[k] == sum((mult[k][r] * Fv[r] for r in IRR), Q5()) for k in range(KMAX + 1))
    tw = {r: dim[r] * Fv[r] / (len(O)**2) for r in IRR}
    RES[nm] = (T, Fv, tw)
    zeros = [k for k in range(1, KMAX + 1) if T[k].iszero()]
    print(f'  {nm}: tone zeros k<= {KMAX}: {zeros}', flush=True)
    print(f'     |twisted character|^2: ' + ', '.join(f'{r}:{tw[r]}' for r in IRR), flush=True)
    check(ident, f'{nm}: T_k = sum_rho m(k,rho) F_rho for every k <= {KMAX}')
    check(all(v.b == 0 and v.a.denominator == 1 for v in tw.values()), f'{nm}: every |twisted character|^2 is a rational integer')
    check(all(T[k].b == 0 for k in range(KMAX + 1)), f'{nm}: every tone is rational (Galois-fixed)')
    pred = [k for k in range(1, KMAX + 1) if all(mult[k][r].iszero() or tw[r].iszero() for r in IRR)]
    check(pred == zeros, f'{nm}: zeros predicted from the vanishing blocks = direct zeros')
# the forced law
tw1, tw4 = RES['C1 = X (20)'][2], RES['C4 = Y (30)'][2]
u, v, u2, v2 = tw1['6'].a, tw4['6'].a, tw1['4s'].a, tw4['4s'].a
print(f'D. spin part: 6-block u=|chi6(C1)|^2={u}, v=|chi6(C4)|^2={v}; 4s-block u\'={u2}, v\'={v2}', flush=True)
check(2*u + 3*v == 6 and 2*u2 + 3*v2 == 6 and u + u2 == 3 and v + v2 == 2, 'row and column orthogonality: 2u+3v = 6, u+u\' = 3, v+v\' = 2')
sols = [(a, b) for a in range(4) for b in range(3) if 2*a + 3*b == 6]
print(f'   nonnegative integer solutions of 2u+3v = 6: {sols}  -> u = 0 or v = 0 (forced)', flush=True)
check(sols == [(0, 2), (3, 0)], 'only (0,2) and (3,0): the 6-block vanishes on the (3,2)-type pair C1,C2 or on the 4-cycle pair C4,C5')
check(u == 0 and v == 2 and u2 == 3 and v2 == 0, 'actual: (u,v) = (0,2): 6 vanishes on C1 (T5 = T7 = 0), 4s vanishes on C4 (T3 = 0), as Schur 1911 assigns (chi^(4,1) lives on 4-cycles, chi^(3,2) on (3,2)-type)')
check(tw4['4'].iszero() and tw1['4'] == 1 and RES['C3 antipodal (20)'][2]['4'] == 4, 'non-spin 4 (standard rep of S5): 0 on 4-cycles (C4: T6 = 0), 1 on (3,2), 4 on transpositions (C3)')

print('F. Double Vision: Phi = phi^2 * sigma on the 600-cell', flush=True)
lam = phi2
PhiP = {tuple(lam * c.conj() for c in v) for v in P}
check(PhiP == set(P), 'sigma(P) = P / phi^2, so Phi = phi^2 sigma permutes the 600-cell and maps cosine c to sigma(c)')
for nm, O in ORB:
    img = frozenset(tuple(lam * c.conj() for c in v) for v in O)
    check(img == O, f'Phi fixes {nm} setwise (so it forces no zero, only rational tones)')

print('G. controls', flush=True)
Z = centred([Q5(3), Q5(3), Q5(3), Q5(2), Q5(0)])
Pz = closure(Z, cap=600)
check(len(Pz) > 600, 'control member t = 2: its reflection closure is not finite-small (no 600-cell), mechanism does not apply')
Nz = {}
nz2 = dot(Z[0], Z[0])
for x in Z:
    for y in Z:
        c = dot(x, y) / nz2; Nz[c] = Nz.get(c, 0) + 1
Tz = [sum((Q5(Nz[c]) * U(k, c) for c in Nz), Q5()) for k in range(21)]
zz = [k for k in range(1, 21) if Tz[k].iszero()]
print(f'  t = 2 zeros k<=20: {zz}', flush=True)
check(zz == [1, 2], 'control t = 2 is silent only in degrees 1, 2')
check(not RES['C4 = Y (30)'][0][5].iszero(), 'wrong claim rejected: "the 6-block vanishes on C4" (T5(C4) != 0)')
check(not RES['C1 = X (20)'][0][3].iszero(), 'wrong claim rejected: "C1 is a 3-design" (T3(C1) != 0)')
check(not all(RES[nm][0][5].iszero() for nm, _ in ORB if nm.startswith('C4')), 'wrong mechanism rejected: "every S5-orbit in the 600-cell is silent in 5 and 7"')
print('FINAL ok' if not FAILS else f'FINAL FAIL ({len(FAILS)} failed)', flush=True)
