# DICTO OCD Stella Atom 13 (DICTO 2026-10-16: "can OCD Stella form Atom 13"; "an interlocking pyrochlore network could help spacing, like the
# Bodhi in the group"). Float. Centre + 12 copies on the 5-fold axes (the 12 farthest corners), each pushed out until it touches the centre.
# Interlocking: the 20 gaps between the 12 lie over the centre's 20 triangles (3-fold axes); icosahedra (the crystal's, scaled) flat on
# each triangle, at the largest scale with no clash. -> data/stella-atom13.txt, data/stella-atom13.json
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
from scipy.optimize import linprog
R = json.load(open('data/crystal-render.json')); S = np.array(R['stella']['v']); I = np.array(R['ico']['v'])
def planes(V):
    P = []
    for e in ConvexHull(V).equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in P): P.append(e)
    return np.array(P)
PS, PI = planes(S), planes(I)
def depth(PA, a, PB, b):
    H = np.vstack([np.c_[PA[:, :3], PA[:, 3] - PA[:, :3] @ a], np.c_[PB[:, :3], PB[:, 3] - PB[:, :3] @ b]]); A = H[:, :3]; bb = -H[:, 3]
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A, np.linalg.norm(A, axis=1)], b_ub=bb, bounds=[(None, None)] * 3 + [(0, None)])
    return r.x[3] if r.success else 0
rr = np.linalg.norm(S, axis=1); U = S[rr > rr.max() - 1e-6]; U = U / np.linalg.norm(U, axis=1)[:, None]
def touch(u):
    lo, hi = 0.5, 3.0
    for _ in range(50):
        m = (lo + hi) / 2
        if depth(PS, np.zeros(3), PS, m * u) > 1e-9: lo = m
        else: hi = m
    return hi
t = touch(U[0]); stel = [t * u for u in U]
tri = [e for e in PS if sum(abs(S @ e[:3] + e[3]) < 1e-7) == 3]
rI = -PI[0, 3]
place = lambda s: [(-e[3] + s * rI) * e[:3] for e in tri]
def clash(s):
    Ps = np.c_[PI[:, :3], PI[:, 3] * s]; pos = place(s)
    return (max(depth(Ps, p, PS, np.zeros(3)) for p in pos), max(depth(Ps, p, PS, q) for p in pos for q in stel),
            max(depth(Ps, p, Ps, q) for p, q in itertools.combinations(pos, 2)))
out = ['DICTO · dictospheres.com', 'DICTO OCD Stella Atom 13 (float)', f'12 copies on the 5-fold axes, touching the centre at distance {t:.5f}']
gap = min(max(depth(PS, a, PS, b), 0) for a, b in itertools.combinations(stel, 2))
lo, hi = 0.0, 1.0
for _ in range(30):
    m = (lo + hi) / 2
    if max(clash(m)) > 1e-6: hi = m
    else: lo = m
s = lo; c = clash(min(1.0, s * 1.03))
vS = ConvexHull(S).volume; vI = ConvexHull(I).volume * s ** 3
h13 = ConvexHull(np.vstack([S] + [S + p for p in stel])).volume
h33 = ConvexHull(np.vstack([S] + [S + p for p in stel] + [I * s + p for p in place(s)])).volume
out += [f'interlocking: 20 icosahedra flat on the centre\'s 20 triangles, largest without a clash: {s:.4f} of the crystal icosahedron',
        f'  just above it the first clash is with: {"the centre" if c[0] == max(c) else "the 12 OCD Stellas" if c[1] == max(c) else "each other"} (depths {c[0]:.4f}, {c[1]:.4f}, {c[2]:.4f})',
        f'Atom 13 alone fills {13 * vS / h13:.2%} of its outline; with the 20 icosahedra (33 solids) {(13 * vS + 20 * vI) / h33:.2%}']
print('\n'.join(out)); open('data/stella-atom13.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'stella': R['stella'], 'ico': R['ico'], 'stel': [p.tolist() for p in stel], 'ico_scale': s, 'icos': [p.tolist() for p in place(s)]}, open('data/stella-atom13.json', 'w'))
