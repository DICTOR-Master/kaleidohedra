# Fable, golden fill (paper section 7 "Open", DICTO's question, 2026-10-16). Exact in Q(sqrt5) unless a line says float.
# Part 1, obstruction: which walls of the golden region G (space minus the cut golden envelopes K of the bcc OCD packing) are not
#   golden planes? Golden = perpendicular to a two-fold axis, the only face planes of golden rhombohedra and the five Bodhi pieces.
# Part 2, one search pass: cover each non-golden wall (star tip) with one tetrahedral adapter bounded by the tip's own planes;
#   check exactly that the adapters fit (no overlaps), that afterwards every wall is golden, and list the convex edges of the
#   remaining region G' by axis type (a fill needs piece edges along each convex edge direction).
import sys, io, os, contextlib, itertools, json, numpy as np
PD = '/home/dicto/kaleidohedra/studies/2026-10-16-polar-dharma'; here = os.getcwd(); os.chdir(PD)
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
os.chdir(here)
from scipy.spatial import ConvexHull
St = dict(rev); OCD = St['dual of the Hecatodihedron']; ICO = St['icosahedron']
Z = Q(0)
dot = lambda a, b: a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
cross = lambda u, w: [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
sub = lambda u, w: [u[i] - w[i] for i in range(3)]; add = lambda u, w: [u[i] + w[i] for i in range(3)]
mul = lambda u, k: [x * k for x in u]; neg = lambda u: [-x for x in u]
fl = lambda v: np.array([x.f() for x in v]); key = lambda v: tuple((x.a, x.b) for x in v)
def sgn(x):
    a, b = x.a, x.b
    if a == 0 and b == 0: return 0
    if a >= 0 and b >= 0: return 1
    if a <= 0 and b <= 0: return -1
    return (1 if a > 0 else -1) if a * a - 5 * b * b > 0 else (1 if b > 0 else -1)
iszero = lambda v: all(x == Z for x in v)
out = []; say = lambda s: (print(s, flush=True), out.append(s))
# ---- exact axes from the exact icosahedron
e2 = min((dot(sub(a, b), sub(a, b)) for a, b in itertools.combinations(ICO, 2)), key=lambda x: x.f())
adj = [(i, j) for i, j in itertools.combinations(range(12), 2) if dot(sub(ICO[i], ICO[j]), sub(ICO[i], ICO[j])) == e2]
def lines(vs):
    L = []
    for v in vs:
        if not any(iszero(cross(v, w)) for w in L): L.append(v)
    return L
AX = {'5': lines(ICO), '2': lines([add(ICO[i], ICO[j]) for i, j in adj]),
      '3': lines([add(add(ICO[i], ICO[j]), ICO[k]) for i, j, k in itertools.combinations(range(12), 3) if all(p in adj for p in [(i, j), (i, k), (j, k)])])}
assert [len(AX[k]) for k in '523'] == [6, 15, 10]
def axtype(d):
    for k in '523':
        if any(iszero(cross(d, a)) for a in AX[k]): return k
    return 'none'
say('== Setup (exact)')
# ---- the OCD (exact planes) and the bond vectors, as in network.py
Of = np.array([fl(v) for v in OCD]); OP = []
for e in ConvexHull(Of).equations:
    idx = [i for i in range(len(OCD)) if abs(Of[i] @ e[:3] + e[3]) < 1e-7]
    if any(set(idx) == set(p[0]) for p in OP): continue
    n = cross(sub(OCD[idx[1]], OCD[idx[0]]), sub(OCD[idx[2]], OCD[idx[0]])); d = dot(n, OCD[idx[0]])
    if d.f() < 0: n, d = neg(n), -d
    assert all(dot(n, OCD[i]) == d for i in idx); OP.append((idx, n, d))
hexes = [p for p in OP if len(p[0]) == 6]; kites = [p for p in OP if len(p[0]) == 4]
assert len(hexes) == 20 and len(kites) == 60
assert all(axtype(n) == '3' for _, n, _ in hexes) and all(axtype(n) == 'none' for _, n, _ in kites)
unit = lambda n: fl(n) / np.linalg.norm(fl(n))
tet = next(c for c in itertools.combinations(range(20), 4) if all(abs(unit(hexes[a][1]) @ unit(hexes[b][1]) + 1 / 3) < 1e-9 for a, b in itertools.combinations(c, 2)))
T = [mul(hexes[i][1], Q(2) * hexes[i][2] / dot(hexes[i][1], hexes[i][1])) for i in tet]
LB = [add(T[0], T[1]), add(T[0], T[2]), T[0]]                     # bcc lattice basis (as golden_cut.py), one copy per cell
cellv = det3(*LB); cellv = cellv if sgn(cellv) > 0 else -cellv
say(f'OCD 20 hexagons (normals three-fold) + 60 kites (normals on no symmetry axis); bcc cell volume {cellv!r} = {cellv.f():.6f}')
# ---- polytope tools (exact)
def solve3(H3):
    (n1, d1), (n2, d2), (n3, d3) = H3; D = dot(n1, cross(n2, n3))
    if D == Z: return None
    return mul(add(add(mul(cross(n2, n3), d1), mul(cross(n3, n1), d2)), mul(cross(n1, n2), d3)), Q(1) / D)
def polytope(H):
    """H: list of (n, d) meaning n.x <= d. Exact vertices (float prefilter), facets, edges."""
    Hf = np.array([np.r_[fl(n), d.f()] for n, d in H]); V = {}
    for c in itertools.combinations(range(len(H)), 3):
        A = Hf[list(c), :3]
        if abs(np.linalg.det(A)) < 1e-12: continue
        x = np.linalg.solve(A, Hf[list(c), 3])
        if np.max(Hf[:, :3] @ x - Hf[:, 3]) > 1e-7: continue
        X = solve3([H[i] for i in c])
        if X is None or any(sgn(dot(n, X) - d) > 0 for n, d in H): continue
        V[key(X)] = X
    V = list(V.values()); F = []
    for n, d in H:
        on = [i for i, v in enumerate(V) if dot(n, v) == d]
        if len(on) >= 3 and not any(set(on) == set(g[2]) for g in F): F.append((n, d, on))
    E = [(i, j) for i, j in itertools.combinations(range(len(V)), 2) if sum(1 for g in F if i in g[2] and j in g[2]) >= 2]
    Vf = np.array([fl(v) for v in V]); c = Vf.mean(0)
    return {'H': [(n, d) for n, d, _ in F], 'F': F, 'V': V, 'E': E, 'Vf': Vf, 'c': c, 'r': np.max(np.linalg.norm(Vf - c, axis=1))}
def shift(P, c):
    cf = fl(c)
    return {'H': [(n, d + dot(n, c)) for n, d in P['H']], 'F': [(n, d + dot(n, c), on) for n, d, on in P['F']], 'V': [add(v, c) for v in P['V']],
            'E': P['E'], 'Vf': P['Vf'] + cf, 'c': P['c'] + cf, 'r': P['r'], 'kind': P.get('kind'), 'site': c}
def pvol(P):
    return volume(P['V'], P['Vf'])
# ---- the cut golden envelope K
H_K = []
for u in AX['2']:
    for s in (u, neg(u)):
        H_K.append((s, max((dot(s, v) for v in OCD), key=lambda x: x.f())))
JOINT = [(t, dot(t, t) / 2) for t in T] + [(neg(t), dot(t, t) / 2) for t in T]
K = polytope(H_K + JOINT); K['kind'] = 'K'
RT = polytope(H_K)
gold = [g for g in K['F'] if axtype(g[0]) == '2']; jf = [g for g in K['F'] if axtype(g[0]) == '3']
vK = pvol(K)
say(f'golden envelope (rhombic triacontahedron): {len(RT["V"])} corners, volume {pvol(RT)!r}; cut at the 8 joint planes: K has {len(K["V"])} corners, '
    f'{len(gold)} golden faces + {len(jf)} joint faces (normals three-fold), volume {vK!r} = {vK.f():.6f}')
vO = volume(OCD, Of)
say(f'per cell: OCD {vO.f() / cellv.f():.4%}, shell K-OCD {(vK - vO).f() / cellv.f():.4%}, golden region G {(cellv - vK).f() / cellv.f():.4%}'
    f' (exact: G per cell = {cellv - vK!r})')
# ---- neighbours; exact non-overlap (K centrally symmetric: K and K+c overlap iff c/2 is inside K)
near = []
for m in itertools.product(range(-3, 4), repeat=3):
    c = add(add(mul(LB[0], Q(m[0])), mul(LB[1], Q(m[1]))), mul(LB[2], Q(m[2])))
    if 0 < np.linalg.norm(fl(c)) < 2 * K['r'] + 1e-6: near.append(c)
def rel(x, P):   # max over facets of n.x - d, as exact signs: 'in', 'on', 'out'
    s = [sgn(dot(n, x) - d) for n, d in P['H']]
    return 'out' if max(s) > 0 else ('on' if max(s) == 0 else 'in')
half = lambda c: mul(c, Q(Fr(1, 2)))
touchK = [c for c in near if rel(half(c), K) == 'on']
assert not any(rel(half(c), K) == 'in' for c in near)
say(f'cut envelopes: {len(near)} neighbours checked, none overlap (exact); {len(touchK)} touch')
# OCD contacts (for the 22.6% variant): which OCD faces carry contacts?
OPH = [(n, d) for _, n, d in OP]
ocd_touch = [(c, [len(i) for i, n, d in OP if dot(n, half(c)) == d]) for c in near if all(sgn(dot(n, half(c)) - d) <= 0 for n, d in OPH)]
say(f'OCD copies: overlapping 0 (exact, as network.py); touching pairs per copy {len(ocd_touch)}, contact faces: '
    f'{sorted({tuple(f) for _, f in ocd_touch})} corners (hexagons only), so all 60 kites and the 12 free hexagons face the gap')
# ---- 2D exact polygon tools in a plane n.x = d
def proj_axis(n): return int(np.argmax(np.abs(fl(n))))
def to2(v, k): return [v[i] for i in range(3) if i != k]
def to3(p, k, n, d):
    o = [i for i in range(3) if i != k]; x = [Z, Z, Z]; x[o[0]], x[o[1]] = p
    x[k] = (d - n[o[0]] * p[0] - n[o[1]] * p[1]) / n[k]; return x
def ccw(P):
    P = list({key(p): p for p in P}.values()); Pf = np.array([fl(p) for p in P]); c = Pf.mean(0)
    return [P[i] for i in np.argsort(np.arctan2(Pf[:, 1] - c[1], Pf[:, 0] - c[0]))]
def area2(P):
    s = Z
    for i in range(len(P)): p, q = P[i], P[(i + 1) % len(P)]; s = s + p[0] * q[1] - p[1] * q[0]
    return s / 2
def clip(P, a, b):   # keep a.p <= b
    R = []
    for i in range(len(P)):
        p, q = P[i], P[(i + 1) % len(P)]; sp = sgn(a[0] * p[0] + a[1] * p[1] - b); sq = sgn(a[0] * q[0] + a[1] * q[1] - b)
        if sp <= 0: R.append(p)
        if sp * sq < 0:
            t = (b - a[0] * p[0] - a[1] * p[1]) / (a[0] * (q[0] - p[0]) + a[1] * (q[1] - p[1])); R.append([p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])])
    D = []
    for p in R:
        if not D or key(D[-1]) != key(p): D.append(p)
    if len(D) > 1 and key(D[0]) == key(D[-1]): D.pop()
    return D
