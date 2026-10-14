# Step 6 (DICTO's question): room for something rounder and more rhythmic? The icosahedral Archimedean solids and their Catalan duals
# (many faces, nearly spherical) tested in two places of the original nest:
#   big gap, inside the great stellated dodecahedron (GSD body = icosahedron + 20 spikes), around the triacontahedron (RT)
#   inner gap, inside the icosidodecahedron (ID), around the inner dodecahedron, and around the Hecatodihedron at its touching size
# For each: the scale range [lo, hi] that fits; 'locked' when lo = hi (touches both sides at one size, like the GSD in step 5).
import json, itertools, sys, io, contextlib, numpy as np
from scipy.spatial import ConvexHull
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
C = {n: np.array(V, float) for n, V in json.load(open('data/reversed-chain.json'))}
p = (1 + 5 ** .5) / 2
def cyc(pts):
    out = set()
    for x, y, z in pts:
        for sx, sy, sz in itertools.product(*[[1, -1] if c else [1] for c in (x, y, z)]):
            a = (sx * x, sy * y, sz * z)
            for r in range(3): out.add(tuple(round(v, 12) for v in a[r:] + a[:r]))
    return np.array(sorted(out))
I0 = cyc([(0, 1, p)])
# match the chain's frame: its icosahedron's directions must equal I0's (else swap two axes)
u = lambda V: {tuple(np.round(v / np.linalg.norm(v), 6)) for v in V}
SW = np.eye(3) if u(I0) == u(C['icosahedron']) else np.eye(3)[[1, 0, 2]]
assert u(I0 @ SW) == u(C['icosahedron']), 'frame'
ARCH = {
    'icosidodecahedron': [(0, 0, 2 * p), (1, p, p * p)],
    'truncated icosahedron': [(0, 1, 3 * p), (1, 2 + p, 2 * p), (p, 2, p ** 3)],
    'truncated dodecahedron': [(0, 1 / p, 2 + p), (1 / p, p, 2 * p), (p, 2, p + 1)],
    'rhombicosidodecahedron': [(1, 1, p ** 3), (p * p, p, 2 * p), (2 + p, 0, p * p)],
    'truncated icosidodecahedron': [(1 / p, 1 / p, 3 + p), (2 / p, p, 1 + 2 * p), (1 / p, p * p, 3 * p - 1), (2 * p - 1, 2, 2 + p), (p, 3, 2 * p)],
}
def dual(V):
    e = ConvexHull(V).equations; pl = []
    for x in e:
        if not any(np.allclose(x, y, atol=1e-9) for y in pl): pl.append(x)
    return np.array([x[:3] / -x[3] for x in pl])
CAT = {'pentakis dodecahedron': 'truncated icosahedron', 'triakis icosahedron': 'truncated dodecahedron',
       'deltoidal hexecontahedron': 'rhombicosidodecahedron', 'disdyakis triacontahedron': 'truncated icosidodecahedron',
       'rhombic triacontahedron': 'icosidodecahedron'}
SOL = {k: cyc(v) @ SW for k, v in ARCH.items()}
SOL.update({k: dual(SOL[a]) for k, a in CAT.items()})
for k, V in SOL.items(): assert len(ConvexHull(V).vertices) == len(V), k
def rad(V, u):
    e = ConvexHull(V).equations; nu = e[:, :3] @ u; m = nu > 1e-12; return np.min(-e[m, 3] / nu[m])
def surface(V, n=12):   # corners, edge points and face points of a convex solid
    h = ConvexHull(V); P = [V]
    for s in h.simplices:
        a, b, c = V[s]
        for i in range(n + 1):
            for j in range(n + 1 - i):
                P.append([a + (b - a) * i / n + (c - a) * j / n])
    return np.vstack(P)
# the GSD body of step 5: the chain's icosahedron plus 20 spikes to the corners of D(phi^3)
IC, DO, RT = C['icosahedron'], C['dodecahedron (phi^3)'], C['rhombic triacontahedron']
hI = ConvexHull(IC); spikes = []
for s in hI.simplices:
    c = IC[s].mean(0); T = DO[np.argmax(DO @ (c / np.linalg.norm(c)))]; spikes.append(ConvexHull(np.vstack([IC[s], T])).equations)
pieces = [hI.equations] + spikes
def rho_gsd(u):
    best = 0
    for e in pieces:
        nu = e[:, :3] @ u; t = -e[:, 3] / np.where(abs(nu) > 1e-15, nu, np.nan)
        tin = np.nanmax(np.where(nu < 0, t, -np.inf)); tout = np.nanmin(np.where(nu > 0, t, np.inf))
        tin = max(tin, 0)
        if tout > tin + 1e-12: best = max(best, tout)
    return best
def fit(X, inner, outer):
    lo = max(np.linalg.norm(v) / rad(X, v / np.linalg.norm(v)) for v in inner)
    S = surface(X); n = np.linalg.norm(S, axis=1)
    hi = min((outer(s / m) / m) for s, m in zip(S, n)) if callable(outer) else min(rad(outer, s / m) / m for s, m in zip(S[:len(X)], n[:len(X)]))
    return lo, hi
Hk = [np.array([[c.f() for c in v] for v in V]) for nn, V in stations if nn == 'Hecatodihedron'][0]
Hk = np.unique(np.round(Hk, 9), axis=0); Hk = Hk[ConvexHull(Hk).vertices] * 0.314757   # step 5c, touching the dodecahedron
places = [('big gap: RT -> inside the GSD', RT, rho_gsd), ('inner gap: dodecahedron -> ID', C['dodecahedron (inner)'], C['icosidodecahedron']),
          ('inner gap: Hecatodihedron (touching D) -> ID', Hk, C['icosidodecahedron'])]
lines = []
for name, X in sorted(SOL.items(), key=lambda kv: -min(np.linalg.norm(kv[1], axis=1)) / 1):
    h = ConvexHull(X); r = np.linalg.norm(X, axis=1); sph = min(-h.equations[:, 3]) / r.max()
    nf = len({tuple(np.round(e, 7)) for e in h.equations})
    res = []
    for pn, inner, outer in places:
        lo, hi = fit(X, inner, outer)
        res.append(f'{pn}: ' + ('NO' if lo > hi * (1 + 1e-6) else ('LOCKED' if abs(hi / lo - 1) < 1e-4 else f'room x{hi / lo:.4f}')))
    lines.append(f'{name} ({nf} faces, {len(X)} corners, inradius/circumradius {sph:.4f}): ' + '; '.join(res))
lines.sort(key=lambda s: -float(s.split('circumradius ')[1].split(')')[0]))
print('\n'.join(lines)); open('data/polar-round.txt', 'w').write('\n'.join(lines) + '\n')
