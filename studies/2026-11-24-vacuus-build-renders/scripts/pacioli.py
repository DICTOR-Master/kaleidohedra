"""Pacioli's three golden rectangles against the Vacuus (plates: the plane through the centre O and an edge) and the Resonus
(the planes through O parallel to each face) of the icosahedron, dodecahedron and icosidodecahedron. Exact, in Q(sqrt 5) (sympy).
Icosahedron: the 12 cyclic permutations of (0, +-1, +-phi), edge 2; the three rectangles are its corners in x = 0, y = 0, z = 0.
Dodecahedron (its dual): (+-1,+-1,+-1) and the cyclic permutations of (0, +-1/phi, +-phi), edge 2/phi.
Icosidodecahedron: the 30 midpoints of the icosahedron's edges, edge 1.  Prints FINAL ok only if every check passes."""
import itertools, sympy as sp
phi = (1 + sp.sqrt(5)) / 2
ok = []
def chk(name, c): ok.append(bool(c)); print(('ok  ' if c else 'FAIL') + ' ' + name)
def cyc(v): return [sp.Matrix(v), sp.Matrix([v[2], v[0], v[1]]), sp.Matrix([v[1], v[2], v[0]])]
def signs(v): return [sp.Matrix([s0 * v[0], s1 * v[1], s2 * v[2]]) for s0, s1, s2 in itertools.product((1, -1), repeat=3)]
def uniq(L):
    out = []
    for p in L:
        p = p.applyfunc(sp.nsimplify)
        if not any(sp.simplify((p - q).norm()) == 0 for q in out): out.append(p)
    return out
d2 = lambda p, q: sp.nsimplify(sp.expand((p - q).dot(p - q)))
def solid(V):
    D = sorted({d2(p, q) for p, q in itertools.combinations(V, 2)}, key=lambda x: float(x))
    E = [(p, q) for p, q in itertools.combinations(V, 2) if d2(p, q) == D[0]]
    return D[0], E
def faces(V, E):                                   # face planes: supporting planes n.x = c through >= 3 corners with all corners on one side
    F = []
    for a, b, c in itertools.combinations(V, 3):
        n = (b - a).cross(c - a).applyfunc(sp.nsimplify)
        if n.norm() == 0: continue
        h = [sp.nsimplify(sp.expand(n.dot(p - a))) for p in V]
        if all(x >= 0 for x in h) or all(x <= 0 for x in h):
            nn = (n / n.norm()).applyfunc(sp.nsimplify)
            if not any(sp.simplify((nn - m).norm()) == 0 or sp.simplify((nn + m).norm()) == 0 for m in F): F.append(nn)
    return F
ICO = uniq([w for v in cyc([0, 1, phi]) for w in signs(v)])
DOD = uniq(signs([1, 1, 1]) + [w for v in cyc([0, 1 / phi, phi]) for w in signs(v)])
chk('icosahedron 12 corners, dodecahedron 20', len(ICO) == 12 and len(DOD) == 20)
eI, EI = solid(ICO); eD, ED = solid(DOD)
IDD = uniq([((p + q) / 2) for p, q in EI]); eX, EX = solid(IDD)
chk('edges: icosahedron 30 (length 2), dodecahedron 30 (2/phi), icosidodecahedron 60 (1), 30 corners',
    len(EI) == 30 and eI == 4 and len(ED) == 30 and sp.simplify(eD - 4 / phi**2) == 0 and len(EX) == 60 and eX == 1 and len(IDD) == 30)