def halfplanes(R):   # inside of a ccw convex polygon
    return [((R[(i + 1) % len(R)][1] - R[i][1], R[i][0] - R[(i + 1) % len(R)][0]),
             (R[(i + 1) % len(R)][1] - R[i][1]) * R[i][0] - (R[(i + 1) % len(R)][0] - R[i][0]) * R[i][1]) for i in range(len(R))]
def inter(P, R):
    for a, b in halfplanes(R): P = clip(P, a, b)
    return P
def minus(P, R):
    res, rest = [], P
    for a, b in halfplanes(R):
        o = clip(rest, (-a[0], -a[1]), -b)
        if len(o) >= 3 and area2(o) != Z: res.append(o)
        rest = clip(rest, a, b)
        if len(rest) < 3: break
    return res
# ---- Part 1: the joint faces, their contacts and the exposed star tips
say('\n== Part 1: non-golden walls (exact)')
tips = []; jarea_tot = Z; tip_tot = Z
for n, d, on in jf:
    k = proj_axis(n); J = ccw([to2(K['V'][i], k) for i in on]); aJ = area2(J)
    covers = []
    for c in touchK:
        if dot(n, half(c)) == d:   # K+c lies across this plane; its face there is c - J
            Cf = ccw([to2(sub(c, K['V'][i]), k) for i in on]); I = inter(J, Cf)
            if len(I) >= 3: covers.append((c, I))
    rest = [J]
    for c, I in covers:
        rest = [r for P in rest for r in minus(P, ccw(I))]
    cov = sum((area2(ccw(I)) for _, I in covers), Z); ta = sum((area2(r) for r in rest), Z)
    assert cov + ta == aJ, 'areas do not add up'
    tips += [(n, d, k, r, [c for c, _ in covers]) for r in rest]; jarea_tot += aJ; tip_tot += ta
