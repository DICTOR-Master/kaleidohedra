"""Coordinator follow-up (splash-determinants study): three event types on the two second dual sweeps.
(c) Dehn invariant on every hop of CO ∩ mu RD (prediction: a linear factor with root exactly 5/3) and of ID ∩ mu RT;
(b) golden cuts as METRIC factors: the octagon-hop side lengths as linear forms, #89's two conditions (equal corner sides, golden
    ratio) as two metric factors, golden one-factor stations; cross-check of the C-O golden cuts with splash data/sweep-events.json.
Reuse: CO-RD planes and exact corner enumeration from splash-determinants/scripts/corrd_events.py (exec of its definitions only).
Dihedral angles reduced modulo pi*Q by PSLQ (mpmath, 60 digits, coefficients <= 1000), each relation then checked to 1e-50."""
import sys, os, itertools, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp, mpmath as mpm
import sweeplib as L
from sweeplib import F, Q, ZERO, ONE, dot
mpm.mp.dps = 60
HERE = os.path.dirname(os.path.abspath(__file__))
logf = open(os.path.join(HERE, '..', 'data', 's4_metric_events.log'), 'w')
def log(s): print(s); logf.write(s + '\n'); logf.flush()
checks = []
mu = sp.symbols('mu', positive=True)
SPL = os.path.join(HERE, '..', 'data', 'input-splash')  # copies of splash-determinants scripts/corrd_events.py and data/sweep-events.json

def hop_edges(sw, m1, m2):
    """edges on a hop: list of (bond families, facet pair, length(mu) sympy linear*sqrt, normals)."""
    s1, s2 = sw.structure(m1), sw.structure(m2)
    def emap(st):
        out = {}
        for i, j in st['edges']:
            com = tuple(sorted(st['V'][i][1] & st['V'][j][1] & st['facets']))
            assert len(com) == 2
            e = [a - b for a, b in zip(st['V'][i][0], st['V'][j][0])]
            out[com] = e
        return out
    E1, E2 = emap(s1), emap(s2)
    assert set(E1) == set(E2)
    res = []
    for com, e1 in E1.items():
        e2 = E2[com]
        k = next(t for t in range(3) if e1[t] != ZERO)
        lam = e2[k] / e1[k]
        if not all(e2[t] == lam * e1[t] for t in range(3)):   # endpoints may be swapped
            lam = -e2[k] / e1[k]; assert all(-e2[t] == lam * e1[t] for t in range(3))
        n2 = dot(e1, e1)
        a, b = m1.sym(), m2.sym()
        s = 1 + (lam.sym() - 1) * (mu - a) / (b - a)
        res.append((tuple(sorted(sw.P[c][3] for c in com)), com, sp.expand(s) * sp.sqrt(n2.sym())))
    return res

def interior_angle(sw, c1, c2):
    n1 = [mpm.mpf(float(x.a)) + mpm.mpf(float(x.b)) * mpm.sqrt(L.D) for x in sw.P[c1][0]]
    n2 = [mpm.mpf(float(x.a)) + mpm.mpf(float(x.b)) * mpm.sqrt(L.D) for x in sw.P[c2][0]]
    # exact rationals -> mpf exactly (components are Fractions with small denominators)
    n1 = [mpm.mpf(x.a.numerator) / x.a.denominator + mpm.mpf(x.b.numerator) / x.b.denominator * mpm.sqrt(L.D) for x in sw.P[c1][0]]
    n2 = [mpm.mpf(x.a.numerator) / x.a.denominator + mpm.mpf(x.b.numerator) / x.b.denominator * mpm.sqrt(L.D) for x in sw.P[c2][0]]
    c = sum(a * b for a, b in zip(n1, n2)) / mpm.sqrt(sum(a * a for a in n1) * sum(b * b for b in n2))
    return mpm.pi - mpm.acos(c)

