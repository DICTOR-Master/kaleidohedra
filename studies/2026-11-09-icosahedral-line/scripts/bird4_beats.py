# bird4_beats.py -- DICTO Hopscotch, icosahedral line, bird 4 (study 2026-11-09-icosahedral-line).
# #43 Theorem 3 (reciprocation about rho^2 = 15 - 5 sqrt5 maps beat k of Universal PiTet to beat 5 - k) as the turn of the beat line.
# Exact Q(sqrt5). Stations: S0 = ID (circumradius phi, edge 1; the 30 edge midpoints of the icosahedron (0, +-1, +-phi)),
# S_{k+1} = T(S_k) = {x : v.x <= v.v for every corner v of S_k}.
# Checks: (0) known: S4 = c S0, c = 10/phi^4 = 35 - 15 sqrt5; P(T(S)) = S at every station (P = T^-1 on the line);
# (1) Lemma 3 on the stations: polar(P(S)) = T(polar(S)); (2) the framework step: if every corner of S lies on the sphere of
# radius^2 rho^2, then polar_rho(S) = T(S) (the two half-space lists coincide) -- the ID on phi^2, the GTI on c phi^2 = 15 - 5 sqrt5;
# (3) Theorem 3 itself, polar(S_k) = S_{5-k} for k = 0..5; (4) the shell ratios t_k = min{t : S_k in t S_{k-1}} and their turn
# symmetry t_k = t_{6-k} (indices mod 4), the prediction "the turn maximises t" read on the fixed shells.
import sys, time
from fractions import Fraction as Fr
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from q5 import *
t0 = time.time(); checks = {}
def key(v): return tuple((x.a, x.b) for x in v)
def cset(C): return frozenset(key(x) for x in C)
mids = set()
for i, a in enumerate(AX5):
    for b in AX5[i + 1:]:
        d = sub(a, b)
        if dot(d, d) == Q5(4): mids.add(scl(Q5(Fr(1, 2)), add(a, b)))
ID = sorted(mids, key=lambda v: tuple(x.f() for x in v))
checks['ID: 30 corners, circumradius phi, edge 1'] = len(ID) == 30 and all(dot(v, v) == PHI * PHI for v in ID) and \
    min(dot(sub(u, v), sub(u, v)).f() for u in ID for v in ID if u != v) == 1.0
def T(C):
    pl = [(v, dot(v, v)) for v in C]
    out = corners(pl)
    facet_all = all(any(i in act for _, act in out) for i in range(len(pl)))      # every plane carries a corner
    return [x for x, _ in out], pl, facet_all
def planes_of(C):
    # facet planes of hull(C): via the polar about the unit sphere (corners of {x: v.x <= 1}) -- each corner y of the polar is a facet y.x <= 1
    Y = [y for y, _ in corners([(v, ONE) for v in C])]
    return [(y, ONE) for y in Y]
def P(C):
    return [scl(d / dot(n, n), n) for n, d in planes_of(C)]
def polar(C, rho2):
    return [x for x, _ in corners([(v, rho2) for v in C])]
S = [ID]
for k in range(1, 6):
    C, pl, fa = T(S[-1]); S.append(C)
    checks[f'T step {k}: every plane v.x <= v.v is a facet (every corner survives)'] = fa
names = ['ID', 'RT', 'GTI', 'FPD', 'c ID', 'c RT']
print('corners per beat:', [len(C) for C in S])
c = Q5(35, -15)
checks['c = 10/phi^4 = 35 - 15 sqrt5'] = Q5(10) / (PHI ** 1 * PHI * PHI * PHI) == c if False else Q5(10) / (PHI * PHI * PHI * PHI) == c
checks['S4 = c S0 and S5 = c S1 (one turn of four beats = the hop by c)'] = cset(S[4]) == cset([scl(c, v) for v in S[0]]) and cset(S[5]) == cset([scl(c, v) for v in S[1]])
checks['P(T(S)) = S at S0..S3 (P = T^-1 on the line)'] = all(cset(P(S[k + 1])) == cset(S[k]) for k in range(4))
for rho2, nm in ((PHI * PHI, 'phi^2'), (Q5(15, -5), '15 - 5 sqrt5'), (ONE, '1')):
    checks[f'Lemma 3 at radius^2 {nm}: polar(P(S_k)) = T(polar(S_k)), k = 1..3'] = all(cset(polar(P(S[k]), rho2)) == cset(T(polar(S[k], rho2))[0]) for k in range(1, 4))
