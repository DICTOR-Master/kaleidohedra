# Star Cores study 2 (DICTO 2026-10-30 "go ahead with study 2"): the core of each turn (#78, Proposition 5), followed turn after turn,
# exactly, for the ten solids of study 1. Does the core come back, and after how many turns? The core is the intersection of the hulls of
# the spike tips family by family (a family = faces with the same number of sides at the same distance from the centre). The tips sit at
# t x the feet of the face perpendiculars; t only scales the core, so the run uses t = 1 and the gain at t is t^period x the gain given.
# Usage: ~/geom/bin/python study2.py <dataset solids dir> <exactlib dir> <out json>
import sys, os, json
SOL, LIB, OUT = sys.argv[1:4]; sys.path.insert(0, LIB)
from exactlib import *
from fractions import Fraction as Fr
import sympy
SOLIDS = ['dicto-gti', 'dicto-fpd', 'dicto-palintriacontahedron', 'dicto-icosaxes', 'dicto-unborn-axes', 'dicto-metaxyhexecontahedron',
          'dicto-tweedledum', 'dicto-samson', 'dicto-david', 'dicto-delilah']
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

def core_turn(V, F):
    """the core of one turn at t = 1 (any t only scales it by t): the faces grouped into families (number of sides, distance of the face
    plane from the centre); the tips at the feet of the face perpendiculars; the hull of each family's tips that is solid; the core =
    their intersection."""
    fam = {}
    for f, (n, c) in zip(F, face_planes(V, F)):
        foot = mul(c / dot(n, n), n); fam.setdefault((len(f), fmt(dot(foot, foot))), []).append(foot)
    planes = []; used = 0
    for key, T in fam.items():
        if len(T) < 4: continue
        try: A, AF = hull(T)
        except Exception: continue
        if len(A) < 4: continue
        planes += face_planes(A, AF); used += 1
    C, CF = halfspace_solid(planes)
    return C, CF, len(fam), used
res = []
for slug in SOLIDS:
    m = json.load(open(os.path.join(SOL, slug + '.json'))); d = fkey(m['field'])
    V = [tuple(parse(x, d) for x in v['exact']) for v in m['vertices']]; V, F = hull(V)
    row = dict(solid=m['name'], field=m['field'], symmetry=m.get('symmetry', {}).get('schoenflies'), turns=[])
    hist = [(V, F, rad2(V), volume(V, F))]; S, SF = V, F
    try:
        for k in range(1, 7):
            S, SF, nf, used = core_turn(S, SF); r2 = rad2(S); vs = volume(S, SF)
            st = dict(turn=k, families=nf, families_solid=used, corners=len(S), faces=kinds(SF), radius2_over_start=gstr(r2 / hist[0][2]),
                      volume_over_start=gstr(vs / hist[0][3]))
            for j, (A, AF, ra, va) in enumerate(hist):
                if kinds(AF) == kinds(SF) and similar(A, S, r2 / ra):
                    st['returns_to_turn'] = j
                    row.update(enters_cycle_at_turn=j, period=k - j, gain_radius_squared_t1=gstr(r2 / ra), gain_volume_t1=gstr(vs / va),
                               gain_radius_decimal_t1=(r2 / ra).f() ** .5)
                    break
            row['turns'].append(st); print(m['name'][:30], st, flush=True); hist.append((S, SF, r2, vs))
            if 'period' in row or len(S) > 400: break
    except Exception as e:
        row['error'] = type(e).__name__ + ' ' + str(e)[:160]; print(m['name'], 'ERROR', row['error'], flush=True)
    res.append(row); json.dump(res, open(OUT, 'w'), indent=1, default=str)
print('done', len(res))
