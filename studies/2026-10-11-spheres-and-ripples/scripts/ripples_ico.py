# DICTO's icosahedral ripples on the Lotus seed: from each of the 13 icosahedron centres, icosahedral wavefronts
# (face planes n.(x-c) = rho) on a golden ladder rho = r_in * phi^k. A gap-piece corner is "made" by the ripples if at
# least 3 ripple faces with independent normals pass through it. Two orientations: parallel to the solids, and turned
# 36 degrees (each ripple turned about the five-fold axis from the cluster centre to its own centre).
import json, sys, math, itertools, numpy as np
P = json.load(open(sys.argv[1])); PHI = (1 + 5 ** .5) / 2
icos = [p for p in P if p['role'] == 'ico']
cen = [np.mean(p['vertices'], 0) for p in icos]
def normals(p):
    V = np.array(p['vertices']); c = V.mean(0); out = []
    for f in p['faces']:
        a, b, d = V[f[0]], V[f[1]], V[f[2]]; n = np.cross(b - a, d - a); n /= np.linalg.norm(n)
        out.append(n if n @ (a - c) > 0 else -n)
    return np.array(out), float(np.mean([out[i] @ (V[f[0]] - c) for i, f in enumerate(p['faces'])]))
N0, rin = normals(icos[0])            # an edge-1 icosahedron's face normals and inradius
ladder = {k: rin * PHI ** k for k in range(-6, 5)}
corners = {tuple(np.round(v, 6)) for p in P if p['role'] != 'ico' for v in p['vertices']}
corners = [np.array(c) for c in corners]
def rot(axis, ang):
    a = axis / np.linalg.norm(axis); K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * K @ K
O = np.mean(cen, 0)
for label in ('parallel', 'turned 36'):
    made = 0; used = {}; per = []
    for v in corners:
        planes = []
        for c in cen:
            axis = c - O
            Nn = N0 if label == 'parallel' or np.linalg.norm(axis) < 1e-6 else N0 @ rot(axis, math.radians(36)).T
            vals = Nn @ (v - c)
            for n, val in zip(Nn, vals):
                for k, rho in ladder.items():
                    if abs(val - rho) < 1e-6: planes.append(n); used[k] = used.get(k, 0) + 1
        rank = np.linalg.matrix_rank(np.array(planes), tol=1e-6) if planes else 0
        per.append(rank); made += rank >= 3
    print(f'{label}: corners made by >= 3 independent ripple faces: {made} of {len(corners)}; ladder steps used (k: count): {dict(sorted(used.items()))}')
