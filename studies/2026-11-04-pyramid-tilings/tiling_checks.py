# DICTO 2026-11-04, paper #92 (DICTO's idea: which tilings by the tetrahedron's and octahedron's centre pyramids exist?).
# Exact checks for the paper. Run with the geom venv on dicto-big-brother:
#   ~/geom/bin/python3 tiling_checks.py > data/tiling-checks.log
# Part A (sympy): the two pyramids' edges, faces and dihedral angles; alpha/pi irrational; the edge equations.
# Part B (integers/Fractions): Barlow stacking patches built from layers, cut into pyramids; face pairing, edge and vertex
#   configurations, h/c vertices against the stacking sequence.  Every coordinate is exact: a point (a, b, c) with integer or
#   rational a, b, c means (a/2, b*sqrt3/6, c*sqrt6/3), so squared lengths are rational and orientation signs are integer dets.
# Part C (Fractions): the cube of edge 1/sqrt2 is 4 T + 4 O pyramids, in either of two ways.
import itertools, random, json, sys
from fractions import Fraction as Fr
import sympy as sp

NPASS = NFAIL = 0
def check(name, ok, info=''):
    global NPASS, NFAIL
    if ok: NPASS += 1
    else: NFAIL += 1
    print(('PASS ' if ok else 'FAIL ') + name + (f'   [{info}]' if info else ''))

# ------------------------------------------------------------------ Part A
print('== Part A: the two pyramids (base edge 1)')
s2, s3, s6 = sp.sqrt(2), sp.sqrt(3), sp.sqrt(6)
tet = [sp.Matrix(v) for v in [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]]
tet = [v / (2 * s2) for v in tet]                      # regular tetrahedron of edge 1, centre 0
octa = [sp.Matrix(v) / s2 for v in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]]  # edge 1
O0 = sp.zeros(3, 1)
def dihedral_cos(p, q, r1, r2):
    """cos of the dihedral angle along edge pq of the solid angle spanned towards r1 and r2"""
    e = q - p
    u = (r1 - p) - e * (e.dot(r1 - p) / e.dot(e)); w = (r2 - p) - e * (e.dot(r2 - p) / e.dot(e))
    return sp.nsimplify(sp.simplify(u.dot(w) / sp.sqrt(u.dot(u) * w.dot(w))))
TA, TB, TC = tet[0], tet[1], tet[2]
OA, OB, OC = octa[0], octa[2], octa[4]
L = lambda u, v: sp.simplify((u - v).norm())
check('T pyramid: base edge 1, lateral edges sqrt6/4', L(TA, TB) == 1 and L(O0, TA) == s6 / 4, f'{L(O0, TA)}')
check('O pyramid: base edge 1, lateral edges sqrt2/2', L(OA, OB) == 1 and L(O0, OA) == s2 / 2, f'{L(O0, OA)}')
check('the three edge lengths sqrt6/4 < sqrt2/2 < 1 are distinct', s6 / 4 < s2 / 2 < 1)
check('faces: T lateral (1, .612, .612), O lateral (1, .707, .707), base (1, 1, 1): pairwise not congruent',
      len({s6 / 4, s2 / 2, sp.Integer(1)}) == 3)
check('O lateral face is right-angled at the apex', sp.simplify((OA - O0).dot(OB - O0)) == 0)
cTb = dihedral_cos(TA, TB, O0, TC)        # T base edge: towards apex and base
cTl = dihedral_cos(O0, TA, TB, TC)        # T lateral edge
cOb = dihedral_cos(OA, OB, O0, OC)
cOl = dihedral_cos(O0, OA, OB, OC)
check('T base-edge dihedral = alpha/2: cos^2 = (1 + 1/3)/2 = 2/3', sp.simplify(cTb**2 - sp.Rational(2, 3)) == 0 and cTb > 0, f'cos={cTb}')
check('T lateral-edge dihedral = 2pi/3 (cos = -1/2)', sp.simplify(cTl + sp.Rational(1, 2)) == 0, f'{cTl}')
check('O base-edge dihedral = (pi - alpha)/2: cos^2 = (1 - 1/3)/2 = 1/3', sp.simplify(cOb**2 - sp.Rational(1, 3)) == 0 and cOb > 0, f'cos={cOb}')
check('O lateral-edge dihedral = pi/2', sp.simplify(cOl) == 0)
check('T base + O base wedges make pi/2: cos(a+b) = cos a cos b - sin a sin b = 0',
      sp.simplify(cTb * cOb - sp.sqrt(1 - cTb**2) * sp.sqrt(1 - cOb**2)) == 0)
