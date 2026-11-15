"""Step 1: the polynomial system of Kulaichev's yantra, rebuilt from the geometry, with every divisor accounted for, and the FULL
elimination (no factor chosen by a numerical point).

Problem (#103 Theorem 1 conditions + Kulaichev's (a)-(d), frame of model.py): circle of diameter 1, axis vertical, depth d below the
top point O; nine isosceles triangles t1..t9 (t1..t5 point down, t6..t9 up), base depth b_i, half-width w_i, apex depth a_i;
Huet's conditions as in Chiodo 2021 (i)-(iii): t3, t7 inscribed (a3 = 1, a7 = 0, corners on the circle); seven apex-on-base points;
nine marma pairs and three corner touches (model.py lists).  Kulaichev: (a) t3 congruent t7 (u = v), (b) t1's corners on the circle,
(c) t9's corners on the circle, (d) the incircle of the innermost triangle (t1's legs and t5's base) is centred at the circle's centre.
Admissible (#103 Theorem 1): b1 < ... < b9, every w_i > 0, apexes on the correct side, corners in the closed disc.

Coordinates: u = w7/b7 (so b7 = R = 1/(1+u^2)), v = w3/(1-b3) (b3 = P = v^2/(1+v^2)), t = b1/w1 (t1's corner = (t, t^2)/(1+t^2)),
S = b9.  Each further quantity is the meeting point of two lines (no choice), so every admissible yantra satisfies
G = 0 ((c)), E146 = 0 (marma (1,4,6), the closing equation) and Dd = 0 ((d), squared), with every divisor nonzero.

The divisor lemma (checked here exactly): starting from NZ = {u, 1+u^2, t, 1+t^2}, each step divisor q is a rational function whose
denominator factors are already in NZ; q is nonzero at every admissible yantra (geometric reason in the table below), so the factors
of its numerator join NZ.  Then the reduced denominators of G, E146, Dd consist of NZ factors, so their numerators vanish, and NZ
factors of the numerators may be dropped.  Resultants are in the ideal, so every admissible yantra has its u among the roots of
E(u) = Res_t(A, B) where A, B are the non-NZ parts of Res_S(G, H1), Res_S(G, D).
Writes data/system-K.txt, data/nz-factors.txt, data/R1-factors.txt, data/R2-factors.txt, data/E-factors.txt, data/candidates.txt
(the univariate factors left after dropping NZ factors).  FINAL ok iff: the system matches #103's (stage4) up to constants,
the lemma closes, E is not identically zero, and f348 (Theorem 10) is one of the candidate factors."""
import sys, time, os
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
D = lambda *p: os.path.join(ROOT, *p)
from sage.all__sagemath_singular import QQ, ZZ, PolynomialRing
Rg = PolynomialRing(QQ, 'u,t,S'); u, t, S = Rg.gens(); Fr = Rg.fraction_field()
u, t, S = Fr(u), Fr(t), Fr(S); one = Fr(1)
print('PROGRESS 0.05 construction')
# ---------------- construction (each line: what meets what) ----------------
v = u                                                   # (a)
P = v**2 / (1 + v**2); R = one / (1 + u**2)             # t3, t7 inscribed
w3 = v / (1 + v**2); w7 = u / (1 + u**2)
b1 = t**2 / (1 + t**2); w1 = t / (1 + t**2)             # (b)
steps = []                                              # (name, quantity, why nonzero at an admissible yantra)
def step(name, q, why): steps.append((name, q, why)); return q
step('R', R, 'b7 > 0')
xW = w7 * P / R                                         # t7's leg at depth P (marma (2,3,7): t2's leg passes here)
step('S - P', S - P, 'b9 > b3')
xX = xW * (S - R) / (S - P)                             # t2's leg (apex S = a2 = b9) at depth R
step('R - P', R - P, 'b7 > b3')
k9 = xX / (R - P)                                       # t9's leg (apex P = a9 = b3) through (xX, R): marma (2,7,9); x = k9 (d - P)
w9 = k9 * (S - P)
Gx = w9**2 + S**2 - S                                   # (c)
step('1 - P', 1 - P, 'b3 < 1 = a3')
k3 = w3 / (1 - P)                                       # t3's leg x = k3 (1 - d)
xZ = k3 * (1 - R)                                       # t3's leg at depth R (marma (3,7,8): t8's leg passes here)
step('R - b1', R - b1, 'b1 < b7')
# marma (1,3,8): t1's leg (apex Q = a1 = b6, corner (w1, b1)) and t8's leg (apex b1 = a8, through (xZ, R)) meet at depth P:
#   w1 (Q - P)/(Q - b1) = xZ (P - b1)/(R - b1)   ->  linear in Q:  Q c138 = w1 P (R - b1) - xZ b1 (P - b1)
c138 = w1 * (R - b1) - xZ * (P - b1)
step('c138', c138, 'if 0, the marma equation reduces to w1 (R - b1)(b1 - P) = 0, impossible (w1 > 0, b1 < b3 < b7)')
Q = (w1 * P * (R - b1) - xZ * b1 * (P - b1)) / c138
step('Q - b1', Q - b1, 'b6 > b1')
m1 = w1 / (Q - b1)                                      # t1's leg x = m1 (Q - d)
step('k3 + k9', k3 + k9, 'both slopes positive (S > R > P)')
b8 = (k3 + k9 * P) / (k3 + k9)                          # t3's leg meets t9's leg at depth b8 (marma (3,8,9))
xF = k9 * (Q - P)                                       # t9's leg at depth Q (marma (4,6,9): t4's leg passes here)
w6 = xW * (S - Q) / (S - P)                             # t2's leg at depth Q = t6's corner (corner touch (2,6,6))
k7 = w7 / R                                             # t7's leg x = k7 d
step('m1 + k7', m1 + k7, 'both slopes positive')
b2 = m1 * Q / (m1 + k7)                                 # t1's leg meets t7's leg at depth b2 (marma (1,2,7))
step('b8 - Q', b8 - Q, 'b8 > b6')
c4 = xF / (b8 - Q)                                      # t4's leg (apex b8 = a4) through (xF, Q): x = c4 (b8 - d)
c8 = xZ / (R - b1)                                      # t8's leg x = c8 (d - b1)
step('c4 + c8', c4 + c8, 'both slopes positive (xF > 0 since Q > P)')
b4 = (c4 * b8 + c8 * b1) / (c4 + c8)                    # t4's corner on t8's leg (corner touch (4,4,8))
step('Q - b2', Q - b2, 'b6 > b2 (t6 apex = b2, base Q)')
# marma (1,4,6): t1's leg and t6's leg (apex b2 = a6, corner (w6, Q)) meet at depth b4, times (Q - b2):
E146 = m1 * (Q - b4) * (Q - b2) - w6 * (b4 - b2)
step('m1 + k9', m1 + k9, 'both slopes positive')
b5 = (m1 * Q + k9 * P) / (m1 + k9)                      # t1's leg meets t9's leg at depth b5 (marma (1,5,9))
h = Q - b5; hw = m1 * h; c = one / 2 - b5               # innermost triangle: apex (0, Q), base at b5, corners (+-hw, b5)
Dd = (hw**2 + h**2) * c**2 - (hw * (Q - one / 2))**2    # (d): distance from the centre (0, 1/2) to the base = to the leg, squared
# further quantities that admissibility makes nonzero (used only to drop factors, never as divisors)
extra = [('P - b1', P - b1, 'b1 < b3'), ('Q - P', Q - P, 'b6 > b3'), ('S - R', S - R, 'b9 > b7'), ('S - Q', S - Q, 'b9 > b6'),
         ('1 - S', 1 - S, 'b9 < 1 (t9 corner on the circle with w9 > 0)'), ('b8 - b1', b8 - b1, 'b8 > b1'), ('R - b8', R - b8, 'b7 < b8? no: b7 < b8'),
         ('b5 - b4', b5 - b4, 'b5 > b4'), ('b2 - b1', b2 - b1, 'b2 > b1')]
