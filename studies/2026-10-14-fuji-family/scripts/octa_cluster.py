# Searching for an octahedral analogue of the Lotus seed (DICTO, 2026-10-14). In the Lotus seed 12 icosahedra sit on the 5-fold axes
# and FUJI fills the 3-fold corners, its base lying flat in the outer face. Octahedral analogue: 8 outer solids on the 3-fold axes,
# so that 4 of them surround each 4-fold axis; a square-family pyramid would fill those 6 corners if the cluster's hull face on the
# 4-fold axis is a flat-ended square (an octagon with all angles 135° and sides 1 and r alternating) above a pocket whose 4 walls
# are the outer solids' triangles. Outer solids: octahedron, cuboctahedron, rhombicuboctahedron (unit edges), parallel, slid in
# until neighbours touch. Reports each hull face on the 4-fold axis. DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
def perms(v): return {p for s in itertools.product((1, -1), repeat=3) for p in itertools.permutations([a * b for a, b in zip(v, s)])}
SOL = {'octahedron': np.array(sorted(perms((1, 0, 0)))) / math.sqrt(2),
       'cuboctahedron': np.array(sorted(perms((1, 1, 0)))) / math.sqrt(2),
       'rhombicuboctahedron': np.array(sorted(perms((1, 1, 1 + math.sqrt(2))))) / 2}
for k, V in SOL.items():
    h = ConvexHull(V); e = min(np.linalg.norm(V[a] - V[b]) for s in h.simplices for a, b in itertools.combinations(s, 2)); SOL[k] = V / e
U = np.array(list(itertools.product((1, -1), repeat=3)), float) / math.sqrt(3)
def overlap(A, B, eps=1e-9):
    hA, hB = ConvexHull(A), ConvexHull(B); axes = list(hA.equations[:, :3]) + list(hB.equations[:, :3])
    EA = [A[b] - A[a] for s in hA.simplices for a, b in itertools.combinations(s, 2)]; EB = [B[b] - B[a] for s in hB.simplices for a, b in itertools.combinations(s, 2)]
    for e1 in EA[:60]:
        for e2 in EB[:60]:
            n = np.cross(e1, e2)
            if np.linalg.norm(n) > 1e-9: axes.append(n / np.linalg.norm(n))
    for n in axes:
        a, b = A @ n, B @ n
        if a.max() <= b.min() + eps or b.max() <= a.min() + eps: return False
    return True
res = {}
for name, V in SOL.items():
    pairs = [(i, j) for i, j in itertools.combinations(range(8), 2) if abs(U[i] @ U[j] - 1 / 3) < 1e-9]
    ok = lambda t: not any(overlap(V + U[i] * t, V + U[j] * t) for i, j in pairs)
    lo, hi = 0.1, 6.0
    for _ in range(45):
        m = (lo + hi) / 2; (hi := m) if ok(m) else (lo := m)
    t = hi; P = np.vstack([V + u * t for u in U]); H = ConvexHull(P)
    faces = []
    for e in np.unique(np.round(H.equations, 6), axis=0):
        if not np.allclose(e[:3], [0, 0, 1], atol=1e-5): continue
        on = np.unique(np.round(P[np.abs(P @ e[:3] + e[3]) < 1e-6], 9), axis=0); c = on.mean(0)
        Q = on[np.argsort(np.arctan2(on[:, 1] - c[1], on[:, 0] - c[0]))]
        L = [float(np.linalg.norm(Q[i] - Q[(i + 1) % len(Q)])) for i in range(len(Q))]
        ang = [math.degrees(math.acos(np.clip((Q[i - 1] - Q[i]) @ (Q[(i + 1) % len(Q)] - Q[i]) / np.linalg.norm(Q[i - 1] - Q[i]) / np.linalg.norm(Q[(i + 1) % len(Q)] - Q[i]), -1, 1))) for i in range(len(Q))]
        faces.append(dict(corners=len(Q), sides=[round(x, 4) for x in L], angles=[round(x, 2) for x in ang]))
    # what lies under the axis: the highest point of the cluster on the 4-fold axis line, vs the hull face height
    res[name] = dict(contact=round(t, 6), hullFaceOn4fold=faces)
    print(name, json.dumps(res[name]))
json.dump(res, open(os.path.join(ROOT, 'octa-cluster.json'), 'w'), indent=1)
