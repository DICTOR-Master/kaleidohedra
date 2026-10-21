# DICTO 2026-10-21, "what could Aristotle have meant" (DICTO's question): exact checks for paper #44.
# Every angle identity used in the proof, in exact arithmetic in Q(sqrt5) (numbers a + b*sqrt5 as Fraction pairs; angles are
# handled through cos^2 and the sign of cos, which fix an angle in (0, pi)), the irrationality and square-class facts fed to the
# Conway-Radin-Sadun Splitting Theorem, the counting map h on all 31 sets of face pyramids, the octet cut into pyramids, and
# Cleo-Icos + Antonius in the prolate golden rhombohedron (#20). Floats appear only in printed approximations.
#   python3 pyramid_checks.py  > pyramid-checks.log
import itertools
from fractions import Fraction as Fr
# ---- Q(sqrt5)
Z, ONE = (Fr(0), Fr(0)), (Fr(1), Fr(0))
qa = lambda x, y: (x[0] + y[0], x[1] + y[1]); qs = lambda x, y: (x[0] - y[0], x[1] - y[1])
qm = lambda x, y: (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]); qr = lambda r: (Fr(r), Fr(0))
def qinv(x): n = x[0] * x[0] - 5 * x[1] * x[1]; return (x[0] / n, -x[1] / n)
qd = lambda x, y: qm(x, qinv(y)); qf = lambda x: float(x[0]) + float(x[1]) * 5 ** .5
def sgn(x):
    a, b = x
    if b == 0: return (a > 0) - (a < 0)
    if a == 0: return (b > 0) - (b < 0)
    if a > 0 and b > 0: return 1
    if a < 0 and b < 0: return -1
    s = 1 if a * a > 5 * b * b else -1
    return s if a > 0 else -s
def qstr(x):
    a, b = x
    return f'{a}' if b == 0 else f'{a} + {b}*sqrt5' if a != 0 else f'{b}*sqrt5'
PHI = (Fr(1, 2), Fr(1, 2)); IPHI = (Fr(-1, 2), Fr(1, 2))
V = lambda *c: [qr(t) if not isinstance(t, tuple) else t for t in c]
add = lambda u, v: [qa(a, b) for a, b in zip(u, v)]; sub = lambda u, v: [qs(a, b) for a, b in zip(u, v)]
mul = lambda u, s: [qm(a, s) for a in u]
dot = lambda u, v: qa(qa(qm(u[0], v[0]), qm(u[1], v[1])), qm(u[2], v[2]))
def cross(u, v): return [qs(qm(u[1], v[2]), qm(u[2], v[1])), qs(qm(u[2], v[0]), qm(u[0], v[2])), qs(qm(u[0], v[1]), qm(u[1], v[0]))]
det = lambda a, b, c: dot(a, cross(b, c))
bad = 0
def chk(c, m):
    global bad; print(('PASS ' if c else 'FAIL ') + m); bad += (not c)
# ---- exact convex hull of a small point set: faces (planes holding >= 3 points, all others on one side), edges, dihedral angles
def hull(P):
    F = {}
    for i, j, k in itertools.combinations(range(len(P)), 3):
        n = cross(sub(P[j], P[i]), sub(P[k], P[i]))
        if all(t == Z for t in n): continue
        s = [sgn(dot(n, sub(p, P[i]))) for p in P]
        if all(x <= 0 for x in s) or all(x >= 0 for x in s):
            if any(x > 0 for x in s): n = [(-a[0], -a[1]) for a in n]   # outward
            key = frozenset(m for m in range(len(P)) if sgn(dot(n, sub(P[m], P[i]))) == 0)
            F.setdefault(key, n)
    E = {}
    for (f1, n1), (f2, n2) in itertools.combinations(F.items(), 2):
        c = f1 & f2
        if len(c) == 2: E[tuple(sorted(c))] = (n1, n2)
    return F, E
def dihedral(n1, n2):
    """interior dihedral angle between faces with outward normals n1, n2: (cos^2, sign of cos), exact"""
    c = qs(Z, dot(n1, n2)); return qd(qm(c, c), qm(dot(n1, n1), dot(n2, n2))), sgn(c)
