# DICTO 2026-10-21, Reuleaux Platonics (DICTO's idea: a ball on every corner, radius = the solid's diameter): checks for paper #45.
# Part A is exact (Q(sqrt5), numbers a + b*sqrt5 as Fraction pairs): diameters, diametric pairs, inradius/circumradius, the corner
# heights that put the extreme point on the face axis, and the closed forms of the face-axis widths. Part B is numerical (float64,
# labelled): the face-axis widths against widths.log, the volumes by radial quadrature (the Reuleaux tetrahedron against the
# Harbourne formula quoted by Hynd 2023), and which faces meet along an arc, with the fewest colours.
#   python3 reuleaux_checks.py > reuleaux-checks.log
import itertools, math, os, re
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
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
qstr = lambda x: f'{x[0]}' if x[1] == 0 else f'{x[0]} + {x[1]}*sqrt5'
PHI, IPHI = (Fr(1, 2), Fr(1, 2)), (Fr(-1, 2), Fr(1, 2))
V = lambda *c: [qr(t) if not isinstance(t, tuple) else t for t in c]
sub = lambda u, v: [qs(a, b) for a, b in zip(u, v)]
dot = lambda u, v: qa(qa(qm(u[0], v[0]), qm(u[1], v[1])), qm(u[2], v[2]))
def cross(u, v): return [qs(qm(u[1], v[2]), qm(u[2], v[1])), qs(qm(u[2], v[0]), qm(u[0], v[2])), qs(qm(u[0], v[1]), qm(u[1], v[0]))]
bad = 0
def chk(c, m):
    global bad; print(('PASS ' if c else 'FAIL ') + m); bad += (not c)
cyc = lambda v: [v, [v[1], v[2], v[0]], [v[2], v[0], v[1]]]
S = {'Tetrahedron': [V(*p) for p in itertools.product((1, -1), repeat=3) if p[0] * p[1] * p[2] > 0],
     'Cube': [V(*p) for p in itertools.product((1, -1), repeat=3)],
     'Octahedron': [V(*[s if k == i else 0 for k in range(3)]) for i in range(3) for s in (1, -1)],
     'Dodecahedron': [V(*p) for p in itertools.product((1, -1), repeat=3)] + [w for a, b in itertools.product((1, -1), repeat=2) for w in cyc(V(0, qm(qr(a), IPHI), qm(qr(b), PHI)))],
     'Icosahedron': [w for a, b in itertools.product((1, -1), repeat=2) for w in cyc(V(0, a, qm(qr(b), PHI)))]}
LOOK = {'Tetrahedron': 'tetrahedron', 'Cube': 'octahedron', 'Octahedron': 'cube', 'Dodecahedron': 'icosahedron', 'Icosahedron': 'dodecahedron'}
def faces(P):
    F = {}
    for i, j, k in itertools.combinations(range(len(P)), 3):
        n = cross(sub(P[j], P[i]), sub(P[k], P[i]))
        if all(t == Z for t in n): continue
        s = [sgn(dot(n, sub(p, P[i]))) for p in P]
        if all(x <= 0 for x in s) or all(x >= 0 for x in s):
            if any(x > 0 for x in s): n = [(-a[0], -a[1]) for a in n]
            F.setdefault(frozenset(m for m in range(len(P)) if sgn(dot(n, sub(P[m], P[i]))) == 0), n)
    return F
def edges(P):
    F = list(faces(P)); return {tuple(sorted(a & b)) for a, b in itertools.combinations(F, 2) if len(a & b) == 2}