# alpha = arccos(1/3) is not a rational multiple of pi: else 2cos(alpha) = 2/3 would be an algebraic integer (sum of roots of unity)
check('alpha/pi irrational: 2cos(alpha) = 2/3 is not an algebraic integer (not an integer rational)', not sp.Rational(2, 3).is_integer)
# Edge equations at a generic point of an edge (Lemma 1 of #44): nT*alpha/2 + nO*(pi-alpha)/2 + k*2pi/3 + l*pi/2 = 2pi or pi.
sols = {}
for tot in (2, 1):
    out = []
    for nT, nO, k, l in itertools.product(range(13), repeat=4):
        # alpha-part: (nT - nO)/2 = 0 ; pi-part: nO/2 + 2k/3 + l/2 = tot
        if nT == nO and Fr(nO, 2) + Fr(2 * k, 3) + Fr(l, 2) == tot and nT + nO + k + l > 0:
            out.append((nT, nO, k, l))
    sols[tot] = out
print('   full turn (nT-base, nO-base, k T-lateral, l O-lateral):', sols[2])
print('   flat (edge on a face of another tile):', sols[1])
check('full-turn configurations: exactly 6', sols[2] == [(0, 0, 0, 4), (0, 0, 3, 0), (1, 1, 0, 3), (2, 2, 0, 2), (3, 3, 0, 1), (4, 4, 0, 0)])
check('flat configurations: exactly 3, none with a T lateral edge', sols[1] == [(0, 0, 0, 2), (1, 1, 0, 1), (2, 2, 0, 0)])
check('a T lateral wedge occurs only as 3 T lateral wedges, alone', [s for s in sols[2] + sols[1] if s[2] > 0] == [(0, 0, 3, 0)])
# whole solids, face to face: n tets (alpha) + m octs (pi - alpha) = 2pi
ws = [(n, m) for n in range(7) for m in range(7) if n == m and m * 1 == 2]   # (n - m) alpha = (2 - m) pi
check('whole solids face to face: every edge has exactly 2 tetrahedra and 2 octahedra', ws == [(2, 2)])
# vertex link: t triangles (area 3alpha - pi), s squares (area 2pi - 4alpha), 2 of each at every link vertex
a = sp.symbols('a'); t, s = 8, 6
check('vertex star: 3t = 4s and t(3a - pi) + s(2pi - 4a) = 4pi give t = 8, s = 6 (12 neighbours)',
      3 * t == 4 * s and sp.simplify(t * (3 * a - sp.pi) + s * (2 * sp.pi - 4 * a) - 4 * sp.pi) == 0)
check('upper half of a flat hexagon: 3 rim tets + 3 rim octs leave 2pi - 3(3a-pi) - 3(2pi-4a) = 3a - pi, one tetrahedron',
      sp.simplify(2 * sp.pi - 3 * (3 * a - sp.pi) - 3 * (2 * sp.pi - 4 * a) - (3 * a - sp.pi)) == 0)
vT = sp.sqrt(2) / 12; vO = sp.sqrt(2) / 3
def pvol(apex, f):
    return sp.simplify(sp.Abs(sp.Matrix.hstack(f[0] - apex, f[1] - apex, f[2] - apex).det()) / 6)
VT, VO = pvol(O0, (TA, TB, TC)), pvol(O0, (OA, OB, OC))
check('volumes: T pyramid = sqrt2/48 = tetrahedron/4, O pyramid = sqrt2/24 = octahedron/8 (base edge 1)',
      sp.simplify(VT - s2 / 48) == 0 and sp.simplify(VO - s2 / 24) == 0 and sp.simplify(4 * VT - vT) == 0 and sp.simplify(8 * VO - vO) == 0, f'{VT}, {VO}')
print('   solid angles: T apex pi, O apex pi/2, T base corner alpha - pi/3, O base corner pi/2 - alpha')

# ------------------------------------------------------------------ Part B
print('== Part B: Barlow stackings, built layer by layer, cut into pyramids (exact)')
def P(i, j, k, s): return (2 * i + j + s, 3 * j + s, k)
def d2(p, q):
    a, b, c = (Fr(p[0]) - q[0]), (Fr(p[1]) - q[1]), (Fr(p[2]) - q[2])
    return a * a / 4 + b * b / 12 + 2 * c * c / 3
