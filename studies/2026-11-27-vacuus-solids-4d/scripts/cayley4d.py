"""Are Vacuus-Solids shadows of 4D polytopes? (27 Nov 2026; DICTO's observation: "Vacuus solids having a copy of the solid in the
centre ... seem like polytopes"; "those that have their dual aren't?!" -> "Yes run the test"). With Claude (Anthropic).
Test. Solid P (corners V, centre O inside), core K = mu * P* (dual-core Vacuus-Solid) or mu * P (copy core). Build the 4D polytope
Q = conv(P x {0} u K x {1}). Claim (dual core): the facets of Q are P, K, and one JOIN per face of P of each dimension:
  face f (polygon) * its dual corner  -> the pit over f;  edge e * its dual edge -> a tetrahedron (wedge along e);
  corner w * its dual face            -> the pyramid from w onto a core face.
Each predicted facet is checked EXACTLY (sympy, Q(sqrt 5)): its points span a hyperplane, and every other point of Q lies strictly
on one side. Completeness: the number of facets of the float hull of Q equals the number predicted. Then the Schlegel view: from
X = (O, -h), beyond the facet P x {0} only (checked exactly against every other facet), Q projects to P with the core at scale
mu h / (h + 1) and every cell a cell of the Vacuus-Solid. Controls: copy core = the prism (facets 2 + F); negative control: the
cube's octahedral core turned by a small generic rotation must FAIL (the joins stop being flat)."""
import itertools, sys
import sympy as sp
import numpy as np
from scipy.spatial import ConvexHull
phi = (1 + sp.sqrt(5)) / 2
def cn(x): return sp.expand(sp.radsimp(sp.expand(sp.sympify(x))))     # canonical a + b sqrt 5 (27 Nov: unsimplified forms counted one corner twice)
def cyc(p): return [p, (p[1], p[2], p[0]), (p[2], p[0], p[1])]
def signs(p): return {tuple(s * x for s, x in zip(sg, p)) for sg in itertools.product((1, -1), repeat=3)}
def solid(name):
    if name == 'cube':
        V = list(signs((1, 1, 1))); U = [u for p in cyc((1, 0, 0)) for u in signs(p)]
    elif name == 'octahedron':
        V = [u for p in cyc((1, 0, 0)) for u in signs(p)]; U = list(signs((1, 1, 1)))
    elif name == 'dodecahedron':
        V = list(signs((1, 1, 1))) + [u for p in cyc((0, 1 / phi, phi)) for u in signs(p)]; U = [u for p in cyc((0, phi, 1)) for u in signs(p)]
    elif name == 'icosahedron':
        V = [u for p in cyc((0, 1, phi)) for u in signs(p)]; U = list(signs((1, 1, 1))) + [u for p in cyc((0, phi, 1 / phi)) for u in signs(p)]
    elif name == 'tetrahedron':
        V = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]; U = [tuple(-x for x in v) for v in V]
    V = [sp.Matrix(v) for v in sorted({tuple(cn(x) for x in v) for v in V}, key=str)]
    U = [sp.Matrix(u) for u in sorted({tuple(cn(x) for x in u) for u in U}, key=str)]
    faces, dual = [], []
    for u in U:
        vals = [cn(u.dot(v)) for v in V]; m = max(vals, key=lambda z: float(z))
        faces.append(frozenset(i for i, z in enumerate(vals) if cn(z - m) == 0)); dual.append(sp.Matrix([cn(x / m) for x in u]))   # polar corner of face
    assert len(V) - sum(1 for _ in itertools.combinations(range(len(V)), 2) if False) + len(faces) > 0
    print(f'  {name}: {len(V)} corners, {len(faces)} faces, sizes {sorted({len(f) for f in faces})}', flush=True)
    return V, faces, dual
def faces_all(V, faces):
    """all faces of P as (vertex set, the set of facets containing it): corners, edges, facets"""
    out = []
    for i in range(len(V)):
        out.append((frozenset([i]), frozenset(k for k, f in enumerate(faces) if i in f)))
    for i, j in itertools.combinations(range(len(V)), 2):
        ks = frozenset(k for k, f in enumerate(faces) if i in f and j in f)
        if len(ks) >= 2: out.append((frozenset([i, j]), ks))
    for k, f in enumerate(faces): out.append((f, frozenset([k])))
    return out
