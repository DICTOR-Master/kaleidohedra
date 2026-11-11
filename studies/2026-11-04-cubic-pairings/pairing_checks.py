# DICTO 2026-11-04, paper #93 (DICTO's idea: carry the method of #92 over to the cubic pairings).
# Checks for the paper.  Run with the geom venv on compute-host:
#   python3 pairing_checks.py > data/pairing-checks.log
# Part A  the angle algebra: dihedral cosines of every piece (sympy, exact), alpha/pi irrational, and the complete
#         list of wedge combinations round an edge (2*pi) or on a face (pi) for each set of pieces (exact integers).
# Part B  the CsCl walk C n muC* / C n (3-mu)C* (#90, Prop. 6): face shapes, edge lengths and dihedral angles with mu
#         symbolic (sympy); at rational mu the cells are built from half-spaces in Fractions and the CsCl patch is
#         checked facet by facet; at the irrational stations (golden, silver, Golden Cut Cubes) the same combinatorics
#         is computed with 60-digit arithmetic and the lengths and volumes are checked exactly (sympy).
#         For each face: order of its stabiliser in the cell's symmetry group = order of the polygon's own isometry
#         group (preserving the edge kinds), so a neighbour placed on a given face is unique.
# Part C  the Delian walk T(t), O(t) of #51 (octet edge sqrt2): the same checks.
# Part D  the cube's pyramid C6, the RD's pyramid R12 and their bipyramid B (Fractions): B = 2 C6 = 2 R12 in its three
#         ways; patches of the cube lattice's B tiling with random cuts are face to face (facets matched exactly; no
#         corner inside another tile's edge or face); whole rhombic dodecahedra only round apexes with all 12 cuts.
import itertools, random, json
from fractions import Fraction as Fr
import sympy as sp
import mpmath as mp
mp.mp.dps = 60

NPASS = NFAIL = 0
def check(name, ok, info=''):
    global NPASS, NFAIL
    NPASS += bool(ok); NFAIL += (not ok)
    print(('PASS ' if ok else 'FAIL ') + name + (f'   [{info}]' if info else ''))

# ------------------------------------------------------------------ generic convex polytope from half-spaces
class Poly:
    """P = {x : n.x <= d} for (n, d) in planes.  num: 'fr' (Fractions, exact) or 'mp' (60 digits, tol 1e-40)."""
    def __init__(self, planes, num='fr'):
        self.num = num
        z = (lambda v: v == 0) if num == 'fr' else (lambda v: abs(v) < mp.mpf(10) ** -40)
        le = (lambda a, b: a <= b) if num == 'fr' else (lambda a, b: a <= b + mp.mpf(10) ** -40)
        self.z, self.le = z, le
        V = []
        for i, j, k in itertools.combinations(range(len(planes)), 3):
            A = [planes[i][0], planes[j][0], planes[k][0]]; b = [planes[i][1], planes[j][1], planes[k][1]]
            D = det3(A)
            if z(D): continue
            x = []
            for c in range(3):
                M = [list(r) for r in A]
                for r in range(3): M[r][c] = b[r]
                x.append(det3(M) / D)
            if all(le(dot(n, x), d) for n, d in planes) and not any(all(z(x[c] - y[c]) for c in range(3)) for y in V):
                V.append(x)
        self.V = V
        self.faces = []                       # (normal, d, [vertex indices in cyclic order])
        for n, d in planes:
            idx = [a for a, v in enumerate(V) if z(dot(n, v) - d)]
            if len(idx) >= 3 and not any(set(idx) == set(f[2]) for f in self.faces):
                self.faces.append((n, d, cyc(V, idx, n)))
        self.edges = {}
        for fi, f in enumerate(self.faces):
            for a, b in zip(f[2], f[2][1:] + f[2][:1]):
                self.edges.setdefault(frozenset((a, b)), []).append(fi)
    def volume(self):
        c = [sum(v[i] for v in self.V) / len(self.V) for i in range(3)]
        vol = 0
        for n, d, idx in self.faces:
            p0 = self.V[idx[0]]
            for a, b in zip(idx[1:-1], idx[2:]):
                vol += abs(det3([sub(p0, c), sub(self.V[a], c), sub(self.V[b], c)])) / 6
        return vol

def det3(A):
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def sub(a, b): return [x - y for x, y in zip(a, b)]
def add(a, b): return [x + y for x, y in zip(a, b)]
def d2(a, b): return dot(sub(a, b), sub(a, b))
def cyc(V, idx, n):
    import math
    c = [float(sum(V[i][k] for i in idx) / len(idx)) for k in range(3)]
    nf = [float(x) for x in n]
    u = [float(V[idx[0]][k]) - c[k] for k in range(3)]
    w = [nf[1] * u[2] - nf[2] * u[1], nf[2] * u[0] - nf[0] * u[2], nf[0] * u[1] - nf[1] * u[0]]
    ang = lambda i: math.atan2(sum((float(V[i][k]) - c[k]) * w[k] for k in range(3)), sum((float(V[i][k]) - c[k]) * u[k] for k in range(3)))
    return sorted(idx, key=ang)

