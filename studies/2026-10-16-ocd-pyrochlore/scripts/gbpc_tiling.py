# Fable, GBPC tiling of G' (2026-10-16, DICTO's go). Exact in Q(sqrt5) unless a line says FLOAT.
# G' = golden region minus the 24 GBPCs (Golden Bodhi Pyrochlore Corners) per cell. Questions: corner cones, module, walls, tiling.
import sys, io, os, contextlib, itertools, json, numpy as np
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
src = open(os.path.join(HERE, 'golden_fill.py')).read().split('# ---- all bodies')[0]
cwd = os.getcwd(); os.chdir(STUDY)
with contextlib.redirect_stdout(io.StringIO()):
    exec(src)
os.chdir(cwd)
out = []; say = lambda s: (print(s, flush=True), out.append(s))
say('DICTO · dictospheres.com — Fable, GBPC tiling of G\' (exact in Q(sqrt5) unless marked FLOAT)')
GB = ADP  # the 24 GBPCs of the copy at the origin
# ---------- A. G' is the complement of the union of the uncut triacontahedra RT (bcc sites)
RT['kind'] = 'RT'
nearRT = [c for c in near if np.linalg.norm(fl(c)) < 2 * RT['r'] + 1e-9]
inside = lambda x, P: all(sgn(dot(n, x) - d) <= 0 for n, d in P['H'])
def inter_poly(P, C):
    Hf = [(n, d) for n, d in P['H']] + [(n, d) for n, d in C['H']]
    try: X = polytope(Hf)
    except Exception: return None
    return X if len(X['V']) >= 4 else None
pair = []
for c in nearRT:
    X = inter_poly(RT, shift(RT, c))
    if X is not None and pvol(X) != Z: pair.append((c, pvol(X)))
vRT = pvol(RT); union = vRT - sum((v for _, v in pair), Z) * Q(Fr(1, 2))
assert all(inside(v, RT) for v in K['V']) and all(any(inside(v, shift(RT, c)) for c in [[Z, Z, Z]] + nearRT) is True for A in GB for v in A['V'])
assert all(all(inside(v, RT) for v in A['V']) for A in GB), 'GBPC not inside own RT'
# triple overlaps: for every two overlapping neighbours c1, c2, RT ∩ RT+c1 ∩ RT+c2 has zero volume
trip = 0
for (c1, _), (c2, _) in ([] if os.environ.get('FAST') else itertools.combinations(pair, 2)):
    H = RT['H'] + shift(RT, c1)['H'] + shift(RT, c2)['H']
    X = inter_poly({'H': H}, {'H': []})
    if X is not None and pvol(X) != Z: trip += 1
say(f'\n== A. What G\' is (exact)')
say(f'uncut triacontahedra RT on the bcc sites: {len(pair)} neighbours overlap each RT, each overlap volume {pair[0][1]!r}; triple overlaps of positive volume: {trip}')
say(f'union per cell = vol(RT) - (1/2) sum of pair overlaps = {union!r}; K + 24 GBPC per cell = {vK + vA * Q(24)!r}; equal: {union == vK + vA * Q(24)}')
assert union == vK + vA * Q(24) and trip == 0  # FAST=1 skips the triple check (development only)
say('K and every GBPC lie inside the uncut RT, and the volumes match, so G\' = space minus the union of the uncut RTs (up to measure zero).')
say('Each GBPC is the part of an RT corner cap that sticks out beyond the joint plane and is not inside the joined neighbour.')
# ---------- B. the walls of G' (exact): each wall lies in a face plane of some RT; in the plane, wall = (union of RT faces in it)
# minus (open cross-sections of the RTs that cut it). Coordinates (x, y): p = o + x*a + y*b, a, b the two five-fold vectors in the plane.
say('\n== B. Walls of G\' (exact)')
sites = []
for m in itertools.product(range(-4, 5), repeat=3):
    c = add(add(mul(LB[0], Q(m[0])), mul(LB[1], Q(m[1]))), mul(LB[2], Q(m[2])))
    if np.linalg.norm(fl(c)) < 3 * RT['r']: sites.append(c)
def frame(n):
    ab = [v for v in AX['5'] if dot(n, v) == Z]; assert len(ab) == 2; return ab
