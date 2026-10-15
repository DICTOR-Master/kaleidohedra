# Both cycles in one space (DICTO, 2026-10-16: an up-down toggle). The original Spheres of Dharma turn (I .. I*phi^3) and its polar
# image in a sphere of radius rho, drawn as shells. Two alignments: rho^2 = phi^2/4 (the cycles share the ends I and D) and
# rho^2 = 3 phi^2/4 (they share the middle, ID and RT). Writes data/toggle-<name>-render.json; shared stations are flagged.
import sys, io, contextlib, json, numpy as np
from scipy.spatial import ConvexHull
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
p = (1 + 5 ** .5) / 2
orig = []
for n, V in stations:
    X = np.unique(np.round(np.array([[c.f() for c in v] for v in V]), 9), axis=0); orig.append((n, X[ConvexHull(X).vertices]))
def planes(X):
    pl = []
    for e in ConvexHull(X).equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in pl): pl.append(e)
    return pl
def shell(X):
    F = []
    for e in planes(X):
        idx = [i for i in range(len(X)) if abs(X[i] @ e[:3] + e[3]) < 1e-7]; Q = X[idx]; c = Q.mean(0)
        a = Q[0] - c; a /= np.linalg.norm(a); b = np.cross(e[:3], a); F.append([idx[i] for i in np.argsort(np.arctan2((Q - c) @ b, (Q - c) @ a))])
    return {'v': X.tolist(), 'f': F}
def polar(X, r2): return np.array([r2 * e[:3] / -e[3] for e in planes(X)])
same = lambda A, B: len(A) == len(B) and all(np.min(np.linalg.norm(B - a, axis=1)) < 1e-6 for a in A)
for name, r2 in (('ends', p * p / 4), ('middle', 3 * p * p / 4)):
    rev = [(f'polar of {n}', polar(X, r2)) for n, X in orig]
    S = []
    for n, X in orig: S.append({'name': n, 'cycle': 'original', 'shared': any(same(X, Y) for _, Y in rev), **shell(X)})
    for n, Y in rev:
        if not any(same(Y, X) for _, X in orig): S.append({'name': n, 'cycle': 'reversed', 'shared': False, **shell(Y)})
    json.dump({'shells': S, 'rho2': r2}, open(f'data/toggle-{name}-render.json', 'w'))
    print(name, 'rho^2 =', round(r2, 9), '| shared:', [s['name'] for s in S if s['shared']], '| radii', round(min(np.linalg.norm(np.array(s['v']), axis=1).min() for s in S), 3), '..', round(max(np.linalg.norm(np.array(s['v']), axis=1).max() for s in S), 3))

# movie data (pure geometry): the original turn and its full polar image at rho^2 = phi^2/4. Every other toggle sphere rho gives
# the same flipped cycle scaled by rho^2 / (phi^2/4), so the movie scales one set of shells; at scale 1 the cycles share I and D,
# at scale 3 they share ID and RT (both exact settings of the toggle, nothing bent in between).
r2 = p * p / 4
M = {'orig': [{'name': n, **shell(X)} for n, X in orig], 'flip': [{'name': f'polar of {n}', **shell(polar(X, r2))} for n, X in orig],
     'shared_ends': ['icosahedron', 'dodecahedron'], 'shared_middle': ['icosidodecahedron', 'rhombic triacontahedron']}
json.dump(M, open('data/toggle-movie.json', 'w')); print('movie data', len(M['orig']), len(M['flip']))
