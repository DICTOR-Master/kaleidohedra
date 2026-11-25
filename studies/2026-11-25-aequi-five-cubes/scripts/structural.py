# Copy from study 2026-11-24-aequi-certify-extend; edits marked 'study 2026-11-25' (|q|^2 = 8 for RDa, RDb; die 95 check dropped).
# Exact proof that every "structural" corner (four or more planes through one point for EVERY depth vector of the
# die's orbit structure) really is one: the extra plane's offset at the corner of a triple is sum_o c_o d_o with
# every c_o exactly 0. Arithmetic: unnormalised normals q in Q(sqrt5)^3, plane q.x = d * |q| with
# |q|^2 in {1, 2, 3, 4, phi + 2}; c_o = sum_i |q_i| (q_f . w_i) / det - [o = orb f] |q_f|, collected by the radical
# |q| (1, sqrt2, sqrt3, sqrt(phi+2); 2 = 2*1); each radical's coefficient (in Q(sqrt5)) is shown to be exactly 0.
# Zero coefficients on every radical is sufficient for c_o = 0.
# Also: the exact claim for Td: D12+D12'/24 + RT24+RT24'/24 (die 95 of study 2026-11-20-aequi-two-placements):
# at depth ratio RT/D = cos 18 deg = sqrt(10 + 2 sqrt5)/4 its 26 corners lie on the 26 cube axes and its 48 faces
# project onto the 48 triangles of the disdyakis dodecahedron (Oh fundamental triangles, area pi/12 = 4 pi/48 each).
# usage: structural.py certify-pass1.jsonl OUT.json
import json, sys, os, itertools
from fractions import Fraction as Q
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import certify as C
import sympy as sp

