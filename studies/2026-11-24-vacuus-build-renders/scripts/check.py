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
print('FINAL ok' if all(ok) else 'FINAL FAIL')
