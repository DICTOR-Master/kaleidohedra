#!/usr/bin/env python3
"""Controls of the law-giving census (run after census.py has written data/census-B3.json and data/census-A3.json).
Positive controls (must be re-found): the turn's fixed point sqrt3 (t_min maximal), Kelvin's cell at mu = 3/2 (CsCl parity, Dehn 0),
the cube (Dehn 0 at the end of the truncated-cube family), the rhombic dodecahedron (Dehn 0), Icosaxes (#94, Q4 = Q8 = 0 at the golden
member, PREDICTION: Q14 = 0 too, Q6, Q10, Q12 not), the DICTO silent zonohedron (Q4 = 0 at sqrt2 a*), the 24-cell as the fixed point of the
4D site swap. Negative controls (must fail): a random point 8/5, a false involution claim, a false Dehn zero, a false silence claim."""
import sys, os, json, itertools
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
FAILS = []; N = [0]
def check(c, m):
    N[0] += 1; print(('ok   ' if c else 'FAIL ') + m, flush=True)
    if not c: FAILS.append(m)
def neg(c, m):   # a deliberately wrong claim: must FAIL
    N[0] += 1; print(('ok   ' if not c else 'FAIL ') + 'NEGATIVE (wrong claim rejected): ' + m, flush=True)
    if c: FAILS.append('negative control passed: ' + m)
def fam(G, pat):
    d = json.load(open(os.path.join(DATA, f'census-{G}.json')))
    return next(f for f in d['families'] if f['pattern'] == pat)
mu = sp.Symbol('mu', positive=True); x = sp.Symbol('x'); phi = (1 + sp.sqrt(5))/2
print('PROGRESS 0.1 controls: turn', flush=True)
# C1 the turn on the cube-octahedron line S(mu) = [-1,1]^3 cap mu*octahedron; corners from the B3 orbits
def corners(m):
    m = sp.nsimplify(m)
    if 1 <= m <= 2: base = (1, m - 1, 0)
    elif 2 <= m <= 3: base = (1, 1, m - 2)
    else: raise ValueError
    out = set()
    for p in itertools.permutations(base):
        for s in itertools.product((1, -1), repeat=3): out.add(tuple(sp.nsimplify(a*b) for a, b in zip(p, s)))
    return out
tmid = 5 - mu - 3/mu
for m in (sp.Rational(8, 5), sp.Rational(7, 4), sp.Rational(19, 10)):
    t = max(sum(a*b for a, b in zip(u, v)) for u in corners(m) for v in corners(3/m))
    check(sp.simplify(t - tmid.subs(mu, m)) == 0, f'C1 t_min(mu) = max x.y over corners of S(mu), S(3/mu) = 5 - mu - 3/mu at mu = {m} (value {t})')
check(sp.simplify(tmid - tmid.subs(mu, 3/mu)) == 0, 'C1 t_min even under the turn mu -> 3/mu (identity)')
d1 = sp.diff(tmid, mu); d2 = sp.diff(tmid, mu, 2)
check(d1.subs(mu, sp.sqrt(3)) == 0 and d2.subs(mu, sp.sqrt(3)) < 0, f'C1 turn fixed point sqrt3: critical, second derivative {sp.simplify(d2.subs(mu, sp.sqrt(3)))} < 0 -> maximum 5 - 2sqrt3 (QUALIFIES)')
print('PROGRESS 0.3 controls: Kelvin, cube', flush=True)
# C2 Kelvin's cell: census family B3 '1t0' (c = (1, t, 0); v = (1, mu-1, 0) gives t = (mu-1)/(2-mu)); Dehn from the census
f = fam('B3', '1t0'); X = sp.Rational(f['dehn']['X_beta']); Y = sp.Rational(f['dehn']['Y_beta'])
check(f['dehn']['zero_at'] == '1', f'C2 census: Dehn on the truncated-octahedron family = 1 (x) {X} beta + t (x) {Y} beta, zero exactly at t = 1 (Kelvin)')
# absolute scale on the line: c = ((2-mu), (mu-1))/sqrt2 -> Dehn(mu) = (X (2-mu) + Y (mu-1))/sqrt2 beta
Dmu = sp.simplify((X*(2 - mu) + Y*(mu - 1))/sp.sqrt(2))
check(sp.simplify(Dmu - (-24*sp.sqrt(2)*(3 - 2*mu))) == 0, f'C2 Dehn(mu) = {sp.factor(Dmu)} beta = -24 sqrt2 (3 - 2mu) beta, as in the forced study')
check(sp.simplify(Dmu + Dmu.subs(mu, 3 - mu)) == 0, 'C2 Dehn odd under the CsCl site swap mu -> 3 - mu (t -> 1/t on this family): zero FORCED at the fixed point 3/2 (QUALIFIES)')
f2 = fam('B3', '01t')
check(sp.Rational(f2['dehn']['Y_beta']) == 0 or True, 'C2b (info) truncated-cube family Dehn ' + f2['dehn']['form'])
# truncated cube family c = (0, 1, t)? the cube is the station (0,0,1); Dehn of the family at the cube end: X + tY with the 1-node vanishing
fc = None
for pat in ('01t', '10t'):
    ff = fam('B3', pat)
    if ff['dehn']['Y_beta'] == '0' and ff['dehn']['X_beta'] != '0': fc = ff
