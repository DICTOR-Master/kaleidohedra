# pentakis_family.py, DICTO 11 Nov 2026 ("i wonder if other pentakis produce dodecahedrons, icosahedrons and rhombicosidodecahedrons").
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
STARTS = [('Catalan pentakis', CAT)] + [(f'pentakis h = {h}', pentakis(R5(mpq(*h)) if isinstance(h, tuple) else h)) for h in [(1, 20), (1, 10), (1, 5), (3, 10)]]
STARTS.append(('pentakis h = 1/phi^3', pentakis(R5(-2, 1))))                    # 1/phi^3 = sqrt5 - 2
rows = []; ok = True; t0 = time.time()
for name, W0 in STARTS:
    Wf0 = np.array([fl(v) for v in W0]); h0 = ConvexHull(Wf0)
    nv = len(h0.vertices); ok_s = nv == 32
    print(f'== {name}: start corners {nv} (convex pentakis: {ok_s})', flush=True)
    if not ok_s: rows.append(dict(start=name, convex_pentakis=False)); continue
    W = W0; res = []
    for k in range(KMAX + 1):
        kind, F, cor = twin_kind(W)
        Wr = np.array([fl(W[i]) for i in cor]); hr = ConvexHull(Wr); rr = np.linalg.norm(Wr, axis=1)
        rsig = tuple(sorted(np.unique(np.round(rr / rr.max(), 9))))                     # real shape signature: corner radii (relative)
        real = f'real D_{k}: {len(cor)} corners, {len(F)} faces, radii {len(rsig)}'
        if k >= 4 and res[k - 4].get('rsig') == rsig and res[k - 4].get('nF') == len(F): real += ' = D_{k-4} up to scale'
        res.append(dict(k=k, twin_hull=kind, real=real, rsig=rsig, nF=len(F))); print(f'   k {k}: twin hull = {kind} | {real} ({time.time() - t0:.0f}s)', flush=True)
        feet = {}
        for n_, d_, _ in F.values():
            s_ = d_ / dot(n_, n_); feet[tuple(s_ * x for x in n_)] = 1
        W = list(feet)
    rows.append(dict(start=name, convex_pentakis=True, levels=res)); print(f'PROGRESS {len(rows) / len(STARTS):.3f}', flush=True)
[l.pop('rsig', None) for r in rows for l in r.get('levels', [])]
json.dump(rows, open(OUTJ, 'w'), indent=1)
print('FINAL ok' if ok else 'FINAL FAIL')
