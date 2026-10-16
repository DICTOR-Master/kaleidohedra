# The gap of the pyrochlore two-solid crystal cut into convex pieces (DICTO 2026-10-16: "do the gap"). Every site of the OCD packing holds an
# OCD Stella (network 1) or the OCD's hexagon icosahedron (network 2); each site's share of space is its Voronoi cell V (bcc truncated
# octahedron). V minus the solid is cut by cones from the centre over the solid's faces, as for the OCD's 72 gap pieces: each piece convex.
# Pieces sorted into kinds by congruence (sorted edge lengths, volume). Float. -> data/crystal-gap-pieces.txt, data/crystal-gap-pieces.json
import json, itertools, numpy as np
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.optimize import linprog
N = json.load(open('data/network.json')); T = np.array(N['T']); Lb = np.array(N['Lb']).T
R = json.load(open('data/crystal-render.json')); SV = {'stella': np.array(R['stella']['v']), 'ico': np.array(R['ico']['v'])}
def planes(V):   # unique outward planes n.x <= d of a convex hull
    P = []
    for e in ConvexHull(V).equations:
        if not any(np.allclose(e, q, atol=1e-7) for q in P): P.append(e)
    return np.array(P)
def poly(H):     # H rows (n, -d): n.x - d <= 0; returns corners or None
    A, b = H[:, :3], -H[:, 3]; nr = np.linalg.norm(A, axis=1)
    r = linprog([0, 0, 0, -1], A_ub=np.c_[A, nr], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)])
    if not r.success or r.x[3] < 1e-7: return None
    return HalfspaceIntersection(H, r.x[:3]).intersections
sites = [Lb @ np.array(m, float) + k * T[0] for m in itertools.product(range(-2, 3), repeat=3) for k in range(4)]
nb = [s for s in sites if 1e-9 < np.linalg.norm(s) < 2.0]
Hv = np.array([np.r_[s, -(s @ s) / 2] for s in nb])          # bisector planes s.x <= |s|^2/2
Vc = poly(Hv); Vh = ConvexHull(Vc); Hv = planes(Vc)
cell = abs(np.linalg.det(Lb)); out = ['DICTO · dictospheres.com', 'Gap of the pyrochlore two-solid crystal in convex pieces (float)',
      f'Voronoi cell V: {len(Vc)} corners, volume {Vh.volume:.6f}; 4 sites per cell: {4 * Vh.volume:.6f} vs cell {cell:.6f}']
pieces = []; gap_total = 0
for name, P in SV.items():
    ex = P @ Hv[:, :3].T + Hv[:, 3]; hp = ConvexHull(P); on = int(np.sum(np.any(np.abs(ex) < 1e-6, axis=1)))
    out.append(f'{name}: {len(P)} corners, volume {hp.volume:.6f}, furthest outside V {ex.max():.1e} (inside up to rounding); corners on V walls {on}')
    Ps = planes(P); faces = []
    for e in Ps:
        idx = [i for i in range(len(P)) if abs(P[i] @ e[:3] + e[3]) < 1e-7]; c = P[idx].mean(0); u = P[idx[0]] - c; u /= np.linalg.norm(u); w = np.cross(e[:3], u)
        faces.append((e, sorted(idx, key=lambda i: np.arctan2((P[i] - c) @ w, (P[i] - c) @ u))))
    vol = 0
    for e, f in faces:
        H = [np.r_[-e[:3], -e[3]]]                                   # outside the face plane: n.x >= d
        for i in range(len(f)):                                      # inside the cone from the centre over the face
            a, b = P[f[i]], P[f[(i + 1) % len(f)]]; nn = np.cross(a, b)
            if nn @ P[f].mean(0) < 0: nn = -nn
            H.append(np.r_[-nn, 0.0])
        Q = poly(np.vstack([np.array(H), Hv]))
        if Q is None: continue
        U = []
        for x in Q:                                                  # merge corners closer than 1e-6 (float duplicates)
            if not any(np.linalg.norm(x - y) < 1e-6 for y in U): U.append(x)
        Q = np.array(U); h = ConvexHull(Q); vol += h.volume; Q = Q[h.vertices]
        E = sorted({round(float(np.linalg.norm(Q[i] - Q[j])), 5) for s in h.simplices for i, j in itertools.combinations(s, 2)})
        pieces.append({'solid': name, 'face': len(f), 'v': Q.tolist(), 'vol': h.volume, 'corners': len(h.vertices), 'sig': (name, len(f), round(h.volume, 6), len(Q), tuple(np.round(np.sort(np.linalg.norm(Q - Q.mean(0), axis=1)), 4)))})
    out.append(f'  gap in its cell V − {name}: {Vh.volume - hp.volume:.6f}; sum of cone pieces {vol:.6f}')
    gap_total += 2 * (Vh.volume - hp.volume)
out.append(f'gap per cell {gap_total:.6f} = {gap_total / cell:.4%} of space; pieces per cell {2 * len(pieces)} ({len(pieces)} per stella+ico pair)')
kinds = {}
for p in pieces: kinds.setdefault(p['sig'], []).append(p)
out.append(f'kinds: {len(kinds)}')
for k, ps in sorted(kinds.items(), key=lambda kv: -kv[0][2]):
    q = np.array(ps[0]['v']); h = ConvexHull(q); nf = len({tuple(np.round(e, 5)) for e in h.equations})
    E = sorted({round(float(np.linalg.norm(q[i] - q[j])), 4) for s_ in h.simplices for i, j in itertools.combinations(s_, 2)})
    out.append(f'  around the {k[0]}, over a {k[1]}-gon face: {len(ps)} pieces, each volume {k[2]:.6f}, {k[3]} corners, {nf} faces')
print('\n'.join(out)); open('data/crystal-gap-pieces.txt', 'w').write('\n'.join(out) + '\n')
json.dump({'V': Vc.tolist(), 'pieces': [{k: p[k] for k in ('solid', 'face', 'v', 'vol')} for p in pieces], 'stella': R['stella'], 'ico': R['ico']}, open('data/crystal-gap-pieces.json', 'w'))