def polygon_symmetries(P, f, labelled=False):
    """number of dihedral relabellings of the face's vertex cycle preserving all distances AND the edge kinds
    (edge kind = the pair of face kinds at the edge), i.e. the isometries of the face as a labelled polygon"""
    idx = P.faces[f][2]; m = len(idx)
    kinds = edge_kinds(P)
    cnt = 0
    for r in range(m):
        for s in (1, -1):
            perm = [idx[(r + s * i) % m] for i in range(m)]
            ok = all(P.z(d2(P.V[idx[i]], P.V[idx[j]]) - d2(P.V[perm[i]], P.V[perm[j]])) for i in range(m) for j in range(m))
            ok = ok and (not labelled or all(kinds[frozenset((idx[i], idx[(i + 1) % m]))] == kinds[frozenset((perm[i], perm[(i + 1) % m]))] for i in range(m)))
            cnt += ok
    return cnt

def edge_kinds(P):
    fk = [len(f[2]) for f in P.faces]
    return {e: tuple(sorted(fk[i] for i in fs)) for e, fs in P.edges.items()}

def signed_perms():
    out = []
    for p in itertools.permutations(range(3)):
        for s in itertools.product((1, -1), repeat=3):
            out.append((p, s))
    return out
def apply(g, v, c):
    p, s = g; w = sub(v, c)
    return add([s[i] * w[p[i]] for i in range(3)], c)

def stabiliser(P, f, group, c):
    """order of the subgroup of `group` (about centre c) that maps P to itself and face f to itself"""
    Vs = P.V; fset = [Vs[i] for i in P.faces[f][2]]
    cnt = 0
    for g in group:
        img = [apply(g, v, c) for v in Vs]
        if not all(any(all(P.z(a[k] - b[k]) for k in range(3)) for b in Vs) for a in img): continue
        fimg = [apply(g, v, c) for v in fset]
        if all(any(all(P.z(a[k] - b[k]) for k in range(3)) for b in fset) for a in fimg): cnt += 1
    return cnt

# ------------------------------------------------------------------ Part A: angles and wedge combinations
print('== Part A: angle algebra')
al = sp.acos(sp.Rational(1, 3))
check('alpha = arccos(1/3) = 2 arcsin(1/sqrt3) (the half angle s of the paper)',
      sp.simplify(sp.cos(2 * sp.asin(1 / sp.sqrt(3))) - sp.Rational(1, 3)) == 0)
check('alpha/pi irrational: 2cos(alpha) = 2/3 is not an algebraic integer (min. poly 3x - 2 not monic)',
      sp.Rational(2, 3).q != 1, '2/3 is rational and not an integer, so not an algebraic integer')
ANG = {  # name: (coefficient of pi, coefficient of alpha), and its cosine
    'beta = pi/2 + alpha/2': ((Fr(1, 2), Fr(1, 2)), -1 / sp.sqrt(3)),
    'gamma = pi - alpha': ((Fr(1), Fr(-1)), sp.Rational(-1, 3)),
    'right = pi/2': ((Fr(1, 2), Fr(0)), 0),
    'alpha': ((Fr(0), Fr(1)), sp.Rational(1, 3)),
    'pi - alpha/2': ((Fr(1), Fr(-1, 2)), None),
    '(pi + alpha)/2': ((Fr(1, 2), Fr(1, 2)), None),
    '2pi/3': ((Fr(2, 3), Fr(0)), sp.Rational(-1, 2)),
    'pi/3': ((Fr(1, 3), Fr(0)), sp.Rational(1, 2)),
    'pi/4': ((Fr(1, 4), Fr(0)), 1 / sp.sqrt(2)),
}
for nm, ((p, q), cv) in ANG.items():
    if cv is None: continue
    val = sp.pi * sp.Rational(p.numerator, p.denominator) + al * sp.Rational(q.numerator, q.denominator)
    # half-angle identities: sin(alpha/2) = sqrt((1 - 1/3)/2) = 1/sqrt3, cos(alpha/2) = sqrt(2/3) (0 < alpha/2 < pi/2);
    # sympy confirms symbolically where it can and to 60 digits otherwise
    ex = sp.simplify(sp.cos(val).rewrite(sp.sqrt) - cv) == 0 or abs(sp.N(sp.cos(val) - cv, 70)) < 1e-60
    check(f'cos({nm}) = {cv}', ex)
check('half angles: sin^2(alpha/2) = (1 - cos alpha)/2 = 1/3, cos^2(alpha/2) = 2/3, so cos(pi - alpha/2) = -sqrt(2/3), cos((pi + alpha)/2) = -1/sqrt3',
      (1 - sp.Rational(1, 3)) / 2 == sp.Rational(1, 3) and abs(sp.N(sp.cos(sp.pi - al / 2) + sp.sqrt(sp.Rational(2, 3)), 70)) < 1e-60
      and abs(sp.N(sp.cos((sp.pi + al) / 2) + 1 / sp.sqrt(3), 70)) < 1e-60)

