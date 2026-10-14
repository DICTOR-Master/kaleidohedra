# Cleo core to the DICTO Hecatodihedron (DICTO 2026-10-15, "new standalone object"): our edge-1 core held by Cleo-Icos inside the
# icosidodecahedron of edge 1 (steps 1-2), then Spheres of Dharma's shells from the icosidodecahedron outward, scaled by 2/phi.
import itertools, json, sys, numpy as np
from scipy.spatial import ConvexHull
D = json.load(open(sys.argv[1])); g = (1 + 5 ** .5) / 2; s = 2 / g
roles = lambda *rs: [np.array(V, float) * s for r, V, *_ in D if r in rs]
outer = {'tripyr (to dodecahedron)': roles('npyr3'), 'twisted pentagonal frustum': roles('nfru5'), 't1': roles('nt1'),
         'cap (to Hecatodihedron)': [P for P in roles('ncap') if len(P) == 7]}
ID = ConvexHull(np.vstack(roles('core', 'npyr5', 'nfru3'))); IDv = ID.points[ID.vertices]
vol = lambda P: ConvexHull(P).volume
e_id = min(np.linalg.norm(a - b) for a, b in itertools.combinations(IDv, 2))
out = [f'0. Dharma\'s icosidodecahedron scaled by 2/phi: {len(IDv)} corners, edge {e_id:.12f}']
F = []
for e in ID.equations:
    idx = tuple(sorted(i for i in range(len(IDv)) if abs(IDv[i] @ e[:3] + e[3]) < 2e-5))
    if idx not in [f for f, _ in F] and len(idx) in (3, 5): F.append((idx, e))
tri = [(IDv[list(i)], e[:3]) for i, e in F if len(i) == 3]; pent = [(IDv[list(i)], e[:3]) for i, e in F if len(i) == 5]
R = (10 + 2 * 5 ** .5) ** .5 / 4; r = g * g / (2 * 3 ** .5)
core = np.array([n * R for _, n in pent]); CH = ConvexHull(core); cf = [core[t] for t in CH.simplices]
inner = {'core icosahedron': [core], 'Cleo-Ico': [], 'flat pentagonal pyramid': [np.vstack([P, n * R]) for P, n in pent], 'X': [], 'Y': []}
for T, n in tri:
    B = max(cf, key=lambda Q: Q.mean(0) @ n); b0 = B.mean(0); inner['Cleo-Ico'].append(np.vstack([T, b0]))
    for i, j in itertools.combinations(range(3), 2):
        bk = min(B, key=lambda b: np.linalg.norm(b - (T[i] + T[j]) / 2)); inner['X'].append(np.array([T[i], T[j], bk, b0]))
    for k, l in itertools.combinations(range(3), 2):
        tm = min(T, key=lambda t: np.linalg.norm(t - (B[k] + B[l]) / 2)); inner['Y'].append(np.array([B[k], B[l], tm, b0]))
allp = {**inner, **outer}
H = ConvexHull(np.vstack([P for L in allp.values() for P in L]))
tot = sum(vol(P) for L in allp.values() for P in L)
nf = len({tuple(np.round(e, 7)) for e in H.equations})
out.append('1. pieces: ' + ', '.join(f'{len(L)} {k}' for k, L in allp.items()) + f' = {sum(map(len, allp.values()))}')
out.append(f'2. volumes: pieces {tot:.12f}; their hull {H.volume:.12f}; difference {tot - H.volume:.1e}; hull has {nf} face planes (the Hecatodihedron has 102)')
inner_tot = sum(vol(P) for L in inner.values() for P in L)
out.append(f'3. inside the icosidodecahedron: {inner_tot:.12f} vs its volume {ID.volume:.12f}')
# overlaps: every pair of pieces whose bounding spheres meet, by separating axes
def axes(P):
    h = ConvexHull(P); A = [e[:3] for e in h.equations]
    E = {tuple(np.round(P[j] - P[i], 12)) for t in h.simplices for i, j in itertools.combinations(t, 2)}
    return A, [np.array(x) for x in E]
