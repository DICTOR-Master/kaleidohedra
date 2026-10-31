# DICTO · dictospheres.com — math-data dataset VERSION 7 builder (2026-10-31). Created by DICTO. Licence CC BY-SA 4.0.
# Adds the four Star Cores solids DICTO named on 31 October 2026, exact, with D-numbers:
#   D106 Cube Pearl: the cube x = ±1 with its edges cut back by the planes (±1, ±1, 0)·x <= 6/5 (depth 3/5); all 32 corners on one sphere.
#   D107 Golden Clasp: the faces of the truncated cuboctahedron at depths 1 : 1/phi : 3/4 (planes v·x <= s v·v on the 4-, 3- and
#        2-fold axes); its chain of T closes with period four, while the Archimedean truncated cuboctahedron's does not.
#   D108 Hamlet and D109 Ophelia: steps 5 and 6 of the chain of DICTO's growth rule T (#38) from the Ogdoecontahedron (OG), after
#        KRE, PHE, TPP and DPHP (studies/2026-10-30-star-cores-exact, study 4).
# Usage (dicto-big-brother, in a copy of dataset-v6 as dataset-v7): ~/geom/bin/python build/build_v7.py
import json, os, sys, glob, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from exactlib import *
import exactlib, sympy, numpy as np
SOL = os.path.join(HERE, '..', 'solids')
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
LOG = []
def log(ok, msg): LOG.append(('PASS ' if ok else 'FAIL ') + msg); print(LOG[-1], flush=True); return ok
COMMON = {'credit_note': 'Credit: DICTO (idea, names); exact computation with Claude (Anthropic).', 'version_added': 7,
          'paper': 'Star Cores (in preparation)', 'dicto_doi': None, 'finding': '', 'convex': True, 'symmetry_label': 'auto',
          'source': {'app': 'study', 'path': 'research:studies/2026-10-31-star-cores-names', 'id': None}}
def emit(slug, meta, V, F, published):
    V, F = canon(V, F)
    meta = dict(COMMON, **meta); meta['published_values'] = published
    r = write_solid(os.path.join(SOL, slug), meta, V, F)
    log((r['V'], r['E'], r['F']) == tuple(published['f_vector']), f"{slug}: f-vector {(r['V'], r['E'], r['F'])} vs {published['f_vector']}")
    log({str(a): b for a, b in r['fk'].items()} == published['faces_by_sides'], f"{slug}: faces {dict(sorted(r['fk'].items()))}")
    log(True, f"{slug}: volume {fmt(r['vol'])}, symmetry {r['cls']} ({r['order']})")
    return V, F
def orbit(vs):
    out = []
    for v in vs:
        for p in (v, v[1:] + v[:1], v[2:] + v[:2]):
            for sg in itertools.product((1, -1), repeat=3):
                w = tuple(Q(s) * x for s, x in zip(sg, p))
                if all(x.sign() == 0 for x in w): continue
                if not any(all((a - b).sign() == 0 for a, b in zip(w, u)) for u in out): out.append(w)
    return out
def planes(fams): return [(v, s * dot(v, v)) for vs, s in fams for v in vs]
Z, I1 = Q(0), Q(1)
ax4 = orbit([(I1, Z, Z)]); ax3 = orbit([(I1, I1, I1)]); ax2 = orbit([(I1, I1, Z)])
log(len(ax4) == 6 and len(ax3) == 8 and len(ax2) == 12, 'axis sets 6, 8, 12')

V, F = halfspace_solid(planes([(ax4, I1), (ax2, Q(Fr(3, 5)))]))
r2 = {fmt(dot(v, v)) for v in V}; log(r2 == {fmt(Q(Fr(27, 25)))}, f'Cube Pearl: all corners at radius^2 {r2}')
emit('dicto-cube-pearl', {'name': 'Cube Pearl', 'status': 'new as a named proportion: the chamfered-cube family (cube ∩ rhombic dodecahedron) is classical; the depth 3/5, where all 32 corners lie on one sphere, was not found in the sources checked (Polytope Wiki, Klitzing).',
     'scale_note': 'cube faces at x = ±1; edge planes (±1, ±1, 0)·x <= 6/5'}, V, F, {'f_vector': [32, 48, 18], 'faces_by_sides': {'4': 6, '6': 12}})

V, F = halfspace_solid(planes([(ax4, I1), (ax3, PHI - I1), (ax2, Q(Fr(3, 4)))]))
emit('dicto-golden-clasp', {'name': 'Golden Clasp', 'status': 'new as a named proportion of the truncated cuboctahedron\'s face set (depths 1 : 1/phi : 3/4 on the 4-, 3- and 2-fold axes); its chain of T closes with period four (Star Cores study 3), the Archimedean truncated cuboctahedron\'s does not (study 5).',
     'scale_note': 'planes v·x <= s v·v, s = 1, 1/phi, 3/4 on the axes (1,0,0), (1,1,1), (1,1,0)'}, V, F, {'f_vector': [48, 72, 26], 'faces_by_sides': {'4': 12, '6': 8, '8': 6}})

m = json.load(open(os.path.join(SOL, 'dicto-ogdoecontahedron.json'))); d = fkey(m['field'])
S, SF = hull([tuple(parse(x, d) for x in v['exact']) for v in m['vertices']])
for k in range(1, 7):
    S, SF = ustep(S); print('OG step', k, len(S), flush=True)
    if k == 5:
        emit('dicto-hamlet', {'name': 'Hamlet', 'status': 'new: step 5 of the chain of DICTO\'s growth rule T from the Ogdoecontahedron (OG → KRE → PHE → TPP → DPHP → Hamlet → Ophelia; the chain does not close).',
             'scale_note': 'T applied five times to the dataset\'s OG'}, S, SF, {'f_vector': [452, 720, 270], 'faces_by_sides': {'3': 60, '4': 30, '5': 120, '9': 60}})
    if k == 6:
        emit('dicto-ophelia', {'name': 'Ophelia', 'status': 'new: step 6 of the chain of DICTO\'s growth rule T from the Ogdoecontahedron, after Hamlet.',
             'scale_note': 'T applied six times to the dataset\'s OG'}, S, SF, {'f_vector': [642, 1080, 440], 'faces_by_sides': {'4': 300, '6': 120, '12': 20}})
json.dump(LOG, open(os.path.join(HERE, 'build_v7.log.json'), 'w'), indent=1)
print('FAILS:', sum(1 for l in LOG if l.startswith('FAIL')))