def same_angle(a, b): return tuple(a[0]) == tuple(b[0]) and a[1] == b[1]
half = lambda th: (qm(qa(ONE, th), (Fr(1, 2), Fr(0))), 1)        # cos^2(theta/2) = (1 + cos theta)/2, theta/2 acute
def cos_of(c): return (qm(c, c), sgn(c))                           # angle with cosine c, as (cos^2, sign)
import math
# ---- the five solids (centre at the origin)
cyc = lambda v: [v, [v[1], v[2], v[0]], [v[2], v[0], v[1]]]
S = {'cube': [V(*p) for p in itertools.product((1, -1), repeat=3)],
     'tetrahedron': [V(*p) for p in itertools.product((1, -1), repeat=3) if p[0] * p[1] * p[2] > 0],
     'octahedron': [V(*[s if k == i else 0 for k in range(3)]) for i in range(3) for s in (1, -1)],
     'dodecahedron': [V(*p) for p in itertools.product((1, -1), repeat=3)] + [w for a, b in itertools.product((1, -1), repeat=2) for w in cyc(V(0, qm(qr(a), IPHI), qm(qr(b), PHI)))],
     'icosahedron': [w for a, b in itertools.product((1, -1), repeat=2) for w in cyc(V(0, a, qm(qr(b), PHI)))]}
# the classical dihedral angles: cos = -1/3 + ... as (cos^2, sign); names of the angle in the basis (pi, alpha, thD, thI)
r5 = (Fr(0), Fr(1))
DIH = {'cube': cos_of(Z), 'tetrahedron': cos_of(qr(Fr(1, 3))), 'octahedron': cos_of(qr(Fr(-1, 3))),
       'dodecahedron': cos_of((Fr(0), Fr(-1, 5))), 'icosahedron': cos_of((Fr(0), Fr(-1, 3)))}
# coefficient vectors (pi, alpha, thD, thI) of the solid's dihedral angle: alpha = arccos(1/3), thD = arccos(-1/sqrt5), thI = arccos(-sqrt5/3)
COEF = {'cube': (Fr(1, 2), 0, 0, 0), 'tetrahedron': (0, 1, 0, 0), 'octahedron': (1, -1, 0, 0), 'dodecahedron': (0, 0, 1, 0), 'icosahedron': (0, 0, 0, 1)}
FACES_AT_CORNER = {'cube': 3, 'tetrahedron': 3, 'octahedron': 4, 'dodecahedron': 3, 'icosahedron': 5}
COS2PI = {3: qr(Fr(-1, 2)), 4: Z, 5: (Fr(-1, 4), Fr(1, 4))}        # cos(2pi/q); cos 72 deg = (sqrt5 - 1)/4
print('== 1. The solids\' dihedral angles and the face pyramids\' angles (exact)')
PYR = {}
O = V(0, 0, 0)
for name, P in S.items():
    F, E = hull(P)
    # the solid's dihedral angle at every edge
    angs = {dihedral(*E[e]) for e in E}
    chk(len(angs) == 1 and same_angle(list(angs)[0], DIH[name]), f'{name}: {len(F)} faces, {len(E)} edges, every dihedral angle has cos^2 = {qstr(DIH[name][0])}, cos sign {DIH[name][1]:+d} (= the classical value)')
    # its face pyramid on one face: apex O
    f0 = min(F, key=lambda k: sorted(k)); base = [P[i] for i in f0]
    Fp, Ep = hull(base + [O]); apex = len(base)
    bang = {dihedral(*Ep[e]) for e in Ep if apex not in e}
    sang = {dihedral(*Ep[e]) for e in Ep if apex in e}
    # base edge: cos^2(beta) = (1 + cos theta)/2 with beta acute  <=>  beta = theta/2
    c2, s = DIH[name]
    cos_theta = None
    for cand in [qr(Fr(1, 3)), qr(Fr(-1, 3)), (Fr(0), Fr(-1, 5)), (Fr(0), Fr(-1, 3)), Z]:
        if qm(cand, cand) == c2 and sgn(cand) == s: cos_theta = cand
    b = list(bang)[0]
    chk(len(bang) == 1 and b[1] == 1 and b[0] == qm(qa(ONE, cos_theta), qr(Fr(1, 2))), f'{name} pyramid: {len(base)} base edges, angle beta with cos^2 beta = (1 + cos theta)/2 = {qstr(b[0])}, beta acute: beta = theta/2 = {math.degrees(math.acos(qf(cos_theta))) / 2:.4f} deg')
    q = FACES_AT_CORNER[name]; sa = list(sang)[0]
    chk(len(sang) == 1 and sa == (qm(COS2PI[q], COS2PI[q]), sgn(COS2PI[q])), f'{name} pyramid: {len(base)} side edges, angle 360/{q} = {360 / q:g} deg exactly (cos^2 = {qstr(sa[0])}, sign {sa[1]:+d})')
    cb = tuple(Fr(x) / 2 for x in COEF[name]); cs = (Fr(2, q), 0, 0, 0)
    PYR[name] = {'base': cb, 'side': cs, 'n': len(base)}
