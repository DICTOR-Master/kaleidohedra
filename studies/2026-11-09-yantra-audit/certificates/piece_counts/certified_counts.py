"""Certified piece counts (Proposition 3 / Proposition 11): the DICTO Yantra (43) and Kulaichev's yantra (45).
usage: python -u certified_counts.py D|K      (run in the folder holding stage2-<case>.json, stage5-<case>.json, model.py)
Input: the interval enclosures (about 500 correct digits) of every base depth, half-width and apex of the EXACT yantra
certified in stage 5. Every combinatorial decision of the arrangement of the 27 sides reduces to one predicate,
  conc(l1, l2, l3): do three of the 27 lines pass through one point?  (the 3x3 determinant of their line coordinates)
plus the signs of coordinate differences and orientations, all evaluated in interval arithmetic. A sign is CERTIFIED when its
interval excludes 0. When an interval contains 0, the predicate is decided EXACTLY instead: the same determinant is computed
symbolically from the model (Singular via sage, generic in y = u^2, p = uv, Q, S, t = b1) and must be identically zero or a
multiple of the closing polynomial Fc (both vanish exactly at the yantra by stages 2 and 5); otherwise the script stops.
Then: vertices (points where segments meet), edges, the faces of the planar arrangement (rotation system), each face's set of
containing triangles (by crossing edges from the outer face; every face must be reached consistently), and the counts:
odd faces by containment depth 1, 3, 5, 7, 9; how many are triangles; marmas (three sides, not a corner) and sandhis (two).
Reports the minimum certified margin (smallest |value| over all certified-nonzero predicates) against the enclosure width."""
import sys, json, time, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '.')
T0 = time.time(); say = lambda *a: print(f'[{time.time() - T0:7.1f} s]', *a, flush=True)
case = sys.argv[1]
import mpmath as mp
from mpmath import iv
mp.mp.dps = 560; iv.dps = 560
lo = lambda z: mp.make_mpf(z._mpi_[0]); hi = lambda z: mp.make_mpf(z._mpi_[1])
st5 = json.load(open(f'stage5-{case}.json'))
J = lambda pr: iv.mpf([pr[0], pr[1]])
b = {int(k): J(v) for k, v in st5['b'].items()}; w = {int(k): J(v) for k, v in st5['w'].items()}; a = {int(k): J(v) for k, v in st5['a'].items()}
width = max(hi(z) - lo(z) for d in (b, w, a) for z in d.values())
say(f'case {case}: enclosures of all 27 coordinates, widest {mp.nstr(width, 3)}')
# symbolic model (scaled, as in stage 2) for the exact decisions
import model
from sage.all__sagemath_singular import QQ, PolynomialRing
Rg = PolynomialRing(QQ, 'y,p,Q,S,t'); y, p, Qs, Ss, ts = Rg.gens(); Fd = Rg.fraction_field()
one = Fd(1)
if case == 'K': P_ = Fd(y) / (1 + y); R_ = one / (1 + y); W3 = one / (1 + y); W7 = one / (1 + y)
else: P_ = Fd(p * p) / (y + p * p); R_ = one / (1 + y); W3 = Fd(p) / (y + p * p); W7 = one / (1 + y)
trs = model.solve(P_, Fd(Qs), R_, Fd(Ss), W3, W7, sqrt=None, b1=Fd(ts))
Fc = Rg(json.load(open(f'stage2-{case}.json'))['Fc'])
# lines: ('B', i) base, ('R', i) right leg, ('L', i) left leg; as point pairs
def pts(tri, kind, i, zero):
    W_, B_, A_ = tri['w'][i], tri['b'][i], tri['a'][i]
    if kind == 'B': return ((-W_, B_), (W_, B_))
    if kind == 'R': return ((W_, B_), (zero, A_))
    return ((-W_, B_), (zero, A_))
LINES = [(k, i) for i in range(1, 10) for k in ('B', 'R', 'L')]
def lc(pp):
    (x1, y1), (x2, y2) = pp
    return (y1 - y2, x2 - x1, x1 * y2 - x2 * y1)
trI = {'b': b, 'w': w, 'a': a}
LI = {l: lc(pts(trI, l[0], l[1], iv.mpf(0))) for l in LINES}
LS = {l: lc(pts(trs, l[0], l[1], Fd(0))) for l in LINES}
def det3(A, B, C):
    return (A[0] * (B[1] * C[2] - B[2] * C[1]) - A[1] * (B[0] * C[2] - B[2] * C[0]) + A[2] * (B[0] * C[1] - B[1] * C[0]))
margins = []           # |value| lower bounds of certified-nonzero predicates
exact_zero = {}; nexact = [0]; kinds = {}
def sign_or_exact(val_iv, exact_fn, what):
    if lo(val_iv) > 0: margins.append((lo(val_iv), what)); return 1
    if hi(val_iv) < 0: margins.append((-hi(val_iv), what)); return -1
    v = exact_fn()
    if v == 0 or Fc.divides(Fd(v).numerator()):
        nexact[0] += 1; kinds[what[:4]] = kinds.get(what[:4], 0) + 1; return 0
    raise SystemExit(f'FINAL FAIL: undecided predicate {what} (interval contains 0, not an exact identity)')