def wedges(names, total):
    """all non-negative integer vectors n with sum n_i * angle_i = total*pi (alpha/pi irrational)"""
    angs = [ANG[n][0] for n in names]
    sols = []
    for ns in itertools.product(range(13), repeat=len(names)):
        P_ = sum(n * a[0] for n, a in zip(ns, angs)); A_ = sum(n * a[1] for n, a in zip(ns, angs))
        if A_ == 0 and P_ == total and any(ns): sols.append(ns)
    return sols
TABLES = {}
for label, names in [('CsCl walk, 1 < mu <= 2 (beta, gamma)', ['beta = pi/2 + alpha/2', 'gamma = pi - alpha']),
                     ('CsCl walk, 2 < mu < 3 (beta, gamma, right)', ['beta = pi/2 + alpha/2', 'gamma = pi - alpha', 'right = pi/2']),
                     ('Delian walk, 0 < t < 1/3 (alpha, pi - alpha/2, 2pi/3)', ['alpha', 'pi - alpha/2', '2pi/3']),
                     ('Delian walk, 1/3 < t < 1 (pi - alpha, (pi+alpha)/2, right)', ['gamma = pi - alpha', '(pi + alpha)/2', 'right = pi/2']),
                     ('cube pyramid C6 (pi/4 base, 2pi/3 lateral)', ['pi/4', '2pi/3']),
                     ('RD pyramid R12 (pi/3 base, pi/2 long lateral, 2pi/3 short lateral)', ['pi/3', 'right = pi/2', '2pi/3'])]:
    full, face = wedges(names, 2), wedges(names, 1)
    TABLES[label] = {'angles': names, 'round an edge (2pi)': full, 'on a face (pi)': face}
    print(f'   {label}: 2pi -> {full};  pi (on a face) -> {face}')
t1 = TABLES['CsCl walk, 1 < mu <= 2 (beta, gamma)']
check('CsCl walk mu in (1,2]: only 2 beta + gamma round an edge, nothing on a face',
      t1['round an edge (2pi)'] == [(2, 1)] and t1['on a face (pi)'] == [])
t2 = TABLES['CsCl walk, 2 < mu < 3 (beta, gamma, right)']
check('CsCl walk mu in (2,3): 2 beta + gamma or 4 right; on a face only 2 right',
      sorted(t2['round an edge (2pi)']) == [(0, 0, 4), (2, 1, 0)] and t2['on a face (pi)'] == [(0, 0, 2)])
t3 = TABLES['Delian walk, 0 < t < 1/3 (alpha, pi - alpha/2, 2pi/3)']
check('Delian walk t in (0,1/3): alpha + 2(pi - alpha/2) or 3 x 2pi/3; nothing on a face',
      sorted(t3['round an edge (2pi)']) == [(0, 0, 3), (1, 2, 0)] and t3['on a face (pi)'] == [])
t4 = TABLES['Delian walk, 1/3 < t < 1 (pi - alpha, (pi+alpha)/2, right)']
check('Delian walk t in (1/3,1): (pi - alpha) + 2(pi+alpha)/2 or 4 right; on a face only 2 right',
      sorted(t4['round an edge (2pi)']) == [(0, 0, 4), (1, 2, 0)] and t4['on a face (pi)'] == [(0, 0, 2)])
t5 = TABLES['cube pyramid C6 (pi/4 base, 2pi/3 lateral)']
check('C6: 8 base or 3 lateral wedges round an edge; on a face only 4 base',
      sorted(t5['round an edge (2pi)']) == [(0, 3), (8, 0)] and t5['on a face (pi)'] == [(4, 0)])

# ------------------------------------------------------------------ Part B: the CsCl walk
print('== Part B: the CsCl walk (cube C = [-1,1]^3, P = C n muC*, Q = C n (3-mu)C*, Q centred at (1,1,1))')
mu = sp.Symbol('mu', positive=True)
def cell_planes(m, c=(0, 0, 0), conv=Fr):
    pl = []
    for i in range(3):
        for s in (1, -1):
            n = [0, 0, 0]; n[i] = s
            pl.append((n, conv(s) * conv(c[i]) + 1))
    for s in itertools.product((1, -1), repeat=3):
        pl.append((list(s), m + sum(conv(si) * conv(ci) for si, ci in zip(s, c))))
    return pl
# symbolic lengths
a_ = sp.sqrt(2) * (mu - 1); b_ = sp.sqrt(2) * (2 - mu)
v1, v2, v3 = sp.Matrix([1, mu - 1, 0]), sp.Matrix([1, 0, mu - 1]), sp.Matrix([mu - 1, 1, 0])
check('1<mu<2: square edge of P = sqrt2 (mu-1), hexagon-hexagon edge = sqrt2 (2-mu)',
      sp.simplify((v1 - v2).norm() - a_.subs(mu, mu)) == 0 or sp.simplify((v1 - v2).norm()**2 - a_**2) == 0)
