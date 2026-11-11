# cut_family.py (from scale_norm.py), DICTO 11 Nov 2026 ("set up the cut-depth family and it only has two edge lengths"): the Catalan
# pentakis (same five-fold corners as the OG) with its 20 six-fold corners cut by planes perpendicular to the three-fold axes at distance
# lam * (six-fold corner radius); lam* = the OG's hexagon planes. Per depth (exact Q(sqrt5)): corners, faces, edge lengths, hexagons
# regular?, hop cycle test (D_{k+4} = c D_k exact), face counts k <= 6. Control: lam* reproduces the OG exactly. Original: scale_norm.py, DICTO 11 Nov 2026 ("check the 3/phi^2 scale with a common normalisation"): the level-1 twin
# hulls of the OG and the Catalan pentakis are similar with raw scale c = (9 - 3 sqrt5)/2 = 3/phi^2, but the Catalan start's size was
# arbitrary. Scaling a start by s (in Q(sqrt5)) scales its family by s and its TWIN family by s' = conj(s). Normalise the starts to equal
# circumradius, and to equal inradius; when the needed s is in Q(sqrt5) (ratio of squares is a square there), the normalised scale is
# c_norm = c_raw * conj(s_CAT) for s_CAT scaling the Catalan start to the OG's size. Original: level1_match.py (from pentakis_cycle.py), DICTO 11 Nov 2026 ("check the level 1 match exactly"): are the OG's level-1 and level-5
# Angeli exactly the Catalan pentakis's level-1 Angelus? Exact fin cos^2 classes, and exact similarity of the twin hulls (corner sets,
# c^2 = R^2 ratio denested, same orientation). Original: pentakis_cycle.py (from pentakis_family.py), DICTO 11 Nov 2026 ("check the exact scale of the 4-cycle and angel family thread"):
# (1) EXACT 4-cycle: is D_{k+4} = c * D_k as exact point sets, with c in Q(sqrt5)? (c^2 = R^2(D_{k+4}) / R^2(D_k), denested);
# (2) the ANGELI THREAD: the Angelus (Vacuus of the twin hull) at each step of the cycle: fins, exact apex cos^2, fin planes, discs.
# Original header: pentakis_family.py, DICTO 11 Nov 2026 ("i wonder if other pentakis produce dodecahedrons, icosahedrons and rhombicosidodecahedrons").
# The OG family's twin hulls pass exactly through the regular icosahedron (k = 2) and dodecahedron (k = 3, 7) and rhombicosidodecahedron
# patterns (k = 1, 5, 6). Do other PENTAKIS DODECAHEDRA, used as the start D_0 of the same hop (D_{k+1} = hull of the foot points of D_k's
# face planes), do the same? Starts (exact Q(sqrt5)): the Catalan pentakis dodecahedron (polar dual of the regular truncated icosahedron)
# and dodecahedra with a pyramid on each face, apex at relative heights h (apex radius = face distance * (1 + h)), h in Q(sqrt5).
# Per start and level k <= KMAX: twin hull (sqrt5 -> -sqrt5 on the exact corners), corners, faces by sides, and its kind: REGULAR
# ICOSAHEDRON / REGULAR DODECAHEDRON (exact: one edge length, regular faces), rhombicosidodecahedron pattern (60 corners; 20, 30, 12 faces;
# with the rectangles' side ratio), other. Control: the start is convex with 32 corners and 60 triangles.
# usage: python -u pentakis_family.py <five-fold-octet dir> <KMAX> <out.json>
import sys, os, json, time, itertools
ARGS = list(sys.argv); OUTJ = os.path.abspath(ARGS[3]); KMAX = int(ARGS[2])
here = os.path.expanduser('~/k-research/studies/2026-11-09-og-margin/scripts')
sys.argv = [ARGS[0], ARGS[1], '0', '/dev/null']; exec(open(os.path.join(here, 'exact_family.py')).read().split("t0 = time.time()")[0])
KMAX = int(ARGS[2])                                                         # 11-11: the library head resets KMAX
import numpy as np
from collections import Counter
from scipy.spatial import ConvexHull
from gmpy2 import mpq
PHI = R5(mpq(1, 2), mpq(1, 2)); IPHI = R5(mpq(-1, 2), mpq(1, 2)); ONE = R5(1); ZERO = R5(0)
def cyc(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def signs(v):
    out = set()
    for sg in itertools.product((1, -1), repeat=3):
        out.add(tuple(x if s == 1 else -x for x, s in zip(v, sg)))
    return list(out)
def uniq(P): return list(dict.fromkeys(P))
DOD = uniq([p for base in [(ONE, ONE, ONE)] for p in signs(base)] + [p for base in cyc((ZERO, PHI, IPHI)) for p in signs(base)])   # 11-11: orientation of the group G (dual of the icosahedron (0, +-1, +-phi))
assert len(DOD) == 20, len(DOD)
# five-fold directions = face normals of DOD: take whichever of (0, 1, phi) / (0, phi, 1) cyclic families are face normals
Df = np.array([fl(v) for v in DOD]); hD = ConvexHull(Df); FN = hD.equations[:, :3]
def is_normal(d):
    d = np.array([x.f() for x in d]); d /= np.linalg.norm(d); return np.abs(FN @ d - 1).min() < 1e-9
fam = None
for base in ((ZERO, ONE, PHI), (ZERO, PHI, ONE)):
    if is_normal(base): fam = base
assert fam is not None
AX = uniq([p for b in cyc(fam) for p in signs(b)]); assert len(AX) == 12
# face distance of DOD along an axis direction a: d_f = min over DOD corners of (v.a)/|a| ... exact: plane n.x = c with n = a; c = max v.a over the face = (v.a) for v on the face
a0 = AX[0]; c0 = max((dot(v, a0) for v in DOD), key=lambda x: x.f())       # n.x = c0 is the face plane for normal a0 (unnormalised)
def pentakis(hrel):
    """apex t*a with a.(t a) = c0 (1 + h): t = c0 (1 + h) / (a.a)."""
    t = c0 * (ONE + hrel) / dot(a0, a0)
    return DOD + [tuple(t * x for x in a) for a in AX]
# Catalan pentakis: polar dual of the regular truncated icosahedron (edge 2): corners even perms of (0, 1, 3phi), (1, 2+phi, 2phi), (phi, 2, 2phi+1)
TWO = R5(2); THREE = R5(3)
TIb = [(ZERO, ONE, THREE * PHI), (ONE, TWO + PHI, TWO * PHI), (PHI, TWO, TWO * PHI + ONE)]
TI = uniq([p for b in TIb for c in cyc(b) for p in signs(c)]); assert len(TI) == 60, len(TI)
def polar_dual(P):
    Pf = np.array([fl(v) for v in P]); idx = {v: i for i, v in enumerate(P)}; F, ne, _ = exact_faces(P, idx, Pf)
    return [tuple(x / d_ for x in n_) for n_, d_, _ in F.values()]           # face n.x = d  ->  dual point n/d
CAT = polar_dual(TI)
def twinf(x):
    re = float(x.a) + float(x.b) * S5
    return float(x.a) - float(x.b) * S5 if abs(re) < 1e-6 or x.b == 0 else float(x.a * x.a - 5 * x.b * x.b) / re
def twin_kind(Wk):
    idx = {v: i for i, v in enumerate(Wk)}; Wfx = np.array([fl(v) for v in Wk]); F, ne, _ = exact_faces(Wk, idx, Wfx)
    cor = sorted(set(i for mem in F for i in mem)); T = np.array([[twinf(x) for x in Wk[i]] for i in cor]); T /= np.linalg.norm(T, axis=1).max()
    h = ConvexHull(T); En = h.equations; n = len(En); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if np.abs(En[f] - En[g]).max() < 1e-9: par[find(f)] = find(g)
    grp = {}
    for f in range(n): grp.setdefault(find(f), set()).update(h.simplices[f].tolist())
    sides = Counter(len(p) for p in grp.values()); V = len(h.vertices)
    E = set()
    for p in grp.values():
        ii = np.array(sorted(p)); Q = T[ii]; c = Q.mean(0); B = np.linalg.svd(Q - c)[2][:2]; q = (Q - c) @ B.T; cy = list(ii[np.argsort(np.arctan2(q[:, 1], q[:, 0]))])
        for a, b in zip(cy, cy[1:] + cy[:1]): E.add((min(a, b), max(a, b)))
    L = np.array([np.linalg.norm(T[a] - T[b]) for a, b in E]); Ls = np.unique(np.round(L / L.max(), 9))
    if V == 12 and sides == {3: 20}: kind = 'REGULAR ICOSAHEDRON' if len(Ls) == 1 else 'icosahedron pattern'
    elif V == 20 and sides == {5: 12}: kind = 'REGULAR DODECAHEDRON' if len(Ls) == 1 else 'dodecahedron pattern'
    elif V == 60 and sides == {3: 20, 4: 30, 5: 12}: kind = 'rhombicosidodecahedron ' + ('(uniform)' if len(Ls) == 1 else f'pattern, rectangles {Ls.max() / Ls.min():.6f}:1')
    elif V == 30 and sides == {3: 20, 5: 12}: kind = 'icosidodecahedron ' + ('(uniform)' if len(Ls) == 1 else 'pattern')
    else: kind = f'{V} corners, faces {dict(sorted(sides.items()))}'
    return kind, F, cor

import gmpy2
def denest(r):
    a, b = r.a, r.b; disc = a * a - 5 * b * b
    if disc < 0: return None
    if not (gmpy2.is_square(disc.numerator) and gmpy2.is_square(disc.denominator)): return None
    sd = mpq(gmpy2.isqrt(disc.numerator), gmpy2.isqrt(disc.denominator))
    for p2 in ((a + sd) / 2, (a - sd) / 2):
        if p2 <= 0 or not (gmpy2.is_square(p2.numerator) and gmpy2.is_square(p2.denominator)): continue
        p = mpq(gmpy2.isqrt(p2.numerator), gmpy2.isqrt(p2.denominator)); x = R5(p, b / (2 * p))
        if x.a * x.a + 5 * x.b * x.b == a and 2 * x.a * x.b == b: return x if x.f() > 0 else R5(-x.a, -x.b)
    return None
def rs(x): return f"{x.a}" if x.b == 0 else f"{x.a} + {x.b}√5"
def conj(x): return R5(x.a, -x.b)
def corners_of(W):
    idx = {v: i for i, v in enumerate(W)}; Wfx = np.array([fl(v) for v in W]); F, ne, _ = exact_faces(W, idx, Wfx)
    cor = sorted(set(i for mem in F for i in mem)); return [W[i] for i in cor], F
def angelus(C):
    """Vacuus of the twin hull of exact corners C: fins (hull edges), exact apex cos^2 classes, fin planes, discs."""
    T = [tuple(conj(x) for x in v) for v in C]; Tf = np.array([[twinf(x) for x in v] for v in C]); nrm = np.linalg.norm(Tf, axis=1).max(); Tf /= nrm
    h = ConvexHull(Tf); keep = list(h.vertices); T = [T[i] for i in keep]; Tf = Tf[keep]; h = ConvexHull(Tf)
    En = h.equations; n = len(En); par = list(range(n))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for f in range(n):
        for g in h.neighbors[f]:
            if np.abs(En[f] - En[g]).max() < 1e-9: par[find(f)] = find(g)
    grp = {}
    for f in range(n): grp.setdefault(find(f), set()).update(h.simplices[f].tolist())
    E = set()
    for p in grp.values():
        ii = np.array(sorted(p)); Q = Tf[ii]; c = Q.mean(0); B = np.linalg.svd(Q - c)[2][:2]; q = (Q - c) @ B.T; cy = list(ii[np.argsort(np.arctan2(q[:, 1], q[:, 0]))])
        for a, b in zip(cy, cy[1:] + cy[:1]): E.add((min(a, b), max(a, b)))
    cls = Counter(); planes = {}
    for a, b in E:
        u, v = T[a], T[b]; d = dot(u, v); c2 = (d * d) / (dot(u, u) * dot(v, v)); ang = float(np.degrees(np.arccos(np.sign(d.f()) * np.sqrt(c2.f()))))
        cls[(round(ang, 4), rs(c2))] += 1
        nn = np.cross(Tf[a], Tf[b]); nn /= np.linalg.norm(nn); nn *= np.sign(nn[np.argmax(np.abs(nn) > 1e-9)]); planes.setdefault(tuple(np.round(nn, 7)), []).append((a, b))
    discs = 0
    for key, es in planes.items():
        tot = sum(np.degrees(np.arccos(np.clip(Tf[a] @ Tf[b] / (np.linalg.norm(Tf[a]) * np.linalg.norm(Tf[b])), -1, 1))) for a, b in es)
        discs += abs(tot - 360) < 1e-6
    return dict(corners=len(T), faces=dict(sorted(Counter(len(p) for p in grp.values()).items())), fins=len(E), apex={f"{k[0]} deg (cos^2 = {k[1]})": v for k, v in sorted(cls.items())}, fin_planes=len(planes), discs=discs)

def level(W0, k):
    W = W0
    for _ in range(k):
        C, F = corners_of(W); feet = {}
        for n_, d_, _ in F.values():
            s_ = d_ / dot(n_, n_); feet[tuple(s_ * x for x in n_)] = 1
        W = list(feet)
    C, F = corners_of(W); return C
def twin_hull_corners(C):
    T = [tuple(conj(x) for x in v) for v in C]; Tf = np.array([[twinf(x) for x in v] for v in C]); Tf /= np.linalg.norm(Tf, axis=1).max()
    h = ConvexHull(Tf); return [T[i] for i in h.vertices]


OGW = [tuple(cv(x) for x in v) for v in OG]; S9 = R5(mpq(9, 2), mpq(3, 2)); P = [tuple(S9 * x for x in v) for v in CAT]
r2 = sorted(set(dot(v, v) for v in P), key=lambda x: x.f()); six = [v for v in P if dot(v, v) == r2[0] or dot(v, v) == r2[-1]]
# which radius class are the 20 six-fold corners? the class with 20 members
cls = {r: [v for v in P if dot(v, v) == r] for r in r2}; SIX = [v for r, vs in cls.items() if len(vs) == 20 for v in vs]; FIVE = [v for r, vs in cls.items() if len(vs) == 12 for v in vs]
assert len(SIX) == 20 and len(FIVE) == 12
idx = {v: i for i, v in enumerate(P)}; Pf = np.array([fl(v) for v in P]); F, ne, _ = exact_faces(P, idx, Pf)
EDG = set()
for mem in F:
    mm = sorted(mem); Q = Pf[mm]; c = Q.mean(0); B = np.linalg.svd(Q - c)[2][:2]; q = (Q - c) @ B.T; cy = [mm[i] for i in np.argsort(np.arctan2(q[:, 1], q[:, 0]))]
    for a, b in zip(cy, cy[1:] + cy[:1]): EDG.add((min(a, b), max(a, b)))
nb = {i: set() for i in range(len(P))}
for a, b in EDG: nb[a].add(b); nb[b].add(a)
# OG hexagon plane: plane n.x = d with n along a three-fold axis; lam* = d / |six-fold corner| along that axis
v6 = SIX[0]; OGset = set(OGW)
ogF = {}
idxO = {v: i for i, v in enumerate(OGW)}; OF, _, _ = exact_faces(OGW, idxO, np.array([fl(v) for v in OGW]))
hexd = None
for mem, (n_, d_, _) in OF.items():
    if len(mem) == 6:
        # is n parallel to v6?
        if all((n_[i] * v6[j] - n_[j] * v6[i]).f() == 0 or abs((n_[i] * v6[j] - n_[j] * v6[i]).f()) < 1e-14 for i in range(3) for j in range(3)) and dot(n_, v6).f() > 0:
            hexd = d_ / dot(n_, v6)                               # plane n.x = d; along v6: x = t v6 with t = d / (n.v6): lam = t
lam_star = hexd; print('OG hexagon planes cut the six-fold corner at lam* =', rs(lam_star), '=', lam_star.f(), flush=True)
def cut(lam):
    pts = [v for v in P if v not in set(SIX)]
    for v in SIX:
        i = idx[v]; n = v; d = lam * dot(v, v)                     # plane n.x = d (n = v): lam * |v|^2
        for j in nb[i]:
            w = P[j]; t = (d - dot(n, v)) / dot(n, sub(w, v))
            if not (t.f() > 0 and t.f() < 1): return None
            pts.append(tuple(a + t * (b - a) for a, b in zip(v, w)))
    return list(dict.fromkeys(pts))
def describe(W):
    idx2 = {v: i for i, v in enumerate(W)}; Wf = np.array([fl(v) for v in W]); F2, _, _ = exact_faces(W, idx2, Wf)
    E = set()
    for mem in F2:
        mm = sorted(mem); Q = Wf[mm]; c = Q.mean(0); B = np.linalg.svd(Q - c)[2][:2]; q = (Q - c) @ B.T; cy = [mm[i] for i in np.argsort(np.arctan2(q[:, 1], q[:, 0]))]
        for a, b in zip(cy, cy[1:] + cy[:1]): E.add((min(a, b), max(a, b)))
    L = set(dot(sub(W[a], W[b]), sub(W[a], W[b])) for a, b in E)
    hexes = [m for m in F2 if len(m) == 6]; hexreg = None
    if hexes:
        mm = sorted(hexes[0]); Q = Wf[mm]; c = Q.mean(0); B = np.linalg.svd(Q - c)[2][:2]; q = (Q - c) @ B.T; cy = [mm[i] for i in np.argsort(np.arctan2(q[:, 1], q[:, 0]))]
        sides = set(dot(sub(W[a], W[b]), sub(W[a], W[b])) for a, b in zip(cy, cy[1:] + cy[:1])); hexreg = len(sides) == 1
    return len(set(i for m in F2 for i in m)), dict(Counter(len(m) for m in F2)), len(L), hexreg, F2
def R2max(Pp): return max((dot(v, v) for v in Pp), key=lambda x: x.f())
def hop(W):
    idx2 = {v: i for i, v in enumerate(W)}; Wf = np.array([fl(v) for v in W]); F2, _, _ = exact_faces(W, idx2, Wf)
    feet = {}
    for n_, d_, _ in F2.values():
        s_ = d_ / dot(n_, n_); feet[tuple(s_ * x for x in n_)] = 1
    return list(feet)
def corners(W):
    idx2 = {v: i for i, v in enumerate(W)}; Wf = np.array([fl(v) for v in W]); F2, _, _ = exact_faces(W, idx2, Wf); return [W[i] for i in sorted(set(i for m in F2 for i in m))]
ok = True
lams = [R5(mpq(n, d)) for n, d in ((19, 20), (9, 10), (17, 20), (4, 5), (3, 4))] + [lam_star]
lams = sorted(set(lams), key=lambda x: -x.f())
for lam in lams:
    W0 = cut(lam)
    if W0 is None: print(f'lam {rs(lam)} = {lam.f():.6f}: cut too deep (planes pass the neighbours)', flush=True); continue
    V, faces_, nL, hexreg, _ = describe(W0)
    isOG = set(W0) == OGset
    if lam == lam_star: ok &= isOG
    L = [W0]; counts = []
    for k in range(6):
        C = corners(L[-1]); counts.append(len(C)); L.append(hop(L[-1]))
    C0, C4 = corners(L[0]), corners(L[4]); c2 = R2max(C4) / R2max(C0); c = denest(c2)
    cyc = c is not None and set(tuple(c * x for x in v) for v in C0) == set(C4)
    print(f'lam {rs(lam)} = {lam.f():.6f}{"  (= OG)" if isOG else ""}: {V} corners, faces {dict(sorted(faces_.items()))}, EDGE LENGTHS {nL}, hexagons regular {hexreg} | '
          f'corners k=0..5 {counts} | 4-cycle: {cyc}', flush=True)
print('FINAL ok' if ok else 'FINAL FAIL: the OG depth does not reproduce the OG')