def dehn(sw, m1, m2, name):
    E = hop_edges(sw, m1, m2)
    basis, comp = [], {}
    angles = {}
    for fams, com, length in E:
        ang = interior_angle(sw, *com)
        key = mpm.nstr(ang, 40)
        if key not in angles:
            # reduce modulo pi*Q over the current basis
            vec = [mpm.pi] + basis + [ang]
            rel = mpm.pslq(vec, maxcoeff=1000, maxsteps=10 ** 5) if basis or True else None
            coeffs = None
            if rel is not None and rel[-1] != 0 and abs(mpm.fsum(r * v for r, v in zip(rel, vec))) < mpm.mpf(10) ** -50:
                coeffs = [sp.Rational(-r, rel[-1]) for r in rel[1:-1]]
            if coeffs is None:
                basis.append(ang); coeffs = [0] * (len(basis) - 1) + [1]
            angles[key] = coeffs
        co = angles[key]
        for i, c in enumerate(co):
            comp[i] = comp.get(i, 0) + c * length
    out = []
    for i in sorted(comp):
        f = sp.nsimplify(sp.expand(comp[i]))
        f = sp.radsimp(sp.expand(f))
        roots = [r for r in sp.solve(f, mu)] if f != 0 else 'identically 0'
        out.append((float(basis[i]) if i < len(basis) else None, f, roots))
        log(f'  [{name}] hop ({m1.sym()}, {m2.sym()}) Dehn component along angle {mpm.nstr(basis[i], 15)} (mod pi Q): {f}; roots {roots}')
    if not comp:
        log(f'  [{name}] hop ({m1.sym()}, {m2.sym()}): every dihedral angle is a rational multiple of pi, Dehn invariant = 0 identically')
    return out, basis

# ---------- CO-RD: planes reused from corrd_events.py
L.set_field(2)
src = open(os.path.join(SPL, 'corrd_events.py')).read()
ns = {'__file__': os.path.join(SPL, 'corrd_events.py')}
exec(src[:src.index('roots = {}')], ns)
pl = []
for n, c, e in ns['planes']:
    fam = 'cube' if sum(map(abs, n)) == 1 else ('oct' if sum(map(abs, n)) == 3 else 'rhomb')
    pl.append(([F(x) for x in n], F(c), F(e), fam))
sw = L.Sweep(pl)
for m0 in [Q(6, 5), Q(7, 5), Q(8, 5)]:
    A = {tuple(F(x) for x in v) for v in ns['verts'](m0)}
    B = {tuple(x) for x, _ in sw.vertices(F(m0))}
    checks.append((f'corners at {m0}: corrd_events.verts == sweeplib', A == B))
log('CO ∩ mu RD: Dehn invariant per hop (theta = arccos(1/sqrt3) is the only irrational angle class)')
hops = [(Q(1), Q(4, 3)), (Q(4, 3), Q(3, 2)), (Q(3, 2), Q(2))]
dco = {}
for a, b in hops:
    m1, m2 = F(a + (b - a) / 3), F(a + 2 * (b - a) / 3)
    dco[(a, b)] = dehn(sw, m1, m2, 'CO-RD')
d1 = dco[hops[0]][0]; d3 = dco[hops[2]][0]
checks.append(('Dehn = 0 identically on (1, 4/3)', all(f == 0 for _, f, _ in d1)))
checks.append(('Dehn on (3/2, 2): one linear factor, root exactly 5/3', len(d3) == 1 and d3[0][2] == [sp.Rational(5, 3)]))
log(f'  factor on (3/2, 2): {sp.factor(d3[0][1])}')
# octagon hop side lengths and golden metric factors
E = hop_edges(sw, F(Q(25, 18)), F(Q(13, 9)))
side = {}
for fams, com, length in E:
    if 'rhomb' in fams:
        other = [f for f in fams if f != 'rhomb'] or ['rhomb']
        side.setdefault(other[0], sp.simplify(length))
log(f'CO-RD octagon hop (4/3, 3/2) rhomb-octagon sides: at squares A = {side["cube"]}, at triangles B = {side["oct"]}, remnant C = {side["rhomb"]}')
checks.append(('octagon sides A = 2(mu-1), B = sqrt2(3mu-4), C = sqrt3(3-2mu)',
               sp.simplify(side['cube'] - 2 * (mu - 1)) == 0 and sp.simplify(side['oct'] - sp.sqrt(2) * (3 * mu - 4)) == 0
               and sp.simplify(side['rhomb'] - sp.sqrt(3) * (3 - 2 * mu)) == 0))