print('\n== 2. Facts for the Conway-Radin-Sadun theorems (exact)')
for nm, (c, d) in {'alpha': (qr(Fr(1, 3)), 2), 'theta_D': ((Fr(0), Fr(-1, 5)), 1), 'theta_I': ((Fr(0), Fr(-1, 3)), 5)}.items():
    c2 = qm(c, c); t2 = qs(qinv(c2), ONE); tc = qm(qr(4), c2)
    chk(c2[1] == 0 and t2[1] == 0, f'{nm}: cos^2 = {c2[0]}, tan^2 = {t2[0]} rational (a geodetic angle); tan = {"+" if sgn(c) > 0 else "-"}sqrt({t2[0]})')
    k = t2[0].numerator * t2[0].denominator
    sf = math.prod(p for p in [2, 3, 5, 7] if (lambda e: e % 2)(next(i for i in range(20) if k % p ** (i + 1))))
    chk(sf == d, f'{nm}: tan is a rational multiple of sqrt{d} (square-free part {sf})')
    chk(tc[0].denominator != 1, f'{nm}: (2 cos)^2 = {tc[0]} is not an integer, so 2 cos is not an algebraic integer and {nm} is not a rational multiple of pi')
chk(len({2, 1, 5}) == 3, 'the three tangents lie in three different square classes (sqrt2, 1, sqrt5): by the Splitting Theorem pi, alpha, theta_D, theta_I are linearly independent over Q')
print('\n== 3. The counting map h on every set of face pyramids')
names = list(S)
print('angles as (pi, alpha, theta_D, theta_I) coefficients:')
for n in names: print(f'  {n:13s} base edge {tuple(str(x) for x in PYR[n]["base"])}  side edge {tuple(str(x) for x in PYR[n]["side"])}')
def blocked(Sset):
    """pyramids of Sset that cannot occur in any tiling of space by copies of pyramids from Sset (the h argument)"""
    out = set()
    for k in (1, 2, 3):                                            # h = the k-th coordinate (h(pi) = 0)
        vals = [PYR[n]['base'][k] for n in Sset if PYR[n]['base'][k] != 0] + [PYR[n]['side'][k] for n in Sset if PYR[n]['side'][k] != 0]
        if vals and (all(v > 0 for v in vals) or all(v < 0 for v in vals)): out |= {n for n in Sset if PYR[n]['base'][k] != 0}
    return out
alive = []
for m in range(1, 6):
    for Sset in itertools.combinations(names, m):
        b = blocked(Sset)
        if not b: alive.append(Sset)
chk(alive == [('cube',), ('tetrahedron', 'octahedron'), ('cube', 'tetrahedron', 'octahedron')], f'sets not excluded by h (of 31): {alive}')
chk(all('dodecahedron' in blocked(s) and 'icosahedron' in blocked(s) for s in [tuple(names)]), 'with all five allowed, the dodecahedron and icosahedron pyramids (Cleo-Icos) are still excluded')
for s in [('tetrahedron',), ('octahedron',), ('cube', 'tetrahedron'), ('cube', 'octahedron')]: chk(blocked(s) == ({'tetrahedron', 'octahedron'} & set(s)), f'{s}: the tetrahedron/octahedron pyramid is excluded without its partner')
print('\n== 4. The octet cut into face pyramids (exact)')
u, v, w = V(1, 1, 0), V(1, 0, 1), V(0, 1, 1)                     # the 60-degree rhombohedron: one cell of the octet (fcc) lattice
R = [add(add(mul(u, qr(a)), mul(v, qr(b))), mul(w, qr(c))) for a, b, c in itertools.product((0, 1), repeat=3)]
lvl = lambda a, b, c: a + b + c
T1 = [R[i] for i, p in enumerate(itertools.product((0, 1), repeat=3)) if lvl(*p) <= 1]
M = [R[i] for i, p in enumerate(itertools.product((0, 1), repeat=3)) if lvl(*p) in (1, 2)]
T2 = [R[i] for i, p in enumerate(itertools.product((0, 1), repeat=3)) if lvl(*p) >= 2]
def vol(P):                                                        # exact volume of a convex polytope (cone from its centroid)
    F, E = hull(P); c = [(sum(p[i][0] for p in P) / len(P), sum(p[i][1] for p in P) / len(P)) for i in range(3)]
    tot = Z
    for f, n in F.items():
        pts = [P[i] for i in f]; o = pts[0]
        # order the face's corners round its normal and fan-triangulate
        cen = [(sum(p[i][0] for p in pts) / len(pts), sum(p[i][1] for p in pts) / len(pts)) for i in range(3)]
        ref = sub(pts[0], cen)
        ang = lambda p: math.atan2(qf(dot(cross(ref, sub(p, cen)), n)) / math.sqrt(qf(dot(n, n))), qf(dot(ref, sub(p, cen))))
        pts = sorted(pts, key=ang)
        for a, b in zip(pts[1:], pts[2:]): tot = qa(tot, qd(det(sub(pts[0], c), sub(a, c), sub(b, c)), qr(6)))
    return tot