extra = [e for e in extra if e[0] != 'R - b8'] + [('b8 - R', b8 - R, 'b8 > b7')]
# ---------------- divisor lemma ----------------
print('PROGRESS 0.15 divisor lemma')
NZ = {}
def addnz(pol, why):
    for f, m in pol.factor():
        if f.degree() > 0:
            f = f / f.lc(); NZ.setdefault(f, why)
for base in (u, 1 + u**2, t, 1 + t**2): addnz(base.numerator(), 'coordinate (u > 0, t > 0) or sum of squares')
def check_den(name, q):
    bad = [f for f, m in q.denominator().factor() if f.degree() > 0 and (f / f.lc()) not in NZ]
    return bad
lemma_ok = True
for name, q, why in steps:
    bad = check_den(name, q)
    if bad: lemma_ok = False; say('LEMMA GAP: denominator of', name, 'has factors outside NZ:', bad)
    addnz(q.numerator(), f'numerator of {name} ({why})')
for name, q, why in extra:
    bad = check_den(name, q)
    if bad: lemma_ok = False; say('LEMMA GAP (extra):', name, bad)
    addnz(q.numerator(), f'numerator of {name} ({why})')
for name, X in (('G', Gx), ('E146', E146), ('Dd', Dd)):
    bad = check_den(name, X)
    if bad: lemma_ok = False; say('LEMMA GAP: denominator of', name, bad)