class K:   # a + b sqrt5, a, b rational
    __slots__ = ('a', 'b')
    def __init__(s, a, b=0): s.a = Q(a); s.b = Q(b)
    def __add__(s, o): o = o if isinstance(o, K) else K(o); return K(s.a + o.a, s.b + o.b)
    __radd__ = __add__
    def __sub__(s, o): o = o if isinstance(o, K) else K(o); return K(s.a - o.a, s.b - o.b)
    def __neg__(s): return K(-s.a, -s.b)
    def __mul__(s, o): o = o if isinstance(o, K) else K(o); return K(s.a * o.a + 5 * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__
    def inv(s): n = s.a * s.a - 5 * s.b * s.b; return K(s.a / n, -s.b / n)
    def __truediv__(s, o): return s * o.inv()
    def zero(s): return s.a == 0 and s.b == 0
    def __repr__(s): return '%s%+s*sqrt5' % (s.a, s.b)
PHI = K(Q(1, 2), Q(1, 2))
def kq(i):
    """exact unnormalised normal of direction i: coordinates a + b*phi"""
    return [K(c[0]) + PHI * c[1] for c in C.EXACT[i]]
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
RAD = {}   # |q|^2 -> (radical name, rational-in-Q(sqrt5) multiplier)
def norm(q):
    n2 = dot(q, q)
    if n2.b == 0 and n2.a in (1, 4): return ('1', K(int(n2.a ** .5 + .5)))
    if n2.b == 0 and n2.a == 2: return ('sqrt2', K(1))
    if n2.b == 0 and n2.a == 8: return ('sqrt2', K(2))   # study 2026-11-25: RDa, RDb
    if n2.b == 0 and n2.a == 3: return ('sqrt3', K(1))
    if n2.b == 0 and n2.a == 12: return ('sqrt3', K(2))
    # phi + 2 = (5 + sqrt5)/2 ; scaled versions
    t = n2 / K(Q(5, 2), Q(1, 2))
    if t.b == 0 and t.a > 0:
        r = sp.sqrt(sp.Rational(t.a.numerator, t.a.denominator))
        if r.is_rational: return ('sqrt(phi+2)', K(Q(int(r.p), int(r.q))))
    raise ValueError('norm %r' % n2)

def check_extra(planes, orbits):
    """planes: [i, j, k, f] direction indices; orbits: their orbit numbers; True iff every c_o is exactly 0"""
    i, j, k, f = planes; qi, qj, qk, qf = kq(i), kq(j), kq(k), kq(f)
    det = dot(qi, cross(qj, qk)); w = {i: cross(qj, qk), j: cross(qk, qi), k: cross(qi, qj)}
    coef = {}   # (orbit, radical) -> K
    for p, o in zip((i, j, k), orbits[:3]):
        rad, mult = norm(kq(p)); key = (o, rad)
        coef[key] = coef.get(key, K(0)) + mult * dot(qf, w[p]) / det
    rad, mult = norm(qf); key = (orbits[3], rad); coef[key] = coef.get(key, K(0)) - mult
    # group by orbit: sum over radicals must vanish; we require each radical's part to vanish (sufficient)
    return all(v.zero() for v in coef.values()), {str(k): repr(v) for k, v in coef.items() if not v.zero()}

def die95():
    """exact check at ratio cos 18 deg for die 95 (two-placement study)"""
    recs = C.load_all(); rec = [x for x in recs if x['study'].startswith('2026-11-20') and x['sid'] == 95][0]
    s = C.Die(rec); s.setup()          # midpoint type: 26 corners (planes meeting at the stratum)
    s5 = sp.sqrt(5); ph = (1 + s5) / 2; c18 = sp.sqrt(10 + 2 * s5) / 4
    def sq(i): return sp.Matrix([sp.nsimplify(c[0]) + sp.nsimplify(c[1]) * ph for c in C.EXACT[i]])
    idx = rec['idx']; sizes = rec['sizes']; dep = [sp.Integer(1), c18]
    orb = [0] * sizes[0] + [1] * sizes[1]
    corners = []
    for vi, I in enumerate(s.full):
        # solve with a triple, check every plane of I passes through it exactly
        t = s.trip[vi]; Mx = sp.Matrix.vstack(*[sq(idx[p]).T for p in t])
        rhs = sp.Matrix([dep[orb[p]] * sp.sqrt(sq(idx[p]).dot(sq(idx[p]))) for p in t])
        v = Mx.LUsolve(rhs)
        for p in I:
            r = sq(idx[p]).dot(v) - dep[orb[p]] * sp.sqrt(sq(idx[p]).dot(sq(idx[p])))
            assert sp.minimal_polynomial(sp.nsimplify(r), sp.Symbol('X')) == sp.Symbol('X'), 'plane off corner'
        corners.append(v)
    # each corner on a cube axis: v parallel to an integer vector with entries in {0, 1, -1}
    kind = []
    for v in corners:
        vv = [sp.nsimplify(x) for x in v]; nz = [x for x in vv if sp.minimal_polynomial(x, sp.Symbol('X')) != sp.Symbol('X')]
        a = nz[0]
        for x in nz: assert sp.minimal_polynomial(sp.simplify(x * x - a * a), sp.Symbol('X')) == sp.Symbol('X'), 'not on a cube axis'
        kind.append({1: 'C6', 2: 'RD12', 3: 'O8'}[len(nz)])
    from collections import Counter
    kc = Counter(kind)
    tri_ok = all(sorted(kind[vi] for vi in s.cyc[f]) == ['C6', 'O8', 'RD12'] for f in range(s.N))
    # and the three axes of each face are mutually nearest (angles 54.74, 45, 35.26 deg): an Oh fundamental triangle.
    # The axes are exact (above); the angles between distinct cube axes differ by >= 9 deg, so floats decide this.
    import numpy as np
    U = [np.array([float(x) for x in v]) for v in corners]; U = [u / np.linalg.norm(u) for u in U]
    want = {('C6', 'O8'): 1 / 3 ** .5, ('C6', 'RD12'): 1 / 2 ** .5, ('O8', 'RD12'): (2 / 3) ** .5}
    for f in range(s.N):
        c = s.cyc[f]
        for a, b in itertools.combinations(c, 2):
            k = tuple(sorted((kind[a], kind[b]))); tri_ok &= abs(U[a] @ U[b] - want[k]) < 1e-9
    return dict(corners=len(corners), corner_axes=dict(kc), every_face_C6_O8_RD12=bool(tri_ok), ratio='sqrt(10+2*sqrt5)/4 = cos(pi/10)')

if __name__ == '__main__':
    R = [json.loads(L) for L in open(sys.argv[1])]
    seen = {}; nd = 0; fails = []
    for r in R:
        if not r.get('structural_extra'): continue
        nd += 1
        for e in r['structural_extra']:
            key = (tuple(e['planes']), tuple(e['orbits']))
            if key not in seen: seen[key] = check_extra(e['planes'], e['orbits'])
            if not seen[key][0]: fails.append((r['study'], r['sid'], e, seen[key][1]))
    out = dict(dice_with_structural_corners=nd, distinct_checks=len(seen), failures=len(fails), failure_list=fails[:20])
    print('structural corners: dice', nd, 'distinct (triple, plane, orbit pattern) checks', len(seen), 'failures', len(fails), flush=True)
    # study 2026-11-25: die 95 of the two-placement frame is not in this direction list
    json.dump(out, open(sys.argv[2], 'w'), indent=1)
    print('FINAL ok' if not fails else 'CHECK FAILED')
