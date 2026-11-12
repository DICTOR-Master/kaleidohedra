"""#103 E1 sandhi count (12 Nov 2026): #103 (Prop. 3, Table 3, sec. 10) lists 28 two-line crossings for E1; the region study (e1_regions.py)
counts 22 sandhis plus two 4-line points on E1's exact edge (t4's right leg through t5's corner, which already lies on t6's right leg).
Which counting gives 28? Method: #103's own rule (counts.py: points where exactly two drawn sides cross, corners left out), applied
  (1) with counts.py itself, unchanged, to #103's stored E1 (figures/even.json, 16 digits, exact Fractions, tolerance 1e-30);
  (2) at 300 digits to E1 on its exact edge (S re-solved from the incidence, as in e1_regions.py);
  (3) at 300 digits to the yantras just off the edge, S -> S +- delta (delta = 1e-30, 1e-60), on both sides.
At every 4-line point the clusters of the split pictures are listed with the drawn sides through them; the odd regions are recounted
on each side (arrangement of chunk 5c, unchanged).
Controls: positive, the DICTO Yantra (GF1, exact-root data) gives 24 sandhis by the same rule (#103) and counts.py's own control row
(K1: 4 up, 5 down, 18, 24); negative, off the edge (S +- delta) the clustering must NOT merge the split points into a 4-line point.
Usage: python -u e1_sandhi.py [pilot]"""
import sys, os, json, itertools, time
from fractions import Fraction as F
from multiprocessing import get_context
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import yantra_regions45 as Y45
from yantra_regions45 import B, Ctx, arrangement
SRI = os.path.normpath(os.path.join(HERE, '..', '..', '2026-11-08-sri-yantra'))
E1J = os.path.normpath(os.path.join(HERE, '..', '..', '2026-11-10-g1-e1-exact', 'e1-refined.json'))
PILOT = 'pilot' in sys.argv[1:]
DPS = 120 if PILOT else 300
KIND = ('base', 'left leg', 'right leg')


def counts_py_on_even():
    """run #103's counts.py function unchanged (source cut before its own rows) on figures/even.json E1"""
    src = open(os.path.join(SRI, 'scripts', 'counts.py')).read().split('\nrows = ')[0]
    out = {}
    for tol in ('10**30', '10**12'):           # as stored (40-digit data) and at the 16 digits even.json actually carries
        ns = {}; exec(compile(src.replace('F(1, 10**30)', f'F(1, {tol})'), 'counts.py', 'exec'), ns)
        out[tol] = ns['counts'](*ns['load'](os.path.join(SRI, 'figures', 'even.json'), 'E1'))
    k1 = ns['counts'](*ns['load'](os.path.join(SRI, 'figures', 'kites.json'), 'K1'))
    return out, k1


def tri_of(K, dS=0):
    mp = K.mp
    from model import solve, det3
    e = json.load(open(E1J))
    u, v, Q = mp.mpf(e['u']), mp.mpf(e['v']), mp.mpf(e['Q'])
    tri = lambda S: solve(v * v / (1 + v * v), Q, 1 / (1 + u * u), S, v / (1 + v * v), u / (1 + u * u), mp.sqrt, root=1)
    def C(S):
        t = tri(S); b, w, a = t['b'], t['w'], t['a']
        return det3(((w[4], b[4]), (0, a[4])), ((-w[5], b[5]), (w[5], b[5])), ((w[6], b[6]), (0, a[6])))
    S = mp.findroot(C, mp.mpf(e['S']), tol=mp.mpf(10) ** (-(K.dps - 20)))
    t = tri(S + dS)
    return {i: (t['b'][i], t['w'][i], t['a'][i]) for i in range(1, 10)}, C(S + dS)


def points(K, Y, tol):
    """counts.py's rule at working precision: clusters of crossings of drawn sides; each with its set of sides"""
    mp = K.mp
    segs = []
    for i in range(1, 10):
        b, w, a = Y[i]; L, R, A = (-w, b), (w, b), (mp.mpf(0), a)
        segs += [((L, R), (i, 0)), ((L, A), (i, 1)), ((R, A), (i, 2))]
    pts = []
    for (s, i), (t, j) in itertools.combinations(segs, 2):
        (x1, y1), (x2, y2) = s; (x3, y3), (x4, y4) = t
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(den) < tol: continue
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
        on = lambda p, q: min(p[0], q[0]) - tol <= px <= max(p[0], q[0]) + tol and min(p[1], q[1]) - tol <= py <= max(p[1], q[1]) + tol
        if not (on(*s) and on(*t)): continue
        for P in pts:
            if abs(P[0][0] - px) < tol and abs(P[0][1] - py) < tol: P[1].update({i, j}); break
        else: pts.append([(px, py), {i, j}])
    corners = []
    for i in range(1, 10):
        b, w, a = Y[i]; corners += [(-w, b), (w, b), (mp.mpf(0), a)]
    isc = lambda p: any(abs(p[0] - c[0]) < tol and abs(p[1] - c[1]) < tol for c in corners)
    return [(p, s, isc(p)) for p, s in pts]