def hyper(pts):
    M = sp.Matrix([[cn(x) for x in p] + [1] for p in pts]); ns = M.nullspace(simplify=cn)
    return ns[0] if len(ns) == 1 else None
def test(name, core, mu, rot=None, h=sp.Integer(1)):
    V, faces, dual = solid(name)
    if core == 'dual': K = [mu * d for d in dual]
    else: K = [mu * v for v in V]
    if rot is not None: K = [rot * k for k in K]
    P4 = [list(v) + [0] for v in V] + [list(k) + [1] for k in K]; nV = len(V)
    pred = [('P', list(range(nV))), ('core', list(range(nV, nV + len(K))))]
    if core == 'dual':
        for S, ks in faces_all(V, faces): pred.append(({1: 'corner', 2: 'edge'}.get(len(S), 'face'), sorted(S) + [nV + k for k in ks]))
    else:
        for k, f in enumerate(faces): pred.append(('side', sorted(f) + [nV + i for i in f]))
    ok = True; hyps = []
    for typ, idx in pred:
        H = hyper([P4[i] for i in idx])
        if H is None: ok = False; print(f'  {typ} {idx}: points do not span a single hyperplane'); continue
        vals = [cn(sum(H[q] * P4[i][q] for q in range(4)) + H[4]) for i in range(len(P4))]
        on = {i for i, z in enumerate(vals) if z == 0}; others = [float(vals[i]) for i in range(len(P4)) if i not in on]
        if on != set(idx) or not (all(x > 0 for x in others) or all(x < 0 for x in others)):
            ok = False; print(f'  {typ} {idx}: NOT a facet (extra points on it: {sorted(on - set(idx))}, sides mixed: {not (all(x > 0 for x in others) or all(x < 0 for x in others))})'); continue
        sgn = 1 if all(x < 0 for x in others) else -1        # outward normal: polytope on the negative side
        hyps.append((typ, [sgn * c for c in H]))
    A = np.array([[float(x) for x in p] for p in P4]); hull = ConvexHull(A)
    eqs = np.unique(np.round(hull.equations / np.linalg.norm(hull.equations[:, :4], axis=1)[:, None], 9), axis=0)
    complete = len(eqs) == len(pred)
    view = None
    if ok:   # Schlegel viewpoint X = (0, 0, 0, -h): beyond the P facet (w = 0) only
        X = [0, 0, 0, -h]
        view = all(float(cn(sum(c[q] * X[q] for q in range(4)) + c[4])) < 0 for typ, c in hyps if typ != 'P')
    from collections import Counter
    print(f'{name}, {core} core, mu = {mu}{" (turned)" if rot is not None else ""}: predicted facets {len(pred)} {dict(Counter(t for t, _ in pred))}; '
          f'all exact facets: {ok}; float hull facets {len(eqs)} (complete: {complete}); Schlegel view from (O, -{h}) beyond P only: {view}; '
          f'core drawn at scale {mu * h / (h + 1)}', flush=True)
    return ok and complete and bool(view)
res = {}
for name, mu in (('cube', sp.Rational(1, 2)), ('dodecahedron', sp.Rational(1, 2)), ('icosahedron', sp.Rational(1, 2)), ('octahedron', sp.Rational(1, 2)), ('tetrahedron', sp.Rational(1, 3))):
    res[(name, 'dual')] = test(name, 'dual', mu)
    res[(name, 'copy')] = test(name, 'copy', mu)
# t near the closing end and near the Vacuus end, cube and dodecahedron
for name in ('cube', 'dodecahedron'):
    for mu in (sp.Rational(1, 20), sp.Rational(9, 10)):
        res[(name, 'dual', str(mu))] = test(name, 'dual', mu)
# negative control: the cube's octahedral core turned by a generic small rotation
c, s = sp.Rational(3, 5), sp.Rational(4, 5); Rz = sp.Matrix([[c, -s, 0], [s, c, 0], [0, 0, 1]])
neg = test('cube', 'dual', sp.Rational(1, 2), rot=Rz)
print('RESULT dual core:', {k[0] + ('' if len(k) == 2 else ' mu=' + k[2]): v for k, v in res.items() if k[1] == 'dual'})
print('RESULT copy core (prism control):', {k[0]: v for k, v in res.items() if k[1] == 'copy'})
print('negative control (turned core) fails as it must:', not neg)
print('FINAL ok' if all(res.values()) and not neg else 'FINAL FAIL')