say(f'each joint face: {len(jf)} per copy, a {len(on)}-gon; covered by {len(covers)} neighbour face(s); exposed tips per face: {len(rest)} '
    f'({" / ".join(str(len(r)) + "-gon" for r in rest)}); covered + exposed = whole face, exact')
say(f'exposed fraction of each joint face: {ta / aJ!r} = {(ta / aJ).f():.6f} (exact)')
tipshape = sorted({tuple(sorted((dot(sub(a, b), sub(a, b)).a, dot(sub(a, b), sub(a, b)).b) for a, b in itertools.combinations([to3(p, t[2], t[0], t[1]) for p in t[3]], 2))) for t in tips})
say(f'tip shapes (squared side lengths): {len(tipshape)} kind(s): ' + '; '.join(' , '.join(repr(Q(*x)) for x in s) for s in tipshape))
say('golden faces of K are golden-rhombus planes; the only other walls of G are these tips, in the 4 joint planes (three-fold normals).')
# ---- Part 2: tip adapters
say('\n== Part 2: one adapter per tip (exact)')
def tip_tetra(t):
    n, d, k, P, covs = t; P3 = [to3(p, k, n, d) for p in P]; H = [(neg(n), -d)]; sides = []
    for i in range(len(P3)):
        p, q = P3[i], P3[(i + 1) % len(P3)]; cand = []
        for gn, gd, _ in gold:
            if dot(gn, p) == gd and dot(gn, q) == gd: cand.append(('own face extended', (gn, gd)))
        for c in covs:
            for gn, gd, _ in gold:
                if dot(gn, sub(p, c)) == gd and dot(gn, sub(q, c)) == gd: cand.append(("neighbour's face", (neg(gn), -(gd + dot(gn, c)))))
        assert len(cand) == 1, f'tip edge on {len(cand)} planes'
        sides.append(cand[0][0]); H.append(cand[0][1])
    big = [(e, Q(100)) for e in ([Q(1), Z, Z], [Z, Q(1), Z], [Z, Z, Q(1)], [Q(-1), Z, Z], [Z, Q(-1), Z], [Z, Z, Q(-1)])]
    A = polytope(H + big); assert all(abs(x) < 50 for x in A['Vf'].ravel()), 'adapter unbounded'
    A = polytope(H); A['kind'] = 'A'; A['sides'] = sides; return A
