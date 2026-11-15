"""Step 1: the polynomial system of the DICTO Yantra (#103 Theorem 9), rebuilt from the geometry, with every divisor accounted for,
and the FULL elimination over Q(sqrt5) (no factor chosen by a numerical point).

Problem (#103 Theorem 1 conditions + Theorem 9's fourth condition; frame of model.py): circle of diameter 1, axis vertical, depth d
below the top point O; nine isosceles triangles t1..t9 (t1..t5 point down, t6..t9 up), base depth b_i, half-width w_i, apex depth a_i.
Huet's conditions in Chiodo's form (2021, (i)-(iii)): t3, t7 inscribed; seven apex-on-base points; nine marma pairs and three corner
touches (model.py lists).  Kulaichev's (b) t1's corners on the circle, (c) t9's corners on the circle, (d) the incircle of the innermost
triangle (t1's legs and t5's base) centred at the circle's centre.  In place of Kulaichev's (a) (equal great triangles, u = v): the
Cleo-Antonius condition u v = 2/phi^3 = 2 sqrt5 - 4 (#103 sec. 9.1).  Admissible (#103 Theorem 1): b1 < ... < b9, every w_i > 0,
apexes on the correct side, corners in the closed disc.

Coordinates: u = w7/b7 (b7 = R = 1/(1+u^2)), v = w3/(1-b3) (b3 = P = v^2/(1+v^2)), t = b1/w1 (t1's corner = (t, t^2)/(1+t^2)), S = b9.
The construction is the one of the Kulaichev census (studies/2026-11-15-yantra-uniqueness, s1_system.py) with v kept free: each further
quantity is the meeting point of two lines, so every admissible yantra satisfies G = 0 ((c)), E146 = 0 (marma (1,4,6)), Dd = 0 ((d)
squared), with every divisor nonzero (divisor lemma, done here over Q in (u, v, t, S), i.e. for every pair of great slopes).
Then v = c/u, c = 2 sqrt5 - 4, is substituted (u > 0, so u^k may be cleared); the numerators are factored over K = Q(sqrt5), and a
K-factor is dropped only if it divides the substitution of a lemma factor (then it is nonzero wherever that factor is).
Elimination over K: R1 = Res_S(G, H1), R2 = Res_S(G, D) (Singular over K), A, B = their kept factors, E = Res_t(A, B) (PARI, coefficients
in Q[s]/(s^2 - 5)), factored over K (nffactor); the kept K-factors' norms N(g) = g * conj(g) in Q[u] are factored over Q: these rational
factors are the candidate polynomials (every admissible u is a real root of one of them; the norm can only add roots).
FINAL ok iff the system matches #103's (audit stage 4, case D) up to constants and NZ factors, the lemma closes, E != 0, A and B have no
common factor, and f160 (Theorem 9) is one of the candidate factors."""
import sys, time, os, json
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
D = lambda *p: os.path.join(ROOT, *p)
from sage.all__sagemath_singular import QQ, ZZ, PolynomialRing
from sage.rings.number_field.number_field import QuadraticField
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
# ---------------- substitution v = c/u over K = Q(sqrt5) ----------------
print('PROGRESS 0.20 substitution v = (2 sqrt5 - 4)/u')
K = QuadraticField(5, 's'); s = K.gen(); c = 2 * s - 4
RK = PolynomialRing(K, 'u,t,S'); FK = RK.fraction_field(); U, T, SS = RK.gens()
phi = Rg.hom([FK(U), FK(c) / FK(U), FK(T), FK(SS)], FK)
NZK = {}
def addnzk(pol, why):
    pol = RK(pol)
    if pol.degree() <= 0: return                        # a nonzero constant after substitution (e.g. u v - 1 -> c - 1)
    for f, m in pol.factor():
        f = RK(f)
        if f.degree() > 0: NZK.setdefault(f / f.lc(), why)
addnzk(U, 'u > 0')
for f, why in NZ.items(): addnzk(phi(f).numerator(), f'divides the substitution of lemma factor {str(f)[:60]} ({why})')
say('NZ factors over K after substitution:', len(NZK))
with open(D('data', 'nz-factors.txt'), 'w') as fh:
    for f, why in NZ.items(): fh.write(f'Q {f}    # {why}\n')
    for f, why in NZK.items(): fh.write(f'K {f}    # {why}\n')
