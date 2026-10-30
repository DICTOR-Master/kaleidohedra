# Star Cores study 2b (2026-10-31): study 2's exact core-turn (study2.py, unchanged) run for EVERY convex solid of the float study
# (../../2026-10-30-star-cores/data/star-cores.json, "convex": true), plus the four study-2 solids not in that list, to reconcile the
# float result ("core returns" only for GTI D40 and TI Star core D105: it asked only whether core(core(S)) = S) with study 2's finding
# that cores settle into period 2. exactlib.hull is replaced by study 5's exact gift-wrapping hull (float angle ordering fails on short
# edges). Per-solid limit STUDY2B_LIMIT s (default 900, signal.alarm), recorded as 'timeout'.
# Usage: ~/geom/bin/python study2b.py <dataset solids dir> <exactlib dir> <star-cores.json> <out json> [start end]
import sys, os, json, signal, time
SOL, LIB, SC, OUT = sys.argv[1:5]; sys.path.insert(0, LIB)
LO, HI = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (0, 10**9)
from exactlib import *
from fractions import Fraction as Fr
import sympy
def fkey(s): return 1 if s == 'Q' else (('cbrt', 2) if s == 'Q(2**(1/3))' else int(s[7:-2]))
def parse(s, d):
    if d == 1:
        e = sympy.Rational(sympy.sympify(s)); return QF(Fr(int(e.p), int(e.q)), 0, 5)
    e = sympy.expand(sympy.sympify(s))
    if isinstance(d, tuple):
        cs = [Fr(0)] * 3; basis = {sympy.Integer(1): 0, sympy.Integer(2) ** sympy.Rational(1, 3): 1, sympy.Integer(2) ** sympy.Rational(2, 3): 2}
        for t, c in e.as_coefficients_dict().items(): cs[basis[t]] += Fr(int(c.p), int(c.q))
        return KC(*cs, k=2)
    a = b = Fr(0)
    for t, c in e.as_coefficients_dict().items():
        if t == 1: a += Fr(int(c.p), int(c.q))
        else: assert t == sympy.sqrt(d), s; b += Fr(int(c.p), int(c.q))
    return QF(a, b, d)
def kinds(F):
    k = {}
    for f in F: k[len(f)] = k.get(len(f), 0) + 1
    return {str(a): b for a, b in sorted(k.items())}
def rad2(V): return max((dot(v, v) for v in V), key=lambda x: x.f())
def similar(A, B, g2):
    """exact: the corners of B are k x the corners of A, k^2 = g2 (|B|^2/|A|^2), by matching each corner of B to a parallel corner of A
    with the right squared ratio; no square root needed."""
    if len(A) != len(B): return False
    for v in B:
        if not any(all(x.sign() == 0 for x in cross(u, v)) and dot(u, v).sign() > 0 and (dot(v, v) - g2 * dot(u, u)).sign() == 0 for u in A):
            return False
    return True
def gstr(x): return fmt(x)
import time, glob, itertools, numpy as np
import exactlib
def exact_order(V, f, n):
    # the face's corners in exact CCW order seen from outside (normal n): gift wrapping with exact left-turn tests (float angle sorting
    # fails on the very short edges the long chains make)
    start = min(f, key=lambda j: tuple(x.f() for x in V[j])); order = [start]
    while True:
        a = order[-1]; cand = None
        for b in f:
            if b == a: continue
            if cand is None: cand = b; continue
            s = dot(cross(sub(V[cand], V[a]), sub(V[b], V[a])), n).sign()
            if s < 0: cand = b                     # b lies to the right of a->cand: wrap tighter
        if cand == start: break
        order.append(cand)
        assert len(order) <= len(f)
    return order
def hull_exact_order(points):
    P = list(dict.fromkeys(tuple(p) for p in points))
    from scipy.spatial import ConvexHull
    X = np.array([fv(p) for p in P]); cen = X.mean(0); ch = ConvexHull(X); planes = {}
    for simp in ch.simplices:
        a, b, c = (P[i] for i in simp); n = cross(sub(b, a), sub(c, a))
        if all(x.sign() == 0 for x in n): continue
        planes[plane_key(n, dot(n, a))] = (n, dot(n, a))
    good = {}
    for key, (n, cc) in planes.items():
        sg = [(dot(n, p) - cc).sign() for p in P]
        if all(x <= 0 for x in sg): good[key] = (n, cc, [i for i, x in enumerate(sg) if x == 0])
        elif all(x >= 0 for x in sg): good[key] = (mul(-1, n), -cc, [i for i, x in enumerate(sg) if x == 0])
        else: raise AssertionError('float facet is not a supporting plane')
    on = {i: [] for i in range(len(P))}
    for key, (n, cc, idx) in good.items():
        for i in idx: on[i].append(n)
    corners = [i for i in range(len(P)) if len(on[i]) >= 3 and any(det3(*t).sign() != 0 for t in itertools.combinations(on[i], 3))]
    V = [P[i] for i in corners]; vid = {i: k for k, i in enumerate(corners)}; F = []
    for key, (n, cc, idx) in good.items():
        f = [vid[i] for i in idx if i in vid]; assert len(f) >= 3
        order = exact_order(V, f, n)
        assert len(order) == len(f), 'a face point is not a corner of the face'
        F.append(order)
    exactlib.check_closed(V, F)
    return V, F