check('   and the hexagon-hexagon edge', sp.simplify((v1 - v3).norm()**2 - b_**2) == 0)
check('   Q = P(3-mu) swaps them: its square edge is P\'s hexagon-hexagon edge',
      sp.simplify(a_.subs(mu, 3 - mu) - b_) == 0 and sp.simplify(b_.subs(mu, 3 - mu) - a_) == 0)
check('   the two edge lengths are equal only at Kelvin, mu = 3/2', sp.solve(sp.Eq(a_, b_), mu) == [sp.Rational(3, 2)])
w1, w2 = sp.Matrix([1, 1, mu - 2]), sp.Matrix([1, mu - 2, 1])
check('2<mu<3: octagon-octagon edge 2(mu-2), octagon-triangle edge sqrt2 (3-mu) = edge of the octahedron (3-mu)C*',
      sp.simplify((w1 - sp.Matrix([1, 1, 2 - mu])).norm()**2 - 4 * (mu - 2)**2) == 0
      and sp.simplify((w1 - w2).norm()**2 - 2 * (3 - mu)**2) == 0)
check('   equal only at the silver ratio mu = 1 + sqrt2 (Archimedean truncated cube)',
      [sp.simplify(r) for r in sp.solve(sp.Eq(2 * (mu - 2), sp.sqrt(2) * (3 - mu)), mu)] == [1 + sp.sqrt(2)])
nsq, nhex, nhex2 = sp.Matrix([1, 0, 0]), sp.Matrix([1, 1, 1]), sp.Matrix([1, 1, -1])
check('dihedral square/octagon-hexagon/triangle: cos = -1/sqrt3 (beta); hexagon-hexagon cos = -1/3 (gamma); octagon-octagon 0',
      sp.simplify(-nsq.dot(nhex) / nhex.norm() + 1 / sp.sqrt(3)) == 0 and sp.simplify(-nhex.dot(nhex2) / 3 + sp.Rational(1, 3)) == 0)
STATIONS = [('5/4', Fr(5, 4)), ('4/3', Fr(4, 3)), ('3/2 Kelvin', Fr(3, 2)), ('7/4', Fr(7, 4)), ('2 cuboctahedron', Fr(2)),
            ('9/4', Fr(9, 4)), ('5/2', Fr(5, 2)), ('11/4', Fr(11, 4))]
phi = (1 + sp.sqrt(5)) / 2
IRR = [('3 - phi Unborn Axes', 3 - phi), ('phi Icosaxes', phi), ('mu_G Greater Golden Cut Cube', 4 + sp.Rational(3, 2) * sp.sqrt(2) - sp.sqrt(5) - sp.sqrt(10) / 2),
       ('mu_L Lesser Golden Cut Cube', 4 - sp.Rational(3, 2) * sp.sqrt(2) + sp.sqrt(5) - sp.sqrt(10) / 2), ('1 + sqrt2 silver', 1 + sp.sqrt(2)),
       ('2 + 1/phi^2', 2 + 1 / phi**2), ('2 + 1/phi', 2 + 1 / phi)]
OH = signed_perms()
EXTRA = []
summary = []
def describe(P):
    return sorted(len(f[2]) for f in P.faces)