def isnz(f): f = RK(f); return f.degree() > 0 and (f / f.lc()) in NZK
def strip(pol, label):
    keep = RK(1); dropped = []
    for f, m in pol.factor():
        if f.degree() == 0: continue
        if isnz(f): dropped.append((f, m))
        else: keep *= f**m
    say(f'{label}: kept degrees (u, t, S) = {(keep.degree(U), keep.degree(T), keep.degree(SS))}; dropped NZ factors:',
        [(str(f) if len(str(f)) < 40 else f'<deg {f.degree()}>', m) for f, m in dropped])
    return keep
print('PROGRESS 0.25 equations over K')
def sub(X): return RK(phi(Rg(X.numerator())).numerator())
G = strip(sub(Gx), 'G'); H1 = strip(sub(E146), 'E146 -> H1'); Dn = strip(sub(Dd), 'Dd -> D')
# compare with #103's system (audit stage 4, case D; w there is sqrt5)
old = {}
for line in open(D('inputs', 'stage4-D-system.txt')):
    k_, e = line.split(' = ', 1); old[k_] = RK(eval(e.strip().replace('^', '**'), {'w': s, 'u': U, 't': T, 'S': SS}))
def same(a, b):                                         # b = a * (constant * NZ factors) or a = b * (...)
    for x, y in ((a, b), (b, a)):
        q, r = y.quo_rem(x)
        if r == 0 and all(f.degree() == 0 or isnz(f) for f, m in q.factor()): return True
    return False
match = {k_: same(x, old[k_]) for k_, x in (('G', G), ('H1', H1), ('D', Dn))}
say('matches #103 system (audit stage 4, case D), up to constants and NZ factors:', match)
open(D('data', 'system-D.txt'), 'w').write(f'# over K = Q(s), s^2 = 5\nG = {G}\nH1 = {H1}\nD = {Dn}\n')
# ---------------- full elimination over K ----------------
print('PROGRESS 0.30 resultants in S (Singular over K)')
t1 = time.time(); R1 = G.resultant(H1, SS); say(f'R1 = Res_S(G, H1): degrees (u, t) {R1.degree(U)}, {R1.degree(T)} ({time.time() - t1:.1f} s)')
t1 = time.time(); R2 = G.resultant(Dn, SS); say(f'R2 = Res_S(G, D): degrees (u, t) {R2.degree(U)}, {R2.degree(T)} ({time.time() - t1:.1f} s)')
assert R1 != 0 and R2 != 0
print('PROGRESS 0.40 factor R1, R2 over K')
def dump(pol, fn, label):
    t1 = time.time(); fl = pol.factor(); rows = []
    with open(D('data', fn), 'w') as fh:
        for f, m in fl:
            if f.degree() == 0: continue
            nz = isnz(f); fh.write(f'{m} {"NZ" if nz else "KEEP"} {f}\n'); rows.append((f, m, nz))
            say(f'   {label} factor degrees (u, t) = ({f.degree(U)}, {f.degree(T)})^{m}', 'NZ' if nz else 'KEEP', str(f) if len(str(f)) < 60 else '')
    say(f'   ({label} factored in {time.time() - t1:.1f} s)')
    return rows
r1 = dump(R1, 'R1-factors.txt', 'R1'); r2 = dump(R2, 'R2-factors.txt', 'R2')
Akeep = [f for f, m, nz in r1 if not nz]; Bkeep = [f for f, m, nz in r2 if not nz]
say('kept factors of R1:', [(f.degree(U), f.degree(T)) for f in Akeep], ' of R2:', [(f.degree(U), f.degree(T)) for f in Bkeep])
print('PROGRESS 0.50 resultants in t (PARI over Q[s]/(s^2-5))')
import cypari2
pari = cypari2.Pari(); pari.allocatemem(int(os.environ.get('PARIMEM', 8 * 10**9)))
pari('[u, z, s]')                                       # variable priority u > z > s (s lowest, for polmods)
MS = pari('Mod(s, s^2 - 5)')
def toP(f, tvar='z'):                                   # K[u,t,S] -> PARI with Mod(s, s^2-5) coefficients
    return pari.subst(pari(str(f).replace('t', tvar)), 's', MS)