print('== A. Exact (Q(sqrt5))')
RR = {}
for name, P in S.items():
    m = len(P); d2 = {(i, j): dot(sub(P[i], P[j]), sub(P[i], P[j])) for i, j in itertools.combinations(range(m), 2)}
    D2 = max(d2.values(), key=qf); assert all(sgn(qs(D2, x)) >= 0 for x in d2.values())
    pairs = [k for k, x in d2.items() if x == D2]; R2 = dot(P[0], P[0])
    chk(all(dot(p, p) == R2 for p in P), f'{name}: {m} corners on one sphere, R^2 = {qstr(R2)}')
    if name == 'Tetrahedron':
        chk(len(pairs) == 6 == 2 * m - 2, f'{name}: diameter = edge, {len(pairs)} diametric pairs = 2m - 2 (extremal: the classical Reuleaux tetrahedron)')
    else:
        chk(D2 == qm(qr(4), R2) and len(pairs) == m // 2, f'{name}: diameter = 2R (opposite corners), {len(pairs)} diametric pairs, fewer than 2m - 2 = {2 * m - 2}')
        on = [sum(1 for k in pairs if i in k) for i in range(m)]
        chk(set(on) == {1}, f'{name}: each corner lies on exactly 1 of the other balls\' spheres, so it is not a vertex (0-singular point) of the body: a ball polyhedron, not a Reuleaux polyhedron in Sallee\'s sense')
        F = faces(P); f0, n = next(iter(F.items())); r_n = dot(n, P[next(iter(f0))])   # r * |n|
        r2 = qd(qm(r_n, r_n), dot(n, n)); RR[name] = qd(r2, R2)
        chk(all(sgn(qa(dot(n, p), r_n)) >= 0 for p in P) and sum(1 for p in P if qa(dot(n, p), r_n) == Z) == len(f0),
            f'{name}: along a face axis every corner has height >= -r, with equality exactly at the {len(f0)} corners of the opposite face')
        chk(True, f'{name}: (r/R)^2 = {qstr(RR[name])} ({qf(RR[name]):.12f})')
# the Reuleaux tetrahedron (edge = diameter 1) along the axis through the midpoints of two opposite edges: the edges are 1/sqrt2
# apart, each corner 1/2 from the axis; the far edge's corners hold the axis point, so w = 2 sqrt(1 - 1/4) - 2/(2 sqrt2)
T = S['Tetrahedron']; mid = lambda a, b: [(x[0] / 2 + y[0] / 2, x[1] / 2 + y[1] / 2) for x, y in zip(a, b)]
m1, m2 = mid(T[0], T[1]), mid(T[2], T[3]); ax = sub(m1, m2); E2 = dot(sub(T[0], T[1]), sub(T[0], T[1]))
h = [qd(qm(dot(p, ax), dot(p, ax)), qm(dot(ax, ax), E2)) for p in T]            # (height / edge)^2 of each corner
rho = [qd(qs(dot(p, p), qd(qm(dot(p, ax), dot(p, ax)), dot(ax, ax))), E2) for p in T]   # (distance from the axis / edge)^2
chk(qd(dot(ax, ax), E2) == qr(Fr(1, 2)) and all(x == qr(Fr(1, 8)) for x in h) and all(x == qr(Fr(1, 4)) for x in rho),
    'Reuleaux tetrahedron: opposite edges 1/sqrt2 apart, every corner at height +-1/(2 sqrt2) and 1/2 from the edge-midpoint axis, so the width there is 2 sqrt(3/4) - 1/sqrt2 = sqrt3 - sqrt2/2')
chk(RR['Cube'] == RR['Octahedron'] == qr(Fr(1, 3)), 'cube and octahedron share (r/R)^2 = 1/3')
chk(RR['Dodecahedron'] == RR['Icosahedron'] == (Fr(1, 3), Fr(2, 15)), 'dodecahedron and icosahedron share (r/R)^2 = (5 + 2 sqrt5)/15')
# width along the face axis at diameter 1 (R = 1/2): w = A - B with A^2 = 4(3/4 + r^2) = 3 + 4 r^2, B^2 = 4 r^2, r^2 = (r/R)^2 / 4
W = {}
for name in ['Cube', 'Octahedron', 'Dodecahedron', 'Icosahedron']:
    r2 = qm(RR[name], qr(Fr(1, 4))); A2, B2 = qa(qr(3), qm(qr(4), r2)), qm(qr(4), r2); W[name] = (A2, B2)
    print(f'     {name}: A^2 = {qstr(A2)}, B^2 = {qstr(B2)}')
chk(W['Cube'] == W['Octahedron'] == (qr(Fr(10, 3)), qr(Fr(1, 3))) and Fr(30, 9) == Fr(10, 3) and Fr(3, 9) == Fr(1, 3),
    'cube/octahedron: A = sqrt30/3, B = sqrt3/3, so w = (sqrt30 - sqrt3)/3')
chk(W['Dodecahedron'] == W['Icosahedron'] == ((Fr(10, 3), Fr(2, 15)), (Fr(1, 3), Fr(2, 15))),
    'dodecahedron/icosahedron: A^2 = (50 + 2 sqrt5)/15, B^2 = (5 + 2 sqrt5)/15, so w = (sqrt(50 + 2 sqrt5) - sqrt(5 + 2 sqrt5))/sqrt15')
print('\n== B. Numerical (float64)')
log = open(os.path.join(HERE, 'widths.log')).read()
mx = {m.group(1): float(m.group(3)) for m in re.finditer(r'balls on the (\w+)\): width ([\d.]+) \.\. ([\d.]+)', log)}
mn = {m.group(1): float(m.group(2)) for m in re.finditer(r'balls on the (\w+)\): width ([\d.]+) \.\. ([\d.]+)', log)}
for name, (A2, B2) in W.items():
    w = math.sqrt(qf(A2)) - math.sqrt(qf(B2))
    chk(abs(w - mx[name.lower()]) < 1e-11, f'Reuleaux {LOOK[name]}: face-axis width {w:.12f} = the largest width found in widths.log ({mx[name.lower()]:.12f})')
chk(abs((30 ** .5 - 3 ** .5) / 3 - 1.248391589161) < 1e-12 and abs(((50 + 2 * 5 ** .5) ** .5 - (5 + 2 * 5 ** .5) ** .5) / 15 ** .5 - 1.110988655456) < 1e-12, 'closed forms = 1.248391589161 and 1.110988655456')
chk(abs(3 ** .5 - 2 ** .5 / 2 - mx['tetrahedron']) < 1e-11, f'Reuleaux tetrahedron: sqrt3 - sqrt2/2 = {3 ** .5 - 2 ** .5 / 2:.12f} = the largest width found in widths.log')
chk(all(abs(v - 1) < 1e-12 for v in mn.values()) and len(mn) == 5, 'widths.log: smallest width 1 (the diameter) for all five')
def vol(P, N):
    P = np.array(P, float); D = max(np.linalg.norm(a - b) for a, b in itertools.combinations(P, 2)); P = P / D
    x, wx = np.polynomial.legendre.leggauss(N); ph = (np.arange(2 * N) + .5) * np.pi / N
    tot = 0.0
    for z, wz in zip(np.array_split(x, 40), np.array_split(wx, 40)):
        s = np.sqrt(1 - z ** 2); U = np.stack([np.outer(s, np.cos(ph)), np.outer(s, np.sin(ph)), np.outer(z, np.ones_like(ph))], -1)
        uv = U @ P.T; t = uv + np.sqrt(uv ** 2 - (P ** 2).sum(1) + 1); r = t.min(-1)
        tot += (wz[:, None] * r ** 3).sum() * (np.pi / N)
    return tot / 3
Sf = {k: [[qf(c) for c in p] for p in P] for k, P in S.items()}
harb = 8 * math.pi / 3 + math.sqrt(2) / 4 - 27 / 4 * math.acos(1 / 3)
for name, P in Sf.items():
    v1, v2 = vol(P, 1000), vol(P, 2000)
    print(f'     Reuleaux {LOOK[name]:13s} volume at diameter 1: {v2:.7f} (N = 2000; N = 1000 gives {v1:.7f})')
    if name == 'Tetrahedron': chk(abs(v2 - harb) < 1e-5, f'Reuleaux tetrahedron volume {v2:.7f} = 8pi/3 + sqrt2/4 - (27/4) arccos(1/3) = {harb:.7f} (Harbourne, quoted by Hynd 2023), to {abs(v2 - harb):.1e}')
# which faces meet along an arc: the face on ball v and the face on ball w share an arc iff some point of the circle
# |x - v| = |x - w| = 1 lies strictly inside every other ball (sampled, 7200 points, margin 1e-9)
def adjacency(P):
    P = np.array(P, float); D = max(np.linalg.norm(a - b) for a, b in itertools.combinations(P, 2)); P = P / D; A = set()
    t = np.linspace(0, 2 * np.pi, 7200, endpoint=False)
    for i, j in itertools.combinations(range(len(P)), 2):
        a, b = P[i], P[j]; m = (a + b) / 2; e = (b - a) / np.linalg.norm(b - a); r2 = 1 - ((b - a) @ (b - a)) / 4
        if r2 <= 0: continue
        e1 = np.cross(e, [1, 0, 0] if abs(e[0]) < .9 else [0, 1, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(e, e1)
        X = m + np.sqrt(r2) * (np.outer(np.cos(t), e1) + np.outer(np.sin(t), e2))
        d = np.linalg.norm(X[:, None] - P[None], axis=2); d[:, [i, j]] = 0
        if (d.max(1) < 1 - 1e-9).any(): A.add((i, j))
    return A
def chromatic(n, A):
    nb = {i: set() for i in range(n)}
    for a, b in A: nb[a].add(b); nb[b].add(a)
    order = sorted(nb, key=lambda o: -len(nb[o]))
    for k in range(1, 6):
        cl = {}
        def go(i):
            if i == n: return True
            o = order[i]
            for c in range(k):
                if all(cl.get(x) != c for x in nb[o]):
                    cl[o] = c
                    if go(i + 1): return True
                    del cl[o]
            return False
        if go(0): return k
WANT = {'Tetrahedron': 4, 'Cube': 2, 'Octahedron': 3, 'Dodecahedron': 3, 'Icosahedron': 4}
for name, P in Sf.items():
    A = adjacency(P); E = edges(S[name])
    chk(A == E, f'Reuleaux {LOOK[name]}: two faces meet along an arc exactly when their balls\' centres are joined by an edge of the {name.lower()} ({len(A)} arcs)')
    k = chromatic(len(P), A); chk(k == WANT[name], f'Reuleaux {LOOK[name]}: {len(P)} faces, fewest colours with no two neighbours alike: {k}')
print('\nALL PASS' if bad == 0 else f'\n{bad} FAIL')