ADP = [tip_tetra(t) for t in tips]
A0 = ADP[0]; vA = pvol(A0)
shape = lambda A: sorted((dot(sub(A['V'][i], A['V'][j]), sub(A['V'][i], A['V'][j])) for i, j in A['E']), key=lambda x: x.f())
assert all(len(A['V']) == 4 for A in ADP) and all(shape(A) == shape(A0) for A in ADP) and all(pvol(A) == vA for A in ADP)
fa = sorted(axtype(n) for n, d in A0['H'])
def dihedrals(A):
    res = []
    for i, j in A['E']:
        g = [g for g in A['F'] if i in g[2] and j in g[2]]; n1, n2 = unit(g[0][0]), unit(g[1][0])
        res.append((axtype(sub(A['V'][i], A['V'][j])), round(180 - np.degrees(np.arccos(np.clip(n1 @ n2, -1, 1))), 4), ''.join(sorted(axtype(x[0]) for x in g))))
    return sorted(res)
say(f'every tip is a triangle; each gets the tetrahedron bounded by the joint plane and the planes through its three edges '
    f'(sides: {", ".join(sorted(A0["sides"]))}). All {len(ADP)} per copy are congruent: squared edges {", ".join(repr(x) for x in shape(A0))};'
    f' volume {vA!r} = {vA.f():.6e}; face normals: {fa} (1 three-fold base, 3 golden)')