def edges_equal(P):
    F, E = hull(P); L = {tuple(dot(sub(P[a], P[b]), sub(P[a], P[b]))) for a, b in E}; return len(E), L
nE, L = edges_equal(M); chk(len(M) == 6 and nE == 12 and L == {(Fr(2), Fr(0))}, 'the middle of the 60-degree rhombohedron is a regular octahedron (6 corners, 12 edges, all edge^2 = 2)')
for T in (T1, T2): nE, L = edges_equal(T); chk(len(T) == 4 and nE == 6 and L == {(Fr(2), Fr(0))}, 'a corner piece is a regular tetrahedron (edge^2 = 2)')
vR, vM, vT1, vT2 = qr(abs(det(u, v, w)[0])), vol(M), vol(T1), vol(T2)
chk(vM == qr(Fr(4, 3)) and vT1 == qr(Fr(1, 3)) and vT2 == qr(Fr(1, 3)) and qa(vM, qa(vT1, vT2)) == vR, f'volumes: octahedron {qstr(vM)} + 2 tetrahedra {qstr(vT1)} = rhombohedron {qstr(vR)} (one lattice cell: the octet has 1 octahedron and 2 tetrahedra per cell)')
nO, nT = len(hull(M)[0]), len(hull(T1)[0]) + len(hull(T2)[0])
chk(nO == 8 and nT == 8, f'cut from their centres: {nO} octahedron pyramids and {nT} tetrahedron pyramids per cell, equal numbers')
ed = tuple(4 * PYR['tetrahedron']['base'][i] + 4 * PYR['octahedron']['base'][i] for i in range(4))
chk(ed == (2, 0, 0, 0), 'round an octet edge (2 tetrahedra, 2 octahedra) the pyramids give 4 x alpha/2 + 4 x (pi - alpha)/2 = 2 pi')
hb = PYR['tetrahedron']['n'] * PYR['tetrahedron']['base'][1] + PYR['octahedron']['n'] * PYR['octahedron']['base'][1]
chk(hb == 0, f'h-weighted base edges, one tetrahedron pyramid + one octahedron pyramid of the same edge: 3 x (+1/2) + 3 x (-1/2) = {hb}')
# the three kinds together: in the octet with octahedra centred at the integer points of odd coordinate sum (corners at +-1 along the
# axes) and tetrahedra in the unit cubes (corners at the even-sum corners), every face pyramid lies in a slab k <= z <= k + 1, so each
# plane z = k is made of pyramid faces: the octet's pyramids fill z <= 0 and the cube pyramids of unit cubes fill z >= 0
E3 = [V(*[s if k == i else 0 for k in range(3)]) for i in range(3) for s in (1, -1)]
slab_ok, nO, nT = True, 0, 0
for c in itertools.product(range(-1, 2), repeat=3):
    if sum(c) % 2 == 0: continue
    cc = V(*c); Oct = [add(cc, e) for e in E3]
    for f in hull(Oct)[0]:
        zs = [Oct[i][2][0] for i in f] + [cc[2][0]]; nO += 1
        slab_ok &= max(zs) - min(zs) <= 1
for c in itertools.product(range(-1, 1), repeat=3):
    Tt = [V(*[c[i] + p[i] for i in range(3)]) for p in itertools.product((0, 1), repeat=3) if (sum(c) + sum(p)) % 2 == 0]
    cen = [(sum(t[i][0] for t in Tt) / 4, Fr(0)) for i in range(3)]
    for f in hull(Tt)[0]:
        zs = [Tt[i][2][0] for i in f] + [cen[2][0]]; nT += 1
        slab_ok &= max(zs) - min(zs) <= 1 and min(zs) == int(min(zs))