def coords(p, o, a, b, n):
    w = sub(p, o); D = dot(cross(a, b), n)
    return [dot(cross(w, b), n) / D, dot(cross(a, w), n) / D]
def section(P, n, d, o, a, b):
    """P ∩ plane as ccw polygon in (x, y), or None. Returns (poly, is_face)."""
    s = [sgn(dot(nn, n_) ) for nn, _ in [(n, d)] for n_ in [n]]
    on = [v for v in P['V'] if dot(n, v) == d]
    up = [v for v in P['V'] if sgn(dot(n, v) - d) > 0]; dn = [v for v in P['V'] if sgn(dot(n, v) - d) < 0]
    if not up or not dn:
        if len(on) >= 3: return (ccw([coords(v, o, a, b, n) for v in on]), True)
        return None
    pts = [coords(v, o, a, b, n) for v in on]
    for i, j in P['E']:
        p, q = P['V'][i], P['V'][j]; sp, sq = sgn(dot(n, p) - d), sgn(dot(n, q) - d)
        if sp * sq < 0:
            t = (d - dot(n, p)) / dot(n, sub(q, p)); pts.append(coords(add(p, mul(sub(q, p), t)), o, a, b, n))
    return (ccw(pts), False)
def inpoly(pt, R, strict):
    for (u, w), b in halfplanes(R):
        s = sgn(u * pt[0] + w * pt[1] - b)
        if s > 0 or (strict and s == 0): return False
    return True
walls = []
for fn, fd, on in RT['F']:
    a, b = frame(fn); o = RT['V'][on[0]]
    plus, minus_ = [], []
    for c in sites:
        R = shift(RT, c); sct = section(R, fn, fd, o, a, b)
        if sct is None: continue
        (plus if sct[1] else minus_).append((sct[0], np.linalg.norm(fl(c))))
    pieces = []
    plusP = [P for P, _ in plus]; minusP = [M for M, _ in minus_]
    for P, r in plus:
        rest = [P]
        for M in minusP:
            rest = [q for X in rest for q in minus(X, M)]
        pieces += [(X, r) for X in rest]
    walls.append(dict(n=fn, d=fd, a=a, b=b, o=o, plus=plusP, minus=minusP, pieces=pieces))