FI, FD, FX = faces(ICO, EI), faces(DOD, ED), faces(IDD, EX)
chk('face planes up to sign: icosahedron 10, dodecahedron 6, icosidodecahedron 10 + 6 = 16', (len(FI), len(FD), len(FX)) == (10, 6, 16))
P = [sp.Matrix([1, 0, 0]), sp.Matrix([0, 1, 0]), sp.Matrix([0, 0, 1])]   # normals of the three Pacioli planes x = 0, y = 0, z = 0
for k, n in enumerate(P):
    R = [p for p in ICO if p.dot(n) == 0]
    sides = sorted(sp.sqrt(d2(R[0], q)) for q in R[1:])
    chk(f'plane {"xyz"[k]} = 0: 4 icosahedron corners, a golden rectangle (sides 2, 2 phi, diagonal 2 sqrt(phi+2))',
        len(R) == 4 and sp.simplify(sides[0] - 2) == 0 and sp.simplify(sides[1] - 2 * phi) == 0)
    ein = [(p, q) for p, q in EI if p.dot(n) == 0 and q.dot(n) == 0]
    chk(f'  (a) its two short sides are icosahedron edges, the only two in the plane: plane = Vacuus plate plane of the icosahedron', len(ein) == 2)
    chk(f'  (b) not an icosahedron Resonus plane (no face parallel)', all(sp.simplify(m.cross(n).norm()) != 0 for m in FI))
    chk(f'  (b) not a dodecahedron Resonus plane', all(sp.simplify(m.cross(n).norm()) != 0 for m in FD))
    dn = [(p, q) for p, q in ED if p.dot(n) == 0 and q.dot(n) == 0]
    par = all(sp.simplify((p - q).cross(ein[0][0] - ein[0][1]).norm()) == 0 for p, q in dn)
    chk(f'  (c) dodecahedron: the plane holds exactly two opposite dodecahedron edges (a Vacuus plate plane), parallel to the short sides', len(dn) == 2 and par)
    DR = [p for p in DOD if p.dot(n) == 0]
    ds = sorted(d2(DR[0], q) for q in DR[1:])
    chk(f'  (c) its 4 dodecahedron corners make a rectangle of sides 2/phi and 2 phi (ratio phi^2, not golden)',
        len(DR) == 4 and sp.simplify(ds[0] - 4 / phi**2) == 0 and sp.simplify(ds[1] - 4 * phi**2) == 0)
    xn = [(p, q) for p, q in EX if p.dot(n) == 0 and q.dot(n) == 0]
    XR = [p for p in IDD if p.dot(n) == 0]
    mids = [((p + q) / 2) for p, q in ein]
    chk(f'  (c) icosidodecahedron: no edge in the plane (not a Vacuus plate plane) and no face parallel (not Resonus)',
        len(xn) == 0 and all(sp.simplify(m.cross(n).norm()) != 0 for m in FX))
    chk(f'  (c) the plane holds 4 icosidodecahedron corners, a square of side phi sqrt 2; two are the midpoints of the short sides',
        len(XR) == 4 and {d2(XR[0], q) for q in XR[1:]} == {sp.nsimplify(sp.expand(2 * phi**2)), sp.nsimplify(sp.expand(4 * phi**2))}
        and all(any(sp.simplify((m - x).norm()) == 0 for x in XR) for m in mids))
chk('the three planes are mutually perpendicular', all(P[i].dot(P[j]) == 0 for i in range(3) for j in range(i + 1, 3)))
# all fifteen: every icosahedron plane through O and an edge holds exactly two opposite edges and a golden rectangle
planes = []
for p, q in EI:
    n = p.cross(q).applyfunc(sp.nsimplify); n = n / n.norm()
    if not any(sp.simplify(n.cross(m).norm()) == 0 for m in planes): planes.append(n)
gold = all(len([1 for a, b in EI if sp.simplify(a.dot(n)) == 0 and sp.simplify(b.dot(n)) == 0]) == 2 for n in planes)
trip = sum(1 for a, b, c in itertools.combinations(planes, 3) if all(sp.simplify(x.dot(y)) == 0 for x, y in ((a, b), (a, c), (b, c))))
chk('the icosahedron has 15 such planes (one per opposite edge pair), each with two edges; they make 5 mutually perpendicular triples',
    len(planes) == 15 and gold and trip == 5)
# Pacioli's 12th effect (Divina proportione, Cap. XXI): a line a cut in mean and extreme ratio, major part M, minor part m;
# sqrt(a^2 + M^2) : sqrt(a^2 + m^2) = cube edge : icosahedron edge, both in one sphere. Our reading: the first root is the diagonal
# of the golden rectangle (sides M, a), the second the diagonal of the phi^2 rectangle (sides m, a), the two rectangles found above.
a = sp.Integer(1); M = a / phi; m = a - M
lhs = sp.sqrt(a**2 + M**2) / sp.sqrt(a**2 + m**2)
D = 2 * sp.sqrt(1 + phi**2)                                 # circumdiameter of the icosahedron above (edge 2) = rectangle diagonal
rhs = (D / sp.sqrt(3)) / 2                                  # cube edge in that sphere : icosahedron edge 2
chk("Pacioli's 12th effect holds: sqrt(a^2+M^2)/sqrt(a^2+m^2) = cube edge / icosahedron edge (same sphere)", sp.simplify(lhs - rhs) == 0)
chk('  (a, M) is a golden rectangle and (a, m) a phi^2 rectangle (the dodecahedron one in the same plane)',
    sp.simplify(a / M - phi) == 0 and sp.simplify(a / m - phi**2) == 0)
chk('  the dodecahedron rectangle diagonal is the dodecahedron circumdiameter 2 sqrt 3',
    sp.simplify(4 / phi**2 + 4 * phi**2 - 12) == 0 and all(sp.simplify(p.dot(p) - 3) == 0 for p in DOD))
print('FINAL ok' if all(ok) else 'FINAL FAIL')