chk(slab_ok and nO == 14 * 8 and nT == 8 * 4, f'octet patch ({nO} octahedron and {nT} tetrahedron pyramids): every face pyramid lies in a slab k <= z <= k + 1, so the planes z = k are unions of pyramid faces and cube pyramids can fill one side')
print('\n== 5. Cleo-Icos + Antonius + Cleo-Icos = the prolate golden rhombohedron (#20; exact)')
I = S['icosahedron']; Fi, _ = hull(I); f0 = sorted(Fi, key=lambda k: sorted(k))[0]; u, v, w = [I[i] for i in sorted(f0)]
cu = qd(dot(u, v), dot(u, u))
chk(qm(cu, cu) == qr(Fr(1, 5)) and sgn(cu) == 1, f'the centre-to-corner lines of one face meet at arccos(1/sqrt5) = {math.degrees(math.acos(1 / 5 ** .5)):.2f} deg, the golden rhombus angle')
R = {p: add(add(mul(u, qr(p[0])), mul(v, qr(p[1]))), mul(w, qr(p[2]))) for p in itertools.product((0, 1), repeat=3)}
C1 = [R[p] for p in R if sum(p) <= 1]; A = [R[p] for p in R if sum(p) in (1, 2)]; C2 = [R[p] for p in R if sum(p) >= 2]
chk(sorted(map(str, C1)) == sorted(map(str, [V(0, 0, 0), u, v, w])), 'the sharp corner piece is the icosahedron\'s face pyramid (Cleo-Icos)')
vR = det(u, v, w); vR = vR if sgn(vR) > 0 else qs(Z, vR); vC, vA = vol(C1), vol(A)
chk(qm(vC, qr(6)) == vR and vA == qm(vC, qr(4)) and vol(C2) == vC, f'volumes: Cleo-Icos {qstr(vC)} ({qf(vC):.6f}), Antonius 4 x that, rhombohedron 6 x that')
FA, EA = hull(A)
chk(len(A) == 6 and len(FA) == 8 and len(EA) == 12, 'Antonius: 6 corners, 8 faces, 12 edges (a trigonal antiprism)')
ci = (Fr(0), Fr(-1, 3)); tri, lat = [], []
for (a, b), (n1, n2) in EA.items():
    d = dihedral(n1, n2); s = sum(next(p for p in R if R[p] == A[a])) + sum(next(p for p in R if R[p] == A[b]))
    (tri if s in (2, 4) else lat).append(d)
# triangle edges: angle pi - thI/2, i.e. cos^2 = (1 + cos thI)/2 and cos < 0
chk(len(tri) == 6 and all(d == (qm(qa(ONE, ci), qr(Fr(1, 2))), -1) for d in tri), f'Antonius\'s 6 triangle edges: angle pi - theta_I/2 = {180 - math.degrees(math.acos(-5 ** .5 / 3)) / 2:.2f} deg; with the Cleo-Icos\'s theta_I/2 they make a flat 180 deg')
c72 = COS2PI[5]
chk(len(lat) == 6 and all(d == (qm(c72, c72), -1) for d in lat), 'Antonius\'s 6 zigzag side edges: every one 108 deg exactly (cos = -(sqrt5 - 1)/4), a rational multiple of pi (h = 0); Antonius\'s dihedral angles are {108 deg, 110.91 deg}')
# the rhombohedron itself: 72 deg along the 6 edges at its two sharp tips, 108 deg along the 6 zigzag edges (which Antonius keeps)
FR, ER = hull(list(R.values())); tip = [e for e in ER if any(sum(next(p for p in R if R[p] == list(R.values())[i])) in (0, 3) for i in e)]
chk(len(ER) == 12 and len(tip) == 6 and all(dihedral(*ER[e]) == (qm(c72, c72), 1) for e in tip) and all(dihedral(*ER[e]) == (qm(c72, c72), -1) for e in ER if e not in tip), 'golden rhombohedron: 72 deg exactly along the 6 edges at its sharp tips (in the Cleo-Icos), 108 deg along the other 6')
chk(PYR['icosahedron']['base'][3] * 3 * -2 == 6 * (-Fr(1, 2)), 'h (h(theta_I) = 1): Cleo-Icos 3 edges x 1/2, Antonius 6 edges x (-1/2) of the same length: Antonius = -2 x Cleo-Icos, balanced two to one')
print('\nALL PASS' if bad == 0 else f'\n{bad} FAIL')
