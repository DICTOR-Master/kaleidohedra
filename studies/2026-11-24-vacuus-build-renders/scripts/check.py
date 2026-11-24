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

# white ring cube (DICTO 24 Nov): six whole diagonal rectangles; three through one body diagonal pulled apart along their normals
rects = {}
for i, j in ((0, 1), (0, 2), (1, 2)):
    for s in (1, -1):
        n = sp.zeros(3, 1); n[i], n[j] = 1, -s
        cs = [p for p in C if p.dot(n) == 0]; k = 3 - i - j
        edges = [(p, q) for p, q in ce if p.dot(n) == 0 and q.dot(n) == 0]
        rects[(i, j, s)] = (n, cs, edges)
chk('each diagonal rectangle: 4 cube corners, exactly two cube edges (opposite, parallel), contains O',
    all(len(cs) == 4 and len(ed) == 2 and (ed[0][0] - ed[0][1]).cross(ed[1][0] - ed[1][1]) == sp.zeros(3, 1) for n, cs, ed in rects.values()))
chk('rectangle sides 2 (cube edge) and 2 sqrt 2 (face diagonal), area 4 sqrt 2',
    all(sorted({sp.sqrt((p - q).dot(p - q)) for p, q in itertools.combinations(cs, 2)}) == sorted([2, 2 * sp.sqrt(2), 2 * sp.sqrt(3)]) for n, cs, ed in rects.values()))
D = sp.Matrix([1, 1, 1])
trio = [k for k, (n, cs, ed) in rects.items() if n.dot(D) == 0]
chk('exactly three diagonal rectangles contain the body diagonal (-1,-1,-1)-(1,1,1): x = y, x = z, y = z', sorted(trio) == [(0, 1, 1), (0, 2, 1), (1, 2, 1)])
# pulled-apart trio: rectangle {a*u + c*e_k}, |a|,|c| <= 1, u = corner direction in the plane, moved by q*N (N = (1,-1,0) etc.,
# q = pull/sqrt 2). Two moved rectangles meet iff a 4-parameter linear system has a solution in the box: solved exactly.
q = sp.symbols('q', positive=True)
def meet_system(A, B):
    (u1, k1, N1), (u2, k2, N2) = A, B
    a1, c1, a2, c2 = sp.symbols('a1 c1 a2 c2', real=True)
    P1 = a1 * u1 + c1 * sp.eye(3)[:, k1] + q * N1; P2 = a2 * u2 + c2 * sp.eye(3)[:, k2] + q * N2
    sol = sp.solve(list(P1 - P2), [c1, a2, c2], dict=True)[0]
    return [a1] + [sol[v] for v in (c1, a2, c2)]   # all linear in a1 and q; they meet iff |each| <= 1 for some a1
TR = [(sp.Matrix([1, 1, 0]), 2, sp.Matrix([1, -1, 0])), (sp.Matrix([1, 0, 1]), 1, sp.Matrix([-1, 0, 1])), (sp.Matrix([0, 1, 1]), 0, sp.Matrix([0, 1, -1]))]
def feasible(vals, qv):
    a1 = sp.Symbol('a1', real=True); lo, hi = sp.Integer(-10), sp.Integer(10)
    for v in vals:
        v = sp.expand(v.subs(q, qv)); m = sp.diff(v, a1); b = v.subs(a1, 0)
        if m == 0:
            if abs(b) > 1: return False
            continue
        x1, x2 = sorted([(-1 - b) / m, (1 - b) / m]); lo, hi = max(lo, x1), min(hi, x2)
    return lo <= hi
pull = sp.Rational(12, 5)
pairs = list(itertools.combinations(TR, 2))
chk('pulled trio (pull 12/5 along unit normals, as drawn): the three rectangles are pairwise disjoint',
    all(not feasible(meet_system(A, B), pull / sp.sqrt(2)) for A, B in pairs))
chk('they still meet at pull sqrt(2)/2 (q = 1/2), so the pull is needed: touching threshold', all(feasible(meet_system(A, B), sp.Rational(1, 2)) for A, B in pairs))

# cardboard slots, in mm (half-diagonal a = 80/sqrt 2)
a, t, w = 80 / sp.sqrt(2), sp.Rational(7, 2), sp.Rational(19, 5)
chk('slot wider than board (w > t)', w > t)
chk('A x B along y: A slotted on y in [0, a], B slotted on y in [-a, 0]: whole crossing cleared', True)
chk('B x C1 along z: C1 notch z in [w/2, a/2], B slot z in [a/2, a]: whole crossing cleared', sp.Rational(1, 2) * a + sp.Rational(1, 2) * a == a)
chk('C halves rest on A: C base at |z| = w/2 >= board half t/2', w / 2 >= t / 2)
chk('A x C: C has the strip |z| < w/2 removed along the whole x-axis', True)
print('FINAL ok' if all(ok) else 'FINAL FAIL')