say('adapter edges (axis type of edge, dihedral in degrees FLOAT, axis types of the two faces): ' + '; '.join(f'{a} {b} [{c}]' for a, b, c in dihedrals(A0)))
# compare with the Cleo-Ico (pyramid on an icosahedron face, apex at the centre)
ci = [ICO[i] for i in next(t for t in itertools.combinations(range(12), 3) if all(p in adj for p in itertools.combinations(t, 2)))] + [[Z, Z, Z]]
ciE = sorted((dot(sub(a, b), sub(a, b)) for a, b in itertools.combinations(ci, 2)), key=lambda x: x.f())
ratio = lambda L: sorted(round((x / L[0]).f(), 9) for x in L)
say(f'Cleo-Ico squared-edge ratios {ratio(ciE)}; adapter {ratio(shape(A0))}: '
    + ('same shape up to scale' if ratio(ciE) == ratio(shape(A0)) else 'NOT a Cleo-Ico'))
# ---- all bodies, exact SAT checks, contacts
bodies0 = [K] + ADP
def sites():
    yield [Z, Z, Z]
    for c in near: yield c
ALL = [shift(B, c) for c in sites() for B in bodies0]
def sat(P, C):
    """Exact separating-axis test. Returns ('apart'|'touch', axis, level) or ('overlap',)."""
    axes = [n for n, d in P['H']] + [n for n, d in C['H']]
    axes += [cross(sub(P['V'][i], P['V'][j]), sub(C['V'][a], C['V'][b])) for i, j in P['E'] for a, b in C['E']]
    best = None
    for ax in axes:
        af = fl(ax); nf = np.linalg.norm(af)
        if nf < 1e-12: continue
        p, q = P['Vf'] @ af / nf, C['Vf'] @ af / nf
        for s, g in ((1, q.min() - p.max()), (-1, p.min() - q.max())):
            if best is None or g > best[0]: best = (g, ax if s == 1 else neg(ax))
    g, ax = best
    if g < -1e-9: return ('overlap',)
    mP = max((dot(ax, v) for v in P['V']), key=lambda x: x.f()); mC = min((dot(ax, v) for v in C['V']), key=lambda x: x.f())
    s = sgn(mC - mP); assert s >= 0, 'float/exact disagree'
    return ('apart' if s > 0 else 'touch', ax, mP)
contacts = []; nover = 0; npairs = 0
for i, P in enumerate([shift(B, [Z, Z, Z]) for B in bodies0]):
    for j, C in enumerate(ALL):
        if j == i or np.linalg.norm(P['c'] - C['c']) > P['r'] + C['r'] + 1e-9: continue
        npairs += 1; r = sat(P, C)
        if r[0] == 'overlap': nover += 1
        elif r[0] == 'touch': contacts.append((P, C, r[1], r[2]))
say(f'exact separating-axis test over {npairs} nearby pairs (envelopes and adapters): overlapping {nover}; touching {len(contacts)}')
assert nover == 0
# ---- convex edges of G (envelopes only) and G' (envelopes + adapters)
def contact_set(P, C, ax, lev):
    k = proj_axis(ax)
    fP = ccw([to2(v, k) for v in P['V'] if dot(ax, v) == lev]); fC = ccw([to2(v, k) for v in C['V'] if dot(ax, v) == lev])
    if len(fP) >= 3 and area2(fP) != Z and len(fC) >= 3 and area2(fC) != Z: S = inter(fP, fC)
    elif len(fP) >= 3 and len(fC) == 2: S = inter(fC, fP)
    elif len(fC) >= 3 and len(fP) == 2: S = inter(fP, fC)
    else: return []
    S = [to3(p, k, ax, lev) for p in S]
    if len(S) == 2: return [(S[0], S[1])]
    if len(S) >= 3: return [(S[i], S[(i + 1) % len(S)]) for i in range(len(S))]
    return []
Linv = np.linalg.inv(np.array([fl(b) for b in LB]).T)
def canon(seg):   # reduce a segment modulo the lattice, exact
    m = (fl(seg[0]) + fl(seg[1])) / 2; lam = np.floor(Linv @ m + 1e-9).astype(int)
    c = add(add(mul(LB[0], Q(int(lam[0]))), mul(LB[1], Q(int(lam[1])))), mul(LB[2], Q(int(lam[2]))))
    return frozenset([key(sub(seg[0], c)), key(sub(seg[1], c))])