def det3(u, v, w):
    return (u[0] * (v[1] * w[2] - v[2] * w[1]) - u[1] * (v[0] * w[2] - v[2] * w[0]) + u[2] * (v[0] * w[1] - v[1] * w[0]))
def side(f, x):      # sign of x relative to the plane of triangle f (integer/Fraction det: the metric factor is positive)
    p0 = f[0]; u = [Fr(f[1][i]) - p0[i] for i in range(3)]; v = [Fr(f[2][i]) - p0[i] for i in range(3)]
    w = [Fr(x[i]) - p0[i] for i in range(3)]; d = det3(u, v, w)
    return (d > 0) - (d < 0)
def centre(pts): return tuple(sum(Fr(p[i]) for p in pts) / len(pts) for i in range(3))

def build(seq, R):
    """tiles (kind, vertices) between layers 0..len(seq)-1, lattice indices |i|,|j| <= R"""
    tiles = []
    for k in range(len(seq) - 1):
        s0, s1 = seq[k], seq[k + 1]
        up_tets = (s1 - s0) % 3 == 1
        for i in range(-R, R + 1):
            for j in range(-R, R + 1):
                up = (P(i, j, k, s0), P(i + 1, j, k, s0), P(i, j + 1, k, s0))
                dn = (P(i + 1, j, k, s0), P(i, j + 1, k, s0), P(i + 1, j + 1, k, s0))
                for tri, is_up in ((up, True), (dn, False)):
                    g = centre(tri)
                    if is_up == up_tets:   # a point of layer k+1 lies over the centroid
                        top = (g[0], g[1], k + 1)
                        tiles.append(('T', tri + (tuple(int(x) for x in top),)))
                    else:
                        top = tuple((int(2 * g[0] - p[0]), int(2 * g[1] - p[1]), k + 1) for p in tri)
                        tiles.append(('O', tri + top))
                # down tetrahedra: triangles of layer k+1 over a point of layer k
                up1 = (P(i, j, k + 1, s1), P(i + 1, j, k + 1, s1), P(i, j + 1, k + 1, s1))
                dn1 = (P(i + 1, j, k + 1, s1), P(i, j + 1, k + 1, s1), P(i + 1, j + 1, k + 1, s1))
                for tri, is_up in ((up1, True), (dn1, False)):
                    g = centre(tri)
                    # layer-k point under g? layer-k points have (a - b/... ) : test membership of (g0, g1) with shift s0
                    a0, b0 = g[0], g[1]
                    jj = (b0 - s0) / 3; ii = (a0 - jj - s0) / 2
                    if jj.denominator == 1 and ii.denominator == 1:
                        tiles.append(('T', tri + ((int(a0), int(b0), k),)))
    return tiles

def faces_of(kind, v):
    if kind == 'T': return [tuple(f) for f in itertools.combinations(v, 3)]
    out = []
    for f in itertools.combinations(v, 3):
        if all(d2(p, q) == 1 for p, q in itertools.combinations(f, 2)): out.append(f)
    return out

def pyramids(tiles):
    out = []
    for kind, v in tiles:
        c = centre(v)
        for f in faces_of(kind, v): out.append((kind, c, f))
    return out