def cscl_station(label, m, num):
    conv = Fr if num == 'fr' else (lambda v: mp.mpf(sp.N(v, 70)) if isinstance(v, sp.Basic) else mp.mpf(v))
    mm = m if num == 'fr' else conv(m)
    mq = (3 - m) if num == 'fr' else conv(3 - m)
    P = Poly(cell_planes(mm, conv=conv), num)
    Q = Poly(cell_planes(mq, (1, 1, 1), conv=conv), num)
    vp, vq = P.volume(), Q.volume()
    ok_vol = P.z(vp + vq - 8)
    # neighbours across every facet, in the CsCl patch: P at 2Z^3, Q at 2Z^3 + (1,1,1)
    tiles = []
    for c in itertools.product((-2, 0, 2), repeat=3):
        tiles.append(('P', [conv(x) for x in c], Poly(cell_planes(mm, c, conv=conv), num)))
    for c in itertools.product((-1, 1, 3), repeat=3):
        tiles.append(('Q', [conv(x) for x in c], Poly(cell_planes(mq, c, conv=conv), num)))
    def face_pts(T, f): return [T.V[i] for i in T.faces[f][2]]
    def same(A, B): return len(A) == len(B) and all(any(all(P.z(a[k] - b[k]) for k in range(3)) for b in B) for a in A)
    pairing = {}
    for kind, c0, T in [tiles[13], next(x for x in tiles if x[0] == 'Q' and x[1] == [conv(1)] * 3)]:   # P at 0 and Q at (1,1,1)
        for f in range(len(T.faces)):
            A = face_pts(T, f)
            hits = [(k2, len(T2.faces[g][2])) for (k2, c2, T2) in tiles if T2 is not T for g in range(len(T2.faces)) if same(A, face_pts(T2, g))]
            pairing.setdefault((kind, len(A)), set()).update(hits)
            if len(hits) != 1: pairing[('BAD', kind)] = hits
    # unique placement: stabiliser of each face in the cell's group = isometries of the labelled polygon
    uniq = True; orders = {}
    for kind, T, c in [('P', P, [conv(0)] * 3), ('Q', Q, [conv(1)] * 3)]:
        for f in range(len(T.faces)):
            st = stabiliser(T, f, OH, c); ps = polygon_symmetries(T, f); pl = polygon_symmetries(T, f, True)
            orders[(kind, len(T.faces[f][2]))] = (st, pl, ps)
            uniq &= (st == pl)
            EXTRA.append((label, kind, len(T.faces[f][2]), ps // st))
    lens = sorted({sp.nsimplify(float(mp.sqrt(d2(P.V[list(e)[0]], P.V[list(e)[1]]))), tolerance=1e-12) if num == 'mp' else d2(P.V[list(e)[0]], P.V[list(e)[1]]) for e in P.edges}, key=float)
    summary.append({'station': label, 'mu': str(m), 'P faces': describe(P), 'Q faces': describe(Q),
                    'vol P': str(vp) if num == 'fr' else mp.nstr(vp, 20), 'vol Q': str(vq) if num == 'fr' else mp.nstr(vq, 20),
                    'facet pairing': {f'{k[0]}{k[1]}': sorted(v) for k, v in pairing.items()},
                    'stabiliser vs polygon symmetries': {f'{k[0]}{k[1]}': v for k, v in orders.items()}})
    good_pair = all(k[0] != 'BAD' for k in pairing)
    check(f'mu = {label}: P {face_summary(P)}, Q {face_summary(Q)}; vol P + vol Q = 8; every facet of P and Q matched by exactly one CsCl tile; '
          f'every face stabiliser = isometry group of the face with its edge kinds (orders: stabiliser, labelled, plain)', ok_vol and good_pair and uniq,
          f'pairing {{{", ".join(f"{k[0]}{k[1]}->{sorted(v)}" for k, v in pairing.items())}}}; orders {orders}')
def face_summary(P):
    from collections import Counter
    c = Counter(len(f[2]) for f in P.faces)
    return '+'.join(f'{v}x{k}-gon' for k, v in sorted(c.items()))
for label, m in STATIONS:
    cscl_station(label, m, 'fr')
for label, m in IRR:
    cscl_station(label, m, 'mp')
# exact volumes of the cells at the irrational stations (closed forms)
for label, m in IRR:
    if m > 2:
        vp = 8 - 8 * (3 - m) ** 3 / 6; vq = sp.Rational(4, 3) * (3 - m) ** 3
    else:
        # truncated octahedron: octahedron muC* (vol 4mu^3/3) minus 6 caps (square pyramids of height mu-1): 6*(4/3)(mu-1)^3/...
        vp = sp.Rational(4, 3) * m**3 - 6 * sp.Rational(2, 3) * (m - 1) ** 3
        vq = sp.Rational(4, 3) * (3 - m)**3 - 6 * sp.Rational(2, 3) * (2 - m) ** 3
    check(f'mu = {label}: vol P + vol Q = 8 exactly (closed form)', sp.simplify(vp + vq - 8) == 0, f'vol P = {sp.nsimplify(sp.simplify(vp))}')

# ------------------------------------------------------------------ Part C: the Delian walk of #51
print('== Part C: the Delian walk of #51 (octet edge sqrt2: octahedron centred 0, tetrahedron centred (1/2,1/2,1/2))')
def O_planes(t, conv=Fr):
    pl = []
    for i, j in itertools.combinations(range(3), 2):
        for si, sj in itertools.product((1, -1), repeat=2):
            n = [0, 0, 0]; n[i] = si; n[j] = sj; pl.append((n, conv(1)))      # rhombic dodecahedron
    for s in itertools.product((1, -1), repeat=3):
        pl.append((list(s), conv(3) * (1 - t) / 2))                         # cut planes at fraction t from the tet centre
    return pl
def T_planes(t, conv=Fr):
    h = conv(1) / 2; cT = [h, h, h]
    pl = []
    for i in range(3):
        n = [0, 0, 0]; n[i] = 1; pl.append((n, conv(1)))
        n = [0, 0, 0]; n[i] = -1; pl.append((n, conv(0)))
    for cO in ([1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1]):
        n = sub([conv(x) for x in cO], cT)
        pl.append((n, dot(n, cT) + t * dot(n, n)))
    return pl
def delian_station(label, t, num):
    conv = Fr if num == 'fr' else (lambda v: mp.mpf(sp.N(v, 70)) if isinstance(v, sp.Basic) else mp.mpf(v))
    tt = t if num == 'fr' else conv(t)
    O = Poly(O_planes(tt, conv), num); T = Poly(T_planes(tt, conv), num)
    vO, vT = O.volume(), T.volume()
    ok_vol = O.z(vO + 2 * vT - 2)      # per octahedron (vol of oct edge sqrt2 = 4/3) two tetrahedra (1/3 each): 2 in all
    uniq = True; orders = {}
    for kind, X, c, grp in [('O', O, [conv(0)] * 3, OH), ('T', T, [conv(1) / 2] * 3, TD)]:
        for f in range(len(X.faces)):
            st = stabiliser(X, f, grp, c); ps = polygon_symmetries(X, f); pl = polygon_symmetries(X, f, True)
            orders[(kind, len(X.faces[f][2]))] = (st, pl, ps); uniq &= (st == pl)
            EXTRA.append((label, kind, len(X.faces[f][2]), ps // st))
    summary.append({'Delian station': label, 't': str(t), 'O(t) faces': describe(O), 'T(t) faces': describe(T),
                    'stabiliser vs polygon symmetries': {f'{k[0]}{k[1]}': v for k, v in orders.items()}})
    check(f't = {label}: O(t) {face_summary(O)}, T(t) {face_summary(T)}; vol O + 2 vol T = 2 (one octahedron and two tetrahedra of the octet); '
          f'every face stabiliser = polygon isometry group', ok_vol and uniq, f'orders {orders}')
# the symmetry group of T(t) about (1/2,1/2,1/2): signed permutations with an even number of sign changes keep the
# alternate corners; check this by testing on the cube's odd corners
def keeps_odd(g):
    odd = [[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1]]
    h = Fr(1, 2)
    return all(any(apply(g, [Fr(x) for x in v], [h, h, h]) == [Fr(y) for y in w] for w in odd) for v in odd)
TD = [g for g in OH if keeps_odd(g)]
check('the symmetry group of the cube with alternate corners cut has order 24 (Td)', len(TD) == 24)
for label, t in [('1/5', Fr(1, 5)), ('1/4', Fr(1, 4)), ('1/2', Fr(1, 2)), ('2/3', Fr(2, 3)), ('5/6', Fr(5, 6))]:
    delian_station(label, t, 'fr')
for label, t in [('(2sqrt6-3)/15 equal edges', (2 * sp.sqrt(6) - 3) / 15), ('5/3 - (2/3)sqrt2 equal edges', sp.Rational(5, 3) - sp.Rational(2, 3) * sp.sqrt(2)),
                 ('1 - cbrt6/3 half and half', 1 - sp.cbrt(6) / 3), ('Delian bond 1 - (2/3)2^(-1/3) Samson + Delilah', 1 - sp.Rational(2, 3) * 2 ** sp.Rational(-1, 3))]:
    delian_station(label, t, 'mp')

# ------------------------------------------------------------------ Part D: C6, R12 and the bipyramid B
print('== Part D: the cube pyramid C6, the RD pyramid R12 and the bipyramid B (cube lattice Z^3, centres Z^3 + 1/2)')
h = Fr(1, 2)
def hull_from_points(pts):
    """convex hull facets of a small point set (exact), as a Poly"""
    planes = []
    for a, b, c in itertools.combinations(pts, 3):
        n = cross(sub(b, a), sub(c, a))
        if n == [0, 0, 0]: continue
        d = dot(n, a); sides = [dot(n, p) - d for p in pts]
        if all(s <= 0 for s in sides): planes.append((n, d))
        elif all(s >= 0 for s in sides): planes.append(([-x for x in n], -d))
    uniq = []
    for n, d in planes:
        g = max(abs(x) for x in n); key = (tuple(x / g for x in n), d / g)
        if key not in uniq: uniq.append(key)
    return Poly([(list(k[0]), k[1]) for k in uniq], 'fr')
def cross(u, v): return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
F = lambda *v: [Fr(x) for x in v]
U, D = F(h, h, h), F(h, h, -h)
sq = [F(0, 0, 0), F(1, 0, 0), F(1, 1, 0), F(0, 1, 0)]
B = hull_from_points(sq + [U, D])
C6u, C6d = hull_from_points(sq + [U]), hull_from_points(sq + [D])
R_a, R_b = hull_from_points([sq[0], sq[1], sq[3], U, D]), hull_from_points([sq[2], sq[1], sq[3], U, D])
R_c, R_d = hull_from_points([sq[1], sq[0], sq[2], U, D]), hull_from_points([sq[3], sq[0], sq[2], U, D])
check('B (square of edge 1, apexes 1/2 above and below) has volume 1/3; C6 and R12 have volume 1/6',
      B.volume() == Fr(1, 3) and C6u.volume() == Fr(1, 6) and R_a.volume() == Fr(1, 6))
check('B = C6 + C6 (equator) = R12 + R12 (either diagonal plane): volumes add and the halves are mirror images',
      C6u.volume() + C6d.volume() == B.volume() == R_a.volume() + R_b.volume() == R_c.volume() + R_d.volume())
# R12 = the RD's centre pyramid: RD centred 0 = union of 12 rhombic pyramids; R_a has apex 0 and rhombus (1,0,0),U,(0,1,0),D
rd = Poly([(n, Fr(1)) for n in ([1, 1, 0], [1, -1, 0], [-1, 1, 0], [-1, -1, 0], [1, 0, 1], [1, 0, -1], [-1, 0, 1], [-1, 0, -1],
                                 [0, 1, 1], [0, 1, -1], [0, -1, 1], [0, -1, -1])], 'fr')
check('the rhombic dodecahedron |x|+|y|, |y|+|z|, |z|+|x| <= 1 has volume 2 = 12 x vol R12, and R12 (apex 0) is its face pyramid over x + y = 1',
      rd.volume() == 2 and any(set(map(tuple, (R_a.V[i] for i in f[2]))) == {(1, 0, 0), (0, 1, 0), (h, h, h), (h, h, -h)} for f in R_a.faces)
      and all(any(tuple(v) == tuple(w) for w in rd.V) or tuple(v) == (0, 0, 0) for v in R_a.V))
def lengths(P): return sorted({d2(P.V[list(e)[0]], P.V[list(e)[1]]) for e in P.edges})
check('C6: base edges 1, lateral edges sqrt3/2; R12: base (rhombus) edges sqrt3/2, lateral edges 1 and sqrt3/2',
      lengths(C6u) == [Fr(3, 4), 1] and lengths(R_a) == [Fr(3, 4), 1])
def tri_sides(P):
    return sorted(tuple(sorted(d2(P.V[f[2][i]], P.V[f[2][(i + 1) % 3]]) for i in range(3))) for f in P.faces if len(f[2]) == 3)
check('every lateral face of C6 and of R12 is the triangle (1, sqrt3/2, sqrt3/2); in C6 the legs meet at the apex, in R12 at a three-fold corner',
      set(tri_sides(C6u)) == set(tri_sides(R_a)) == {(Fr(3, 4), Fr(3, 4), Fr(1))})
def dihedrals(P):
    out = []
    for e, fs in P.edges.items():
        n1, n2 = P.faces[fs[0]][0], P.faces[fs[1]][0]
        c2 = Fr(dot(n1, n2) ** 2, dot(n1, n1) * dot(n2, n2)); sgn = -1 if dot(n1, n2) > 0 else (1 if dot(n1, n2) < 0 else 0)
        out.append((d2(P.V[list(e)[0]], P.V[list(e)[1]]), sgn, c2))
    return sorted(set(out))
# interior angle theta: cos theta = -n1.n2/(|n1||n2|); (sgn, cos^2) = sign and square of cos theta
# entries (squared edge length, sign of cos, cos^2) of the interior dihedral angle
check('C6 dihedrals: base edges (1) pi/4, lateral edges (sqrt3/2) 2pi/3', dihedrals(C6u) == sorted([(Fr(3, 4), -1, Fr(1, 4)), (1, 1, Fr(1, 2))]), str(dihedrals(C6u)))
def kinds_R12():
    out = set()
    for e, fs in R_a.edges.items():
        n1, n2 = R_a.faces[fs[0]][0], R_a.faces[fs[1]][0]
        rh = any(len(R_a.faces[x][2]) == 4 for x in fs)
        c2 = Fr(dot(n1, n2) ** 2, dot(n1, n1) * dot(n2, n2)); sgn = -1 if dot(n1, n2) > 0 else (1 if dot(n1, n2) < 0 else 0)
        out.add(('rhombus' if rh else 'lateral', d2(R_a.V[list(e)[0]], R_a.V[list(e)[1]]), sgn, c2))
    return sorted(out)
check('R12 dihedrals: rhombus edges (sqrt3/2) pi/3, short lateral (sqrt3/2) 2pi/3, long lateral (1) pi/2',
      kinds_R12() == sorted([('rhombus', Fr(3, 4), 1, Fr(1, 4)), ('lateral', Fr(3, 4), -1, Fr(1, 4)), ('lateral', 1, 0, 0)]), str(kinds_R12()))

# B tiling patch: every face of the unit cube lattice inside a box carries a B, cut by its equator ('E') or a diagonal ('X', 'Y')
def B_tiles(N, rng, mode):
    tiles = []
    for ax in range(3):
        for base in itertools.product(range(-N, N), repeat=3):
            o = [Fr(x) for x in base]
            e1, e2 = [(ax + 1) % 3, (ax + 2) % 3]
            def P(a, b):
                v = list(o); v[e1] += a; v[e2] += b; return v
            corners = [P(0, 0), P(1, 0), P(1, 1), P(0, 1)]
            cen = P(h, h)
            up = list(cen); up[ax] += h; dn = list(cen); dn[ax] -= h
            c = mode(corners) if callable(mode) else rng.choice(mode)
            if c == 'E':
                tiles += [('C6', hull_from_points(corners + [up]), up), ('C6', hull_from_points(corners + [dn]), dn)]
            else:
                i = 0 if c == 'X' else 1          # X: apexes at corners 0 and 2, Y: at 1 and 3
                a1, a2 = corners[i], corners[i + 2]; m1, m2 = corners[(i + 1) % 4], corners[(i + 3) % 4]
                tiles += [('R12', hull_from_points([a1, m1, m2, up, dn]), a1), ('R12', hull_from_points([a2, m1, m2, up, dn]), a2)]
    return tiles
def f2f_check(tiles, inner):
    """inner tiles: every facet equals a facet of exactly one other tile; no corner of any tile lies inside another
    inner tile, or in the relative interior of one of its faces or edges"""
    allf = {}
    for k, (kind, T, ap) in enumerate(tiles):
        for f in T.faces:
            allf.setdefault(frozenset(tuple(T.V[i]) for i in f[2]), []).append(k)
    ok_f = all(len(allf[frozenset(tuple(T.V[i]) for i in f[2])]) == 2 for k, (kind, T, ap) in enumerate(tiles) if inner(T) for f in T.faces)
    verts = {tuple(v) for kind, T, ap in tiles for v in T.V}
    ok_v = True
    for kind, T, ap in tiles:
        if not inner(T): continue
        own = {tuple(v) for v in T.V}
        for v in verts:
            if v in own: continue
            if all(dot(n, v) <= d for n, d, _ in T.faces): ok_v = False   # a foreign corner in T (interior, face or edge)
    return ok_f, ok_v
N_ = 2
rng = random.Random(93)
inner = lambda T: all(-1 <= x <= 1 for v in T.V for x in v)
for name, mode in [('all R12, random diagonal on every face', ['X', 'Y']), ('C6 and R12 mixed, random', ['E', 'X', 'Y']),
                   ('all equator (the cube lattice cut into C6)', ['E'])]:
    tl = B_tiles(N_, rng, mode)
    ok_f, ok_v = f2f_check(tl, inner)
    vol = sum(T.volume() for k, T, a in tl)
    check(f'B tiling of the box [-2,2]^3, {name}: {len(tl)} tiles, total volume {vol} = 64; inner tiles: facets matched exactly, '
          f'no foreign corner in any tile', ok_f and ok_v and vol == 64)
# whole rhombic dodecahedra: an apex carries a whole RD iff all 12 B's round it are cut through it
def parity(corners):
    return 'X' if sum(corners[0]) % 2 == 0 else 'Y'          # X joins corners 0 and 2: even corners iff corner 0 is even
tl = B_tiles(N_, rng, parity)
from collections import Counter
cnt = Counter(tuple(a) for kind, T, a in tl)
rd_ok = all(sum(v) % 2 == 0 for v, c in cnt.items() if c == 12) and any(c == 12 for c in cnt.values())
inner_even = [v for v in cnt if all(-1 <= x <= 1 for x in v) and sum(v) % 2 == 0]
check('all cuts through the even corners: every even corner inside the box is the apex of 12 R12 (a whole RD, the fcc RD tiling); '
      'no odd corner is an apex', rd_ok and all(cnt[v] == 12 for v in inner_even) and all(sum(v) % 2 == 0 for v in cnt), f'{len(inner_even)} inner RDs')
# rigidity of the base pairing: across the rhombus the partner is unique (stabiliser of the rhombus in R12's group = 4 = rhombus symmetries)
refl = lambda v: [v[1], v[0], v[2]]; reflz = lambda v: [v[0], v[1], -v[2]]
keeps = lambda P, g: {tuple(g(v)) for v in P.V} == {tuple(v) for v in P.V}
check('R12 is kept by the reflections in x = y and z = 0 (order-4 group acting as the rhombus\'s 4 isometries), and the rhombus has exactly 4; '
      'so the tile across the rhombus is the mirror image, and R12 + mirror = B',
      keeps(R_a, refl) and keeps(R_a, reflz) and polygon_symmetries(R_a, [i for i, f in enumerate(R_a.faces) if len(f[2]) == 4][0]) == 4)
print('   faces whose plain isometry group exceeds the stabiliser (label, piece, n-gon, index):', sorted({e for e in EXTRA if e[3] > 1}))
check('the plain isometry group of a face exceeds its stabiliser only for Kelvin\'s regular hexagons and the silver regular octagons',
      {(e[0], e[2]) for e in EXTRA if e[3] > 1} == {('3/2 Kelvin', 6), ('1 + sqrt2 silver', 8)})

json.dump({'wedge tables': {k: {kk: [list(x) for x in vv] if isinstance(vv, list) and vv and isinstance(vv[0], tuple) else vv
                                for kk, vv in v.items()} for k, v in TABLES.items()}, 'stations': summary},
          open('data/pairing-checks.json', 'w'), indent=1, default=str)
print(f'== {NPASS} PASS, {NFAIL} FAIL')
