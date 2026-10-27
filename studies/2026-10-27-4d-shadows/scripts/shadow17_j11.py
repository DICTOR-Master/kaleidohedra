# Shadow-17 = two J11 base to base? (DICTO 2026-10-27: "maybe our rule of halves, swap rules or similar might help pin down Shadow-17")
# Halves idea: cut Shadow-17's pattern at its middle ring; each half a gyroelongated pentagonal pyramid (J11). Check: (1) rebuild the
# 600-cell edge-first slices (float, independent of shadows.py), find the 17-vertex all-triangle one; (2) build 2 x J11 glued on their
# pentagons (edge 1, exact in Q(sqrt5) by construction); (3) graph isomorphism of the two face patterns (networkx).
import itertools, numpy as np, networkx as nx
from scipy.spatial import ConvexHull
p = (1 + 5 ** .5) / 2
V = set()
for i in range(4):
    for s in (1, -1): v = [0] * 4; v[i] = s; V.add(tuple(v))
for s in itertools.product((.5, -.5), repeat=4): V.add(s)
base = (p / 2, .5, 1 / (2 * p), 0)
ev = [q for q in itertools.permutations(range(4)) if sum(1 for a in range(4) for b in range(a + 1, 4) if q[a] > q[b]) % 2 == 0]
for q in ev:
    for s in itertools.product((1, -1), repeat=3):
        w = [base[0] * s[0], base[1] * s[1], base[2] * s[2], 0]; V.add(tuple(round(w[q.index(k)], 12) + 0.0 for k in range(4)))
V = np.array(sorted(V)); assert len(V) == 120, len(V)
D = np.linalg.norm(V[:, None] - V[None], axis=2); e = D[D > 1e-9].min()
E = [(a, b) for a in range(120) for b in range(a + 1, 120) if abs(D[a, b] - e) < 1e-9]; assert len(E) == 720
n = V[E[0][0]] + V[E[0][1]]; n /= np.linalg.norm(n)
Q, _ = np.linalg.qr(np.column_stack([n, np.eye(4)[:, :3]])); B = Q[:, 1:]
h = np.round(V @ n, 9); levels = sorted(set(h)); cands = sorted(set(levels + [a + (b - a) * k / 8 for a, b in zip(levels, levels[1:]) for k in range(1, 8)]))
def graph(P):
    H = ConvexHull(P); G = nx.Graph()
    # merge coplanar hull triangles into faces; keep only real edges
    eqs = np.round(H.equations, 9); faces = {}
    for t, q in zip(H.simplices, map(tuple, eqs)): faces.setdefault(q, set()).update(t)
    tri = all(len(f) == 3 for f in faces.values())
    for f in faces.values():
        f = list(f); c = P[f].mean(0); nrm = np.array(list(next(q for q in faces if set(faces[q]) == set(f))[:3]))
        ang = np.arctan2(((P[f] - c) @ np.cross(nrm, P[f][0] - c)), ((P[f] - c) @ (P[f][0] - c)))
        f = [f[i] for i in np.argsort(ang)]
        for i in range(len(f)): G.add_edge(f[i], f[(i + 1) % len(f)])
    return G, tri, len(faces)
found = None
for t in cands:
    pts = []
    for a, b in E:
        ha, hb = V[a] @ n, V[b] @ n
        if abs(ha - t) < 1e-9: pts.append(V[a])
        if abs(hb - t) < 1e-9: pts.append(V[b])
        if (ha - t) * (hb - t) < -1e-12: s = (t - ha) / (hb - ha); pts.append(V[a] + s * (V[b] - V[a]))
    if len(pts) < 4: continue
    P = np.unique(np.round(np.array(pts) @ B, 9), axis=0)
    print(f"h={t:.4f} V={len(P)}", end=" | ")
    if len(P) != 17: continue
    G, tri, nf = graph(P)
    print(f'slice at height {t:.6f}: 17 vertices, {nf} faces, all triangles: {tri}, degrees {sorted(d for _, d in G.degree())}')
    if tri and nf == 30: found = G
# two J11 base to base: pentagon ring P0 (shared), antiprism ring P1 + apex on each side
c = 1 / (2 * np.sin(np.pi / 5)); hA = np.sqrt(1 - (2 * c * np.sin(np.pi / 10)) ** 2); hP = np.sqrt(1 - c * c)
ring = lambda z, off: [np.array([c * np.cos(2 * np.pi * k / 5 + off), c * np.sin(2 * np.pi * k / 5 + off), z]) for k in range(5)]
X = ring(0, 0) + ring(hA, np.pi / 5) + [np.array([0, 0, hA + hP])] + ring(-hA, np.pi / 5) + [np.array([0, 0, -hA - hP])]
X = np.array(X); DX = np.linalg.norm(X[:, None] - X[None], axis=2)
J = nx.Graph([(a, b) for a in range(17) for b in range(a + 1, 17) if abs(DX[a, b] - 1) < 1e-9])
print('2 x J11: vertices', J.number_of_nodes(), 'edges', J.number_of_edges(), 'degrees', sorted(d for _, d in J.degree()), '(all edges length 1 by construction)')
print('Shadow-17 pattern == 2 x J11 pattern (graph isomorphic):', found is not None and nx.is_isomorphic(found, J))
