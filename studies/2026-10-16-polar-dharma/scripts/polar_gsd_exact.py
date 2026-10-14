# Step 5, exact: the great stellated dodecahedron with its 20 points at the outer dodecahedron's corners. Its face planes (one per
# 5-fold axis, through the 5 corners of the near-equator level) are checked exactly in Q(sqrt5) against the chain's icosahedron.
import json, itertools, sys, io, contextlib, numpy as np
sys.argv = ['polar.py', 'data/dharma_cycle.json']
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('scripts/polar.py').read())
St = dict(rev); DO, IC, RTx = St[rev[-1][0]], St['icosahedron'], St['rhombic triacontahedron']
f = lambda v: np.array([x.f() for x in v])
dot = lambda n, v: sum((n[i] * v[i] for i in range(3)), Q(0))
out = []; inc = {}
for u in IC:
    uf = f(u); h = [f(v) @ uf for v in DO]; lev = sorted(set(np.round(h, 6)))
    L = [v for v, hv in zip(DO, h) if abs(hv - lev[2]) < 1e-5]
    a, b, c = L[:3]; uu = [b[i] - a[i] for i in range(3)]; ww = [c[i] - a[i] for i in range(3)]
    n = [uu[1] * ww[2] - uu[2] * ww[1], uu[2] * ww[0] - uu[0] * ww[2], uu[0] * ww[1] - uu[1] * ww[0]]; d = dot(n, a)
    assert all(dot(n, v) == d for v in L), 'level not planar'
    for j, w in enumerate(IC):
        if dot(n, w) == d: inc[j] = inc.get(j, 0) + 1
    for j, w in enumerate(RTx):
        if dot(n, w) == d: inc[('RT', j)] = inc.get(('RT', j), 0) + 1
out.append(f'icosahedron corners lying exactly on GSD face planes: {sum(1 for k in inc if not isinstance(k, tuple))} of 12, '
           f'each on {sorted(set(v for k, v in inc.items() if not isinstance(k, tuple)))} planes')
out.append(f'other triacontahedron corners on GSD face planes: {sum(1 for k in inc if isinstance(k, tuple) and k[1] >= 0 and f(RTx[k[1]]).tolist() not in [f(w).tolist() for w in IC])}')
r2 = lambda v: dot(v, v)
out.append(f'squared radii: GSD points {r2(DO[0])!r}, valley icosahedron {r2(IC[0])!r}')
print('\n'.join(out)); open('data/polar-gsd-exact.txt', 'w').write('\n'.join(out) + '\n')