rad = [sorted(set(dot(v, v) for v in C), key=lambda q: q.f()) for C in S[:4]]
print('corner radii^2 per station:', [[r.f() for r in R] for R in rad])
checks['ID corners on one sphere, radius^2 phi^2; GTI corners on one sphere, radius^2 15 - 5 sqrt5 = c phi^2'] = rad[0] == [PHI * PHI] and rad[2] == [Q5(15, -5)] and Q5(15, -5) == c * PHI * PHI
checks['RT and FPD corners are NOT on one sphere (only the inscribed stations fix the turn)'] = len(rad[1]) > 1 and len(rad[3]) > 1
# framework step: corners on the sphere rho => polar_rho(S) = T(S)
checks['polar_{phi^2}(ID) = T(ID) = RT and polar_{c phi^2}(GTI) = T(GTI) = FPD'] = cset(polar(S[0], PHI * PHI)) == cset(S[1]) and cset(polar(S[2], Q5(15, -5))) == cset(S[3])
# Theorem 3
rho2 = Q5(15, -5)
pol_ok = True
for k in range(6):
    j = 5 - k
    tgt = S[j] if 0 <= j <= 5 else None
    pol_ok &= tgt is not None and cset(polar(S[k], rho2)) == cset(tgt)
checks['#43 Theorem 3: polar_rho(S_k) = S_{5-k}, k = 0..5, rho^2 = 15 - 5 sqrt5'] = pol_ok
checks['the companion turn about phi^2: polar(S_k) = S_{1-k} up to the hop (polar_{phi^2}(S_1) = S_0, polar_{phi^2}(S_2) = S_3/c)'] = \
    cset(polar(S[1], PHI * PHI)) == cset(S[0]) and cset(polar(S[2], PHI * PHI)) == cset([scl(ONE / c, v) for v in S[3]])
# shell ratios
def ratio(Cin, Cout):     # min t with hull(Cin) inside t * hull(Cout)
    pl = planes_of(Cout); best = None
    for v in Cin:
        for n, d in pl:
            q = dot(n, v) / d
            if best is None or q > best: best = q
    return best
tk = {k: ratio(S[k], S[k - 1]) for k in range(1, 6)}
for k in tk: print(f'shell {k - 1}->{k} ({names[k - 1]} -> {names[k]}): t = {tk[k]} = {tk[k].f():.9f}')
checks['shell ratios periodic: t_5 = t_1'] = tk[5] == tk[1]
checks['turn symmetry of the shells: t_k = t_{6-k} mod 4 (t_2 = t_4; t_1, t_3 on the fixed shells)'] = tk[2] == tk[4]
mx = max(tk.values(), key=lambda q: q.f())
print('largest shell ratio', mx.f(), 'on shells', [k for k in tk if tk[k] == mx])
fixed_max = (tk[1] >= tk[2] and tk[3] >= tk[2])
print('prediction "the turn maximises t": the fixed shells are ID->RT (k = 1) and GTI->FPD (k = 3); both >= the moving shells:', fixed_max)
checks['shell ratio test recorded (verdict printed above)'] = True
for k, v in checks.items(): print(('  ok   ' if v else '  FAIL ') + k)
print(f'time {time.time() - t0:.0f} s')
print('FINAL ok' if all(checks.values()) else 'FINAL FAIL: ' + ', '.join(k for k, v in checks.items() if not v))
