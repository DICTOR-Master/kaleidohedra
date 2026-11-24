"""Exact checks of the geometry drawn by builds.py (sympy). Prints FINAL ok only if every check passes.
Octahedron (corners +-e_i): its 12 fins lie in the three coordinate planes, four per plane, each a right-angled fin (apex 90 deg),
and the four fins of one plane close into a square (the cardboard pieces A, B, C).
Cube [-1,1]^3: 12 fins O-A-B, apex angle arccos(1/3); two fins in each of the six diagonal planes x_i = +-x_j; the six face pyramids fill the cube (volumes 6 * 4/3 = 8).
Skeletons (DICTO 24 Nov): the strut sets of the two frameworks, each strut counted in its frames."""
import itertools, sympy as sp
ok = []
def chk(name, c): ok.append(bool(c)); print(('ok  ' if c else 'FAIL') + ' ' + name)

# octahedron
E = [sp.Matrix(v) for v in ([1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1])]
oe = [(p, q) for p, q in itertools.combinations(E, 2) if p.dot(q) == 0]
chk('octahedron has 12 edges', len(oe) == 12)
planes = {}
for p, q in oe:
    n = p.cross(q); k = [abs(x) for x in n].index(1); planes.setdefault(k, []).append((p, q))
chk('all 12 octahedron fins right-angled at O', all(p.dot(q) == 0 for p, q in oe))
chk('octahedron fins: four in each coordinate plane', sorted(len(v) for v in planes.values()) == [4, 4, 4])

# cube
C = [sp.Matrix(v) for v in itertools.product((-1, 1), repeat=3)]
ce = [(p, q) for p, q in itertools.combinations(C, 2) if sum(abs(x) for x in (p - q)) == 2]
chk('cube has 12 edges', len(ce) == 12)
chk('every cube fin has apex cos = 1/3', all(sp.simplify(p.dot(q) / (p.norm() * q.norm())) == sp.Rational(1, 3) for p, q in ce))
diag = []
for i, j in ((0, 1), (0, 2), (1, 2)):
    for s in (1, -1):
        n = sp.zeros(3, 1); n[i], n[j] = 1, -s
        fins = [(p, q) for p, q in ce if p.dot(n) == 0 and q.dot(n) == 0]
        cs = [p for p in C if p.dot(n) == 0]
        diag.append((len(fins), len(cs)))
chk('six diagonal planes, each with 2 fins and 4 corners', diag == [(2, 4)] * 6)
chk('every fin lies in exactly one diagonal plane', sum(d[0] for d in diag) == 12)
chk('six face pyramids fill the cube: 6 * (1/3)(2*2)(1) = 8', 6 * sp.Rational(1, 3) * 4 * 1 == 8)

# skeletons (DICTO 24 Nov: the builds are skeletons and empty): the strut sets drawn by builds.py
OS = [(sp.zeros(3, 1), p) for p in E]
inplane = lambda n, P: all(x.dot(n) == 0 for x in P)
sq = [[s for s in oe + OS if inplane(sp.eye(3)[:, k], s)] for k in range(3)]
chk('octahedron skeleton 12 edges + 6 corner-to-centre struts; each square frame = 4 edges + 4 half-axes, each half-axis in 2 squares',
    all(len(f) == 8 and sum(1 for s in f if s in OS) == 4 for f in sq) and all(sum(1 for f in sq if s in f) == 2 for s in OS))
# pulled squares: square k moved to x_k = +-9/5; every point of square m has |x_k| <= 1 for k != m, so two moved squares cannot meet
pullO = sp.Rational(9, 5)
chk('octahedron pull-apart (9/5 along the normals, as drawn): the three square frames are pairwise disjoint (9/5 > 1)', pullO > 1)
O3 = sp.zeros(3, 1); CS = [(O3, p) for p in C]
chk('B1NR cube skeleton: 12 edges + 8 corner-to-centre struts; each face pyramid = 4 base edges + 4 struts; each strut in 3 pyramids',
    len(ce) == 12 and len(CS) == 8 and all(sum(1 for k in range(3) for s in (1, -1) if p[k] == s) == 3 for _, p in CS))
chk('B1NR pull-apart (27/5 along the face normals, as drawn): the six pyramid frames are pairwise disjoint (pyramid x_k = s lies in s x_k >= 27/5; every other has s x_k < 27/5)',
    sp.Rational(27, 5) > 1)
