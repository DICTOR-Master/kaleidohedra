# Spheres of Dharma turned inside out by polar reciprocation (DICTO's 2026-10-13 idea; step 1, 2026-10-16): each station replaced by its
# dual (polar in the unit sphere), the nesting reversed. Corners snapped to exact a + b*sqrt5 (as in Theaetetus' exact.py) and every
# reciprocal corner computed exactly. Reports: the reversed chain, edges, phi^3 closure, touching (corners on faces), layer volumes.
import json, sys, itertools, numpy as np
from scipy.spatial import ConvexHull
sys.path.insert(0, '/home/dicto/kaleidohedra/studies/2026-10-15-icosa-star-hollow/scripts')
src = open('/home/dicto/kaleidohedra/studies/2026-10-15-icosa-star-hollow/scripts/exact.py').read().split('out = []')[0].replace('qmax=48', 'qmax=12')
exec(src)
D = json.load(open(sys.argv[1]))
order = [('icosahedron', ['core']), ('icosidodecahedron', ['npyr5', 'nfru3']), ('dodecahedron', ['npyr3']), ('truncated icosahedron', ['nfru5', 'nt1']),
         ('Hecatodihedron', ['ncap7']), ('rhombic triacontahedron', ['ncap6', 'nwedge']), ('icosahedron (phi^3)', ['nedge', 'nface'])]
role = lambda r, V: f'ncap{len(V)}' if r == 'ncap' else r
acc, stations = [], []
for name, roles in order:
    acc += [np.array(V, float) for r, V, *_ in D if role(r, V) in roles]
    Hh = ConvexHull(np.vstack(acc)); P = Hh.points[Hh.vertices]
    V = [[S(x) for x in p] for p in P]; stations.append((name, V))
def planes(V):
    Vf = np.array([[x.f() for x in v] for v in V]); h = ConvexHull(Vf); out = []
    for e in h.equations:
        idx = [i for i in range(len(V)) if abs(Vf[i] @ e[:3] + e[3]) < 1e-7]
        if any(set(idx) == set(o) for o in out): continue
        out.append(idx)
    return out
def polar(V):
    """Corners of the dual: for each face plane n.x = d (exact, through three exact corners), the pole n/d."""
    res = []
    for idx in planes(V):
        for i0, i1, i2 in itertools.combinations(idx, 3):       # three corners not in a line
            a, b, c = V[i0], V[i1], V[i2]
            u = [b[i] - a[i] for i in range(3)]; w = [c[i] - a[i] for i in range(3)]
            n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
            if any(x.f() != 0 for x in n): break
        d = sum(n[i] * a[i] for i in range(3))
        if d.f() < 0: n = [-x for x in n]; d = -d
        res.append([n[i] / d for i in range(3)])
    return res
DUAL = {'icosahedron': 'dodecahedron', 'icosidodecahedron': 'rhombic triacontahedron', 'dodecahedron': 'icosahedron', 'truncated icosahedron': 'pentakis dodecahedron',
        'Hecatodihedron': 'dual of the Hecatodihedron', 'rhombic triacontahedron': 'icosidodecahedron', 'icosahedron (phi^3)': 'dodecahedron'}
rev = [(DUAL[n], polar(V)) for n, V in reversed(stations)]
f = lambda V: np.array([[x.f() for x in v] for v in V])
out = ['Reversed chain (polar in the unit sphere), inside to outside:']
for k, (n, V) in enumerate(rev):
    W = f(V); h = ConvexHull(W); E = sorted({round(np.linalg.norm(W[a] - W[b]), 6) for s in h.simplices for a, b in itertools.combinations(s, 2)})
    R = np.linalg.norm(W, axis=1); vol = volume(V, W)
    out.append(f'  {k}. {n}: {len(V)} corners, {len(planes(V))} faces, radius {R.min():.6f}-{R.max():.6f}, shortest distance {E[0]:.6f}, volume {vol!r} = {vol.f():.6f}')
r0, r6 = volume(rev[0][1], f(rev[0][1])), volume(rev[-1][1], f(rev[-1][1]))
ratio = r6 / r0
out.append(f'closure: outer dodecahedron / inner dodecahedron volume = {ratio!r} = {ratio.f():.6f} (phi^9 = {((1 + 5 ** .5) / 2) ** 9:.6f})')
out.append('Touching (inner corners on outer faces, inner faces through outer corners), and layer volumes:')
for (n1, A), (n2, B) in zip(rev, rev[1:]):
    Af, Bf = f(A), f(B); hb = ConvexHull(Bf); ha = ConvexHull(Af)
    on = sum(1 for p in Af if np.min(np.abs(hb.equations[:, :3] @ p + hb.equations[:, 3])) < 1e-7)
    thru = sum(1 for p in Bf if np.min(np.abs(ha.equations[:, :3] @ p + ha.equations[:, 3])) < 1e-7)
    inside = np.all(Af @ hb.equations[:, :3].T + hb.equations[:, 3] <= 1e-7)
    lv = volume(B, Bf) - volume(A, Af)
    out.append(f'  {n1} -> {n2}: inside {inside}; {on} inner corners on outer faces; {thru} outer corners on inner face planes; layer volume {lv!r} = {lv.f():.6f}')
print('\n'.join(out)); open('data/polar-step1.txt', 'w').write('\n'.join(out) + '\n')
json.dump([[n + (' (inner)' if k == 0 else ' (phi^3)' if k == len(rev) - 1 else ''), f(V).tolist()] for k, (n, V) in enumerate(rev)], open('data/reversed-chain.json', 'w'))