def analyse(seq, R, label):
    tiles = build(seq, R)
    nT = sum(1 for t in tiles if t[0] == 'T'); nO = len(tiles) - nT
    inner = lambda p: abs(Fr(p[0])) <= 6 and abs(Fr(p[1])) <= 9 and 1 <= p[2] <= len(seq) - 2
    # face pairing of solids
    fmap = {}
    for idx, (kind, v) in enumerate(tiles):
        for f in faces_of(kind, v):
            fmap.setdefault(frozenset(f), []).append(idx)
    ok_pair = True
    for f, lst in fmap.items():
        fl = sorted(f)
        if all(inner(p) for p in fl):
            if len(lst) != 2: ok_pair = False; continue
            o = [next(x for x in tiles[t][1] if x not in f) for t in lst]
            if side(fl, o[0]) * side(fl, o[1]) != -1: ok_pair = False
    check(f'{label}: every inner face is shared by exactly two solids, one on each side', ok_pair)
    # vertex stars and edge types
    vt = {}
    for idx, (kind, v) in enumerate(tiles):
        for p in v: vt.setdefault(p, []).append(idx)
    ok_star = True; hc_ok = True; nH = nC = 0
    for p, lst in vt.items():
        if not inner(p): continue
        kinds = sorted(tiles[t][0] for t in lst)
        if kinds.count('T') != 8 or kinds.count('O') != 6: ok_star = False
        # edges at p
        nb = {q for t in lst for q in tiles[t][1] if q != p and d2(p, q) == 1}
        if len(nb) != 12: ok_star = False
        ttoo = []
        for q in nb:
            around = [t for t in lst if q in tiles[t][1]]
            ks = [tiles[t][0] for t in around]
            if sorted(ks) != ['O', 'O', 'T', 'T']: ok_star = False; continue
            Ts = [t for t in around if tiles[t][0] == 'T']
            shareTT = len(set(tiles[Ts[0]][1]) & set(tiles[Ts[1]][1])) == 3
            if shareTT: ttoo.append(q)
        k = p[2]
        is_h = seq[k - 1] == seq[k + 1]
        if is_h: nH += 1
        else: nC += 1
        if is_h != (len(ttoo) == 6): hc_ok = False
        if is_h and not all(q[2] == k for q in ttoo): hc_ok = False
        if not is_h and ttoo: hc_ok = False
    check(f'{label}: every inner vertex has 8 tetrahedra, 6 octahedra, 12 neighbours, 2T + 2O round every edge', ok_star)
    check(f'{label}: a vertex has twisted (TTOO) edges iff its layer is h (neighbour layers equal); then exactly its 6 in-layer edges', hc_ok, f'h={nH} c={nC}')
    # pyramid level
    pyr = pyramids(tiles)
    pf = {}
    for idx, (kind, c, f) in enumerate(pyr):
        fs = [f, (c, f[0], f[1]), (c, f[1], f[2]), (c, f[0], f[2])]
        for g in fs: pf.setdefault(frozenset(g), []).append(idx)
    okp = True; lat_ok = True
    for g, lst in pf.items():
        gl = sorted(g)
        if all(inner(p) for p in gl):
            if len(lst) != 2: okp = False; continue
            o = []
            for t in lst:
                kind, c, f = pyr[t]
                allv = list(f) + [c]
                o.append(next(x for x in allv if x not in g))
            if side(gl, o[0]) * side(gl, o[1]) != -1: okp = False
            # lateral faces: shared by two pyramids of the same kind and the same apex
            k0, c0, f0 = pyr[lst[0]]; k1, c1, f1 = pyr[lst[1]]
            if c0 in g:
                if not (c0 == c1 and k0 == k1): lat_ok = False
    check(f'{label} cut into pyramids: every inner pyramid face shared by exactly two pyramids on opposite sides (face to face)', okp)
    check(f'{label} cut into pyramids: every lateral face joins two pyramids of one kind with one apex', lat_ok)
    # edge configurations of pyramids
    ecount = {}
    for kind, c, f in pyr:
        for e in itertools.combinations(f, 2): ecount.setdefault(frozenset(e), []).append(kind + 'b')
        for p in f: ecount.setdefault(frozenset((c, p)), []).append(kind + 'l')
    conf = {}
    for e, lst in ecount.items():
        if all(inner(p) for p in e):
            key = (lst.count('Tb'), lst.count('Ob'), lst.count('Tl'), lst.count('Ol'))
            conf[key] = conf.get(key, 0) + 1
    check(f'{label} cut into pyramids: edge configurations only (4,4,0,0), (0,0,3,0), (0,0,0,4)', set(conf) == {(4, 4, 0, 0), (0, 0, 3, 0), (0, 0, 0, 4)}, str(conf))
    nTp = sum(1 for x in pyr if x[0] == 'T'); nOp = len(pyr) - nTp
    print(f'   {label}: {nT} tetrahedra, {nO} octahedra -> {nTp} T and {nOp} O pyramids in the patch')
    return dict(label=label, seq=seq, tetrahedra=nT, octahedra=nO, T_pyramids=nTp, O_pyramids=nOp, h=nH, c=nC, edge_configs={str(k): v for k, v in conf.items()})