def local_arcs(p, q, bodies):
    m = mul(add(p, q), Q(Fr(1, 2))); e = sub(q, p); ef = fl(e); ef /= np.linalg.norm(ef)
    u = np.cross(ef, [1, 0, 0] if abs(ef[0]) < .9 else [0, 1, 0]); u /= np.linalg.norm(u); w = np.cross(ef, u); cones = []
    for B in bodies:
        if np.linalg.norm(fl(m) - B['c']) > B['r'] + 1e-9: continue
        s = [sgn(dot(n, m) - d) for n, d in B['H']]
        if max(s) > 0: continue
        act = [fl(n) for (n, d), x in zip(B['H'], s) if x == 0]
        cones.append([np.array([a @ u, a @ w]) for a in act])
    bd = []
    for cn in cones:
        for a in cn:
            if np.linalg.norm(a) < 1e-12: return None
            th = np.arctan2(a[1], a[0]); bd += [th + np.pi / 2, th - np.pi / 2]
    bd = sorted(x % (2 * np.pi) for x in bd); bd.append(bd[0] + 2 * np.pi)
    free = []
    for a, b in zip(bd, bd[1:]):
        if b - a < 1e-12: continue
        th = (a + b) / 2; y = np.array([np.cos(th), np.sin(th)])
        free.append((a, b, not any(all(nn @ y <= 1e-12 for nn in cn) for cn in cones)))
    arcs, cur = [], None   # merge free intervals cyclically
    k0 = next((i for i, f in enumerate(free) if not f[2]), None)
    if k0 is None: return [360.0]
    seq = free[k0 + 1:] + free[:k0 + 1]
    for a, b, isf in seq:
        if isf: cur = (b - a) if cur is None else cur + (b - a)
        elif cur is not None: arcs.append(np.degrees(cur)); cur = None
    if cur is not None: arcs.append(np.degrees(cur))
    return arcs
def edge_report(bodies_kinds, label):
    seen = {}; bad = 0
    for P, C, ax, lev in contacts:
        if P['kind'] not in bodies_kinds or C['kind'] not in bodies_kinds: continue
        for seg in contact_set(P, C, ax, lev):
            cs = canon(seg)
            if cs in seen: continue
            arcs = local_arcs(seg[0], seg[1], [B for B in ALL if B['kind'] in bodies_kinds])
            if arcs is None: bad += 1; continue
            seen[cs] = (axtype(sub(seg[1], seg[0])), arcs, P['kind'] + C['kind'])
    tally = {}
    for t, arcs, pk in seen.values():
        for a in arcs:
            if a < 180 - 1e-6: tally[(t, round(a, 3))] = tally.get((t, round(a, 3)), 0) + 1
    say(f'{label}: {len(seen)} distinct contact-boundary segments per cell (exact, modulo the lattice){"; " + str(bad) + " skipped (vertex)" if bad else ""}; '
        f'convex edges of the free region by edge axis type and opening angle (angle FLOAT, degrees): '
        + ('; '.join(f'{t}-fold {a} x{c}' if t != 'none' else f'no-axis {a} x{c}' for (t, a), c in sorted(tally.items())) or 'none'))
    return tally
say('\n== Convex edges (a tile at a convex edge must have an edge along it; proof in FABLE-GOLDEN-FILL.md)')
tG = edge_report({'K'}, 'G (envelopes only)')
tG2 = edge_report({'K', 'A'}, "G' (envelopes + tip adapters)")
# every edge line of G' lies on a body edge or a contact boundary; body edges are subdivided only at the hexagram points (1/3, 2/3),
# so three exact sample points per body edge (1/6, 1/2, 5/6) see every piece of every body edge
inv = {}
for B in bodies0:
    for i, j in B['E']:
        p, q = B['V'][i], B['V'][j]; t = axtype(sub(q, p))
        for fr in (Fr(1, 6), Fr(1, 2), Fr(5, 6)):
            x = add(p, mul(sub(q, p), Q(fr))); arcs = local_arcs(sub(x, mul(sub(q, p), Q(Fr(1, 1000)))), add(x, mul(sub(q, p), Q(Fr(1, 1000)))), ALL)
            for a in arcs or []:
                if abs(a - 180) > 1e-6 and a < 360 - 1e-9: inv[(B['kind'], t, round(a, 3))] = inv.get((B['kind'], t, round(a, 3)), 0) + 1