def summary(P):
    from collections import Counter
    return dict(Counter(('corner' if c else 'free', len(s)) for p, s, c in P))


def near(P, X, r):
    return [(len(s), c, sorted(f't{i} {KIND[k]}' for i, k in s)) for p, s, c in P if abs(p[0] - X[0]) < r and abs(p[1] - X[1]) < r]


def odd_regions(K, Y):
    A = arrangement(K, Y); odd = [f for f in A['faces'] if f['c'] % 2]
    from collections import Counter
    return len(odd), dict(Counter(len(f['V']) for f in odd))


def task(arg):
    name, dS = arg
    K = Ctx(DPS); mp = K.mp; tol = mp.mpf(10) ** (-(DPS - 60))
    if name == 'GF1':
        Y, ok = B.load_gf1(K, lambda *a: None); res = 0
    else:
        Y, res = tri_of(K, mp.mpf(dS))
    P = points(K, Y, tol)
    sand = sum(1 for p, s, c in P if len(s) == 2 and not c)
    four = [p for p, s, c in P if len(s) == 4]
    reg = odd_regions(K, Y)
    out = {'name': name, 'dS': dS, 'incidence_residual': mp.nstr(abs(res), 3), 'sandhis': sand, 'classes': summary(P), 'four_line_points': [(mp.nstr(p[0], 15), mp.nstr(p[1], 15)) for p in four], 'odd_regions': reg}
    return out, Y, P


def main():
    t0 = time.time(); OK = True
    def check(m, c):
        nonlocal OK
        OK &= bool(c); print(('ok   ' if c else 'FAIL ') + m, flush=True)
    cp, k1 = counts_py_on_even()
    print(f"counts.py on #103 figures/even.json E1 (16 digits stored): tolerance 1e-30 as written (meant for 40-digit data): (up, down, marmas, sandhis) = {cp['10**30']}; "
          f"tolerance 1e-12 (fits 16 digits): {cp['10**12']}", flush=True)
    check(f"#103 reproduced: counts.py's rule at the stored 16 digits gives 18 marmas and 28 sandhis for E1: {cp['10**12']}", tuple(cp['10**12'][2:]) == (18, 28))
    check(f'counts.py control row K1 = (4, 5, 18, 24): {k1}', tuple(k1) == (4, 5, 18, 24))
    deltas = ['1e-30'] if PILOT else ['1e-10', '1e-30', '1e-60']
    jobs = [('E1 on edge', '0'), ('GF1', '0')] + [(f'E1 S{sg}{d}', ('' if sg == '+' else '-') + d) for d in deltas for sg in '+-']
    with get_context('fork').Pool(4) as pool:
        R = pool.map(task, jobs)
    for o, _, _ in R: print('FIND', o, flush=True)
    edge = next(r for r in R if r[0]['name'] == 'E1 on edge'); gf = next(r for r in R if r[0]['name'] == 'GF1')
    check(f"control: the DICTO Yantra by the same rule: {gf[0]['sandhis']} sandhis (#103: 24), {gf[0]['odd_regions']}", gf[0]['sandhis'] == 24)
    e = edge[0]
    check(f"E1 on its exact edge: {e['sandhis']} sandhis, {len(e['four_line_points'])} points where four drawn sides meet, odd regions {e['odd_regions']}",
          e['sandhis'] == 22 and len(e['four_line_points']) == 2 and e['odd_regions'][0] == 43)
    mp = Ctx(DPS).mp
    X4 = [p for p, s, c in edge[2] if len(s) == 4]
    for p, s, c in edge[2]:
        if len(s) == 4: print(f"  4-line point ({mp.nstr(p[0], 12)}, {mp.nstr(p[1], 12)}): corner {c}; sides {sorted(f't{i} {KIND[k]}' for i, k in s)}", flush=True)
    for o, Y, P in R:
        if o['name'].startswith('E1 S'):
            print(f"{o['name']}: sandhis {o['sandhis']}, odd regions {o['odd_regions']}", flush=True)
            for X in X4:
                print(f"   near ({mp.nstr(X[0], 8)}, {mp.nstr(X[1], 8)}): {near(P, X, mp.mpf(10) ** -6)}", flush=True)
    side = {o['name']: o['sandhis'] for o, _, _ in R if o['name'].startswith('E1 S')}
    print('side counts:', side, flush=True)
    check('each 4-line point splits off the edge into a corner touch (3 sides, a corner) plus 3 two-side crossings on one side of the edge (22 + 2 x 3 = 28)',
          28 in side.values())
    off4 = [len(o['four_line_points']) for o, _, _ in R if o['name'].startswith('E1 S')]
    check(f'NEG off the edge the split points are not merged: 4-line points {off4} (all 0)', all(x == 0 for x in off4))
    print(f'total {time.time() - t0:.0f} s', flush=True)
    print('FINAL ok' if OK else 'FINAL FAIL: see the FAIL lines above', flush=True)


if __name__ == '__main__':
    main()