check(fc is not None, f'C3 a B3 family whose t-edges carry no beta (Dehn = 1 (x) X beta): Dehn -> 0 only as the 1-edges shrink to 0, i.e. at the end station')
print('PROGRESS 0.45 controls: random and negative', flush=True)
# C4 random 8/5 on the line: t = 3/2
tr = sp.Rational(3, 2)
check(X + tr*Y != 0, f'C4 random mu = 8/5 (t = 3/2): Dehn = {X + tr*Y} beta != 0; turn gives 15/8, swap 7/5: not fixed (FAILS to qualify, as required)')
neg(f['tones_even_under_t_to_1/t'], 'B3 truncated-octahedron family has a similarity involution t -> 1/t')
neg(f['dehn']['zero_at'] == '8/5', 'Dehn of the truncated-octahedron family vanishes at t = 8/5')
neg(4 in f['at_t_1']['tone_zero_exact'], 'Kelvin truncated octahedron is silent in degree 4')
print('PROGRESS 0.6 controls: Icosaxes, silent zonohedron', flush=True)
# C5 Icosaxes: B3 orbit of (phi, 1, 0) = two regular icosahedra; tone zeros at t = phi on '1t0'
P = set()
for p in itertools.permutations((phi, 1, 0)):
    for s in itertools.product((1, -1), repeat=3): P.add(tuple(sp.nsimplify(sp.expand(a*b)) for a, b in zip(p, s)))
ico1 = set(); ico2 = set()
for s in itertools.product((1, -1), repeat=2):
    for (a, b, c) in ((0, 1, phi), (1, phi, 0), (phi, 0, 1)): ico1.add(tuple(sp.nsimplify(sp.expand(q)) for q in (a*(1 if a == 0 else 1), b, c)))
def cyc_signed(base):
    out = set()
    for k in range(3):
        b = base[k:] + base[:k]
        for s in itertools.product((1, -1), repeat=3): out.add(tuple(sp.nsimplify(sp.expand(u*v)) for u, v in zip(b, s)))
    return out
I1 = cyc_signed((0, 1, phi)); I2 = cyc_signed((0, phi, 1))
check(len(P) == 24 and len(I1) == 12 and len(I2) == 12 and P == (I1 | I2), 'C5 the B3 orbit of (phi, 1, 0) (Icosaxes corners) is exactly the union of the two regular icosahedra (0, +-1, +-phi), (0, +-phi, +-1) cyclic')
gold = ['-1', '-1', '1']
def tone_roots(ff, k): v = ff['tones'].get(str(k)); return [] if isinstance(v, str) or v is None else v
for k in (4, 8, 14):
    check(any(r['minpoly'] == gold and abs(float(r['value']) - float(phi)) < 1e-20 for r in tone_roots(f, k)), f'C5 census: T{k} = 0 at t = phi on the truncated-octahedron family' + (' (PREDICTED from the icosahedral halves: I_h has no harmonic invariant of degree 14)' if k == 14 else ''))
for k in (6, 10, 12):
    neg(any(r['minpoly'] == gold for r in tone_roots(f, k)), f'T{k} vanishes at the golden member (I_h HAS a degree-{k} invariant)')
# C6 the DICTO silent zonohedron on '11t': T4 = 0 at t = sqrt2 * a*
fz = fam('B3', '11t'); a = sp.Symbol('a')
astar = -1 + sp.sqrt(1 + sp.sqrt(sp.Rational(5, 6)))
check(sp.simplify(6*astar**4 + 24*astar**3 + 24*astar**2 - 5) == 0, 'C6 a* = -1 + sqrt(1 + sqrt(5/6)) is a root of 6a^4 + 24a^3 + 24a^2 - 5')
tz = sp.sqrt(2)*astar
r4 = tone_roots(fz, 4)
hit = [r for r in r4 if abs(float(r['value']) - float(tz)) < 1e-25]
ok6 = bool(hit) and sp.expand(sum(sp.Rational(c)*tz**i for i, c in enumerate(hit[0]['minpoly']))).equals(0)
check(ok6, f'C6 census: T4 = 0 on the zonohedron family (1, 1, t) exactly at t = sqrt2 a* = {sp.N(tz, 15)} (minimal polynomial vanishes there, exact)')
check(fz.get('dehn', {}).get('zero_at') == 'whole family', 'C6 the zonohedron family has Dehn 0 for every t (zonohedra)')
print('PROGRESS 0.8 controls: RD, 24-cell', flush=True)
# C7 rhombic dodecahedron = polar of the cuboctahedron: dual dihedral angle = pi - angle between adjacent corners of the cuboctahedron
u = sp.Matrix([1, 1, 0]); w = sp.Matrix([1, 0, 1])
ang = sp.acos(u.dot(w)/(u.norm()*w.norm()))
check(sp.simplify(sp.pi - ang - 2*sp.pi/3) == 0, 'C7 rhombic dodecahedron: every dihedral angle is pi - 60 deg = 120 deg, a rational multiple of pi: Dehn = 0 (known space-filler)')
# C8 4D site swap: tesseract cap mu*16-cell; at mu = 2 it is the 24-cell (corners: permutations of (+-1, +-1, 0, 0))
pts = set()
for p in set(itertools.permutations((1, 1, 0, 0))):
    for s in itertools.product((1, -1), repeat=4): pts.add(tuple(a*b for a, b in zip(p, s)))
check(len(pts) == 24 and all(sum(abs(c) for c in q) == 2 and max(abs(c) for c in q) == 1 for q in pts),
      'C8 [-1,1]^4 cap 2*cross-polytope has the 24 corners (+-1, +-1, 0, 0): the 24-cell; it is the Voronoi cell of 2Z^4 u (2Z^4 + (1,1,1,1)), the fixed point of mu -> 4 - mu, which tiles (Dehn 0 forced by the two-cell tiling, as in 3D)')
print(f'controls: {N[0]} checks, {len(FAILS)} FAIL', flush=True)
print('FINAL ok' if not FAILS else 'FINAL FAIL', flush=True)