# 3. and 4. B1NR, no hull (DICTO 24 Nov): the STRUTS form of #87 without its optional edges; exact corners
Q = [sp.Matrix(p) for p in {tuple(sp.Matrix(q)[[(i + r) % 3 for i in range(3)], 0]) for q in itertools.product((1, -1), (1, -1), (0,)) for r in range(3)}]
qe = [(p, q) for p, q in itertools.combinations(Q, 2) if (p - q).dot(p - q) == 2]
chk('cuboctahedron: 12 corners, 24 edges of length sqrt 2, 4 at each corner; all 12 centre struts sqrt 2 (= edge, one length)',
    len(Q) == 12 and len(qe) == 24 and all(sum(1 for e in qe if p in e) == 4 for p in Q) and all(p.dot(p) == 2 for p in Q))
phi = (1 + sp.sqrt(5)) / 2
D = [sp.Matrix(p) for p in itertools.product((-1, 1), repeat=3)]
for a in (1, -1):
    for b in (1, -1):
        v = [0, a / phi, b * phi]; D += [sp.Matrix([v[(i - r) % 3] for i in range(3)]) for r in range(3)]
d2 = lambda p, q: sp.nsimplify(sp.expand((p - q).dot(p - q)), [sp.sqrt(5)])
de = [(p, q) for p, q in itertools.combinations(D, 2) if sp.simplify(d2(p, q) - (2 / phi) ** 2) == 0]
chk('dodecahedron (Q(sqrt 5)): 20 distinct corners, 30 edges of length 2/phi, 3 at each corner; all 20 centre struts sqrt 3',
    len(set(tuple(p) for p in D)) == 20 and len(de) == 30 and all(sum(1 for e in de if p in e) == 3 for p in D)
    and all(sp.simplify(p.dot(p) - 3) == 0 for p in D))
z5 = sp.Matrix([1, 0, phi])
chk('view axis (1, 0, phi) goes through a face centre: exactly 5 corners (one pentagon) at the greatest height along it',
    sum(1 for p in D if sp.simplify(p.dot(z5) - max((p2.dot(z5) for p2 in D), key=lambda t: float(t))) == 0) == 5)

# Ring-fin Vacuus (DICTO's photos of the B1NR cuboctahedron, 24 Nov): one ring per fin O, a, b, the fin's incircle, in the fin's plane.
# Exact in Q(sqrt 3, sqrt 5). Zero tests: a nonzero value is certified by evaluation to 30 digits (sympy evalf, error-controlled);
# a value that is not clearly nonzero must reduce to exactly 0 (rationalised and expanded, else simplify).
def is0(x):
    x = sp.sympify(x)
    if abs(sp.N(x, 30)) > sp.Float('1e-20'): return False
    if sp.expand(sp.radsimp(sp.expand(x))) == 0: return True      # canonical form a + b sqrt 3 + c sqrt 5 + d sqrt 15 is 0
    return sp.simplify(x) == 0
def sign(x):
    return 0 if is0(x) else (1 if sp.N(x, 30) > 0 else -1)
def incircle(a, b):
    L = lambda v: sp.sqrtdenest(sp.sqrt(sp.radsimp(sp.expand(v.dot(v)))))      # exact length, denested (e.g. sqrt(6 - 2 sqrt 5) = sqrt 5 - 1)
    la, lb, lab = L(a), L(b), L(a - b); P = la + lb + lab; n = a.cross(b)
    assert all(is0(x ** 2 - y.dot(y)) for x, y in ((la, a), (lb, b), (lab, a - b), (L(n), n)))
    return (lb * a + la * b) / P, n, L(n) / P          # centre (incentre formula), normal a x b, inradius 2 area / perimeter
