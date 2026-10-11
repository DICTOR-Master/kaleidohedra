# DICTO 2026-10-12: are there missing forms like octahedra present anywhere? The cube family enters the icosahedral shells as
# compounds of five: five octahedra on the icosidodecahedron's 30 corners, five cubes and ten tetrahedra on the dodecahedron's 20.
# For each, in the twin network (dodecahedron edge 1), where do their edges run: along piece edges, across piece faces, or through
# piece interiors?
import itertools, numpy as np
from scipy.spatial import ConvexHull
src = open('gen_twin.py').read(); src = src[:src.index('net_in = [(r, V @ SW.T)')]
exec(src)
pieces = [V for _, V in net_in + net_out]
H = [ConvexHull(V) for V in pieces]
EDGES = []
for V, h in zip(pieces, H):
    for s in h.simplices:
        for a, b in itertools.combinations(s, 2):
            EDGES.append((V[a], V[b]))
def seg_dist(p, a, b):
    t = np.clip((p - a) @ (b - a) / ((b - a) @ (b - a)), 0, 1); return np.linalg.norm(p - (a + t * (b - a)))
def classify(a, b, k=25):
    kinds = []
    for t in np.linspace(0.02, 0.98, k):
        p = a + t * (b - a)
        if any(np.all(p @ h.equations[:, :3].T + h.equations[:, 3] < -1e-7) for h in H): kinds.append('interior'); continue
        on_edge = any(seg_dist(p, x, y) < 1e-6 and abs(np.linalg.norm(np.cross(y - x, b - a))) / np.linalg.norm(y - x) / np.linalg.norm(b - a) < 1e-6 for x, y in EDGES)
        kinds.append('edge' if on_edge else 'face')
    return 'through piece interiors' if 'interior' in kinds else ('along piece edges' if all(k == 'edge' for k in kinds) else 'across piece faces')
def report(name, sets, nverts):
    from collections import Counter
    c = Counter()
    for S in sets:
        d = min(np.linalg.norm(S[0] - w) for w in S[1:])
        for i, j in itertools.combinations(range(len(S)), 2):
            if abs(np.linalg.norm(S[i] - S[j]) - d) < 1e-6: c[classify(S[i], S[j])] += 1
    print(f'{name}: {len(sets)} found; their edges: ' + ', '.join(f'{n} {k}' for k, n in c.items()))
# five octahedra on the ID's corners: triples of mutually perpendicular corner directions
octs = set()
for i, j, k in itertools.combinations(range(30), 3):
    a, b, c = ID[i], ID[j], ID[k]
    if abs(a @ b) < 1e-9 and abs(a @ c) < 1e-9 and abs(b @ c) < 1e-9: octs.add(tuple(sorted([i, j, k])))
oct_sets = [np.array([s * ID[x] for x in t for s in (1, -1)]) for t in octs]
report('Octahedra on the icosidodecahedron (edge phi/2)', oct_sets, 6)
# five cubes and ten tetrahedra on the dodecahedron's corners
dD = min(np.linalg.norm(D[0] - w) for w in D[1:])
cubes = set()
for i in range(20):
    nb = [j for j in range(20) if abs(np.linalg.norm(D[i] - D[j]) - PHI * dD) < 1e-9]
    for a, b, c in itertools.combinations(nb, 3):
        u, v, w = D[a] - D[i], D[b] - D[i], D[c] - D[i]
        if abs(u @ v) < 1e-9 and abs(u @ w) < 1e-9 and abs(v @ w) < 1e-9:
            pts = [D[i] + x * u + y * v + z * w for x in (0, 1) for y in (0, 1) for z in (0, 1)]
            idx = tuple(sorted(int(np.argmin(np.linalg.norm(D - p, axis=1))) for p in pts))
            if all(np.min(np.linalg.norm(D - p, axis=1)) < 1e-9 for p in pts): cubes.add(idx)
report('Cubes on the dodecahedron (edge 1)', [D[list(c)] for c in cubes], 8)
tets = []
for cidx in cubes:
    C = D[list(cidx)]
    for start in (0,):
        par = [k for k in range(8) if (np.round(np.sum(np.sign(C[k] - C.mean(0)) > 0)) % 2) == 0]
        T1 = C[par]; T2 = C[[k for k in range(8) if k not in par]]
        tets += [T1, T2]
report('Tetrahedra on the dodecahedron (edge 1)', tets, 4)