exactlib.hull = hull_exact_order; hull = hull_exact_order
SKIP = []
def core_turn(V, F):
    """the core of one turn at t = 1 (any t only scales it by t): the faces grouped into families (number of sides, distance of the face
    plane from the centre); the tips at the feet of the face perpendiculars; the hull of each family's tips that is solid; the core =
    their intersection."""
    SKIP.clear(); fam = {}
    for f, (n, c) in zip(F, face_planes(V, F)):
        foot = mul(c / dot(n, n), n); fam.setdefault((len(f), fmt(dot(foot, foot))), []).append(foot)
    planes = []; used = 0
    for key, T in fam.items():
        if len(T) < 4: continue
        try: A, AF = hull(T)
        except Exception as e: SKIP.append('family %s (%d tips): hull fails: %s' % (key, len(T), (type(e).__name__ + ' ' + str(e))[:80])); continue
        if len(A) < 4: SKIP.append('family %s: hull has %d corners' % (key, len(A))); continue
        planes += face_planes(A, AF); used += 1
    bad = [c for n, c in planes if c.sign() <= 0]
    if bad:   # study 2b: the centre is not strictly inside every family hull, so the core does not contain the centre
        raise NoCore('the centre is not strictly inside the hull of every family (%d face planes with offset <= 0)' % len(bad))
    if not planes:   # study 2b: name the case instead of numpy's empty-array error
        raise NoCore('no family gives a solid hull of tips: %d families, sizes %s; %s' % (len(fam), sorted(len(T) for T in fam.values()), '; '.join(SKIP)))
    C, CF = halfspace_solid(planes)
    return C, CF, len(fam), used
class NoCore(Exception): pass
def parse_alg(m):
    # study 2b: the Q(t) files (Sonsam, Lahdeli): t the root of the minimal polynomial in the isolating interval (field_definition)
    fd = m['field_definition']; t = sympy.Symbol(fd['generator'])
    co = [int(c) for c in sympy.Poly(sympy.sympify(fd['minimal_polynomial']), t).all_coeffs()]
    F = AlgField.get(co, Fr(fd['isolating_interval'][0]), Fr(fd['isolating_interval'][1]), fd['generator'])
    def p(x):
        cs = sympy.Poly(sympy.expand(sympy.sympify(x)), t).all_coeffs()[::-1]
        return RF([Fr(int(sympy.Rational(c).p), int(sympy.Rational(c).q)) for c in cs], F)
    return p
STUDY2_EXTRA = ['dicto-icosaxes', 'dicto-unborn-axes', 'dicto-david', 'dicto-delilah']   # in study2.json but not convex-listed
SCR = json.load(open(SC)); LIST = [(r['D'], os.path.basename(r['file'])[:-5]) for r in SCR if r['convex']]
have = {s for _, s in LIST}; LIST += [(None, s) for s in STUDY2_EXTRA if s not in have]
LIMIT = int(os.environ.get('STUDY2B_LIMIT', '900'))
class TO(Exception): pass
def alarm(*a): raise TO()
signal.signal(signal.SIGALRM, alarm)
res = []
for i, (D, slug) in enumerate(LIST):
    if not (LO <= i < HI): continue
    m = json.load(open(os.path.join(SOL, slug + '.json')))
    if m['field'] == 'Q(t)': pa = parse_alg(m)
    else: d = fkey(m['field']); pa = lambda x, d=d: parse(x, d)
    row = dict(index=i, D=D or m.get('D') or m.get('d_number'), slug=slug, solid=m['name'], field=m['field'],
               symmetry=m.get('symmetry', {}).get('schoenflies'), turns=[])
    t0 = time.time(); signal.alarm(LIMIT)
    try:
        V = [tuple(pa(x) for x in v['exact']) for v in m['vertices']]; V, F = hull(V)
        row.update(corners0=len(V), faces0=kinds(F))
        hist = [(V, F, rad2(V), volume(V, F))]; S, SF = V, F
        for k in range(1, 7):
            S, SF, nf, used = core_turn(S, SF); r2 = rad2(S); vs = volume(S, SF)
            st = dict(turn=k, families=nf, families_solid=used, families_skipped=list(SKIP), corners=len(S), faces=kinds(SF), radius2_over_start=gstr(r2 / hist[0][2]),
                      volume_over_start=gstr(vs / hist[0][3]))
            for j, (A, AF, ra, va) in enumerate(hist):
                if kinds(AF) == kinds(SF) and similar(A, S, r2 / ra):
                    st['returns_to_turn'] = j
                    row.update(enters_cycle_at_turn=j, period=k - j, gain_radius_squared_t1=gstr(r2 / ra), gain_volume_t1=gstr(vs / va),
                               gain_radius_decimal_t1=(r2 / ra).f() ** .5)
                    break
            row['turns'].append(st); print(i, m['name'][:30], st, flush=True); hist.append((S, SF, r2, vs))
            if 'period' in row or len(S) > 400: break
        if 'period' not in row: row['outcome'] = 'no return within %d turns' % len(row['turns'])
    except NoCore as e:
        row['outcome'] = 'no core at turn %d: %s' % (len(row['turns']) + 1, e); print(i, m['name'], 'NOCORE', e, flush=True)
    except TO:
        row['error'] = 'timeout %d s' % LIMIT; print(i, m['name'], 'TIMEOUT', flush=True)
    except Exception as e:
        row['error'] = type(e).__name__ + ' ' + str(e)[:160]; print(i, m['name'], 'ERROR', row['error'], flush=True)
    finally:
        signal.alarm(0)
    row['seconds'] = round(time.time() - t0, 1)
    res.append(row); json.dump(res, open(OUT, 'w'), indent=1, default=str)
print('done', len(res))