nf = pari.nfinit(pari('s^2 - 5'))
cands = []; Kfactors = []
with open(D('data', 'E-factors.txt'), 'w') as fh:
    univ = [(f, 'R1') for f in Akeep if f.degree(T) == 0] + [(f, 'R2') for f in Bkeep if f.degree(T) == 0]
    pairs = [(i, j) for i, a in enumerate(Akeep) for j, b in enumerate(Bkeep) if a.degree(T) > 0 and b.degree(T) > 0]
    polsE = [(toP(f), f'u-only factor of {org}') for f, org in univ]
    for i, j in pairs:
        a, b = Akeep[i], Bkeep[j]
        g = a.gcd(b); assert g.degree() == 0, 'common factor of A and B: a curve of common zeros (needs separate treatment)'
        t1 = time.time(); E = pari.polresultant(toP(a), toP(b), 'z'); assert E != 0, 'Res_t identically zero'
        say(f'E{i}{j} = Res_t(A{i}, B{j}) over K: degree {int(pari.poldegree(E, "u"))} ({time.time() - t1:.1f} s)')
        polsE.append((E, f'Res_t(A{i}, B{j})'))
    for E, org in polsE:
        t1 = time.time(); Fz = pari.nffactor(nf, pari.liftall(E)); say(f'   nffactor over K: {time.time() - t1:.1f} s')
        for k in range(len(Fz[0])):
            g = Fz[0][k]; m = int(Fz[1][k]); deg = int(pari.poldegree(g, 'u'))
            gs = RK(str(pari.liftall(g))); nz = isnz(gs)
            fh.write(f'{org} K-factor {m} {"NZ" if nz else "KEEP"} {pari.liftall(g)}\n')
            say(f'   K-factor degree {deg} ^{m}', 'NZ' if nz else 'KEEP', str(pari.liftall(g)) if deg <= 2 else '')
            if nz: continue
            Kfactors.append((g, org))
            Ng = pari.polresultant(pari.liftall(g), pari('s^2 - 5'), 's')          # norm to Q[u]
            Fq = pari.factor(Ng)
            for kk in range(len(Fq[0])):
                q = Fq[0][kk]
                if pari.poldegree(q, 'u') == 0: continue
                if not any(q == q2 or q == -q2 for q2, _ in cands):
                    cands.append((q, f'norm of a degree-{deg} K-factor of {org}'))
                    fh.write(f'   rational factor of its norm: degree {int(pari.poldegree(q, "u"))}\n')
f160 = pari(open(D('inputs', 'f160-u.txt')).read().strip())
def is160(q): return pari.poldegree(q, 'u') == 160 and pari.pollead(f160, 'u') * q == pari.pollead(q, 'u') * f160
same160 = [bool(is160(q)) for q, _ in cands]
with open(D('data', 'candidates.txt'), 'w') as fh:
    for (q, org), sm in zip(cands, same160): fh.write(f'# degree {pari.poldegree(q, "u")} from {org}{" = f160 (Theorem 9)" if sm else ""}\n{q}\n')
say('candidate rational factors:', [(int(pari.poldegree(q, 'u')), org) for q, org in cands], '; f160 among them:', any(same160))
# machine-readable polynomials over K: each coefficient a + b s stored as two integers (one common denominator per polynomial)
def kdict(F):
    F = RK(F); items = []; den = ZZ(1)
    for e, cf in F.dict().items():
        a, b = cf.vector() if hasattr(cf, 'vector') else (cf, 0)
        den = den.lcm(QQ(a).denominator()).lcm(QQ(b).denominator())
    for e, cf in F.dict().items():
        a, b = cf.vector()
        items.append([list(map(int, e)), [str(ZZ(QQ(a) * den)), str(ZZ(QQ(b) * den))]])
    return items
assert len(Akeep) == 1 and len(Bkeep) == 1, 'more than one kept factor: extend the census to every pair'
polys = {'field': 'Q(s), s^2 = 5; coefficient [a, b] = a + b s; exponents (u, t, S)',
         'G': kdict(G), 'H1': kdict(H1), 'D': kdict(Dn), 'A': kdict(Akeep[0]), 'B': kdict(Bkeep[0]),
         'candidates': [{'origin': org, 'is_f160': sm, 'coeffs': [str(x) for x in pari.Vecrev(q * pari.denominator(pari.content(q)))]}
                        for (q, org), sm in zip(cands, same160)]}
json.dump(polys, open(D('data', 'polys-D.json'), 'w'))
say('wrote data/polys-D.json')
ok = lemma_ok and all(match.values()) and any(same160)
print('PROGRESS 1.0 done')
print('FINAL ok' if ok else f'FINAL FAIL: lemma {lemma_ok}, match {match}, f160 found {any(same160)}')