phi = (1 + sp.sqrt(5)) / 2
def stations(side, lo, hi, name):
    rows = []
    for (x, y) in [('cube', 'oct'), ('cube', 'rhomb'), ('oct', 'rhomb'), ('pent', 'tri'), ('pent', 'rhomb'), ('tri', 'rhomb')]:
        if x not in side or y not in side: continue
        for g, gl in [(1, 'equal'), (phi, 'phi'), (1 / phi, '1/phi')]:
            for r in sp.solve(sp.Eq(side[x], g * side[y]), mu):
                r = sp.radsimp(sp.simplify(r)); inside = lo < float(r) < hi
                rows.append((x, y, gl, r, inside))
                log(f'  [{name}] metric factor {x}-side - {gl}*{y}-side: root mu = {r} (~{float(r):.8f}) {"IN the octagon hop" if inside else "outside"}')
    return rows
rco = stations(side, 4 / 3, 1.5, 'CO-RD')
eq_in = [r for r in rco if r[2] == 'equal' and r[0] == 'cube' and r[1] == 'oct' and r[4]]
checks.append(('CO-RD: the equal-corner-side factor A - B has no root in the octagon hop (so no #89 cut)', not eq_in))
# C-O golden cuts against splash sweep-events.json (their m = mu/sqrt3)
spl = json.load(open(os.path.join(SPL, 'sweep-events.json')))['cube']['golden']
mine = {'P 4-gon x_G': (8 + 3 * sp.sqrt(2) - 2 * sp.sqrt(5) - sp.sqrt(10)) / 2, 'P 4-gon x_L': (8 - 3 * sp.sqrt(2) + 2 * sp.sqrt(5) - sp.sqrt(10)) / 2,
        'P* 3-gon x_G': phi, 'P* 3-gon x_L': 3 - phi}
ok = all(abs(float(mine[k] / sp.sqrt(3)) - v['m_float']) < 1e-12 for k, v in spl.items())
log(f'C-O golden cuts (this study, mu) vs splash sweep-events.json (m = mu/sqrt3): agree {ok}')
checks.append(('C-O golden cuts agree with splash sweep-events.json', ok))
# ---------- ID-RT
L.set_field(5)
_ = None
g = {}
g = {'F': F, 'Q': Q, 'ZERO': ZERO, 'ONE': ONE, 'dot': dot, 'L': L}
exec(open(os.path.join(HERE, 's2_geometry.py')).read(), g)
swI = L.Sweep(g['pl'])
w = [F(1, Q(2, 5)), F(Q(7, 6), Q(1, 2)), F(Q(5, 4), Q(1, 2)), F(Q(3, 2), Q(1, 2))]
log('ID ∩ mu RT: Dehn invariant per hop (angle classes found by PSLQ)')
did = {}
for a, b in zip(w[:-1], w[1:]):
    m1, m2 = a + (b - a) * Q(1, 3), a + (b - a) * Q(2, 3)
    did[(a, b)] = dehn(swI, m1, m2, 'ID-RT')
E = hop_edges(swI, w[1] + (w[2] - w[1]) * Q(1, 3), w[1] + (w[2] - w[1]) * Q(2, 3))
sideI = {}
for fams, com, length in E:
    if 'rhomb' in fams:
        other = [f for f in fams if f != 'rhomb'] or ['rhomb']
        sideI.setdefault(other[0], sp.radsimp(sp.simplify(length)))
log(f'ID-RT octagon hop rhomb-octagon sides: at pentagons A = {sideI["pent"]}, at triangles B = {sideI["tri"]}, remnant C = {sideI["rhomb"]}')
rid = stations(sideI, float(w[1]), float(w[2]), 'ID-RT')
eqI = [r for r in rid if r[2] == 'equal' and r[0] == 'pent' and r[1] == 'tri' and r[4]]
checks.append(('ID-RT: the equal-corner-side factor has no root in the octagon hop (so no #89 cut)', not eqI))
for n, ok in checks: log(('ok   ' if ok else 'FAIL ') + n)
allok = all(ok for _, ok in checks)
log('FINAL ok' if allok else 'FINAL FAIL: ' + '; '.join(n for n, ok in checks if not ok))
