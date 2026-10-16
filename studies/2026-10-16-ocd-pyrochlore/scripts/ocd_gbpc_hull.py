# DICTO 2026-10-16: "a new hull from the OCD with the GB adapters". The hull of the Ogdoecontahedron with GBPCs around it (float, from
# data/adapter-render.json). (a) The cell's own 24 (3 per joint, one side): 36 corners, 44 faces, symmetry only S6 (the one-side choice
# breaks it). (b) The full orbit under the copy's cubic symmetry, 60 GBPCs: 72 corners, 50 faces = 30 hexagons in the envelope's golden
# planes + 20 equilateral triangles in the OCD's own 20 hexagon planes, i.e. the golden envelope (rhombic triacontahedron) cut flat at all
# 20 hexagon planes of the OCD; icosahedral by construction (Antiprism reports Th at its default tolerance from 8-decimal input).
# Structure = Conway t3jD (Antiprism), the triacontahedron truncated at its 20 three-fold corners. -> antiprism/ocd-gbpc*-hull.off
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
from collections import Counter
d = json.load(open('data/adapter-render.json')); O = np.array(d['ocd']['v']); Ad = [np.array(a['v']) for a in d['adapters']]
key = lambda V: frozenset(map(tuple, np.round(V, 6)))
ops = []
for perm in itertools.permutations(range(3)):
    for s in itertools.product((1, -1), repeat=3):
        M = np.zeros((3, 3))
        for i, p in enumerate(perm): M[i, p] = s[i]
        if key(O @ M.T) == key(O): ops.append(M)
orb = {key(a @ M.T): a @ M.T for a in Ad for M in ops}
for name, G in (('24 (one cell)', Ad), ('60 (full orbit)', list(orb.values()))):
    P = np.vstack([O] + list(G)); h = ConvexHull(P); V = np.unique(P[h.vertices].round(9), axis=0); h = ConvexHull(V); E = []
    for e in h.equations:
        if not any(np.allclose(e, q, atol=1e-6) for q in E): E.append(e)
    print(f'{name}: corners {len(V)}, faces {len(E)} by sides {dict(Counter(int(sum(abs(V @ e[:3] + e[3]) < 1e-6)) for e in E))}, volume {h.volume:.6f}')