say('divisor lemma closes:', lemma_ok, '; NZ factors:', len(NZ))
with open(D('data', 'nz-factors.txt'), 'w') as fh:
    for f, why in NZ.items(): fh.write(f'{f}    # {why}\n')
def strip(pol, label):
    keep = Rg(1); dropped = []
    for f, m in pol.factor():
        if f.degree() == 0: continue
        if (f / f.lc()) in NZ: dropped.append((f, m))
        else: keep *= f**m
    say(f'{label}: kept factor degrees (u, t, S) = {(keep.degree(Rg.gens()[0]), keep.degree(Rg.gens()[1]), keep.degree(Rg.gens()[2]))};',
        'dropped NZ factors:', [(str(f) if len(str(f)) < 40 else f'<deg {f.degree()}>', m) for f, m in dropped])
    return keep
print('PROGRESS 0.25 equations')
G = strip(Rg(Gx.numerator()), 'G'); H1 = strip(Rg(E146.numerator()), 'E146 -> H1'); Dn = strip(Rg(Dd.numerator()), 'Dd -> D')
# compare with #103's system (audit stage4, case K), up to constants
Uo, To, So = Rg.gens()
old = {}
for line in open(D('inputs', 'stage4-K-system.txt')):
    k, e = line.split(' = ', 1); old[k] = Rg(e.strip().replace('^', '**'))
def same(a, b):                                         # b = a * (constant * NZ factors)
    q, r = b.quo_rem(a)
    return r == 0 and all(f.degree() == 0 or (f / f.lc()) in NZ for f, m in q.factor())
match = {k: same(x, old[k]) for k, x in (('G', G), ('H1', H1), ('D', Dn))}
say('matches #103 system (equal up to constants and NZ factors):', match)
open(D('data', 'system-K.txt'), 'w').write(f'G = {G}\nH1 = {H1}\nD = {Dn}\n')
# ---------------- full elimination ----------------
print('PROGRESS 0.35 resultants in S')
uu, tt, SS = Rg.gens()
R1 = G.resultant(H1, SS); say('R1 = Res_S(G, H1): degrees (u, t)', R1.degree(uu), R1.degree(tt))
R2 = G.resultant(Dn, SS); say('R2 = Res_S(G, D): degrees (u, t)', R2.degree(uu), R2.degree(tt))
assert R1 != 0 and R2 != 0
def dump(pol, fn, label):
    fl = pol.factor(); rows = []
    with open(D('data', fn), 'w') as fh:
        for f, m in fl:
            nz = f.degree() > 0 and (f / f.lc()) in NZ
            fh.write(f'{m} {"NZ" if nz else "KEEP"} {f}\n'); rows.append((f, m, nz))
            say(f'   {label} factor degrees (u, t) = ({f.degree(uu)}, {f.degree(tt)})^{m}', 'NZ' if nz else 'KEEP',
                str(f) if len(str(f)) < 50 else '')
    return rows