def sep(P, Q):
    a1, e1 = axes(P); a2, e2 = axes(Q); best = -1e9
    for m in a1 + a2 + [np.cross(u, w) / np.linalg.norm(np.cross(u, w)) for u in e1 for w in e2 if np.linalg.norm(np.cross(u, w)) > 1e-12]:
        p, q = P @ m, Q @ m; best = max(best, q.min() - p.max(), p.min() - q.max())
    return best
flat = [(k, P) for k, L in allp.items() for P in L]
worst, n = 0, 0
for (k1, P), (k2, Q) in itertools.combinations(flat, 2):
    c1, c2 = P.mean(0), Q.mean(0)
    if np.linalg.norm(c1 - c2) > np.linalg.norm(P - c1, axis=1).max() + np.linalg.norm(Q - c2, axis=1).max(): continue
    n += 1; worst = min(worst, sep(P, Q))
out.append(f'4. overlaps: {n} nearby pairs tested, worst separation {worst:.1e} (data stored to 6 places, so >= -1e-5: none)')
print('\n'.join(out)); open('cleo_heca.txt', 'w').write('\n'.join(out) + '\n')
mesh = lambda P: {'v': np.round(P, 6).tolist(), 'f': ConvexHull(P).simplices.tolist(), 'c': np.round(P.mean(0), 6).tolist()}
json.dump({k: [mesh(P) for P in L] for k, L in allp.items()}, open('cleo_heca.json', 'w'))

# 5. fusions (DICTO: "fuse some pieces on the way to make some interesting useful additions"): every pair of pieces sharing a whole face
# whose union is convex (no dents), grouped by the kinds fused, with the fused shape described.
key = lambda p: tuple(np.round(p, 4))
def faces_of(P):
    h = ConvexHull(P); out = []
    for e in h.equations:
        idx = frozenset(key(P[i]) for i in range(len(P)) if abs(P[i] @ e[:3] + e[3]) < 2e-5)
        if idx not in out: out.append(idx)
    return out
FF = [faces_of(P) for _, P in flat]
where = {}
for i, fs in enumerate(FF):
    for f in fs: where.setdefault(f, []).append(i)
fus = {}
for f, ids in where.items():
    if len(ids) != 2: continue
    i, j = ids; P, Q = flat[i][1], flat[j][1]; U = np.unique(np.round(np.vstack([P, Q]), 6), axis=0)
    if abs(vol(U) - vol(P) - vol(Q)) < 1e-6:
        k = ' + '.join(sorted([flat[i][0], flat[j][0]])); fus.setdefault(k, []).append(U)
def describe(U):
    h = ConvexHull(U); planes = {}
    for e, t in zip(h.equations, h.simplices): planes.setdefault(tuple(np.round(e, 5)), set()).update(t)
    sides = sorted(len(v) for v in planes.values())
    L = sorted({round(np.linalg.norm(U[a] - U[b]), 4) for v in planes.values() for a, b in itertools.combinations(v, 2)})
    return f'{len(U)} corners, {len(planes)} faces (sides {dict((s, sides.count(s)) for s in set(sides))}), vol {vol(U):.6f}'
out2 = [f'5. convex fusions of two face-sharing pieces ({sum(len(v) for v in where.values() if len(v) == 2)} shared faces looked at):']
for k, L in sorted(fus.items(), key=lambda kv: -len(kv[1])):
    out2.append(f'   {len(L):3d} x  {k}:  {describe(L[0])}')
if not fus: out2.append('   none')
print('\n'.join(out2)); open('cleo_heca.txt', 'a').write('\n'.join(out2) + '\n')
json.dump({k: [mesh(U) for U in L] for k, L in fus.items()}, open('cleo_heca_fusions.json', 'w'))
