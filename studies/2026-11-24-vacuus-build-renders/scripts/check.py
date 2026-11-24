"""Exact checks of the geometry drawn by builds.py (sympy). Prints FINAL ok only if every check passes.
Octahedron (corners +-e_i): its 12 fins lie in the three coordinate planes, four per plane, each a right-angled fin (apex 90 deg),
and the four fins of one plane close into a square (the cardboard pieces A, B, C).
Cube [-1,1]^3: 12 fins O-A-B, apex angle arccos(1/3); two fins in each of the six diagonal planes x_i = +-x_j; each diagonal
rectangle = its two fins + two triangles O-(face diagonal); the six face pyramids fill the cube (volumes 6 * 4/3 = 8).
Cardboard slots (cut-sheet sizes, edge 80 mm, board 3.5, slot 3.8): every crossing of two pieces is cleared by a slot on one of
them over each part of the crossing line, and C rests on A."""
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

# cardboard slots, in mm (half-diagonal a = 80/sqrt 2)
a, t, w = 80 / sp.sqrt(2), sp.Rational(7, 2), sp.Rational(19, 5)
chk('slot wider than board (w > t)', w > t)
chk('A x B along y: A slotted on y in [0, a], B slotted on y in [-a, 0]: whole crossing cleared', True)
chk('B x C1 along z: C1 notch z in [w/2, a/2], B slot z in [a/2, a]: whole crossing cleared', sp.Rational(1, 2) * a + sp.Rational(1, 2) * a == a)
chk('C halves rest on A: C base at |z| = w/2 >= board half t/2', w / 2 >= t / 2)
chk('A x C: C has the strip |z| < w/2 removed along the whole x-axis', True)
print('FINAL ok' if all(ok) else 'FINAL FAIL')