r1 = dump(R1, 'R1-factors.txt', 'R1'); r2 = dump(R2, 'R2-factors.txt', 'R2')
# u-only factors that are not NZ: their roots are candidate u values directly (none expected; any is kept as a candidate factor)
Akeep = [f for f, m, nz in r1 if not nz and f.degree() > 0]; Bkeep = [f for f, m, nz in r2 if not nz and f.degree() > 0]
say('kept factors of R1:', [(f.degree(uu), f.degree(tt)) for f in Akeep], ' of R2:', [(f.degree(uu), f.degree(tt)) for f in Bkeep])
print('PROGRESS 0.5 resultants in t')
import cypari2
pari = cypari2.Pari(); pari.allocatemem(8 * 10**9)
cands = []                                              # univariate factors in u (PARI objects) with their origin
f348 = pari(open(D('inputs', 'kulaichev-minpoly-u.txt')).read().strip().replace('x', 'u'))
with open(D('data', 'E-factors.txt'), 'w') as fh:
    for i, a in enumerate(Akeep):
        for j, b in enumerate(Bkeep):
            if a.degree(tt) == 0 or b.degree(tt) == 0:
                for f in (a, b):
                    if f.degree(tt) == 0: cands.append((pari(str(f)), f'u-only factor of R{1 if f is a else 2}'))
                continue
            g = a.gcd(b)
            assert g.degree() == 0, 'common factor of A and B: a curve of common zeros (would need separate treatment)'
            E = pari.polresultant(pari(str(a).replace('t', 'z')), pari(str(b).replace('t', 'z')), 'z')
            assert E != 0, 'Res_t identically zero'
            say(f'E{i}{j} = Res_t: degree {pari.poldegree(E, "u")}')
            Fz = pari.factor(E)
            for k in range(len(Fz[0])):
                f = Fz[0][k]; m = int(Fz[1][k]); deg = int(pari.poldegree(f, 'u'))
                fs = Rg(str(f)); nz = (fs / fs.lc()) in NZ
                fh.write(f'pair ({i},{j}) {m} {"NZ" if nz else "KEEP"} {f}\n')
                say(f'   factor degree {deg} ^{m}', 'NZ' if nz else 'KEEP', str(f) if deg <= 2 else '')
                if not nz: cands.append((f, f'Res_t(A{i}, B{j})'))
same348 = [pari.poldegree(f, 'u') == 348 and pari.pollead(f348, 'u') * f == pari.pollead(f, 'u') * f348 for f, _ in cands]
with open(D('data', 'candidates.txt'), 'w') as fh:
    for (f, org), s in zip(cands, same348):
        fh.write(f'# degree {pari.poldegree(f, "u")} from {org}{" = f348 (Theorem 10)" if s else ""}\n{f}\n')
say('candidate factors:', [(int(pari.poldegree(f, 'u')), org) for f, org in cands], '; f348 among them:', any(same348))
# machine-readable polynomials for the census (integer coefficients; exponents in the order u, t, S)
import json
def zdict(F):
    F = Rg(F); den = 1
    for e, c in F.dict().items(): den = den.lcm(c.denominator()) if hasattr(den, 'lcm') else ZZ(den).lcm(c.denominator())
    return [[list(map(int, e)), str(ZZ(c * den))] for e, c in F.dict().items()]
polys = {'G': zdict(G), 'H1': zdict(H1), 'D': zdict(Dn), 'A': zdict(Akeep[0]), 'B': zdict(Bkeep[0]),
         'candidates': [{'origin': org, 'is_f348': bool(s), 'coeffs': [str(c) for c in pari.Vecrev(f * pari.denominator(pari.content(f)))]}
                        for (f, org), s in zip(cands, same348)]}
assert len(Akeep) == 1 and len(Bkeep) == 1
json.dump(polys, open(D('data', 'polys-K.json'), 'w'))
say('wrote data/polys-K.json')
ok = lemma_ok and all(match.values()) and any(same348)
print('PROGRESS 1.0 done')
print('FINAL ok' if ok else f'FINAL FAIL: lemma {lemma_ok}, match {match}, f348 found {any(same348)}')
