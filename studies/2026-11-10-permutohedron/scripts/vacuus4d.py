"""The 4D Vacuus of the 4D permutohedron (DICTO 10 Nov: "B the 4D vacuus is its form"). A 3D Vacuus is built from central great polygons that
carry all the solid's edges (octahedron: 3 squares; cuboctahedron: 4 hexagons). One dimension up: central 3D slices that carry all the
4-polytope's 2-faces. Each 2-face (square or hexagon) spans, with the centre, one hyperplane through the centre. Collect them: how many
central slices, which faces each carries, the 3D shape of each slice (corners, faces), and the planes where two slices slot together."""
import itertools, json, numpy as np
from collections import Counter, defaultdict
from scipy.spatial import ConvexHull
P = np.array(list(itertools.permutations(range(1, 6))), float); P -= 3.0           # centred: values -2..2, sum 0
n = len(P); key = {tuple(p): i for i, p in enumerate(P)}
# 2-faces: hexagons (permute 3 consecutive values among 3 positions, others fixed) and squares (two disjoint adjacent-value swaps)
faces = set()
for v in range(n):
    p = P[v]
    for k in range(-2, 1):                                   # values k, k+1, k+2 permuted
        pos = [i for i in range(5) if p[i] in (k, k + 1, k + 2)]
        hexa = frozenset(key[tuple(q)] for q in (np.array([p[i] if i not in pos else None for i in range(5)], object),) for perm in itertools.permutations([k, k + 1, k + 2])
                         for q in [np.array([perm[pos.index(i)] if i in pos else p[i] for i in range(5)], float)])
        faces.add(hexa)
    for a, b in itertools.combinations(range(-2, 2), 2):    # swaps (a, a+1) and (b, b+1), disjoint value pairs
        if b <= a + 1: continue
        sq = set()
        for s1, s2 in itertools.product([0, 1], repeat=2):
            q = p.copy()
            if s1: q = np.array([a + 1 if x == a else a if x == a + 1 else x for x in q])
            if s2: q = np.array([b + 1 if x == b else b if x == b + 1 else x for x in q])
            sq.add(key[tuple(q)])
        faces.add(frozenset(sq))
fl = [sorted(f) for f in faces]; kinds = Counter(len(f) for f in fl)
print(f'2-faces: {len(fl)} ({kinds[6]} hexagons, {kinds[4]} squares)')
# the central hyperplane of each face: normal orthogonal (within the sum-zero space) to the face's points
one = np.ones(5) / 5 ** .5
def normal_of(f):
    M = np.vstack([P[f], one]); u, s, vt = np.linalg.svd(M); nv = vt[-1]; nv /= np.linalg.norm(nv)
    i = np.argmax(np.abs(nv) > 1e-9); return tuple(np.round(nv * np.sign(nv[np.argmax(np.abs(nv))]), 9))
H = defaultdict(list)
for f in fl: H[normal_of(f)].append(f)
print(f'central slices carrying the faces: {len(H)}')
types = Counter()
slices = []
for nv, fs in H.items():
    nv = np.array(nv); on = [v for v in range(n) if abs(P[v] @ nv) < 1e-9]
    k6 = sum(len(f) == 6 for f in fs); k4 = sum(len(f) == 4 for f in fs)
    # the slice's shape: the 4D permutohedron cut by the hyperplane: corners = vertices on it + edge crossings
    E = [(i, j) for i, j in itertools.combinations(range(n), 2) if np.abs(P[i] - P[j]).sum() == 2]
    pts = [P[v] for v in on] + [P[i] + (P[j] - P[i]) * (P[i] @ nv) / ((P[i] - P[j]) @ nv) for i, j in E if (P[i] @ nv) * (P[j] @ nv) < -1e-12]
    Q = np.unique(np.round(np.array(pts), 9), axis=0); B = np.linalg.svd(np.vstack([nv, one]))[2][2:]; X3 = Q @ B.T
    hh = ConvexHull(X3); FF = {}
    for simp, eq in zip(hh.simplices, hh.equations): FF.setdefault(tuple(np.round(eq, 6)), set()).update(simp)
    t = (len(Q), len(FF), k6, k4, tuple(sorted(Counter(len(x) for x in FF.values()).items())))
    types[t] += 1; slices.append({'normal': nv.tolist(), 'corners': len(Q), 'faces': len(FF), 'hexagons_carried': k6, 'squares_carried': k4})
for t, c in sorted(types.items(), key=lambda x: -x[1]):
    print(f'  {c} slices: {t[0]} corners, {t[1]} faces {dict(t[4])}; each carries {t[2]} hexagons + {t[3]} squares')
json.dump({'slices': slices}, open('vacuus4d.json', 'w'))
print('FINAL ok' if sum(s['hexagons_carried'] + s['squares_carried'] for s in slices) == len(fl) else 'FINAL FAIL: faces not all carried')