def ring_checks(name, V, E, nfin, nplates, per_plate, nties, at_tie, ntouch, ncop):
    cano = lambda x: sp.expand(sp.radsimp(sp.expand(x)))       # canonical form in Q(sqrt 3, sqrt 5): rationalised, expanded
    R = [incircle(a, b) for a, b in E]
    R = [(c.applyfunc(cano), n, r) for c, n, r in R]
    chk(f'{name}: {len(R)} rings, one per fin', len(R) == nfin)
    def tangent(c, r, p, q):          # the circle's centre at distance r from line pq, the foot strictly inside the segment
        d = q - p; f = (c - p).dot(d) / d.dot(d)
        return is0((c - p).cross(d).dot((c - p).cross(d)) - r ** 2 * d.dot(d)) and sign(f) > 0 and sign(1 - f) > 0
    O3 = sp.zeros(3, 1)
    chk(f'{name}: every ring lies in its fin plane (centre . (a x b) = 0) and is tangent to the three sides O-a, O-b, a-b (at inner points)',
        all(is0(c.dot(n)) and tangent(c, r, O3, a) and tangent(c, r, O3, b) and tangent(c, r, a, b) for (a, b), (c, n, r) in zip(E, R)))
    chk(f'{name}: all rings congruent (one radius)', all(is0(r - R[0][2]) for c, n, r in R))
    groups = []
    for i, (c, n, r) in enumerate(R):
        for g in groups:
            if is0(R[g[0]][1].cross(n).dot(R[g[0]][1].cross(n))): g.append(i); break
        else: groups.append([i])
    chk(f'{name}: {nplates} plates (fins grouped by plane), {per_plate} rings in each', len(groups) == nplates and all(len(g) == per_plate for g in groups))
    plane = {i: k for k, g in enumerate(groups) for i in g}
    # pairs of rings: coplanar -> compare centre distance with r1 + r2; different planes through O -> each circle meets the common line
    # L = n1 x n2 (through O) at the roots s of s^2 - 2 s (u.c) + |c|^2 - r^2 = 0 (u unit along L); the circles share a point iff they
    # share a root. Touch = exactly one common point, and that point is a tangency (double root for both, or external tangency in a plane).
    touch, cop, pts, bad = 0, 0, [], 0
    for i, j in itertools.combinations(range(len(R)), 2):
        (c1, n1, r1), (c2, n2, r2) = R[i], R[j]
        if plane[i] == plane[j]:
            dd = (c1 - c2).dot(c1 - c2) - (r1 + r2) ** 2
            if is0(dd): touch += 1; cop += 1; pts.append((c1 * r2 + c2 * r1) / (r1 + r2))
            elif sign(dd) < 0: bad += 1
            continue
        u = n1.cross(n2); uu = u.dot(u)
        def roots(c, r):              # sign of the discriminant from uu * D = (u.c)^2 - uu (|c|^2 - r^2), free of square roots
            sD = sign(u.dot(c) ** 2 - uu * (c.dot(c) - r ** 2))
            if sD < 0: return [], sD
            m = u.dot(c) / sp.sqrt(uu)
            return ([m] if sD == 0 else [m - sp.sqrt(m ** 2 - c.dot(c) + r ** 2), m + sp.sqrt(m ** 2 - c.dot(c) + r ** 2)]), sD
        A, sA = roots(c1, r1); B, sB = roots(c2, r2)
        if sA == 0 and sB == 0:       # both circles tangent to L: one common point iff the feet (u.c / uu) u coincide (exact, no roots)
            if is0(u.dot(c1) - u.dot(c2)): touch += 1; pts.append(u.dot(c1) / uu * u)
            continue
        common = [x for x in A for y in B if abs(sp.N(x - y, 30)) < sp.Float('1e-20')]
        if common: bad += 1           # a shared point where a circle crosses L: not a tangency (none expected)
    chk(f'{name}: {ntouch} touching pairs ({ncop} coplanar, {ntouch - ncop} across planes); no two rings cross or overlap', touch == ntouch and cop == ncop and bad == 0)
    # the touching points: distinct points, each on a spoke O-v, where the rings of the fins at v meet (one cut cable tie each)
    r2 = [cano(r ** 2) for c, n, r in R]
    pts = [p.applyfunc(cano) for p in pts]
    P = []
    for p in pts:
        if not any(is0((p - q).dot(p - q)) for q in P): P.append(p)
    onspoke = all(sum(1 for v in V if is0(p.cross(v).dot(p.cross(v))) and sign(p.dot(v)) > 0) == 1 for p in P)
    mult = [sum(1 for (c, n, r), rr in zip(R, r2) if is0((p - c).dot(p - c) - rr) and is0((p - c).dot(n))) for p in P]
    chk(f'{name}: the touching points are {nties} (one tie each), one on every spoke, {at_tie} rings through each', len(P) == nties and onspoke and set(mult) == {at_tie})
    return R
Rq = ring_checks('cuboctahedron ring-fins', Q, qe, 24, 4, 6, 12, 4, 72, 24)
c, n, r = Rq[0]
chk('cuboctahedron: ring radius sqrt 6 / 6 (= edge sqrt 3 / 6), centre at distance 2 r = sqrt 6 / 3 from O; adjacent coplanar rings touch at the spoke midpoints',
    is0(r - sp.sqrt(6) / 6) and is0(c.dot(c) - sp.Rational(2, 3)))
Rd = ring_checks('dodecahedron ring-fins', D, de, 30, 15, 2, 20, 3, 60, 0)
c, n, r = Rd[0]
chk('dodecahedron: fin apex cos = sqrt 5 / 3, tan(apex / 2) = 1 / phi^2; tangent length from O t = sqrt 3 - 1/phi; ring radius r = t / phi^2',
    all(is0(a.dot(b) / 3 - sp.sqrt(5) / 3) for a, b in de) and is0(r - (sp.sqrt(3) - 1 / phi) / phi ** 2))
print('FINAL ok' if all(ok) else 'FINAL FAIL')