inwall = lambda pt, W: any(inpoly(pt, P, False) for P in W['plus']) and not any(inpoly(pt, M, True) for M in W['minus'])
eps = Q(Fr(1, 10**6)); eps2 = Q(Fr(1, 7 * 10**6))
def corner_coeffs(W):
    C = {}
    for P in W['pieces']:
        for v in P:
            k = key(v)
            if k in C: continue
            occ = [inwall([v[0] + sx * eps, v[1] + sy * (eps + eps2)], W) for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
            cv = occ[0] - occ[1] + occ[2] - occ[3]
            if cv: C[k] = (v, cv)
    return list(C.values())
# connected components of each wall plane (pieces sharing a boundary segment of positive length)
def seg_overlap(p, q, r, s):
    d = [q[0] - p[0], q[1] - p[1]]
    cr = lambda u: d[0] * (u[1] - p[1]) - d[1] * (u[0] - p[0])
    if cr(r) != Z or cr(s) != Z: return False
    t = lambda u: ((u[0] - p[0]) * d[0] + (u[1] - p[1]) * d[1]) / (d[0] * d[0] + d[1] * d[1])
    lo, hi = sorted([t(r), t(s)], key=lambda x: x.f())
    return sgn(min(hi, Q(1), key=lambda x: x.f()) - max(lo, Z, key=lambda x: x.f())) > 0
def components(W):
    P = W['pieces']; n = len(P); parent = list(range(n))
    def f(i):
        while parent[i] != i: i = parent[i]
        return i
    for i, j in itertools.combinations(range(n), 2):
        A, B = P[i][0], P[j][0]
        if np.linalg.norm(np.mean([fl(x) for x in A], 0) - np.mean([fl(x) for x in B], 0)) > 3: continue
        if any(seg_overlap(A[k], A[(k + 1) % len(A)], B[l], B[(l + 1) % len(B)]) for k in range(len(A)) for l in range(len(B))):
            parent[f(i)] = f(j)
    comp = {}
    for i in range(n): comp.setdefault(f(i), []).append(i)
    return [[P[i] for i in c] for c in comp.values()]
def comp_corners(W, comp):
    Wc = dict(W); Wc['pieces'] = [p for p, _ in comp]
    # membership restricted to this component
    Wc['plus'] = [p for p, _ in comp]; Wc['minus'] = []
    return corner_coeffs(Wc)
WALL = []   # distinct walls modulo the lattice, one record each
for W in walls:
    for comp in components(W):
        # keep the components that contain a piece of the origin RT's own face (site 0): every wall is one of these modulo the lattice
        if not any(r < 1e-9 for _, r in comp): continue
        trunc = max(r for _, r in comp) > 2 * RT['r']
        C = comp_corners(W, comp)
        area = sum((area2(p) for p, _ in comp), Z)
        WALL.append(dict(W=W, comp=comp, C=C, area=area, trunc=trunc))
say(f'wall components touching the origin RT\'s faces: {len(WALL)} (truncated by the finite site set: {sum(w["trunc"] for w in WALL)})')
# ---------- C. the wall test (exact). A tile face lying in a wall plane is a parallelogram lam*a x lam*b (a, b the plane's two five-fold
# vectors). In (x, y) units of a, b each such face is a lam x lam square. Dissection invariant (exact): for F(x, y) = g(x) h(y) with g, h
# lam-periodic, the double integral of d2F/dxdy over a lam-square is 0, and over a wall it is sum_v c_v F(v) (c_v = corner sign). So
# a wall can be covered by such faces (in any arrangement, edge-to-edge or not) only if, for every class of corners modulo lam in x
# and in y, the corner signs add up to 0. lam must divide some coordinate difference, so lam is in Q(sqrt5); write lam = theta/N with
# theta = s + t*sqrt5 (direction class t/s). The most permissive choice of N makes two corners equivalent exactly when both their
# x- and y-differences are rational multiples of theta.
def ratio_key(d):
    if d.a == 0 and d.b == 0: return None
    return ('inf' if d.a == 0 else d.b / d.a)
def in_Qtheta(d, th):
    if d.a == 0 and d.b == 0: return True
    return ratio_key(d) == th
def wall_ok(C, th):
    cls = []
    for v, c in C:
        for k in cls:
            w = k[0]
            if in_Qtheta(v[0] - w[0], th) and in_Qtheta(v[1] - w[1], th): k[1] += c; break
        else: cls.append([v, c])
    return all(k[1] == 0 for k in cls)
cand = set()
for w in WALL:
    for (v, _), (u, _) in itertools.combinations(w['C'], 2):
        for d in (v[0] - u[0], v[1] - u[1]):
            if ratio_key(d) is not None: cand.add(ratio_key(d))
tkey = lambda t: 'rational (theta = 1)' if t == 0 else ('theta = sqrt5' if t == 'inf' else f'theta = 1 + ({t})sqrt5')
passing = [set(t for t in cand if wall_ok(w['C'], t)) for w in WALL]
common = set.intersection(*passing) if passing else set()
wshapes = {}
for w, p in zip(WALL, passing):
    sig = (len(w['C']), repr(w['area']), tuple(sorted(map(str, p))))
    wshapes.setdefault(sig, []).append(w)
say(f'\n== C. Wall test (exact; any arrangement of rhombohedron faces, edge-to-edge or not, one rhombohedron size lam*|v|)')
say(f'{len(WALL)} wall components on the 30 faces of one RT, {len(wshapes)} kinds; candidate scale classes theta tested: {len(cand)}')
for (nc, ar, p), ws in wshapes.items():
    say(f'  kind x{len(ws)}: {nc} corners, area {ar} (frame units); scale classes that pass: ' + (', '.join(tkey(Fr(x)) if x not in ('inf',) else tkey(x) for x in p) or 'NONE'))
say(f'scale classes passing on every wall: ' + (', '.join(map(str, common)) or 'NONE'))
# coarsest lam = phi/N that passes on every wall
phiQ = Q(Fr(1, 2), Fr(1, 2))
def wall_ok_lam(C, lam):
    cls = {}
    for v, c in C:
        x, y = v[0] / lam, v[1] / lam
        for z in (x, y): assert z.b == 0
        k = (x.a % 1, y.a % 1); cls[k] = cls.get(k, 0) + c
    return all(s == 0 for s in cls.values())
Nmin = next(N for N in range(1, 400) if all(wall_ok_lam(w['C'], phiQ / N) for w in WALL))
say(f'coarsest passing scale: lam = phi/{Nmin} (rhombohedron edge (phi/{Nmin})|v| = {(phiQ / Nmin).f():.6f}|v|); every lam = phi/(k*{Nmin}) passes too;'
    f' any lam not a rational multiple of phi fails on every wall')
# ---------- D. corners of G' and their free cones (exact)
say('\n== D. Corner test (exact): free cone at each corner vs unions of rhombohedron corner cones')
def red(p):   # reduce a point modulo the lattice (exact key)
    lam = np.floor(Linv @ fl(p) + 1e-9).astype(int)
    c = add(add(mul(LB[0], Q(int(lam[0]))), mul(LB[1], Q(int(lam[1])))), mul(LB[2], Q(int(lam[2]))))
    return sub(p, c)
Linv = np.linalg.inv(np.array([fl(b) for b in LB]).T)
CORN = {}
for w in WALL:
    W = w['W']
    for v, c in w['C']:
        p = add(W['o'], add(mul(W['a'], v[0]), mul(W['b'], v[1]))); r = red(p); CORN.setdefault(key(r), r)
CORN = list(CORN.values())
# the 120 chambers of the mirror (golden-plane) arrangement: rays to 5-, 3-, 2-fold points
P5 = AX['5'] + [neg(v) for v in AX['5']]; P3 = AX['3'] + [neg(v) for v in AX['3']]; P2 = AX['2'] + [neg(v) for v in AX['2']]
G2 = [g for g, _ in [(n, 0) for n in AX['2']]]
def side(u, n): return sgn(dot(u, n))
CH = []
for a5 in P5:
    for a3 in P3:
        for a2 in P2:
            u = add(add(a5, a3), a2)
            # a chamber iff no mirror plane separates the three rays and the interior point is on no mirror
            if any(side(u, n) == 0 for n in AX['2']): continue
            if all(side(x, n) * side(u, n) >= 0 for n in AX['2'] for x in (a5, a3, a2)): CH.append(u)
uniq = {}
for u in CH: uniq.setdefault(tuple(side(u, n) for n in AX['2']), u)
CH = list(uniq.values()); say(f'{len(CH)} chambers of the 15 golden mirror planes (exact)')
assert len(CH) == 120
SITES1 = [[Z, Z, Z]] + nearRT + [c for c in near if c not in nearRT]
def free_chambers(p):
    blocked = set()
    for c in sites:
        R = shift(RT, c)
        if np.linalg.norm(fl(p) - R['c']) > R['r'] + 1e-9: continue
        s = [sgn(dot(n, p) - d) for n, d in R['H']]
        if max(s) > 0: continue
        act = [n for (n, d), x in zip(R['H'], s) if x == 0]
        for i, u in enumerate(CH):
            if all(sgn(dot(n, u)) < 0 for n in act): blocked.add(i)
    return frozenset(range(120)) - blocked
def cone_set(gens, lines=()):
    """chambers whose interior point is a positive combination of gens plus any multiple of the lines (exact, Cramer)."""
    S = set()
    for i, u in enumerate(CH):
        A = list(gens) + list(lines); D = det3(*A)
        if D == Z: return None
        co = [det3(*[u if k == j else A[k] for k in range(3)]) / D for j in range(3)]
        if all(sgn(co[j]) > 0 for j in range(len(gens))): S.add(i)
    return frozenset(S)
TC = {}
for r in itertools.combinations(P5, 3):
    if any(iszero(add(x, y)) for x, y in itertools.combinations(r, 2)): continue
    s = cone_set(r)
    if s: TC.setdefault(s, ('vertex', r))
for l in AX['5']:
    for r in itertools.combinations([x for x in P5 if not iszero(cross(x, l))], 2):
        if iszero(cross(r[0], r[1])): continue
        s = cone_set(r, [l])
        if s is not None and s: TC.setdefault(s, ('edge', r))
for n in AX['2']:
    for nn in (n, neg(n)):
        TC.setdefault(frozenset(i for i, u in enumerate(CH) if sgn(dot(u, nn)) > 0), ('face', nn))
say(f'tile cones at a point, as chamber sets: {sum(1 for v in TC.values() if v[0]=="vertex")} rhombohedron corner cones, '
    f'{sum(1 for v in TC.values() if v[0]=="edge")} edge wedges, {sum(1 for v in TC.values() if v[0]=="face")} half-spaces')
def exact_cover(U, sets, need_vertex):
    U = set(U)
    if not U: return []
    i = min(U)
    for s, kind in sets:
        if i in s and s <= U:
            r = exact_cover(U - s, sets, need_vertex)
            if r is not None: return [kind] + r
    return None
TCl = sorted(TC.items(), key=lambda kv: -len(kv[0]))
TCv = [(s, k) for s, k in TCl if k[0] == 'vertex']
res = {}
for p in CORN:
    F_ = free_chambers(p)
    if not F_ or len(F_) == 120: continue
    sol = exact_cover(F_, TCl, False)
    solv = exact_cover(F_, TCv, True)
    k = (len(F_), sol is not None, solv is not None)
    res.setdefault(k, []).append(p)
say(f'{len(CORN)} wall corners modulo the lattice; by free cone size in chambers (of 120) and whether it splits into tile cones '
    f'(any: corner cones, edge wedges, half-spaces / corner cones only):')
for k, ps in sorted(res.items()):
    say(f'  free {k[0]}/120 chambers x{len(ps)}: tile cones {"yes" if k[1] else "NO"}; rhombohedron corner cones only {"yes" if k[2] else "no"}')
# ---------- E. module check (exact)
say('\n== E. Module check (exact)')
V6 = [v if sgn(next(x for x in v if x != Z)) > 0 else neg(v) for v in AX['5']]
def solveQ(Mx, y):   # rational Gaussian elimination
    n = len(Mx); A = [list(map(Fr, r)) + [Fr(y[i])] for i, r in enumerate(Mx)]
    for c in range(n):
        p = next(r for r in range(c, n) if A[r][c] != 0); A[c], A[p] = A[p], A[c]
        A[c] = [x / A[c][c] for x in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0: A[r] = [x - A[r][c] * z for x, z in zip(A[r], A[c])]
    return [A[i][n] for i in range(n)]
flat = lambda u: [z for x in u for z in (x.a, x.b)]
B6 = [[flat(v)[r] for v in V6] for r in range(6)]
mcoef = lambda u: solveQ(B6, flat(u))
phi_closed = all(all(c.denominator == 1 for c in mcoef(mul(v, phiQ))) for v in V6)
say(f'M = Z-span of the six five-fold vectors v1..v6 (|v| = icosahedron circumradius): rank 6, its rational span is all of Q(sqrt5)^3, '
    f'so every exact point lies in (1/N)M for some N. M is closed under multiplication by phi: {phi_closed}')
x0 = CORN[0]
gens = [sub(p, x0) for p in CORN[1:]] + LB
kmin = None
for k in range(1, 200):
    lam = phiQ / (9 * k)
    if all(all(c.denominator == 1 for c in mcoef(mul(g, Q(1) / lam))) for g in gens): kmin = k; break
say(f'all corners of G\' (48 per cell, all lattice translates) lie in one coset x0 + lam*M for lam = phi/(9k) first at k = {kmin}, '
    f'i.e. lam = phi/{9 * kmin} (edge {(phiQ / (9 * kmin)).f():.6f}|v|); then also for every lam = phi/(9k), k = 1, 2, 3, ...')
# ---------- F. the Galois (perp-space) count (exact). sigma: a + b sqrt5 -> a - b sqrt5, coordinatewise.
# In a face-to-face tiling of a connected region by golden rhombohedra with edges +-lam*v_i, every tile corner lies in x0 + lam*M,
# so sigma is defined on all tile corners; extend it affinely over each tile (map F). Then the signed volume of F(tile) is sigma(vol tile):
# sigma(prolate) and sigma(oblate) volumes. Homotopy formula: for U = the tiles meeting an N^3 block of cells and A the linear map with
# sigma(T) = A T on the lattice, int_U F*w = det(A) vol(U) + flux of the straight homotopy (A -> F) through the boundary of U.
# On the walls F is fixed by the wall geometry (lattice periodic up to A T), so the wall flux per cell, Phi, is a fixed number;
# the cut through the block costs O(N^2) because |F - A| stays bounded (every corner is a bounded number of tile edges from a wall).
say('\n== F. Galois count (exact): what the tile frequencies must satisfy in any face-to-face tiling')
sig = lambda x: Q(x.a, -x.b); sigv = lambda v: [sig(x) for x in v]
def matA(Lc):
    D = det3(*Lc); rows = [mul(cross(Lc[1], Lc[2]), Q(1) / D), mul(cross(Lc[2], Lc[0]), Q(1) / D), mul(cross(Lc[0], Lc[1]), Q(1) / D)]
    S_ = [sigv(c) for c in Lc]
    return lambda x: add(add(mul(S_[0], dot(rows[0], x)), mul(S_[1], dot(rows[1], x))), mul(S_[2], dot(rows[2], x)))
def poly_centroid(P):   # ccw convex polygon in (x, y): (area, centroid)
    Atot, cx, cy = Z, Z, Z
    for i in range(1, len(P) - 1):
        a_, b_, c_ = P[0], P[i], P[i + 1]
        ar = ((b_[0] - a_[0]) * (c_[1] - a_[1]) - (b_[1] - a_[1]) * (c_[0] - a_[0])) / 2
        Atot = Atot + ar; cx = cx + ar * (a_[0] + b_[0] + c_[0]) / 3; cy = cy + ar * (a_[1] + b_[1] + c_[1]) / 3
    return Atot, cx, cy
def wall_flux(o, a, b, nu_out, polys, p0, xy0, s_, Af):
    Atot, cx, cy = Z, Z, Z
    for P in polys:
        ar, x_, y_ = poly_centroid(P); Atot = Atot + ar; cx = cx + x_; cy = cy + y_
    cx, cy = cx / Atot, cy / Atot
    c3 = add(o, add(mul(a, cx), mul(b, cy)))
    FW = add(sigv(p0), add(mul(sigv(a), s_ * (cx - xy0[0])), mul(sigv(b), s_ * (cy - xy0[1]))))
    Dv = sub(FW, Af(c3)); al, ga = Af(a), Af(b); be, de = sub(mul(sigv(a), s_), al), sub(mul(sigv(b), s_), ga)
    I = det3(Dv, al, ga) + (det3(Dv, al, de) + det3(Dv, be, ga)) * Q(Fr(1, 2)) + det3(Dv, be, de) * Q(Fr(1, 3))
    eps_ = sgn(dot(cross(a, b), nu_out))
    return I * Atot * Q(eps_)
# calibration on a known case: U = one RT (tiled by 10 prolate + 10 oblate), any A
def rt_identity(Af, detA):
    tot = Z
    for fn, fd, on in RT['F']:
        a, b = frame(fn); o = RT['V'][on[0]]
        P = ccw([coords(RT['V'][i], o, a, b, fn) for i in on]); t = max((x for p in P for x in p if x != Z), key=lambda z: z.f())
        tot = tot + wall_flux(o, a, b, fn, [P], o, [Z, Z], sig(t) / t, Af)   # U = RT, outward normal fn
    return sig(vRT), detA * vRT, tot
Lc = LB; A_ = matA(Lc); detA = det3(*[A_(e) for e in ([Q(1), Z, Z], [Z, Q(1), Z], [Z, Z, Q(1)])])
cal = []
for Af, dA, nm in [(lambda x: [Z, Z, Z], Z, 'A = 0'), (A_, detA, 'A of the bcc lattice')]:
    sv, dv, fl_ = rt_identity(Af, dA)
    Ssign = 1 if sv == dv + fl_ else (-1 if sv == dv - fl_ else 0); cal.append(Ssign)
    say(f'calibration, U = one RT, {nm}: sigma(vol RT) = {sv!r}; det(A) vol + flux = {dv + fl_!r}; '
        + ('identity holds exactly' if Ssign == 1 else ('holds with flux sign -1' if Ssign == -1 else 'FAILS')))
assert cal[0] == cal[1] != 0; SS = Q(cal[0])
# the walls of G' per cell (distinct modulo the lattice)
WD = {}
for w in WALL:
    W = w['W']; k3 = frozenset(key(red(add(W['o'], add(mul(W['a'], v[0]), mul(W['b'], v[1]))))) for v, _ in w['C'])
    WD.setdefault(k3, w)
own = all(all(r < 1e-9 for _, r in w['comp']) for w in WD.values())
Phi = Z; sphi = sig(phiQ) / phiQ
for w in WD.values():
    W = w['W']; v0 = w['C'][0][0]; p0 = add(W['o'], add(mul(W['a'], v0[0]), mul(W['b'], v0[1])))
    Phi = Phi + wall_flux(W['o'], W['a'], W['b'], neg(W['n']), [p for p, _ in w['comp']], p0, v0, sphi, A_)
say(f'walls of G\' per cell: {len(WD)} (each inside one RT face: {own})')
vG2 = cellv - union
v5 = AX['5']; dets = sorted({(lambda x: x if sgn(x) > 0 else -x)(det3(a, b, c)) for a, b, c in itertools.combinations(v5, 3)}, key=lambda x: x.f()); dO, dP = dets
assert dP == dO * phiQ
lhs = det3(*[A_(e) for e in ([Q(1), Z, Z], [Z, Q(1), Z], [Z, Z, Q(1)])]) * vG2 + SS * Phi
say(f"per cell: det(A) vol(G') + wall flux = {lhs!r}; sigma(vol G') = {sig(vG2)!r}; equal: {lhs == sig(vG2)}")
# densities: p prolate + o oblate per cell at lam = phi/9
lam = phiQ / 9; tP, tO = lam * lam * lam * dP, lam * lam * lam * dO
Dm = tP * sig(tO) - tO * sig(tP)
pbar = (vG2 * sig(tO) - tO * lhs) / Dm; obar = (tP * lhs - sig(tP) * vG2) / Dm
say(f'equations per cell at lam = phi/9: p*vol(P) + o*vol(O) = vol(G\'), p*sigma(vol P) + o*sigma(vol O) = {lhs!r}; '
    f'unique solution p = {pbar!r}, o = {obar!r} (exact; for lam = phi/(9k) multiply by k^3)')
say('o < 0: NO face-to-face tiling of G\' by golden rhombohedra of one size exists, periodic or not, at any scale.' if sgn(obar) < 0 else 'no contradiction from the count')
# ---------- G. what would remove the count obstruction (volume units of the oblate at lam = phi/9: G' = -30 + 66 phi per cell)
say('\n== G. Removing the count obstruction (exact bookkeeping, lam = phi/9; units = oblate volume, x = m + n*phi)')
u = lambda V_: (lambda x: (x.a - x.b, 2 * x.b))(V_ / tO)
cands = [('GBPC', vA), ('small oblate (edge lam/phi)', tO / (phiQ * phiQ * phiQ)), ('small prolate (edge lam/phi)', tP / (phiQ * phiQ * phiQ)),
         ('big oblate (edge phi*lam)', tO * phiQ * phiQ * phiQ), ('big prolate (edge phi*lam)', tP * phiQ * phiQ * phiQ)]
for nm, V_ in cands:
    m, n = u(V_); say(f'  {nm}: m = {m}, n = {n}')
say('with both sizes (edges phi/9 and 1/9 times |v|) the wall test says nothing (the two periods are incommensurable), and the count needs '
    'o - 3o\' + 2p\' = -30, p + 2o\' - p\' = 66 (primes = small): solvable with all >= 0, and it forces at least 10 small oblates per cell.')
if not os.environ.get('FAST'):
    open(os.path.join(STUDY, 'data', 'gbpc-tiling.txt'), 'w').write('\n'.join(out) + '\n')
    json.dump({'mark': 'DICTO · dictospheres.com', 'units': 'same frame as golden-fill.json; |v| = icosahedron circumradius',
               'corners_mod_lattice': [fl(p).tolist() for p in CORN],
               'walls': [[[fl(add(w['W']['o'], add(mul(w['W']['a'], x), mul(w['W']['b'], y)))).tolist() for x, y in P] for P, _ in w['comp']] for w in WD.values()],
               'density_per_cell_lam_phi_over_9': {'prolate': 66, 'oblate': -30}}, open(os.path.join(STUDY, 'data', 'gbpc-tiling.json'), 'w'))