def conc(l1, l2, l3):
    key = tuple(sorted((l1, l2, l3)))
    if key not in exact_zero:
        exact_zero[key] = sign_or_exact(det3(LI[key[0]], LI[key[1]], LI[key[2]]), lambda: det3(LS[key[0]], LS[key[1]], LS[key[2]]), f'conc{key}') == 0
    return exact_zero[key]
def par(l1, l2):     # parallel: A1 B2 - A2 B1 = 0
    A, B = LI[l1], LI[l2]
    return sign_or_exact(A[0] * B[1] - A[1] * B[0], lambda: LS[l1][0] * LS[l2][1] - LS[l1][1] * LS[l2][0], f'par{(l1, l2)}') == 0
def meet(l1, l2):    # intersection point, intervals
    A, B = LI[l1], LI[l2]
    d = A[0] * B[1] - A[1] * B[0]
    return ((A[1] * B[2] - A[2] * B[1]) / d, (A[2] * B[0] - A[0] * B[2]) / d)
# 1. points: every intersection of two non-parallel lines, keyed by the set of lines through it
pairs = [(l1, l2) for l1, l2 in itertools.combinations(LINES, 2) if not par(l1, l2)]
keys = {}
for l1, l2 in pairs:
    through = frozenset([l1, l2] + [l for l in LINES if l not in (l1, l2) and conc(l1, l2, l)])
    keys.setdefault(through, meet(l1, l2))
say(f'{len(pairs)} intersecting line pairs, {len(keys)} distinct points; {nexact[0]} predicates decided exactly (concurrencies), the rest certified by intervals')
# 2. segments and their points
def coord_on(l, P): return P[0] if l[0] == 'B' else P[1]          # position along a line: x on a base, depth on a leg
def endpoint_keys(l):
    k, i = l
    ends = {'B': [('L', i), ('R', i)], 'R': [('B', i), ('L', i)], 'L': [('B', i), ('R', i)]}[k]
    return [next(K for K in keys if l in K and m in K) for m in ends]
def cmp_on(l, K1, K2):
    if K1 == K2: return 0
    d = coord_on(l, keys[K1]) - coord_on(l, keys[K2])
    s = 1 if lo(d) > 0 else (-1 if hi(d) < 0 else None)
    if s is None: raise SystemExit(f'FINAL FAIL: two distinct points on {l} not separated')
    margins.append((abs(mp.mpf(lo(d) if s > 0 else hi(d))), f'order on {l}')); return s
SEG = {}
for l in LINES:
    E1, E2 = endpoint_keys(l)
    if cmp_on(l, E1, E2) > 0: E1, E2 = E2, E1
    SEG[l] = (E1, E2)
def on_seg(l, K):
    if l not in K: return False
    E1, E2 = SEG[l]
    return cmp_on(l, K, E1) >= 0 and cmp_on(l, K, E2) <= 0
segs_at = {K: [l for l in LINES if on_seg(l, K)] for K in keys}
corner_keys = set(K for l in LINES for K in SEG[l])
verts = [K for K in keys if len(segs_at[K]) >= 2 or K in corner_keys]
verts = [K for K in verts if segs_at[K]]
vid = {K: n for n, K in enumerate(verts)}
# 3. edges along each segment
edges = set(); edge_line = {}
for l in LINES:
    on = [K for K in verts if on_seg(l, K)]
    import functools
    on.sort(key=functools.cmp_to_key(lambda A, B: cmp_on(l, A, B)))
    for A, B in zip(on, on[1:]):
        e = (vid[A], vid[B])
        if e in edges or (e[1], e[0]) in edges: raise SystemExit('FINAL FAIL: two sides overlap along an edge')
        edges.add(e); edge_line[e] = l; edge_line[(e[1], e[0])] = l
say(f'{len(verts)} vertices, {len(edges)} edges')
XY = {vid[K]: keys[K] for K in verts}
# 4. rotation system: neighbours sorted by angle, exactly
nb = {}
for (p_, q_) in list(edges):
    nb.setdefault(p_, []).append(q_); nb.setdefault(q_, []).append(p_)
def direction(p_, q_):
    l = edge_line[(p_, q_)]
    dx = XY[q_][0] - XY[p_][0]; dy = XY[q_][1] - XY[p_][1]
    if l[0] == 'B': dy = iv.mpf(0)                     # along a base: exactly horizontal
    return dx, dy
def sgn(z, what):
    if z == 0: return 0
    if lo(z) > 0: margins.append((lo(z), what)); return 1
    if hi(z) < 0: margins.append((-hi(z), what)); return -1
    raise SystemExit(f'FINAL FAIL: undecided sign ({what})')