random.seed(20261104)
rnd = [0]
for _ in range(13): rnd.append(random.choice([x for x in (0, 1, 2) if x != rnd[-1]]))
cases = [('fcc ABCABC', [0, 1, 2, 0, 1, 2, 0]), ('hcp ABAB', [0, 1, 0, 1, 0, 1, 0]), ('dhcp ABCB', [0, 1, 2, 1, 0, 1, 2, 1]),
         ('random 14 layers', rnd)]
summary = [analyse(sq, 9, lab) for lab, sq in cases]
print('   random sequence:', ''.join('ABC'[x] for x in rnd))

# ------------------------------------------------------------------ Part C
print('== Part C: the cube of edge 1/sqrt2 is 4 T + 4 O pyramids (two ways); coordinates x sqrt2, cube [0,1]^3')
cube = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
def dd(p, q): return sum((Fr(a) - b) ** 2 for a, b in zip(p, q))
def det(u, v, w): return det3(u, v, w)
def vol(pts):
    p0 = pts[0]; u, v, w = [[Fr(pts[i][j]) - p0[j] for j in range(3)] for i in (1, 2, 3)]
    return abs(det(u, v, w)) / 6
def cut(parity):
    T4 = [p for p in cube if sum(p) % 2 == parity]; odd = [p for p in cube if sum(p) % 2 != parity]
    c = (Fr(1, 2),) * 3; pieces = []
    for f in itertools.combinations(T4, 3):
        pieces.append(('T', [c] + list(f)))
        o = next(q for q in odd if all(dd(q, x) == 1 for x in f))
        pieces.append(('O', [o] + list(f)))
    return pieces
def sep(A, B):
    """convex hulls with disjoint interiors: some face plane of A or B has A on one side, B on the other (closed)"""
    for X, Y in ((A, B), (B, A)):
        for f in itertools.combinations(X, 3):
            u = [[Fr(f[i][j]) - f[0][j] for j in range(3)] for i in (1, 2)]
            sx = {(lambda d: (d > 0) - (d < 0))(det(u[0], u[1], [Fr(x[j]) - f[0][j] for j in range(3)])) for x in X} - {0}
            sy = {(lambda d: (d > 0) - (d < 0))(det(u[0], u[1], [Fr(y[j]) - f[0][j] for j in range(3)])) for y in Y} - {0}
            if len(sx) == 1 and len(sy) == 1 and sx != sy: return True
    return False
for par in (0, 1):
    pc = cut(par)
    okv = sum(vol(p[1]) for p in pc) == 1
    okin = all(all(0 <= Fr(x) <= 1 for x in v) for _, v in pc for v in v)
    okd = all(sep(a[1], b[1]) for a, b in itertools.combinations(pc, 2))
    # shapes: T pieces have lateral^2 = 3/4 (x 1/2 -> 3/8), O pieces lateral^2 = 1 (-> 1/2), bases 2 (-> 1)
    okshape = all(sorted(dd(v[0], x) for x in v[1:]) == ([Fr(3, 4)] * 3 if k == 'T' else [Fr(1)] * 3) and
                  all(dd(p, q) == 2 for p, q in itertools.combinations(v[1:], 2)) for k, v in pc)
    check(f'cube cut by its {"even" if par == 0 else "odd"} tetrahedron: 4 T + 4 O pyramids, inside the cube, disjoint interiors, volumes add to the cube',
          okv and okin and okd and okshape)
def cross(u, v): return [u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]]
for par in (0, 1):
    pc = cut(par); okf = True
    for ax in range(3):
        for val in (0, 1):
            fs = []
            for k, v in pc:
                for f in itertools.combinations(v, 3):
                    if all(Fr(x[ax]) == val for x in f): fs.append((k, f, v[0] in f))
            areas2 = [sum(t * t for t in cross([Fr(f[1][j]) - f[0][j] for j in range(3)], [Fr(f[2][j]) - f[0][j] for j in range(3)])) for _, f, _ in fs]
            if not (len(fs) == 2 and all(k == 'O' and lat for k, _, lat in fs) and areas2 == [1, 1]): okf = False
    check(f'cube ({"even" if par == 0 else "odd"} cut): each of its 6 faces is exactly two O lateral faces (right isosceles, area 1/2 each)', okf)

print(f'== {NPASS} PASS, {NFAIL} FAIL')
json.dump(summary, open('data/barlow-patches.json', 'w'), indent=1)
