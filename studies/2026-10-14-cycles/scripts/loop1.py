# Cycles Loop 1 (DICTO, 2026-10-14): icosahedron -> great dodecahedron -> small stellated dodecahedron -> great icosahedron -> icosahedron,
# all on the same 12 corners (the icosahedron's, edge 1). For each station: its faces as corner cycles, edge lengths, face planes; and
# for each step what is kept (edges, face planes) and what changes. DICTO · dictospheres.com
import itertools, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
phi = (1 + 5 ** .5) / 2
V = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float) / 2
D = np.linalg.norm(V[:, None] - V[None], axis=2)
near = lambda i, d: [j for j in range(12) if abs(D[i, j] - d) < 1e-9]
anti = lambda i: int(np.argmin(np.linalg.norm(V + V[i], axis=1)))
def cyc(idx, step):                                  # order 5 coplanar corners round their centre, joining every `step`-th
    c = V[idx].mean(0); n = c / np.linalg.norm(c); a = V[idx[0]] - c; a /= np.linalg.norm(a); b = np.cross(n, a)
    o = [idx[k] for k in np.argsort([np.arctan2((V[i] - c) @ b, (V[i] - c) @ a) for i in idx])]
    return [o[(k * step) % 5] for k in range(5)]
tri = lambda d: sorted({tuple(sorted(t)) for t in itertools.combinations(range(12), 3) if all(abs(D[x, y] - d) < 1e-9 for x, y in itertools.combinations(t, 2))})
S = {
    'icosahedron': [list(t) for t in tri(1.0)],
    'great dodecahedron': [cyc(near(i, 1.0), 1) for i in range(12)],                # pentagons through each corner's 5 neighbours
    'small stellated dodecahedron': [cyc(near(i, 1.0), 2) for i in range(12)],      # pentagrams on the same five corners
    'great icosahedron': [list(t) for t in tri(phi)],
}
def info(F):
    E = {tuple(sorted((f[k], f[(k + 1) % len(f)]))) for f in F for k in range(len(f))}
    P = set()
    for f in F:
        n = np.cross(V[f[1]] - V[f[0]], V[f[2]] - V[f[0]]); n /= np.linalg.norm(n); d = n @ V[f[0]]
        if d < 0: n, d = -n, -d
        P.add(tuple(np.round(np.r_[n, d], 6)))
    return E, P
out = {'corners': V.round(6).tolist(), 'stations': {}, 'steps': []}
names = list(S)
for k in names:
    E, P = info(S[k])
    out['stations'][k] = dict(faces=len(S[k]), face_shape={3: 'triangle', 5: 'pentagon' if k == 'great dodecahedron' else 'pentagram'}[len(S[k][0])],
                             edges=len(E), edge_length=sorted({round(float(D[a, b]), 6) for a, b in E}), plane_distance=sorted({p[3] for p in P}))
for a, b in zip(names, names[1:] + names[:1]):
    Ea, Pa = info(S[a]); Eb, Pb = info(S[b])
    out['steps'].append(dict(step=f'{a} -> {b}', same_corners=True, same_edges=Ea == Eb, same_face_planes=Pa == Pb))
json.dump(out, open(os.path.join(ROOT, 'loop1.json'), 'w'), indent=1)
for k, v in out['stations'].items(): print(k, v)
for s in out['steps']: print(s)