def half(d):
    sy = sgn(d[1], 'direction') if not (d[1].a == 0 and d[1].b == 0) else 0
    if sy > 0: return 0
    if sy == 0: return 0 if sgn(d[0], 'direction') > 0 else 1
    return 1
def ang_cmp(d1, d2):
    h1, h2 = half(d1), half(d2)
    if h1 != h2: return -1 if h1 < h2 else 1
    c = d1[0] * d2[1] - d1[1] * d2[0]
    return -sgn(c, 'angle')
import functools
for p_ in nb:
    nb[p_].sort(key=functools.cmp_to_key(lambda q1, q2: ang_cmp(direction(p_, q1), direction(p_, q2))))
# 5. faces (same convention as figure.py)
used, faces = set(), []
half_edges = [(p_, q_) for p_ in nb for q_ in nb[p_]]
face_of = {}
for e in half_edges:
    if e in used: continue
    f = []; cur = e
    while cur not in used:
        used.add(cur); f.append(cur); face_of[cur] = len(faces)
        p_, q_ = cur; k = nb[q_].index(p_); cur = (q_, nb[q_][(k - 1) % len(nb[q_])])
    faces.append(f)
def area(f):
    s = iv.mpf(0)
    for (p_, q_) in f: s += XY[q_][0] * XY[p_][1] - XY[p_][0] * XY[q_][1]
    return s / 2
signs = [sgn(area(f), 'face area') for f in faces]
outer = [i for i, s in enumerate(signs) if s > 0]
if len(outer) != 1: raise SystemExit(f'FINAL FAIL: {len(outer)} faces with positive orientation')
V, E, Fn = len(verts), len(edges), len(faces)
say(f'{Fn} faces (one outer); Euler V - E + F = {V - E + Fn} (2 for a connected plane graph)')
# 6. containing triangles by crossing edges from the outer face
mem = {outer[0]: frozenset()}
queue = [outer[0]]; consistent = True
while queue:
    fi = queue.pop()
    for (p_, q_) in faces[fi]:
        gj = face_of[(q_, p_)]
        tri_i = edge_line[(p_, q_)][1]
        m = mem[fi] ^ frozenset([tri_i])
        if gj in mem: consistent = consistent and mem[gj] == m
        else: mem[gj] = m; queue.append(gj)
if not consistent or len(mem) != Fn: raise SystemExit('FINAL FAIL: containment labels inconsistent')
rings = {d: 0 for d in (1, 3, 5, 7, 9)}; ntri = 0; odd = 0; evenf = 0
for fi, f in enumerate(faces):
    if fi == outer[0]: continue
    dpt = len(mem[fi])
    corners = sum(1 for k in range(len(f)) if edge_line[f[k - 1]] != edge_line[f[k]])
    if dpt % 2:
        odd += 1; rings[dpt] += 1; ntri += corners == 3
    else: evenf += 1
# 7. marmas and sandhis (counts.py's definition)
marma = sum(1 for K in verts if len(segs_at[K]) == 3 and K not in corner_keys)
sandhi = sum(1 for K in verts if len(segs_at[K]) == 2 and K not in corner_keys)
say(f'odd faces {odd} (triangles {ntri}), by depth 1,3,5,7,9: {[rings[d] for d in (1, 3, 5, 7, 9)]}; even bounded faces {evenf}; marmas {marma}; sandhis {sandhi}')
mmin = min(margins, key=lambda x: x[0])
say(f'{len(margins)} certified-nonzero signs; minimum certified margin {mp.nstr(mmin[0], 4)} ({mmin[1]}), against enclosure width {mp.nstr(width, 3)}')
say(f'{nexact[0]} predicates decided exactly (zero by the model identities): {kinds.get("conc", 0)} concurrencies of three lines, {kinds.get("par(", 0)} parallel pairs (all 36 base pairs; for u = v also the 2 pairs of opposite rhombus sides); {len(exact_zero)} concurrency triples examined')
expect = {'D': (43, 43, [14, 10, 10, 8, 1], 18, 24), 'K': (45, None, [14, 10, 12, 8, 1], 18, 28)}[case]
got = (odd, ntri if case == 'D' else None, [rings[d] for d in (1, 3, 5, 7, 9)], marma, sandhi)
json.dump({'case': case, 'odd': odd, 'triangles_among_odd': ntri, 'rings': rings, 'marmas': marma, 'sandhis': sandhi,
           'min_margin': mp.nstr(mmin[0], 6), 'min_margin_at': mmin[1], 'enclosure_width': mp.nstr(width, 3),
           'exact_decisions': nexact[0], 'V': V, 'E': E, 'F': Fn}, open(f'counts-{case}.json', 'w'))
print('FINAL ok' if got == expect and V - E + Fn == 2 else f'FINAL FAIL: got {got}, expected {expect}')