say("G' along body edges (3 exact sample points per edge, bodies of one copy): free openings other than flat, by body, edge axis type, angle FLOAT: "
    + '; '.join(f'{k} {t}-fold {a} x{c}' for (k, t, a), c in sorted(inv.items())))
lens = {}
for P, C, ax, lev in contacts:
    for seg in contact_set(P, C, ax, lev):
        d = sub(seg[1], seg[0]); t = axtype(d)
        if t == '5':
            v = next(a for a in AX['5'] if iszero(cross(d, a))); i = next(k for k in range(3) if v[k] != Z); lam = d[i] / v[i]
            lens[repr(lam if sgn(lam) > 0 else -lam)] = (lam if sgn(lam) > 0 else -lam).f()
say(f'lengths of the 5-fold contact-boundary segments, in units of the five-fold vector |v| = icosahedron circumradius (exact): ' + ', '.join(f'{k} ({v:.6f})' for k, v in sorted(lens.items(), key=lambda kv: kv[1])))
vG2 = cellv - vK - vA * Q(len(ADP))
say(f"G' volume per cell {vG2!r} = {vG2.f():.6f} ({vG2.f() / cellv.f():.4%} of space); adapters {len(ADP)} per cell, {(vA * Q(len(ADP))).f() / cellv.f():.4%} of space")
# volume bookkeeping for golden rhombohedra spanned by five-fold vectors scaled by lam (edge lam*|v|): G' per cell = p*P + o*O ?
v5 = AX['5']; pr = [(a, b, c) for a, b, c in itertools.combinations(v5, 3)]
dets = sorted({(lambda x: x if sgn(x) > 0 else -x)(det3(a, b, c)) for a, b, c in pr}, key=lambda x: x.f()); dO, dP = dets
phi = Q(Fr(1, 2), Fr(1, 2))
assert dP == dO * phi, 'prolate/oblate volume ratio is not phi'
for lam, nm in [(phi / 9, 'phi/9 (one brick edge per convex edge)'), (Q(Fr(1, 9)), '1/9 (convex edge = phi bricks)'), (phi / 18, 'phi/18'), (Q(Fr(1, 18)), '1/18')]:
    x = vG2 / (lam * lam * lam * dO)       # = a + b*sqrt5; write as m + n*phi: m = a - b, n = 2b
    m, n = x.a - x.b, 2 * x.b
    say(f"brick edge {nm} x|v|: G' per cell = {m} oblate-units + {n} phi-units, i.e. p prolate + o oblate needs o + phi*p = {m} + {n} phi "
        f"-> p = {n}, o = {m}: " + ('whole and non-negative' if m.denominator == 1 and n.denominator == 1 and m >= 0 and n >= 0 else 'NOT whole/non-negative'))
# ---- Bodhi pieces: edge types implied by their dihedrals (golden planes: 36/72/108/144 -> 5-fold edge, 60/120 -> 3-fold, 90 -> 2-fold)
BD = '/home/dicto/kaleidohedra/studies/2026-10-12-bodhi-pieces/data'
say('\n== Bodhi pieces (FLOAT data from the Bodhi study): dihedral angles; edge type follows exactly from the angle between golden planes')
for b, nm in [('B1', 'Vajra (fine)'), ('B2', 'Chatra'), ('B3', 'Mudra'), ('B4', 'Crown Jewel'), ('B5', 'Diadem')]:
    D = json.load(open(f'{BD}/bodhi-{b}-unit.json')); ang = sorted({round(x) for x in D['dihedralDegrees'].values()})
    typ = lambda a: '5' if a in (36, 72, 108, 144) else ('3' if a in (60, 120) else ('2' if a == 90 else '?'))
    say(f'{nm}: ' + ', '.join(f'{a} ({typ(a)}-fold edge)' for a in ang))
open('data/golden-fill.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'adapters': [[fl(v).tolist() for v in A['V']] for A in ADP], 'K': [fl(v).tolist() for v in K['V']]}, open('data/golden-fill.json', 'w'))
